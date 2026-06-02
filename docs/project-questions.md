# 项目过程重要问题记录

这个文件专门记录项目推进过程中反复会遇到、并且对方向判断有影响的问题。

用途：

- 记录做项目时的重要疑问
- 记录当时的判断和原因
- 避免后面重复纠结同一个问题
- 为以后写复盘和准备面试提供素材

---

## Q001：这些事情 Agent 能不能替我做？如果可以，为什么不用 Agent？我自己做对找工作的好处是什么？

日期：`2026-05-29`

### 简短结论

能，而且很多基础工作 Agent 都能替你做。  
但这个项目不应该完全交给 Agent，你更适合把 Agent 当成高效搭档，而不是替身。

### Agent 能替我做什么

- 建仓库、配 Git、写 `.gitignore`
- 起 `FastAPI` / `Vue` 骨架
- 写初版 `README`
- 建目录、补模板文件
- 生成基础接口和配置文件
- 帮你查错、改错、补样板代码

### 为什么不能全交给 Agent

- 面试看的不是“仓库里有没有代码”，而是“你会不会讲清楚这些代码为什么这样写”
- 一旦项目跑不起来、依赖冲突、接口报错、数据库连不上，最后还是要靠你自己定位问题
- 如果基础工程动作全没自己做过，后面很容易只会“看懂一点”，但不会真正独立开发

### 自己做对找工作的好处

- 你能解释项目是怎么从 0 搭起来的
- 你能说清楚技术栈为什么这么选
- 你能独立完成最基础的工程初始化
- 你会更容易回答面试里的细节追问
- 你会逐渐形成自己的工程习惯，而不是只会复制结果

### 现在最适合的做法

把 Agent 当成协作工具，而不是外包工具。

建议这样分工：

- 可以让 Agent 做：
  - 搭脚手架
  - 写模板代码
  - 生成文档初稿
  - 帮你排查和修复错误
  - 帮你重构和整理代码

- 最好自己亲自做并搞懂：
  - Git 基本流程
  - 后端服务怎么启动
  - 一个接口怎么从请求走到返回
  - 数据库表为什么这样设计
  - 前后端怎么连起来

- 必须自己能讲清楚：
  - 为什么选这套技术栈
  - 为什么这样拆目录
  - 遇到过什么问题
  - 你是怎么解决的
  - 如果继续做，下一步怎么推进

### 对当前项目的实际建议

这个阶段最好的策略不是“完全自己写”，也不是“完全交给 Agent”，而是：

- 方向和关键决策你来定
- 第一遍工程骨架你亲自参与
- 重复性强、样板化的部分可以让 Agent 帮你完成
- 每做完一步，都要确保自己能复述这一步在做什么

### 一句话记住

项目可以借助 Agent 提高效率，但能力建设和面试竞争力，最终还是来自你自己理解并主导这个项目。

---

## Q002：后端注册接口的数据是怎么流的？

日期：`2026-05-31`

### 问题背景

注册接口是从零开始写的第一个完整后端接口。想知道一个请求从发出到返回，后端都经过哪些环节。

### 简短结论

```
curl (请求) → main.py (路由匹配) → auth.py (业务逻辑) → models.py (操作数据库) → 返回 JSON
```

### 逐文件拆解

#### ① 入口 — `app/main.py`

```python
from app.routers import auth
app.include_router(auth.router)
```

`include_router` 的作用：把 auth.py 里定义的所有接口（`/auth/register`, `/auth/login`）注册到 FastAPI 应用上。这样当请求 `/auth/register` 来时，FastAPI 知道去找 auth.py 处理。

#### ② 路由处理 — `app/routers/auth.py`

```python
@router.post("/register", response_model=UserResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
```

- `@router.post("/register")` — 声明这是一个 POST 方法，路径是 `/auth/register`。`router` 前面定义了 `prefix="/auth"`，所以拼起来就是完整路径。
- `req: RegisterRequest` — 你的请求体 JSON 自动转成 Python 对象。如果少了字段，FastAPI 直接返回 400。
- `db: Session = Depends(get_db)` — FastAPI 自动创建一个数据库连接给你用，函数结束自动关闭。

#### ③ 数据校验 — `app/schemas.py`

```python
class RegisterRequest(BaseModel):
    username: str      # 必须是字符串
    email: str         # 必须是字符串
    password: str      # 必须是字符串
```

你少传一个字段，FastAPI 就返回：
```json
{"detail": [{"msg": "field required", "type": "value_error.missing"}]}
```
**不会执行后面的任何代码**——这是第一道安全门。

#### ④ 查重

```python
if db.query(User).filter(User.username == req.username).first():
    raise HTTPException(status_code=400, detail="用户名已存在")
```

这句 SQL 等价于：
```sql
SELECT * FROM users WHERE username = 'test' LIMIT 1;
```
查到说明用户名被注册了，直接返回 400，不继续。

#### ⑤ 密码加密

```python
def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
```

为什么不能存明文密码？如果数据库被拖，用户密码全泄漏。bcrypt 把 `"123456"` 转成类似这样的密文：
```
$2b$12$LJ3m8Ys0mfDQP.4HkeVuUO2...
```
**无法逆推回原始密码**。登录验证时也是用 bcrypt 比对，不是解密。

#### ⑥ 写数据库

```python
user = User(
    username=req.username,
    email=req.email,
    password_hash=_hash_password(req.password),
)
db.add(user)    # 把 user 对象加到会话
db.commit()     # 提交事务，真正写入 PostgreSQL
db.refresh(user)  # 从数据库回读自动生成的 id
```

数据库里对应的 `users` 表长这样（来自 `app/models/models.py`）：

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(128))
    created_at = Column(DateTime)
```

#### ⑦ 返回结果

```python
return user
```

FastAPI 根据 `response_model=UserResponse` 自动把 User 对象转成 JSON：

```python
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
```

注意没有 `password_hash` 字段，所以密码不会出现在返回结果里。

### 数据流全景图

```
你发的请求                           数据库
  │                                   ▲
  ▼                                   │
┌──────────┐    ┌────────┐    ┌───────────┐
│ main.py  │ →  │auth.py │ →  │models.py  │
│ 路由匹配  │    │ 校验   │    │            │
│          │    │ 查重   │    │ ORM 映射到 │
│          │    │ 加密   │    │ PostgreSQL │
│          │    │ 写库   │    │           │
└──────────┘    └────────┘    └───────────┘
                      │
                      ▼
                  返回 JSON ← schemas.py 控制返回什么字段
```

### 怎么自己验证

```bash
psql -U postgres -d campus_study
```

执行：
```sql
SELECT id, username, email, created_at FROM users;
```

看到刚注册的记录。密码列是密文，看不到原始密码。

### 面试能讲

"用户注册是怎么实现的？"

> 用户 POST 用户名、邮箱、密码过来，FastAPI 先通过 Pydantic 校验格式，没问题后查数据库有没有重名，没有就用 bcrypt 加密密码，ORM 写入 PostgreSQL，最后返回用户信息。密码不存明文也不返回。

后面有新的关键问题，可以直接按这个格式继续追加：

```md
## Q00X：问题标题

日期：`YYYY-MM-DD`

### 问题背景

### 简短结论

### 为什么

### 当前决定

### 后续影响
```
