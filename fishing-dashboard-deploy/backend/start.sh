#!/bin/bash
# Render.com 部署启动脚本
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port $PORT
