# CS-Visual-Learn Java 后端测试用例表

> 项目: Manim AI 智能动画生成系统 | 框架: Spring Boot 2.7 + JUnit 5 + Mockito
> 测试分层: Controller 集成测试 (MockMvc) / Service 单元测试 (Mockito) / 工具类测试 / 过滤器测试

---

## 一、用户认证模块 (AuthController + UserService)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-AUTH-001 | 注册 | 正常注册 | username="newuser", password="123456", nickname="新用户" | code=200, msg="注册成功", data含token/userId/username/nickname | P0 |
| TC-AUTH-002 | 注册 | 用户名为空 | username="" 或 null | code=500, msg="用户名不能为空" | P0 |
| TC-AUTH-003 | 注册 | 密码过短 | password="12345" (少于6位) | code=500, msg="密码不能少于6位" | P0 |
| TC-AUTH-004 | 注册 | 重复注册 | username 已存在于数据库 | code=500, msg="账号已存在" | P0 |
| TC-AUTH-005 | 注册 | nickname为空时默认username | username="abc", password="123456", nickname=null | code=200, nickname 等于 username | P1 |
| TC-AUTH-006 | 登录 | 正常登录 | username="test1", password="123456" (正确) | code=200, msg="登录成功", data含token/userId/username/nickname/avatar | P0 |
| TC-AUTH-007 | 登录 | 用户名为空 | username="" 或 null | code=500, msg="用户名不能为空" | P0 |
| TC-AUTH-008 | 登录 | 密码为空 | password="" 或 null | code=500, msg="密码不能为空" | P0 |
| TC-AUTH-009 | 登录 | 密码错误 | username正确，password错误 | code=500, msg="用户名或密码错误" | P0 |
| TC-AUTH-010 | 登录 | 用户不存在 | username不存在于数据库 | code=500, msg="用户名或密码错误" | P0 |
| TC-AUTH-011 | 获取信息 | 正常获取 | Authorization header 携带有效 JWT | code=200, data含userId/username/nickname/avatar | P0 |
| TC-AUTH-012 | 获取信息 | 未登录 | 无 Authorization header | code=401, 未授权 | P0 |
| TC-AUTH-013 | 获取信息 | Token过期 | Authorization 携带过期JWT | code=401, JWT令牌无效或已过期 | P1 |
| TC-AUTH-014 | 退出登录 | 正常退出 | 携带有效Token | code=200, msg="操作成功" | P1 |

---

## 二、首页模块 (HomeController)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-HOME-001 | 轮播 | 获取热门轮播 | 无参数 | code=200, data为List<CarouselDTO> (最多6条) | P0 |
| TC-HOME-002 | 分类 | 获取知识点分类列表 | 无参数 | code=200, data为List<CategoryDTO> | P0 |
| TC-HOME-003 | 作品列表 | 最新作品(type=latest) | type="latest", page=1, size=10 | code=200, data含list和total | P0 |
| TC-HOME-004 | 作品列表 | 精选作品(type=featured) | type="featured", page=1, size=10 | code=200, result按like_count降序 | P0 |
| TC-HOME-005 | 作品列表 | 默认参数 | 不传type/page/size | type默认"latest", page默认1, size默认10 | P1 |

---

## 三、搜索模块 (SearchController + SearchService)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-SRCH-001 | 搜索 | 关键字搜索 | keyword="排序", page=1, size=10 | code=200, data含知识点/作品/模板/用户四类结果 | P0 |
| TC-SRCH-002 | 搜索 | 空关键字 | keyword="" 或不传 | code=400, 缺少必填参数 | P0 |
| TC-SRCH-003 | 搜索 | 无匹配结果 | keyword="不存在的内容xyz" | code=200, data中各类结果均为空列表 | P1 |
| TC-SRCH-004 | 搜索 | 分页边界 | keyword="test", page=999, size=10 | code=200, 返回空列表 | P1 |

---

## 四、百科知识模块 (KnowledgeController)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-KNOW-001 | 知识点列表 | 按分类查询 | categoryId=1, page=1, size=10 | code=200, data为List<KnowledgeListDTO> | P0 |
| TC-KNOW-002 | 知识点列表 | 按难度筛选 | difficulty=3, page=1, size=10 | code=200, 只返回难度=3的条目 | P1 |
| TC-KNOW-003 | 知识点列表 | 无参数查询 | 所有参数均不传 | code=200, 返回全部条目第一页 | P1 |
| TC-KNOW-004 | 词条详情 | 正常获取 | knowledgeId=1 (存在) | code=200, data为KnowledgeEntry | P0 |
| TC-KNOW-005 | 词条详情 | 词条不存在 | knowledgeId=99999 | code=500, msg="词条不存在" | P0 |
| TC-KNOW-006 | 配套动画 | 获取动画列表 | knowledgeId=1 | code=200, data为List<Animation> | P0 |
| TC-KNOW-007 | 相关推荐 | 获取推荐列表 | knowledgeId=1 | code=200, data为List<KnowledgeListDTO> | P1 |
| TC-KNOW-008 | 收藏 | 收藏知识点 | knowledgeId=1, isCollect=true, 已登录 | code=200 | P0 |
| TC-KNOW-009 | 收藏 | 取消收藏 | knowledgeId=1, isCollect=false, 已登录 | code=200 | P0 |
| TC-KNOW-010 | 收藏 | 未登录操作 | 无Authorization头 | code=401, 未授权 | P0 |
| TC-KNOW-011 | 学习打卡 | 正常打卡 | knowledgeId=1, studyDuration=600 | code=200 | P1 |
| TC-KNOW-012 | 学习打卡 | 未登录 | 无 Authorization 头 | code=401, 未授权 | P1 |

---

## 五、模板创作模块 (TemplateController)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-TPL-001 | 模板列表 | 获取全部模板 | 无参数 | code=200, data为List<Template> | P0 |
| TC-TPL-002 | 模板列表 | 按分类获取 | category="数学" | code=200, 只返回匹配分类的模板 | P1 |
| TC-TPL-003 | 模板详情 | 正常获取 | templateId=1 (存在) | code=200, data为Template | P0 |
| TC-TPL-004 | 模板详情 | 模板不存在 | templateId=99999 | code=500, msg="模板不存在" | P0 |
| TC-TPL-005 | 生成动画 | 正常提交 | userInput="画一个圆", maxRetry=3, 已登录 | code=200, data含taskId | P0 |
| TC-TPL-006 | 生成动画 | userInput为空 | userInput="" 或 null | code=500, msg="userInput 不能为空" | P0 |
| TC-TPL-007 | 生成动画 | 未登录 | 无 Authorization 头 | code=401 | P0 |
| TC-TPL-008 | 查询状态 | 正常查询 | taskId=1 (属于当前用户) | code=200, data为Task对象 | P0 |
| TC-TPL-009 | 查询状态 | 任务不存在 | taskId=99999 | code=500, msg="任务不存在" | P1 |
| TC-TPL-010 | 查询状态 | 无权访问 | taskId 属于其他用户 | code=500, msg="无权访问该任务" | P1 |
| TC-TPL-011 | 保存作品 | 正常保存 | taskId=1, workTitle="我的作品", isPublic=true | code=200, data含workId | P0 |
| TC-TPL-012 | 导出作品 | 导出MP4 | workId=1, exportType="mp4" | code=200, data含downloadUrl | P1 |
| TC-TPL-013 | 导出作品 | 导出代码 | workId=1, exportType="code" | code=200, downloadUrl="/api/v1/work/code/1" | P1 |
| TC-TPL-014 | 导出作品 | 不支持的格式 | exportType="pdf" | code=500, msg="不支持的导出类型" | P1 |
| TC-TPL-015 | 导出作品 | 作品不存在 | workId=99999 | code=500, msg="作品不存在" | P1 |
| TC-TPL-016 | 历史任务 | 获取任务列表 | 已登录 | code=200, data为List<Task> | P1 |

---

## 六、AI沙箱模块 (AiSandboxController)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-AI-001 | AI生成代码 | 正常生成 | userPrompt="画一个旋转的正方形", knowledgeId=null | code=200, data含生成的代码 | P0 |
| TC-AI-002 | AI生成代码 | userPrompt为空 | userPrompt="" | code=500, msg="userPrompt 不能为空" | P0 |
| TC-AI-003 | AI修复代码 | 正常修复 | errorLog="syntax error", oldCode="xxx" | code=200, data含修复后的代码 | P0 |
| TC-AI-004 | AI修复代码 | errorLog为空 | errorLog="" | code=500, msg="errorLog 不能为空" | P0 |
| TC-AI-005 | AI修复代码 | oldCode为空 | oldCode="" | code=500, msg="oldCode 不能为空" | P0 |
| TC-AI-006 | 沙箱渲染 | 正常渲染 | manimCode="from manim import *..." | code=200, data含taskId | P0 |
| TC-AI-007 | 沙箱渲染 | manimCode为空 | manimCode="" | code=500, msg="manimCode 不能为空" | P0 |
| TC-AI-008 | 沙箱渲染 | 未登录 | 无Authorization头 | code=401 | P0 |
| TC-AI-009 | 版本历史 | 正常查询 | workId=1 | code=200, data为List<SandboxDraft> | P1 |
| TC-AI-010 | 保存草稿 | 正常保存 | manimCode="xxx", previewUrl可选 | code=200, data含draftId和version | P0 |
| TC-AI-011 | 保存草稿 | 更新已有草稿 | draftId=1, manimCode="新增内容" | code=200, version自增 | P1 |
| TC-AI-012 | 保存草稿 | manimCode为空 | manimCode="" | code=500, msg="manimCode 不能为空" | P0 |
| TC-AI-013 | 发布作品 | 完整信息发布 | workTitle="测试作品", isPublic=true, code="xxx", tags="数学,几何" | code=200, data含publishedWorkId | P0 |
| TC-AI-014 | 发布作品 | workTitle为空 | workTitle="" | code=500, msg="workTitle 不能为空" | P0 |
| TC-AI-015 | 发布作品 | code为空 | code="" | code=500, msg="code 不能为空" | P0 |
| TC-AI-016 | 发布作品 | Fork来源发布 | sourceWorkId=1 | code=200, 作品记录Fork来源 | P1 |

---

## 七、作品互动模块 (WorkController)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-WORK-001 | 作品详情 | 获取公开作品 | workId=1 (公开作品) | code=200, data为Work, viewCount+1 | P0 |
| TC-WORK-002 | 作品详情 | 作品不存在 | workId=99999 | code=500, msg="作品不存在" | P0 |
| TC-WORK-003 | 点赞 | 点赞作品 | workId=1, isLike=true, 已登录 | code=200, likeCount+1 | P0 |
| TC-WORK-004 | 点赞 | 取消点赞 | workId=1, isLike=false, 已登录 | code=200, likeCount-1 | P0 |
| TC-WORK-005 | 点赞 | 重复点赞不增加 | 连续两次 isLike=true | code=200, likeCount只增加一次 | P1 |
| TC-WORK-006 | 点赞 | 未登录 | 无Authorization头 | code=401 | P0 |
| TC-WORK-007 | 收藏 | 收藏作品 | workId=1, isCollect=true | code=200, collectCount+1 | P0 |
| TC-WORK-008 | 收藏 | 取消收藏 | workId=1, isCollect=false | code=200, collectCount-1 | P0 |
| TC-WORK-009 | 评论列表 | 获取评论 | workId=1 | code=200, data为List<WorkComment> | P0 |
| TC-WORK-010 | 发布评论 | 正常发布 | workId=1, content="不错" | code=200, data含commentId | P0 |
| TC-WORK-011 | 发布评论 | 回复评论 | workId=1, content="谢谢", replyId=1 | code=200, 记录replyId | P1 |
| TC-WORK-012 | 发布评论 | 内容为空 | content="" | code=500, msg="评论内容不能为空" | P0 |
| TC-WORK-013 | Fork | 正常Fork | workId=1, 已登录 | code=200, data含workId/sourceCode/sourceAuthor | P0 |
| TC-WORK-014 | Fork | 作品不存在 | workId=99999 | code=500, msg="作品不存在" | P0 |
| TC-WORK-015 | 关注 | 关注创作者 | authorId=2, isFollow=true | code=200 | P0 |
| TC-WORK-016 | 关注 | 取消关注 | authorId=2, isFollow=false | code=200 | P0 |
| TC-WORK-017 | 关注 | 自己关注自己 | authorId等于当前用户ID | code=500, msg="不能关注自己" | P1 |
| TC-WORK-018 | 删除作品 | 删除自己的作品 | workId属于当前用户 | code=200 | P0 |
| TC-WORK-019 | 删除作品 | 删除他人作品 | workId不属于当前用户 | code=500, msg="无权删除他人作品" | P0 |
| TC-WORK-020 | 删除作品 | 作品不存在 | workId=99999 | code=500, msg="作品不存在" | P1 |
| TC-WORK-021 | 可见性切换 | 公开→私密 | workId (isPublic=1) | code=200, isPublic变为0 | P1 |
| TC-WORK-022 | 可见性切换 | 私密→公开 | workId (isPublic=0) | code=200, isPublic变为1 | P1 |
| TC-WORK-023 | 更新作品 | 更新标题 | workId=1, title="新标题" | code=200 | P0 |
| TC-WORK-024 | 更新作品 | 更新描述 | workId=1, description="新描述" | code=200 | P0 |
| TC-WORK-025 | 更新作品 | title和description都为空 | title="" 且 description="" | code=500, msg="至少需要提供标题或描述" | P1 |
| TC-WORK-026 | 创作者主页 | 获取创作者主页 | authorId=2 (存在) | code=200, data含authorInfo/workCount/totalLikes/followerCount/workList | P0 |
| TC-WORK-027 | 创作者主页 | 创作者不存在 | authorId=99999 | code=500, msg="创作者不存在" | P0 |
| TC-WORK-028 | 用户查询 | 根据用户名查用户 | username="test1" (存在) | code=200, data含userId/username/nickname/avatar/intro | P1 |
| TC-WORK-029 | 用户查询 | 用户不存在 | username="nonexist" | code=500, msg="用户不存在" | P1 |

---

## 八、社区画廊模块 (GalleryController)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-GAL-001 | 画廊列表 | 默认排行榜 | rankType="weekly" | code=200, data含list和total | P0 |
| TC-GAL-002 | 画廊列表 | 按时间排序 | sort="time" | code=200, 结果按create_time降序 | P0 |
| TC-GAL-003 | 画廊列表 | 按点赞排序 | sort="likes" | code=200, 结果按like_count降序 | P0 |
| TC-GAL-004 | 画廊列表 | 按分类筛选 | category="几何" | code=200, 只返回tags含"几何"的作品 | P1 |
| TC-GAL-005 | 画廊列表 | 分页 | page=2, size=5 | code=200, 返回第2页5条 | P1 |

---

## 九、个人中心模块 (UserCenterController)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-UC-001 | 个人首页 | 获取首页数据 | 已登录 | code=200, 含userInfo/workCount/totalStudyMinutes/checkinDays/follower/followee | P0 |
| TC-UC-002 | 个人首页 | 未登录 | 无Authorization | code=401 | P0 |
| TC-UC-003 | 我的作品 | 获取作品列表 | status=1, page=1, size=10 | code=200, data含list和total | P0 |
| TC-UC-004 | 我的作品 | 按状态筛选 | status=0 (草稿) | code=200, 只返回草稿作品 | P1 |
| TC-UC-005 | 我的收藏 | 获取收藏列表 | type=1, page=1, size=10 | code=200, data为List<UserCollect> | P0 |
| TC-UC-006 | 浏览历史 | 获取历史 | page=1, size=10 | code=200, data为List<BrowseHistory> | P0 |
| TC-UC-007 | 学习统计 | 获取统计 | 已登录 | code=200, data为学习统计数据 | P0 |
| TC-UC-008 | 创作者统计 | 获取统计 | 已登录 | code=200, 含totalViews/totalLikes/totalCollects/totalForks/workDetails | P0 |
| TC-UC-009 | 更新资料 | 更新昵称 | nickname="新昵称" | code=200 | P0 |
| TC-UC-010 | 更新资料 | 更新全部字段 | nickname+avatar+intro 全传 | code=200, 全部更新 | P0 |
| TC-UC-011 | 更新资料 | 不传任何字段 | 所有参数不传 | code=200, 不报错 | P1 |

---

## 十、工具类 & 过滤器测试

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-UTIL-001 | JwtUtil | 生成Token并解析 | username="test1" | 生成的token可解析回"test1" | P0 |
| TC-UTIL-002 | JwtUtil | 解析无效Token | token="invalid_token_string" | 返回 null | P0 |
| TC-UTIL-003 | JwtUtil | 解析过期Token | 过期token | 返回 null | P1 |
| TC-UTIL-004 | JwtUtil | 空/null token | token=null | 返回 null | P1 |
| TC-UTIL-005 | Md5Util | MD5加密 | password="123456" | 返回32位十六进制MD5字符串 | P0 |
| TC-UTIL-006 | Md5Util | 空字符串加密 | password="" | 返回MD5("")的固定值 | P1 |
| TC-UTIL-007 | Md5Util | 相同输入产生相同摘要 | 两次 md5("123456") | 返回相同的值 | P0 |
| TC-UTIL-008 | UserContext | set/get/remove | setUsername("test") → getUsername() → remove() → getUsername() | "test" → "test" → 清除后返回null | P0 |
| TC-UTIL-009 | UserContext | 多线程隔离 | 线程A setUsername("A")，线程B setUsername("B") | 线程A getUsername()="A", 线程B getUsername()="B" | P1 |
| TC-FILTER-001 | AuthFilter | 白名单-注册路径放行 | POST /api/v1/user/register | 直接放行, 不校验token | P0 |
| TC-FILTER-002 | AuthFilter | 白名单-登录路径放行 | POST /api/v1/user/login | 直接放行, 不校验token | P0 |
| TC-FILTER-003 | AuthFilter | 白名单-首页路径放行 | GET /api/v1/home/carousel | 直接放行 | P0 |
| TC-FILTER-004 | AuthFilter | 白名单-画廊放行 | GET /api/v1/gallery/list | 直接放行 | P0 |
| TC-FILTER-005 | AuthFilter | 有效Token通过 | Authorization: Bearer <valid_token> | 通过校验, 设置UserContext | P0 |
| TC-FILTER-006 | AuthFilter | 无Authorization头 | 访问 /api/v1/user/info 不带header | 返回401, "缺少 Authorization 请求头" | P0 |
| TC-FILTER-007 | AuthFilter | Token格式错误 | Authorization: "Basic xxx" | 返回401 | P0 |
| TC-FILTER-008 | AuthFilter | Token无效 | Authorization: Bearer invalid_token | 返回401, "JWT 令牌无效或已过期" | P0 |
| TC-FILTER-009 | AuthFilter | 请求结束后清理UserContext | 任意请求通过filter | finally块中UserContext.remove()被调用 | P1 |

---

## 十一、异常处理测试 (GlobalExceptionHandler)

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-EXC-001 | 异常处理 | BusinessException | 抛出 BusinessException(500, "测试错误") | 返回 {code:500, msg:"测试错误"} | P0 |
| TC-EXC-002 | 异常处理 | UnauthorizedException | 抛出 UnauthorizedException("未登录") | 返回 {code:401, msg:"未登录"} | P0 |
| TC-EXC-003 | 异常处理 | 缺少必填参数 | 请求缺少 @RequestParam(required=true) | 返回 {code:400, msg:"缺少必填参数: xxx"} | P0 |
| TC-EXC-004 | 异常处理 | 不支持的HTTP方法 | POST访问只支持GET的接口 | 返回 {code:405, msg:"请求方法不支持: POST"} | P1 |
| TC-EXC-005 | 异常处理 | 未知运行时异常 | 抛出 RuntimeException("内部错误") | 返回 {code:500, msg:"服务器内部错误: 内部错误"} | P0 |

---

## 十二、Result 统一响应测试

| 编号 | 模块 | 测试方法 | 输入/前置条件 | 预期结果 | 优先级 |
|------|------|----------|--------------|----------|--------|
| TC-RES-001 | Result | success() 无数据 | Result.success() | code=200, msg="操作成功", data=null | P0 |
| TC-RES-002 | Result | success(T data) | Result.success("hello") | code=200, msg="操作成功", data="hello" | P0 |
| TC-RES-003 | Result | success(msg, data) | Result.success("自定义", map) | code=200, msg="自定义", data=map | P0 |
| TC-RES-004 | Result | fail(msg) | Result.fail("错误") | code=500, msg="错误", data=null | P0 |
| TC-RES-005 | Result | fail(code, msg) | Result.fail(400, "参数错误") | code=400, msg="参数错误", data=null | P0 |

---

## 统计

| 测试层级 | 测试用例数 | P0 | P1 |
|----------|-----------|----|-----|
| 用户认证 (Auth) | 14 | 9 | 5 |
| 首页 (Home) | 5 | 4 | 1 |
| 搜索 (Search) | 4 | 2 | 2 |
| 百科知识 (Knowledge) | 12 | 7 | 5 |
| 模板创作 (Template) | 16 | 9 | 7 |
| AI沙箱 (AiSandbox) | 16 | 11 | 5 |
| 作品互动 (Work) | 29 | 17 | 12 |
| 社区画廊 (Gallery) | 5 | 4 | 1 |
| 个人中心 (UserCenter) | 11 | 8 | 3 |
| 工具类 (Utils) | 9 | 5 | 4 |
| 过滤器 (Filter) | 9 | 8 | 1 |
| 异常处理 (Exception) | 5 | 4 | 1 |
| Result 响应 | 5 | 5 | 0 |
| **合计** | **140** | **93** | **47** |
