# 🐟 钓鱼数据看板

一个用于记录、统计、分析钓鱼数据的完整 Web 应用，支持多用户注册、数据看板、钓况分析和管理员后台。

**在线访问**: https://fishing-dashboard.onrender.com

---

## ✨ 功能特性

### 用户功能
- ✅ 用户注册/登录（JWT 认证）
- ✅ 记录钓鱼数据（日期、天气、温度、湿度、气压、地点、渔获等）
- ✅ 数据看板（统计图表：品种分布、温度趋势、气压散点等）
- ✅ 历史记录管理（搜索、筛选、编辑、删除）
- ✅ AI 智能分析（最佳钓鱼条件、最佳品种等）

### 管理员功能
- ⚙️ 查看所有用户列表
- ⚙️ 设置/取消管理员权限
- ⚙️ 查看任意用户的数据看板
- ⚙️ 删除用户

---

## 🚀 一键部署到免费云平台

### 方案一：Render.com（推荐，永久免费）

1. **上传代码到 GitHub**
   - 注册 [github.com](https://github.com)
   - 新建仓库，上传本项目所有文件

2. **部署到 Render**
   - 注册 [render.com](https://render.com)，用 GitHub 登录
   - 点 **"New +" → "Web Service"**
   - 连接你的 GitHub 仓库
   - 配置如下：

   | 设置项 | 值 |
   |--------|-----|
   | **Name** | `fishing-dashboard` |
   | **Region** | Singapore |
   | **Root Directory** | `backend` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |

3. **添加环境变量**
   - 在 Environment 页面添加：
   ```
   SECRET_KEY = 任意随机字符串（保护登录安全）
   ```

4. **部署完成！** 获得永久链接如：`https://your-app.onrender.com`

---

### 方案二：Railway.app（更简单）

1. 注册 [railway.app](https://railway.app)
2. 点 **"New Project" → "Empty Project"**
3. 上传本项目文件夹，Railway 自动识别为 Python 项目
4. 部署完成，获得链接！

---

### 方案三：本地运行

**Windows:**
```bash
cd fishing-dashboard/backend
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

**访问:** http://localhost:8000

---

## 📁 项目结构

```
fishing-dashboard/
├── backend/
│   ├── app.py              # FastAPI 主程序
│   ├── models.py           # 数据库模型
│   ├── auth.py             # JWT 认证
│   ├── requirements.txt    # Python 依赖
│   ├── start.sh            # Linux/云平台启动脚本
│   └── Procfile            # Heroku/Render 配置
├── frontend/
│   └── index.html          # 完整前端（登录+看板+管理）
├── railway.toml            # Railway 部署配置
├── .gitignore              # Git 忽略文件
└── README.md               # 说明文档
```

---

## 🔐 默认管理员账号

部署后第一个注册的账号自动成为管理员。

---

## 💡 技术栈

- **后端**: Python FastAPI + SQLite
- **前端**: 原生 HTML/CSS/JavaScript + Chart.js
- **认证**: JWT Token + SHA-256 密码加密

---

## 📝 License

MIT - 随便用！
