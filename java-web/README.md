# Manim 动画生成系统 — Java 后端模块

## 一、项目定位

Vue 前后端分离项目中的 **Java 后端服务**, 负责用户认证、任务管理, 并异步调用 Python AI 服务生成 Manim 动画视频。

| 模块 | 端口 | 技术 |
|------|------|------|
| Java 后端(本模块) | 8080 | Spring Boot + MyBatis-Plus |
| Python AI 服务 | 8000 | FastAPI + Manim |
| Vue 前端 | 8081 | Vue 3 + Axios |

---

## 二、技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Spring Boot | 2.7.18 | 基础框架 |
| MyBatis-Plus | 3.5.7 | ORM(零 XML, 全注解 + LambdaQueryWrapper) |
| MySQL | 8.0 | 数据库 |
| SpringDoc OpenAPI | 1.8.0 | Swagger 接口文档 |
| Hutool | 5.8.34 | HTTP 客户端(调 Python 服务) |
| jjwt | 0.12.6 | JWT 令牌生成与解析 |
| JDK | 1.8+ | 编译运行 |

---

## 三、项目结构

```
java-web/
├── pom.xml                          # Maven 依赖
├── database.sql                     # 建库建表脚本(唯一权威)
│
└── src/main/java/com/manim/
    ├── ManimApplication.java        # 启动类
    │
    ├── config/
    │   ├── AsyncConfig.java         # 异步线程池(core=2, max=5)
    │   ├── FilterConfig.java        # 注册 AuthFilter 到 /api/*
    │   ├── JwtConfig.java           # 启动时读取 yml 注入 JwtUtil
    │   ├── MyMetaObjectHandler.java # 自动填充 createTime/updateTime
    │   ├── SwaggerConfig.java       # Swagger 文档信息
    │   └── WebConfig.java           # CORS 跨域配置
    │
    ├── filter/
    │   └── AuthFilter.java          # JWT 认证过滤器
    │
    ├── controller/
    │   ├── AuthController.java      # 用户注册/登录(白名单, 无需 token)
    │   └── ApiController.java       # 任务接口(需 JWT 认证)
    │
    ├── service/
    │   ├── TaskService.java         # 任务业务接口
    │   ├── UserService.java         # 用户业务接口
    │   └── impl/
    │       ├── TaskServiceImpl.java # 任务实现(含 @Async 调 Python)
    │       └── UserServiceImpl.java # 用户实现
    │
    ├── mapper/
    │   ├── TaskMapper.java          # Task CRUD
    │   └── UserMapper.java          # User CRUD
    │
    ├── pojo/
    │   ├── Result.java              # 统一响应 {code, msg, data}
    │   ├── Task.java                # 任务实体
    │   └── User.java                # 用户实体(密码 @JsonIgnore)
    │
    ├── dto/
    │   └── PythonResponse.java      # Python 服务返回的 DTO
    │
    ├── exception/
    │   ├── BusinessException.java   # 业务异常(含 code + msg)
    │   ├── UnauthorizedException.java # 401 未授权异常
    │   └── GlobalExceptionHandler.java # @RestControllerAdvice 全局处理
    │
    └── utils/
        ├── JwtUtil.java             # JWT 工具类(纯静态方法)
        ├── Md5Util.java             # MD5 加密工具类
        └── UserContext.java         # ThreadLocal 保存当前用户名
```

---

## 四、数据库设计

执行 `database.sql` 建库建表。

### user 表 — 系统登录用户

```text
id          INT PK AUTO_INCREMENT
username    VARCHAR(50) UNIQUE NOT NULL   -- 登录账号
password    VARCHAR(100) NOT NULL         -- MD5 密文
create_time DATETIME DEFAULT CURRENT_TIMESTAMP
```

### task 表 — 动画生成任务

```text
id          INT PK AUTO_INCREMENT
user_id     INT NOT NULL                  -- FK -> user.id
user_input  VARCHAR(600) NOT NULL         -- 用户需求文本
video_path  VARCHAR(1000) NULL            -- Python 返回的视频路径
status      TINYINT DEFAULT 0             -- 0-处理中 1-成功 2-失败
error_log   TEXT NULL                     -- 失败错误日志
create_time DATETIME                      -- 创建时间
update_time DATETIME                      -- 更新时间
```

---

## 五、API 接口总表

所有接口统一返回 `Result<T>` 格式:

```json
{
    "code": 200,
    "msg": "操作成功",
    "data": null
}
```

### 5.1 用户账号模块(白名单, 无需 JWT)

| 方法 | 路径 | 请求参数 | 返回 Result<data> | 说明 |
|------|------|----------|-------------------|------|
| POST | `/api/register` | username, password | `{token, username, userId}` | 校验唯一性 -> MD5 加密入库 -> 生成 JWT |
| POST | `/api/login` | username, password | `{token, username, userId}` | MD5 比对密码 -> 生成 JWT |

> 密码在入库前用 `Md5Util.md5()` 加密。
> JWT 的 claim subject 中存的是 username。

### 5.2 动画任务模块(需 `Authorization: Bearer <token>`)

| 方法 | 路径 | 请求参数 | 返回 Result<data> | 说明 |
|------|------|----------|-------------------|------|
| POST | `/api/submit` | userInput, maxRetry(默认3) | taskId (Integer) | 入库 status=0 -> @Async 调 Python |
| GET | `/api/task/status/{id}` | 路径参数 id | Task 对象 | Vue 轮询用, 校验任务归属 |
| GET | `/api/task/list` | 无 | Task[] | 只返回当前用户的任务, 按时间倒序 |

---

## 六、认证与数据流

```
请求 -> AuthFilter (Filter, 拦截 /api/*)
  |
  +-- 白名单 (/api/register, /api/login) -> 直接放行
  |
  +-- 其他请求 -> 校验 Authorization: Bearer <token>
      +-- 无/无效 -> 返回 401 JSON (Filter 内手动写入)
      +-- 有效 -> JwtUtil.getUsernameFromToken(token)
                  -> UserContext.setUsername(username)
                  -> 放行 -> Controller 从 UserContext 取用户
                  -> finally -> UserContext.remove()
```

### 异步调用 Python 服务流程

```
POST /api/submit
  |
  +-- 入库 task (status=0)
  |
  +-- @Async (独立线程池)
       |
       +-- POST http://localhost:8000/generate
            body: { user_input, max_retry }
            |
            response: { success, video_path, log }
            |
            +-- success=true  -> status=1, 写入 video_path
            +-- success=false -> status=2, 写入 error_log
```

### 前端获取视频播放

```
前端轮询 -> GET /api/task/status/{id}
  |
  +-- status=1 -> 拿到 task.videoPath = "/videos/xxx.mp4"
       |
       +-- 拼接 http://localhost:8000 + videoPath 播放
```

---

## 七、异常处理

```
Filter 层 (AuthFilter)
  +-- 手动 write JSON -> 因为 Filter 在 DispatcherServlet 之前

Controller 层
  +-- throw BusinessException / UnauthorizedException
       +-- @RestControllerAdvice (GlobalExceptionHandler) 捕获
            +-- 封装为 Result{code, msg} 返回前端

GlobalExceptionHandler 处理范围:
  +-- UnauthorizedException          -> 401
  +-- BusinessException              -> 自定义 code
  +-- MissingServletRequestParameterException -> 400
  +-- HttpRequestMethodNotSupportedException  -> 405
  +-- Exception (兜底)               -> 500
```

---

## 八、配置说明

### application.yml 要点

```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/manim_ai
    username: root
    password: root

jwt:
  secret: ManimAI2024SecretKeyForJWTTokenGenerationMustBe256BitsLong!!
  expiration: 86400000          # 24 小时

manim:
  ai:
    base-url: http://localhost:8000
    generate-endpoint: /generate
    read-timeout: 180000
```

> 修改 `spring.datasource.password` 为本地数据库密码。

---

## 九、启动步骤

### 1. 建库建表

执行 `database.sql`, 或用 MySQL 客户端运行:

```bash
mysql -u root -p < database.sql
```

### 2. 插入测试用户

```sql
INSERT INTO user VALUES (1, 'admin', 'e10adc3949ba59abbe56e057f20f883e', NOW());
-- 密码 123456 的 MD5
```

### 3. 修改数据库密码

编辑 `src/main/resources/application.yml`, 修改 `spring.datasource.password`。

### 4. 启动 Python AI 服务

确保 Python 服务已在 `http://localhost:8000` 运行。

### 5. 启动 Java 服务

```bash
mvn spring-boot:run
```

或直接运行 `ManimApplication.main()`。

### 6. 访问

| 地址 | 说明 |
|------|------|
| `http://localhost:8080` | Java 后端(Vue 前端通过 Axios 调用) |
| `http://localhost:8080/swagger-ui.html` | Swagger 接口文档 |
| `http://localhost:8000/docs` | Python AI 服务文档 |

---

## 十、Swagger 测试说明

1. 打开 `http://localhost:8080/swagger-ui.html`
2. 先调用 **用户账号接口** 的 `/api/login` 或 `/api/register`
3. 从返回结果中复制 `token` 值
4. 点击 Swagger 右上角的 **Authorize** 按钮
5. 输入 `Bearer <复制的token>` (注意 Bearer 后有空格)
6. 现在可以测试 **动画任务接口** 的三个接口了
