# 项目推进记录

## 项目名
campus-study-agent

## 项目目标
一个支持课程资料上传、知识问答、复习计划生成的校园课程 AI 学习 Agent。

## 技术栈
- 后端：FastAPI (Python)
- 前端：Vue 3
- 数据库：PostgreSQL + pgvector

---

## 第一阶段：工程骨架

### 第 1 步：建目录 + 初始化 Git

- 创建项目文件夹 `campus-study-agent`
- 子目录：`backend/` `frontend/` `docs/`
- 执行 `git init`
- 创建 `.gitignore`（忽略 .env、.venv、node_modules、__pycache__ 等）
- 第一次 commit：`chore: initialize project structure`
- 验证：`git log --oneline` 看到 `a9c42ea` 提交记录

### 第 2 步：建 GitHub 远程仓库

- GitHub 新建空仓库 `campus-study-agent`
- 关联远程地址并推送
- 远程仓库已同步：`docs/progress.md`、`docs/project-questions.md`、`.gitignore`

### 第 3 步：后端骨架

**做了什么**
- `backend/` 下建 Python 虚拟环境 `.venv`
- 安装 `fastapi` + `uvicorn`
- 创建文件：
  - `backend/requirements.txt` — 依赖清单
  - `backend/app/__init__.py` — 包标识
  - `backend/app/main.py` — FastAPI 入口，定义 `/health` 接口

**代码理解**
```python
# main.py 做了什么：
# 1. 导入 FastAPI
# 2. 创建 app 实例
# 3. 定义一个 GET /health 接口，返回 {"status": "ok"}
```

**下一步**
- 启动 uvicorn 验证 `/health` 能访问
- 搭前端 Vue 3 项目
