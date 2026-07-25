@echo off
title 动数派 - Start All Services

set ROOT=%~dp0
set CONDA_ENV=E:\Anaconda\envs\manim_ai
set REDIS_EXE=C:\Program Files\Redis\redis-server.exe
set REDIS_CLI=C:\Program Files\Redis\redis-cli.exe

echo ============================================
echo   动数派 - Starting All Services...
echo ============================================
echo.

REM --- 1. Redis ---
echo [1/5] Redis...
"%REDIS_CLI%" ping >nul 2>&1
if %errorlevel% equ 0 goto redis_ok
start "Redis" "%REDIS_EXE%"
timeout /t 2 /nobreak >nul
echo   Redis started (port 6379)
goto redis_done
:redis_ok
echo   Redis is already running (port 6379) - skip
:redis_done
echo.

REM --- 2. Java Backend ---
echo [2/5] Starting Java Backend (port 8080)...
cd /d "%ROOT%java-web"
start "Java-Backend" cmd /c "mvn spring-boot:run"
echo   Java Backend started (http://localhost:8080)
echo   Swagger: http://localhost:8080/swagger-ui.html
echo.

REM --- 3. FastAPI ---
echo [3/5] Starting Python AI Engine (port 8000)...
cd /d "%ROOT%ai-service"
start "AI-Engine" cmd /c ""%CONDA_ENV%\python.exe" main.py"
echo   AI Engine started (http://localhost:8000)
echo   API Docs: http://localhost:8000/docs
echo.

REM --- 4. Celery Worker ---
echo [4/5] Starting Celery Worker...
start "Celery-Worker" cmd /c ""%CONDA_ENV%\Scripts\celery.exe" -A workers.celery_app worker --loglevel=info -P solo"
echo   Celery Worker started
echo.

REM --- 5. Frontend ---
echo [5/5] Starting Frontend (port 5173)...
cd /d "%ROOT%front-html"
start "Frontend" cmd /c "npm run dev"
echo   Frontend started (http://localhost:5173)
echo.

echo ============================================
echo   All services started!
echo   Redis:       localhost:6379
echo   Java:        http://localhost:8080
echo   Swagger:     http://localhost:8080/swagger-ui.html
echo   AI Engine:   http://localhost:8000
echo   API Docs:    http://localhost:8000/docs
echo   Celery:      running in background
echo   Frontend:    http://localhost:5173
echo ============================================
echo.
echo Close each window to stop its service.
pause
