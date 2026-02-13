# The Sheland

请遵守中华人民共和国法律和国家领土主权完整

## 项目简介

The Sheland 是一个多人在线伪桌游游戏，玩家可以扮演"政客"竞选选票，或扮演"上帝"掌控全局。

## 技术栈

- **前端**: Vue 3 + TypeScript + Vite
- **后端**: Django + Django REST Framework + Django Channels (WebSocket)
- **数据库**: PostgreSQL (推荐) / SQLite (开发)
- **状态管理**: Pinia
- **UI组件**: Element Plus

## 游戏规则

### 角色
- **政客 (Politician)**: 在地图区域竞选，争取选票，平衡不同地区文化诉求
- **上帝 (God)**: 可以干预选举、修改地图、影响文化参数

### 核心机制
- 使用随机种子生成：地图参数、选举参数、国家/地区/文化参数
- 相同种子生成相同的地图和参数
- 回合制策略游戏

## 项目结构

```
the-sheland/
├── backend/          # Django 后端
│   ├── the_sheland/  # 项目配置
│   ├── game/         # 游戏核心逻辑
│   ├── rooms/        # 房间管理
│   └── users/        # 用户管理
├── frontend/         # Vue 3 前端
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── views/       # 页面
│   │   ├── stores/      # Pinia 状态管理
│   │   ├── api/         # API 请求
│   │   └── utils/       # 工具函数
│   └── package.json
└── README.md
```

## 快速开始

### 后端启动

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

## API 文档

启动后端后访问: http://localhost:8000/api/docs/

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

MIT License
