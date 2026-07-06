# AI Service - Manim 智能动画生成引擎

## 模块简介
本模块是项目的核心 AI 能力层，基于本地开源大模型与 RAG 检索增强技术，实现从自然语言需求到 Manim 动画视频的全自动化生成。具备代码自动调试修复能力，全程离线运行，以标准 HTTP 接口形式供 Java Web 端调用。

## 技术栈
- **大模型框架**：Ollama + Qwen2.5-Coder-3B（4-bit 量化）
- **向量检索**：ChromaDB + nomic-embed-text
- **动画渲染**：Manim Community v0.18.0
- **接口框架**：FastAPI + Uvicorn
- **环境管理**：Anaconda + Python 3.10
- **运行平台**：Windows / Linux，适配 RTX 3060 6G 及以上显卡

## 目录结构
```plaintext
ai-service/
├── kb_data/ # 知识库原始素材（可提交）
│   ├── api_docs/ # Manim 核心 API 说明
│   ├── examples/ # 高质量可运行示例代码
│   └── errors/ # 常见报错与修复方案
├── build_kb.py # 知识库构建脚本
├── ai_engine.py # 核心引擎：RAG、生成、调试、渲染全逻辑
├── main.py # FastAPI 接口服务入口
├── requirements.txt # Python 依赖清单
├── .gitignore # 忽略规则
└── README.md # 本说明文档

以下目录运行时自动生成，不提交到仓库
├── chroma_db/ # 持久化向量库
└── output/ # 渲染输出的代码与视频
```
## 环境要求
### 硬件要求
显存 ≥ 6GB（推荐 RTX 3060 及以上）
内存 ≥ 16GB
剩余磁盘空间 ≥ 10GB
### 软件要求
Anaconda 3
Ollama 服务
ffmpeg（Manim 渲染依赖）
### 环境搭建步骤
1. 创建 Python 虚拟环境
打开 Anaconda Prompt，执行以下命令：
```bash
 #创建环境
conda create -n manim_ai python=3.10 -y

# 激活环境
conda activate manim_ai
```
2. 安装项目依赖
进入 ai-service 目录，执行：
```bash
运行
pip install -r requirements.txt
```

3. 安装 ffmpeg
```bash
conda install -c conda-forge ffmpeg -y
```

4. 拉取本地大模型
(确保 Ollama 服务已启动)，执行：
```bash
# 代码生成模型
ollama pull qwen2.5-coder:3b-instruct-q4_K_M

# 向量嵌入模型
ollama pull nomic-embed-text
```

## 快速启动
### 1. 构建知识库
首次运行必须执行，后续更新 kb_data 素材后重新执行即可：
```bash
python build_kb.py
```

执行成功后会生成 chroma_db 目录。
### 2. 启动 API 服务
```bash
python main.py
```

服务默认运行在 http://localhost:8000
### 3. 验证服务
浏览器访问 http://localhost:8000/docs，可打开 FastAPI 可视化接口文档
调用 /health 接口，返回 {"status":"ok"} 即为启动成功


## 核心工作原理
系统采用「生成 - 执行 - 反馈 - 修复」的 Agent 闭环逻辑：
- 接收用户自然语言需求，通过 RAG 从知识库召回相关示例与 API 说明
- 大模型基于参考资料生成 Manim 动画代码
- 自动调用 Manim 执行渲染，捕获运行结果
- 渲染成功则直接返回视频；渲染失败则提取报错信息，让大模型自动修复代码
最多循环重试 3 次，超过则返回失败日志


## 接口文档
1. 健康检查
接口地址：`GET /health`
返回示例：
```json
{
  "status": "ok",
  "message": "AI引擎运行正常"
}
```
2. 生成动画
- 接口地址：`POST /generate`
- Content-Type：`application/json`
- 请求参数：

| 字段名     | 类型   | 必填 | 说明                         |
| ---------- | ------ | ---- | ---------------------------- |
| user_input | string | 是   | 动画需求的自然语言描述       |
| max_retry  | int    | 否   | 最大调试重试次数，默认 3     |

请求示例：
```json
{
  "user_input": "绘制一个蓝色的圆形并旋转一圈",
  "max_retry": 3
}
```
返回参数：
表格
字段名	类型	说明
success	boolean	是否生成成功
code	string	最终生成的 Manim 代码
video_path	string	渲染成功的视频绝对路径
try_count	int	实际调试重试次数
log	string	运行日志 / 错误信息
成功返回示例：
```json
{
  "success": true,
  "code": "from manim import *\nclass Demo(Scene):...",
  "video_path": "D:/project/output/videos/result.mp4",
  "try_count": 1,
  "log": ""
}
```