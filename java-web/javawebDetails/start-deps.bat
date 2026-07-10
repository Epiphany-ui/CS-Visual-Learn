@echo off
title CS Visual Learn - Start Redis + Python + Celery

set REDIS_EXE=E:\Redis\Redis-x64-3.2.100\redis-server.exe
set AI_SERVICE=%~dp0..\..\ai-service
set VENV_UVICORN=%AI_SERVICE%\.venv\Scripts\uvicorn.exe
set VENV_CELERY=%AI_SERVICE%\.venv\Scripts\celery.exe

echo ============================================
echo   Starting Redis + Python + Celery
echo ============================================
echo.

echo [1/3] Starting Redis (port 6379)...
start /b "" "%REDIS_EXE%" >nul 2>&1
timeout /t 2 /nobreak >nul
echo   Redis started
echo.

echo [2/3] Starting Python AI service (port 8000)...
start /b "" cmd /c "set DEEPSEEK_API_KEY=%DEEPSEEK_API_KEY% && cd /d "%AI_SERVICE%" && "%VENV_UVICORN%" main:app --host 0.0.0.0 --port 8000" > "%TEMP%\cs-ai-service.log" 2>&1
echo   AI service starting... (http://localhost:8000)
echo.

echo [3/3] Starting Celery Worker...
start /b "" cmd /c "set DEEPSEEK_API_KEY=%DEEPSEEK_API_KEY% && cd /d "%AI_SERVICE%" && "%VENV_CELERY%" -A workers.celery_app worker --loglevel=info -P solo" > "%TEMP%\cs-celery.log" 2>&1
echo   Celery Worker started
echo.

echo ============================================
echo   Ready!
echo     Redis:        localhost:6379
echo     AI Service:   http://localhost:8000
echo     API Docs:     http://localhost:8000/docs
echo     Celery:       running
echo.
echo   Java / Vue 请自行启动。
echo   Close this window to stop all services.
echo ============================================

:wait
timeout /t 10 /nobreak >nul
goto wait
