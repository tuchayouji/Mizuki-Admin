@echo off
chcp 65001 >nul
title Mizuki Admin Launcher

echo.
echo  Mizuki Admin Launcher
echo.

:: 检查后端依赖
echo [1/4] Checking backend dependencies...
cd /d D:\boke\mizuki-admin\backend
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing backend dependencies...
    pip install -r requirements.txt
)

:: 检查前端依赖
echo [2/4] Checking frontend dependencies...
cd /d D:\boke\mizuki-admin\frontend
if not exist node_modules (
    echo Installing frontend dependencies...
    npm install
)

:: 启动后端
echo [3/4] Starting backend...
start "Mizuki Backend" cmd /k "cd /d D:\boke\mizuki-admin\backend && python main.py"

:: 等待后端启动
timeout /t 2 >nul

:: 启动前端
echo [4/4] Starting frontend...
start "Mizuki Frontend" cmd /k "cd /d D:\boke\mizuki-admin\frontend && npm run dev"

:: 等待前端启动并打开浏览器
timeout /t 3 >nul
start http://localhost:3000

echo.
echo Done! Browser opened.
echo.
