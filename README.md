# Mizuki Admin

一个基于 Vue + FastAPI 的 Mizuki 博客管理系统，提供图形化界面管理博客内容。

## 功能

### 基础设置
- **站点配置管理** - 修改博客标题、副标题、URL、开始日期等基本信息
- **主题配置** - 调整主题色色相、锁定主题色等样式设置

### 内容管理
- **文章管理** - 创建、编辑、删除 Markdown 文章，支持实时预览
- **日记管理** - 撰写日记，支持图片上传，按时间线展示
- **番剧管理** - 记录追番进度，支持在看/看过/想看状态切换
- **友链管理** - 管理友情链接，支持头像、简介、标签配置
- **相册管理** - 管理图片相册，支持加密相册和标签分类

### 个人展示
- **技能管理** - 展示技术技能，支持前端/后端/数据库/工具分类
- **时间线管理** - 记录教育、工作、项目等人生经历
- **项目管理** - 展示开发项目，支持状态标记和链接配置

## 技术栈

### 后端
- Python 3.11+
- FastAPI
- Uvicorn

### 前端
- Vue 3
- Vite
- Vue Router
- Axios

## 启动方式

### 一键启动
双击 `start.bat` 自动启动后端和前端。

### 手动启动

#### 1. 后端
```bash
cd backend
pip install -r requirements.txt
python main.py
```
后端运行在 http://localhost:8000

#### 2. 前端
```bash
cd frontend
npm install
npm run dev
```
前端运行在 http://localhost:3000

## 目录结构

```
mizuki-admin/
├── backend/            # Python 后端
│   ├── main.py        # 主程序入口
│   ├── requirements.txt
│   └── routers/       # API 路由
│       ├── config.py
│       ├── posts.py
│       ├── diary.py
│       ├── anime.py
│       ├── friends.py
│       ├── albums.py
│       ├── skills.py
│       ├── timeline.py
│       ├── projects.py
│       └── theme.py
├── frontend/           # Vue 前端
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── api/
│   │   └── views/
│   ├── index.html
│   └── package.json
├── start.bat          # 一键启动脚本
└── README.md
```

## 使用说明

1. 确保已安装 Python 3.11+ 和 Node.js 18+
2. 首次运行需要安装依赖
3. 后端需要一直运行，前端才能正常访问 API
4. 修改博客数据后需要重新构建并推送博客才能生效

## 注意事项

- 后端直接读写 Mizuki 博客的数据文件，请确保路径正确
- 建议在本地开发环境使用，生产环境请添加认证机制
- 图片上传功能需要博客目录结构支持
