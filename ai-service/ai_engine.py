#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import uuid
import requests
import subprocess
import chromadb
from typing import List, Dict, Optional, Tuple
import textwrap
from pathlib import Path  # ✅ 优化：引入 Pathlib 解决跨平台路径拼接痛点

# ===================== 全局配置常量 =====================
OLLAMA_BASE_URL: str = "http://localhost:11434"
CODER_MODEL_NAME: str = "qwen2.5-coder:7b-instruct-q4_K_M"
EMBEDDING_MODEL_NAME: str = "nomic-embed-text"
LLM_TEMPERATURE: float = 0.2
API_REQUEST_TIMEOUT: int = 60

CHROMA_PERSIST_DIR: str = "chroma_db"
CHROMA_COLLECTION_NAME: str = "manim_animation_kb"
RAG_TOP_K: int = 2

MAX_ANIMATION_DURATION: int = 30
DEFAULT_RETRY_TIMES: int = 3

# ✅ 优化：使用绝对路径，避免 FastAPI 启动目录不同导致找不到文件夹
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
CODE_OUTPUT_SUBDIR = OUTPUT_DIR / "code"
VIDEO_OUTPUT_SUBDIR = OUTPUT_DIR / "videos"
RENDER_QUALITY_FLAG: str = "-ql"
RENDER_TIMEOUT: int = 120

CODE_BLOCK_PATTERN: str = r"```python\s*(.*?)\s*```|```\s*(.*?)\s*```"
SCENE_CLASS_PATTERN: str = r"class\s+(\w+)\s*\(\s*Scene\s*\)"

# ===================== 全局资源初始化 =====================
try:
    chroma_client = chromadb.PersistentClient(path=os.path.join(BASE_DIR, CHROMA_PERSIST_DIR))
    kb_collection = chroma_client.get_collection(name=CHROMA_COLLECTION_NAME)
except Exception as e:
    # 降级处理，允许服务启动但输出强警告，防止直接 Crash
    kb_collection = None
    print(f"⚠️ 严重警告：向量库初始化失败，请检查是否已执行 build_kb.py。错误：{str(e)}")

# 确保输出目录存在
CODE_OUTPUT_SUBDIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUTPUT_SUBDIR.mkdir(parents=True, exist_ok=True)


# ===================== 通用工具函数 =====================
def generate_embedding(text: str) -> List[float]:
    """调用Ollama嵌入模型生成文本向量"""
    try:
        # ✅ 优化：修复了此前 404/400 错误的旧接口，更新为最新的 embed 标准
        response = requests.post(
            url=f"{OLLAMA_BASE_URL}/api/embed",
            json={
                "model": EMBEDDING_MODEL_NAME,
                "input": text  # 旧版是 prompt，必须用 input
            },
            timeout=API_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        # ✅ 优化：新接口返回的是二维数组 embeddings
        return response.json().get("embeddings", [[]])[0]
    except requests.exceptions.RequestException as e:
        print(f"❌ 向量生成失败：{str(e)}")
        return []


def extract_manim_code(model_response: str) -> str:
    matches = re.findall(CODE_BLOCK_PATTERN, model_response, re.DOTALL)
    if not matches:
        return ""
    for match in matches:
        code = match[0] if match[0] else match[1]
        if code.strip():
            return code.strip()
    return ""


def extract_scene_class_name(code: str) -> Optional[str]:
    match = re.search(SCENE_CLASS_PATTERN, code)
    if match:
        return match.group(1)
    return None


# ===================== 核心业务逻辑 =====================
def rag_retrieve_references(user_query: str) -> str:
    if not kb_collection:
        return "⚠️ 知识库未就绪，使用纯大模型能力生成。"

    query_embedding = generate_embedding(user_query)
    if not query_embedding:
        return "⚠️ 未获取到参考资料（向量生成失败）"

    try:
        results = kb_collection.query(
            query_embeddings=[query_embedding],
            n_results=RAG_TOP_K
        )
        if not results.get("documents") or not results["documents"][0]:
            return "⚠️ 未找到相关参考资料"

        references = []
        for idx, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            ref = f"【参考资料{idx + 1} | 文件：{meta.get('file_name', '未知')}】\n{doc}\n"
            references.append(ref)
        return "\n".join(references)
    except Exception as e:
        print(f"❌ RAG检索失败：{str(e)}")
        return "⚠️ 参考资料检索失败"


def generate_manim_code(user_requirement: str) -> Tuple[bool, str]:
    references = rag_retrieve_references(user_requirement)
    system_prompt = textwrap.dedent(f"""
    你是专业的Manim Community v0.18.0动画工程师，必须严格遵守以下规则：
    1. 仅使用Manim社区版标准语法，禁止使用第三方扩展库
    2. 代码必须完整可直接运行，必须定义继承Scene的类
    3. 动画总时长严格控制在{MAX_ANIMATION_DURATION}秒以内
    4. ⚠️ 核心约束：代码中必须包含至少一个动画播放动作（例如使用 self.play()，如 self.play(Create(obj))），绝不能仅仅使用 self.add() 添加静态物体，必须保证能渲染出视频！
    5. 仅输出```python包裹的代码块，不输出任何额外解释文字
    6. 动态性：必须使用 self.play() 配合 Create, Write, Transform, FadeIn 等动画类。
    7 视觉优化：合理设置圆的颜色(color)、填充(fill_opacity)、半径(radius)和位置(shift)。
    8. 逻辑：如果你需要画两个物体，请使用 VGroup 组合它们，并考虑它们出现的先后顺序。
    9.⚠️ 注释约束：代码注释必须严格如实反映代码功能，禁止在注释中描述代码未实际实现的动画动作。如果无法实现某种视觉效果，直接忽略，严禁在注释中进行虚假描述。

    参考资料：
    {references}
    """)
    user_prompt = f"请根据需求生成Manim动画代码：{user_requirement}"

    try:
        response = requests.post(
            url=f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": CODER_MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": LLM_TEMPERATURE,
                "stream": False
            },
            timeout=API_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        model_raw_response = response.json()["message"]["content"]
        manim_code = extract_manim_code(model_raw_response)
        if not manim_code:
            return False, f"❌ 未提取到有效Manim代码。原始回复：\n{model_raw_response}"
        return True, manim_code
    except Exception as e:
        return False, f"❌ 大模型调用或解析失败：{str(e)}"


def render_manim_animation(code_str: str) -> Tuple[bool, str, str]:
    task_id = uuid.uuid4().hex[:8]
    # ✅ 优化：使用 Path 对象的绝对路径，确保 subprocess 准确找到文件
    code_file_path = CODE_OUTPUT_SUBDIR / f"{task_id}.py"
    # Manim 强行指定 -o 时的最终输出路径
    video_output_path = VIDEO_OUTPUT_SUBDIR / f"{task_id}.mp4"

    try:
        with open(code_file_path, "w", encoding="utf-8") as f:
            f.write(code_str)

        scene_name = extract_scene_class_name(code_str)
        if not scene_name:
            return False, "❌ 渲染失败：代码中未找到继承Scene的场景类", ""

        # ✅ 核心修复：使用 sys.executable 确保调用的是当前 Conda 环境的 Python
        # 相当于在终端执行：E:\Anaconda\...\python.exe -m manim -ql xxx.py SceneName -o xxx.mp4
        render_command = [
            sys.executable,
            "-m", "manim",
            RENDER_QUALITY_FLAG,
            str(code_file_path.absolute()),
            scene_name,
            "-o", str(video_output_path.absolute())
        ]

        result = subprocess.run(
            render_command,
            capture_output=True,
            text=True,
            timeout=RENDER_TIMEOUT,
            encoding="utf-8",
            errors="replace"
        )

        full_log = f"=== 标准输出 ===\n{result.stdout}\n=== 错误输出 ===\n{result.stderr}"

        if result.returncode == 0 and video_output_path.exists():
            # ✅ 优化：向前端返回相对URL路径，而不是物理磁盘路径
            web_accessible_url = f"/videos/{task_id}.mp4"
            return True, f"✅ 渲染成功\n{full_log}", web_accessible_url
        else:
            return False, f"❌ 渲染失败，进程返回码：{result.returncode}\n{full_log}", ""

    except subprocess.TimeoutExpired:
        return False, f"❌ 渲染超时（超过{RENDER_TIMEOUT}秒），进程已强制终止", ""
    except Exception as e:
        return False, f"❌ 渲染执行异常：{str(e)}", ""


def fix_manim_code(original_code: str, error_message: str) -> Tuple[bool, str]:
    system_prompt = textwrap.dedent(f"""
    你是专业的Manim Community v0.18.0调试工程师。
    严格遵守以下规则：
    1. 保留原有动画功能，仅修复语法错误、导入缺失、API误用问题
    2. 返回完整的修复后代码，使用```python代码块包裹，不要输出额外解释
    3. ⚠️ 核心约束：代码中必须包含至少一个动画播放动作（例如使用 self.play()，如 self.play(Create(obj))），绝不能仅仅使用 self.add() 添加静态物体，必须保证能渲染出视频！
    4.⚠️ 注释约束：代码注释必须严格如实反映代码功能，禁止在注释中描述代码未实际实现的动画动作。如果无法实现某种视觉效果，直接忽略，严禁在注释中进行虚假描述。
    
    报错信息：
    {error_message}
    """)
    user_prompt = f"请修复以下Manim代码：\n```python\n{original_code}\n```"

    try:
        response = requests.post(
            url=f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": CODER_MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": LLM_TEMPERATURE,
                "stream": False
            },
            timeout=API_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        fixed_code = extract_manim_code(response.json()["message"]["content"])
        if not fixed_code:
            return False, "❌ 未提取到修复后的有效代码"
        return True, fixed_code
    except Exception as e:
        return False, f"❌ 代码修复异常：{str(e)}"


def run_full_pipeline(user_requirement: str, max_retry: int = DEFAULT_RETRY_TIMES) -> Dict:
    result = {"success": False, "code": "", "video_path": "", "try_count": 0, "log": ""}
    current_code = ""
    all_logs = []

    try:
        gen_success, gen_result = generate_manim_code(user_requirement)
        result["try_count"] = 1
        if not gen_success:
            all_logs.append(f"第1次尝试生成失败：{gen_result}")
            result["log"] = "\n".join(all_logs)
            return result

        current_code = gen_result
        result["code"] = current_code
        render_success, render_log, video_path = render_manim_animation(current_code)
        all_logs.append(f"第1次渲染：\n{render_log}")

        if render_success:
            result.update({"success": True, "video_path": video_path, "log": "\n".join(all_logs)})
            return result

        for retry_index in range(1, max_retry + 1):
            current_try = retry_index + 1
            result["try_count"] = current_try

            fix_success, fix_result = fix_manim_code(current_code, render_log)
            if not fix_success:
                all_logs.append(f"第{current_try}次修复失败：{fix_result}")
                break
            if fix_result.strip() == current_code.strip():
                all_logs.append(f"第{current_try}次修复后代码无变化，终止重试以防死循环。")
                break

            current_code = fix_result
            result["code"] = current_code

            render_success, render_log, video_path = render_manim_animation(current_code)
            all_logs.append(f"第{current_try}次渲染：\n{render_log}")

            if render_success:
                result.update({"success": True, "video_path": video_path, "log": "\n".join(all_logs)})
                return result

        all_logs.append(f"❌ 达到最大重试次数 {max_retry}，任务终止。")
        result["log"] = "\n".join(all_logs)
        return result
    except Exception as e:
        result["log"] = f"❌ 流水线全局异常：{str(e)}"
        return result