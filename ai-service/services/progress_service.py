#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步任务进度追踪服务
基于 Redis 存储任务状态，通过 Pub/Sub 实现实时进度推送。
配合 Celery Worker + SSE 端点使用，为前端提供"渲染中→完成"的实时反馈。
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

import redis

# Redis 连接（复用 Celery 的 Redis，默认本地）
from .config import settings
REDIS_URL = settings.redis_url
_redis_client: Optional[redis.Redis] = None

# 常量
TASK_KEY_PREFIX = "cs:task"
TASK_CHANNEL_PREFIX = "cs:task"
TASK_TTL = 3600  # 任务状态 1 小时后自动过期


def _get_redis() -> redis.Redis:
    """延迟初始化 Redis 连接"""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client


# ===================== 视频元数据持久化（JSON 文件，Redis 重启后恢复） =====================

META_FILE = Path(__file__).resolve().parent.parent / "outputs" / "video_meta.json"


def _read_meta_file() -> dict:
    """从 JSON 文件读取所有视频元数据"""
    try:
        if META_FILE.exists():
            with open(META_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _write_meta_file(meta: dict):
    """写入视频元数据到 JSON 文件"""
    try:
        META_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _restore_meta_to_redis():
    """Redis 启动后，从 JSON 文件恢复所有标题到 Redis"""
    meta = _read_meta_file()
    if not meta:
        return
    try:
        r = _get_redis()
        for filename, data in meta.items():
            key = f"{VIDEO_META_PREFIX}:{filename}"
            r.hset(key, "title", data.get("title", filename))
            r.hset(key, "created_at", data.get("created_at", ""))
            r.hset(key, "username", data.get("username", "匿名"))
            r.expire(key, 86400 * 30)
    except Exception:
        pass


# ===================== 任务进度管理 =====================

def set_progress(
    task_id: str,
    state: str,
    progress: int = 0,
    message: str = "",
    video_path: str = "",
    log: str = "",
    code: str = "",
):
    """
    更新任务进度并发布到 Pub/Sub
    :param task_id: 任务 ID
    :param state: PENDING | STARTED | RENDERING | SUCCESS | FAILURE
    :param progress: 进度百分比 0-100
    :param message: 当前状态描述
    :param video_path: 成功时返回的视频路径
    :param log: 日志信息
    :param code: AI 生成的 Manim 代码
    """
    try:
        r = _get_redis()
        key = f"{TASK_KEY_PREFIX}:{task_id}"
        channel = f"{TASK_CHANNEL_PREFIX}:{task_id}:progress"

        data = {
            "task_id": task_id,
            "state": state,
            "progress": progress,
            "message": message,
            "video_path": video_path,
            "log": log[-2000:] if log else "",
            "code": code[-10000:] if code else "",
            "updated_at": datetime.now().isoformat(),
        }

        r.setex(key, TASK_TTL, json.dumps(data, ensure_ascii=False))
        r.publish(channel, json.dumps(data, ensure_ascii=False))
    except Exception as e:
        # Redis 不可用时降级：记录日志但不中断任务
        import logging
        logging.getLogger("progress").warning("set_progress 失败: %s", e)


def get_progress(task_id: str) -> Dict:
    """查询任务进度（Redis 不可用时返回降级状态）"""
    try:
        r = _get_redis()
        key = f"{TASK_KEY_PREFIX}:{task_id}"
        raw = r.get(key)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return {"task_id": task_id, "state": "UNKNOWN", "progress": 0, "message": "任务不存在或已过期"}


def subscribe_progress(task_id: str):
    """
    订阅任务进度更新（返回生成器，供 SSE 使用）
    使用 Redis Pub/Sub 订阅，阻塞式迭代
    """
    r = _get_redis()
    channel = f"{TASK_CHANNEL_PREFIX}:{task_id}:progress"
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    return pubsub


def unsubscribe_progress(pubsub):
    """取消订阅"""
    try:
        pubsub.unsubscribe()
        pubsub.close()
    except Exception:
        pass


# ===================== 视频文件管理 =====================

def list_videos() -> list:
    """列出 outputs/videos/ 下所有视频文件信息"""
    from pathlib import Path

    video_dir = Path(__file__).resolve().parent.parent / "outputs" / "videos"
    if not video_dir.exists():
        return []

    videos = []
    for f in sorted(video_dir.glob("*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True):
        stat = f.stat()
        poster_name = f"{f.stem}.jpg"
        poster_path = video_dir / poster_name
        videos.append({
            "filename": f.name,
            "task_id": f.stem,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "url": f"/videos/{f.name}",
            "poster": f"/videos/{poster_name}" if poster_path.exists() else "",
        })
    return videos


def delete_video(filename: str) -> bool:
    """删除指定视频文件、代码文件、缩略图及 Redis 元数据"""
    from pathlib import Path

    base = Path(__file__).resolve().parent.parent / "outputs"
    video_path = base / "videos" / filename
    stem = Path(filename).stem
    code_path = base / "code" / f"{stem}.py"
    thumb_path = base / "videos" / f"{stem}.jpg"

    deleted = False
    if video_path.exists():
        video_path.unlink()
        deleted = True
    if code_path.exists():
        code_path.unlink()
        deleted = True
    if thumb_path.exists():
        thumb_path.unlink()

    # 清理 Redis 元数据
    try:
        r = _get_redis()
        r.delete(f"{VIDEO_META_PREFIX}:{filename}")
        r.srem(GALLERY_KEY, filename)
    except Exception:
        pass

    # 清理 JSON 文件中的元数据
    try:
        meta = _read_meta_file()
        if filename in meta:
            del meta[filename]
            _write_meta_file(meta)
    except Exception:
        pass

    return deleted


# ===================== 视频元数据管理 =====================

VIDEO_META_PREFIX = "cs:video"  # Redis Hash: 视频元数据 {filename} → {title, created_at, username}


def save_video_meta(filename: str, title: str = "", username: str = ""):
    """保存视频元数据（标题、创建时间、发布者）——同时写入 Redis 和 JSON 文件"""
    try:
        r = _get_redis()
        key = f"{VIDEO_META_PREFIX}:{filename}"
        r.hset(key, "title", title or filename)
        r.hset(key, "created_at", datetime.now().isoformat())
        r.hset(key, "username", username or "匿名")
        r.expire(key, 86400 * 30)
        if username and username != "匿名":
            r.sadd(f"{VIDEO_META_PREFIX}:user-works:{username}", filename)
            r.expire(f"{VIDEO_META_PREFIX}:user-works:{username}", 86400 * 90)
    except Exception:
        pass

    # 同步写入 JSON 文件（持久化，Redis 重启后恢复）
    try:
        meta = _read_meta_file()
        meta[filename] = {
            "title": title or filename,
            "created_at": datetime.now().isoformat(),
            "username": username or "匿名",
        }
        _write_meta_file(meta)
    except Exception:
        pass


def add_to_user_works(username: str, filename: str) -> bool:
    """将视频加入用户的作品列表（服务端持久化，跨浏览器/设备同步）"""
    try:
        r = _get_redis()
        r.sadd(f"{VIDEO_META_PREFIX}:user-works:{username}", filename)
        r.expire(f"{VIDEO_META_PREFIX}:user-works:{username}", 86400 * 90)
        _maybe_bgsave()
        return True
    except Exception:
        return False


def get_user_works(username: str) -> set:
    """获取用户的作品文件名列表"""
    try:
        r = _get_redis()
        return r.smembers(f"{VIDEO_META_PREFIX}:user-works:{username}") or set()
    except Exception:
        return set()


def get_video_meta(filename: str) -> dict:
    """获取单个视频的元数据"""
    try:
        r = _get_redis()
        key = f"{VIDEO_META_PREFIX}:{filename}"
        return r.hgetall(key) or {}
    except Exception:
        return {}


def get_all_video_metas() -> dict:
    """批量获取所有视频元数据——优先 Redis，回退到 JSON 文件"""
    try:
        r = _get_redis()
        result = {}
        cursor = 0
        while True:
            cursor, keys = r.scan(cursor, match=f"{VIDEO_META_PREFIX}:*", count=200)
            for key in keys:
                ks = key.decode("utf-8") if isinstance(key, bytes) else key
                if ":user-works:" in ks:
                    continue
                fname = ks.replace(f"{VIDEO_META_PREFIX}:", "")
                try:
                    result[fname] = r.hgetall(key) or {}
                except Exception:
                    continue
            if cursor == 0:
                break
        if result:
            return result
    except Exception:
        pass

    # Redis 无数据时从 JSON 文件恢复
    file_meta = _read_meta_file()
    if file_meta:
        # 异步恢复到 Redis（不阻塞）
        try:
            _restore_meta_to_redis()
        except Exception:
            pass
    return file_meta


def update_video_title(filename: str, new_title: str) -> bool:
    """修改视频标题——同时更新 Redis 和 JSON 文件"""
    try:
        r = _get_redis()
        key = f"{VIDEO_META_PREFIX}:{filename}"
        if r.exists(key):
            r.hset(key, "title", new_title)
        else:
            save_video_meta(filename, title=new_title)
    except Exception:
        pass

    # 同步更新 JSON 文件
    try:
        meta = _read_meta_file()
        if filename in meta:
            meta[filename]["title"] = new_title
            _write_meta_file(meta)
    except Exception:
        pass

    return True


# ===================== 画廊收藏管理 =====================

GALLERY_KEY = "cs:gallery"  # Redis Set: 已收藏的视频文件名


def _maybe_bgsave():
    """在关键写入后手动触发持久化。
    使用 SAVE（同步）而非 BGSAVE，因为 BGSAVE 依赖 fork()，
    在 Windows 上不可用，会导致数据静默丢失。
    """
    try:
        r = _get_redis()
        r.save()
    except Exception:
        pass


def save_to_gallery(filename: str) -> bool:
    """
    Toggle 收藏状态：已收藏则取消，未收藏则添加。
    返回操作后的状态 (True=已收藏, False=已取消)。
    """
    try:
        r = _get_redis()
        if r.sismember(GALLERY_KEY, filename):
            r.srem(GALLERY_KEY, filename)
            _maybe_bgsave()
            return False
        else:
            r.sadd(GALLERY_KEY, filename)
            _maybe_bgsave()
            return True
    except Exception:
        return False


def is_in_gallery(filename: str) -> bool:
    """检查视频是否已收藏"""
    try:
        r = _get_redis()
        return bool(r.sismember(GALLERY_KEY, filename))
    except Exception:
        return False


def get_gallery_filenames() -> set:
    """获取所有已收藏的视频文件名"""
    try:
        r = _get_redis()
        return r.smembers(GALLERY_KEY) or set()
    except Exception:
        return set()


# ===================== v1.0 任务队列管理 =====================

def _scan_tasks() -> List[Dict]:
    """
    内部辅助函数：扫描所有 Redis cs:task:* 键，返回任务列表。
    避免 list_tasks / get_task_count 中重复的扫描逻辑。
    """
    r = _get_redis()
    tasks: List[Dict] = []
    cursor = 0
    while True:
        cursor, keys = r.scan(cursor, match=f"{TASK_KEY_PREFIX}:*", count=100)
        for key in keys:
            if ":progress" in key or ":channel" in key:
                continue
            raw = r.get(key)
            if raw:
                try:
                    tasks.append(json.loads(raw))
                except json.JSONDecodeError:
                    pass
        if cursor == 0:
            break
    return tasks


def list_tasks(
    state_filter: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Dict:
    """
    列出所有活跃/最近的任务（扫描 Redis cs:task:* 键），支持分页和状态筛选。
    """
    tasks = _scan_tasks()

    if state_filter:
        tasks = [t for t in tasks if t.get("state") == state_filter]

    tasks.sort(key=lambda t: t.get("updated_at", ""), reverse=True)

    total = len(tasks)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": tasks[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (total + page_size - 1) // page_size),
    }


def mark_task_cancelled(task_id: str):
    """标记任务为已取消（Redis 标记，Celery worker 轮询检查）"""
    try:
        r = _get_redis()
        r.setex(f"{TASK_KEY_PREFIX}:{task_id}:cancelled", 300, "1")  # 5 分钟 TTL
    except Exception:
        pass


def is_task_cancelled(task_id: str) -> bool:
    """检查任务是否已被用户取消"""
    try:
        r = _get_redis()
        return bool(r.exists(f"{TASK_KEY_PREFIX}:{task_id}:cancelled"))
    except Exception:
        return False


def delete_task(task_id: str) -> bool:
    """删除任务状态记录，标记取消，并尝试终止 Celery 任务"""
    r = _get_redis()
    key = f"{TASK_KEY_PREFIX}:{task_id}"
    existed = r.exists(key)
    r.delete(key)
    # 标记取消（Celery worker 会在关键步骤检查此标记）
    mark_task_cancelled(task_id)

    try:
        from workers.celery_app import celery_app
        celery_app.control.revoke(task_id, terminate=True)
    except Exception:
        pass

    return bool(existed)


def get_task_count() -> Dict:
    """按状态统计任务数量"""
    tasks = _scan_tasks()
    counts: Dict = {"total": len(tasks), "by_state": {}}
    for task in tasks:
        state = task.get("state", "UNKNOWN")
        counts["by_state"][state] = counts["by_state"].get(state, 0) + 1
    return counts
