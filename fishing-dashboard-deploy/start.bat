@echo off
title 钓鱼数据看板 - 启动中...

echo.
echo  ====================================
echo    钓鱼数据看板 启动脚本
echo  ====================================
echo.

cd /d "%~dp0backend"

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
python -c "fastapi" >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖（首次运行）...
    pip install -r requirements.txt -q
    echo [完成] 依赖安装完成
)

echo.
echo [启动] 后端服务启动中...
echo [提示] 浏览器自动打开后，关闭此窗口即可停止服务
echo.

REM 启动服务并自动打开浏览器
start http://localhost:8000
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
