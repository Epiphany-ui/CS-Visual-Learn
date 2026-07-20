# CS-Visual-Learn — 让抽象概念，动起来

> 基于 Manim + DeepSeek 大语言模型的交互式知识可视化学习平台

## 项目简介

将教材中抽象的算法、数据结构、数学定理转化为直观可交互的动画，提供"百科学习 → AI 生成 → 模板创作 → 画廊分享 → 社区交流"的完整闭环。

- **学习者**：通过动画直观理解抽象概念，111 个百科词条覆盖 7 大知识领域，支持结构化学习路径
- **创作者**：自然语言描述需求，AI 自动生成 Manim 代码并渲染为动画，支持 Fork 二次创作
- **模板使用者**：10 个参数化模板，零代码生成专业教学动画，支持视频质量调节

### 亮点功能

- 🎠 **首页动画轮播** — 精选动画展示，直观感受知识可视化魅力
- 🧪 **AI 沙箱** — 自然语言 → Manim 代码 → 视频渲染，支持 Canvas 风格交互与 Fork 协作
- 📐 **参数化模板** — 10 个模板，调节参数即可生成动画，零代码门槛
- 🖼️ **画廊** — 发布、收藏、分享动画作品
- 👥 **社区** — 关注创作者，浏览动态流
- 🗺️ **学习路径** — 按知识体系结构化学习

## 技术架构

```
┌──────────────────────────────────────────────────┐
│               前端 (front-html/)                   │
│  Vue 3 + TypeScript + Vite + Element Plus         │
│  Pinia + Vue Router + Axios + SSE                 │
│  CodeMirror 6 + KaTeX + marked + @vueuse          │
│  Sass + vue-codemirror                            │
│  14 个页面：首页/百科/沙箱/模板/画廊/社区/学习路径/登录  │
└────────────────────┬─────────────────────────────┘
                     │ HTTP + SSE
┌────────────────────▼─────────────────────────────┐
│           业务服务层 (java-web/)                    │
│  Spring Boot 2.7 + MyBatis-Plus 3.5 + MySQL       │
│  JWT 认证 + 用户系统 + 社区 + 14 张表               │
│  9 个 Controller：认证/沙箱/画廊/知识库/模板/作品 ...  │
└────────────────────┬─────────────────────────────┘
                     │ HTTP
┌────────────────────▼─────────────────────────────┐
│           核心引擎层 (ai-service/)                  │
│  FastAPI + DeepSeek + Manim Community v0.19       │
│  ChromaDB + Celery + Redis + SSE 实时推送          │
│  30+ REST API + 异步任务队列 + RAG 知识检索         │
│  JWT 中间件 + 限流 + 视频海报生成                    │
└──────────────────────────────────────────────────┘
```

## 项目结构

```
cs-visual-learn/
├── start.bat              # Windows 一键启动脚本
├── README.md
│
├── front-html/            # Vue 3 前端 — 14 个页面
│   └── src/
│       ├── views/         # 页面组件（Home, Wiki, Sandbox, Gallery, Community, Study, …）
│       ├── components/    # 共享组件
│       │   ├── common/    # 通用组件（AnimatedBackground, GlassCard, CodeEditor, …）
│       │   ├── layout/    # 布局组件（AppHeader, AppFooter）
│       │   └── sandbox/   # 沙箱组件（ParamPanel, TaskQueue）
│       ├── api/           # API 客户端层（auth, wiki, generation, tasks, templates, …）
│       ├── stores/        # Pinia 状态管理（app, user, task）
│       ├── composables/   # 组合式函数（useAuth, useSSE, useCurrentUser）
│       ├── directives/    # 自定义指令（magnet, ripple, tilt）
│       ├── types/         # TypeScript 类型定义
│       ├── styles/        # CSS 变量 + 全局样式 + 动画
│       └── router/        # Vue Router 路由
│
├── ai-service/            # Python AI 引擎 — 30+ API
│   ├── main.py            # FastAPI 入口
│   ├── ai_engine.py       # 核心引擎（代码生成 + 渲染 + RAG）
│   ├── services/          # 扩展服务（JWT/限流/模板/进度/评论/校验）
│   ├── workers/           # Celery 异步任务
│   ├── scripts/           # 工具脚本（KB 构建/海报生成/数据修复）
│   ├── prompts/           # LLM 提示词模板
│   ├── tests/             # 测试（pytest + fakeredis + 覆盖率）
│   ├── wiki_data/         # 111 个百科词条（7 大分类）
│   ├── templates/         # 10 个参数化模板
│   └── outputs/           # 渲染产物（代码 + 视频）
│
└── java-web/              # Spring Boot 业务层
    ├── src/main/java/com/manim/
    │   ├── controller/    # 9 个 Controller
    │   ├── service/       # 14 个 Service
    │   ├── mapper/        # MyBatis-Plus 数据访问层
    │   ├── pojo/          # 14 个实体类
    │   ├── config/        # 配置（JWT/Swagger/异步/Web）
    │   └── filter/        # 认证过滤器
    └── javawebDetails/    # 设计文档（API 文档/数据库设计/流程图）
```

## 快速启动

```bash
# Windows 一键启动（推荐）
双击 start.bat

# 或手动启动各服务：
# 1. Redis
"C:\Program Files\Redis\redis-server.exe"

# 2. API 服务
cd ai-service
python main.py  # → http://localhost:8000

# 3. Celery Worker
celery -A workers.celery_app worker --loglevel=info -P solo

# 4. 前端
cd front-html
npm run dev  # → http://localhost:5173
```

## 环境要求

- **Python** ≥ 3.10 + Manim Community v0.19 + FFmpeg
- **Node.js** 18+ + npm 9+
- **Java** 8+ + Maven 3.6+（Spring Boot 业务层）
- **DeepSeek API Key**（必需）
- **Redis**（异步任务 + 画廊数据缓存）
- **MySQL** 8.0（用户系统 + 社区 + 百科数据）
- **Ollama**（RAG 向量检索，可选）

## 许可证

MIT License
