#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import traceback
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware  # ✅ 优化：添加 CORS 拦截器
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles  # ✅ 优化：添加静态资源服务
from pydantic import BaseModel, Field, field_validator

from ai_engine import run_full_pipeline, VIDEO_OUTPUT_SUBDIR

SERVER_HOST: str = "0.0.0.0"
SERVER_PORT: int = 8000
DEFAULT_MAX_RETRY: int = 3

app = FastAPI(
    title="Manim动画自动生成引擎API",
    description="基于本地大模型的Manim动画自动生成服务",
    version="1.0.0"
)

# ✅ 优化：配置跨域（CORS），解决前端 Vue/React 跨域请求报错问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议替换为具体前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 优化：挂载静态视频目录。前端可以通过 http://localhost:8000/videos/xxx.mp4 直接访问视频！
app.mount("/videos", StaticFiles(directory=str(VIDEO_OUTPUT_SUBDIR)), name="videos")

class GenerateResponse(BaseModel):
    success: bool = Field(..., description="任务是否执行成功")
    code: str = Field("", description="最终生成的Manim代码")
    video_path: str = Field("", description="可通过/videos路径访问的视频网络URL")
    try_count: int = Field(0, description="实际执行的尝试次数")
    log: str = Field("", description="完整执行日志与错误信息")

class GenerateRequest(BaseModel):
    user_input: str = Field(..., description="用户自然语言动画需求，必填项", min_length=2)
    max_retry: Optional[int] = Field(DEFAULT_MAX_RETRY, description="最大失败重试次数，范围1-10")

    @field_validator("max_retry", mode="after")
    @classmethod
    def check_retry_range(cls, v):
        if v is None or v < 1 or v > 10:
            return DEFAULT_MAX_RETRY
        return v

@app.get("/health", summary="服务健康检查")
def health_check():
    return {"status": "ok", "service": "manim-animation-engine", "version": "1.0.0"}

@app.post("/generate", summary="Manim动画生成", response_model=GenerateResponse)
def generate_animation(request: GenerateRequest):
    if not request.user_input or not request.user_input.strip():
        raise HTTPException(status_code=400, detail="user_input 不能为空")

    try:
        # FastAPI 会在内部线程池中执行这个同步阻塞函数，不会卡死主 Event Loop
        pipeline_result = run_full_pipeline(
            user_requirement=request.user_input.strip(),
            max_retry=request.max_retry
        )
        return pipeline_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内部错误：{str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # ✅ 优化：打印底层真正的异常堆栈到控制台，方便你排查 Bug
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "code": "",
            "video_path": "",
            "try_count": 0,
            "log": f"服务内部异常：{str(exc)}"
        }
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT, reload=False, log_level="info")