# Java 后端测试说明

## 运行测试

### 运行全部测试
```bash
cd java-web
mvn test
```

### 运行特定包/类的测试
```bash
# 运行所有 Controller 测试
mvn test -Dtest="com.manim.controller.*"

# 运行单个测试类
mvn test -Dtest="AuthControllerTest"

# 运行所有 Service 测试
mvn test -Dtest="com.manim.service.impl.*"
```

### 跳过测试编译
```bash
mvn test -Dmaven.test.skip=true
```

## 测试结构

```
src/test/java/com/manim/
├── controller/          # Controller 层 MockMvc 集成测试 (9个文件)
│   ├── AuthControllerTest.java
│   ├── HomeControllerTest.java
│   ├── SearchControllerTest.java
│   ├── KnowledgeControllerTest.java
│   ├── TemplateControllerTest.java
│   ├── AiSandboxControllerTest.java
│   ├── WorkControllerTest.java
│   ├── GalleryControllerTest.java
│   └── UserCenterControllerTest.java
├── service/impl/        # Service 层 Mockito 单元测试 (2个文件)
│   ├── UserServiceImplTest.java
│   └── WorkServiceImplTest.java
├── filter/              # 过滤器单元测试 (1个文件)
│   └── AuthFilterTest.java
├── exception/           # 异常处理器单元测试 (1个文件)
│   └── GlobalExceptionHandlerTest.java
├── utils/               # 工具类单元测试 (3个文件)
│   ├── JwtUtilTest.java
│   ├── Md5UtilTest.java
│   └── UserContextTest.java
└── pojo/                # POJO 单元测试 (1个文件)
    └── ResultTest.java
```

## 测试技术栈

| 技术 | 用途 |
|------|------|
| JUnit 5 (Jupiter) | 测试框架 |
| Mockito | Mock 框架 |
| MockMvc | Controller HTTP 端点测试 |
| spring-boot-starter-test | Spring Boot 测试启动器 |

## 测试用例覆盖率

| 层级 | 测试文件数 | 对应测试用例编号 |
|------|-----------|-----------------|
| Controller | 9 | TC-AUTH, TC-HOME, TC-SRCH, TC-KNOW, TC-TPL, TC-AI, TC-WORK, TC-GAL, TC-UC |
| Service | 2 | TC-AUTH(Service), TC-WORK(Service) |
| Filter | 1 | TC-FILTER |
| Exception | 1 | TC-EXC |
| Utils | 3 | TC-UTIL |
| POJO | 1 | TC-RES |

详细测试用例表见: `docs/test-case-table.md`

## 常见问题

### @MockBean 导入路径

Spring Boot 2.x 中 `@MockBean` 的正确导入路径：

```java
// ✅ 正确
import org.springframework.boot.test.mock.mockito.MockBean;

// ❌ 错误（包路径缺少 ".mockito"）
import org.springframework.boot.test.mock.bean.MockBean;
```

### MyBatis Plus Mapper Mock 时避免方法歧义

MyBatis Plus 3.5.x 的 `BaseMapper` 中 `insert` 和 `updateById` 等既有单实体版本又有 `Collection` 版本。Mock 时若使用无类型的 `any()` 会导致编译歧义，必须显式指定类型：

```java
// ❌ 编译错误：对 insert/updateById 的引用不明确
verify(mapper, never()).insert(any());
verify(mapper, never()).updateById(any());

// ✅ 显式指定类型避免歧义
verify(mapper, never()).insert(any(WorkLike.class));
verify(mapper, never()).updateById(any(User.class));
```

### KnowledgeEntry 字段说明

`KnowledgeEntry` 没有 `content` 字段。百科词条的内容使用分段的字段名称：
`definition`（定义）、`principle`（核心原理）、`example`（过程示例）、`complexity`（复杂度分析）、`misconception`（常见误区）。
