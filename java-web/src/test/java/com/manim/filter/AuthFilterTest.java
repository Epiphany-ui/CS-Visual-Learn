package com.manim.filter;

import com.manim.utils.JwtUtil;
import com.manim.utils.UserContext;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockFilterChain;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;

import javax.servlet.ServletException;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

/**
 * AuthFilter 认证过滤器测试
 * 对应测试用例: TC-FILTER-001 ~ TC-FILTER-009
 */
@DisplayName("AuthFilter 认证过滤器测试")
class AuthFilterTest {

    private AuthFilter filter;
    private MockHttpServletRequest request;
    private MockHttpServletResponse response;
    private MockFilterChain chain;

    @BeforeEach
    void setUp() {
        // AuthFilter 依赖 JwtUtil 静态方法，需初始化
        JwtUtil.init("ManimAI2024TestSecretKeyForJWTTokenGeneration256b!!", 86400000L);

        filter = new AuthFilter();
        request = new MockHttpServletRequest();
        response = new MockHttpServletResponse();
        chain = new MockFilterChain();
    }

    @AfterEach
    void tearDown() {
        UserContext.remove();
    }

    // ==================== 白名单测试 ====================

    @Test
    @DisplayName("TC-FILTER-001: 白名单 — /api/v1/user/register 直接放行")
    void whitelistRegister() throws IOException, ServletException {
        request.setMethod("POST");
        request.setRequestURI("/api/v1/user/register");

        filter.doFilter(request, response, chain);

        assertEquals(200, response.getStatus());
        assertNull(response.getContentType()); // 没有写 JSON 错误
    }

    @Test
    @DisplayName("TC-FILTER-002: 白名单 — /api/v1/user/login 直接放行")
    void whitelistLogin() throws IOException, ServletException {
        request.setMethod("POST");
        request.setRequestURI("/api/v1/user/login");

        filter.doFilter(request, response, chain);

        assertEquals(200, response.getStatus());
    }

    @Test
    @DisplayName("TC-FILTER-003: 白名单 — /api/v1/home/carousel 直接放行")
    void whitelistHome() throws IOException, ServletException {
        request.setRequestURI("/api/v1/home/carousel");

        filter.doFilter(request, response, chain);

        assertEquals(200, response.getStatus());
    }

    @Test
    @DisplayName("TC-FILTER-004: 白名单 — /api/v1/gallery/list 直接放行")
    void whitelistGallery() throws IOException, ServletException {
        request.setRequestURI("/api/v1/gallery/list");

        filter.doFilter(request, response, chain);

        assertEquals(200, response.getStatus());
    }

    @Test
    @DisplayName("白名单 — /api/v1/knowledge/** 放行")
    void whitelistKnowledge() throws IOException, ServletException {
        request.setRequestURI("/api/v1/knowledge/detail");
        request.setParameter("knowledgeId", "1");

        filter.doFilter(request, response, chain);

        assertEquals(200, response.getStatus());
    }

    @Test
    @DisplayName("白名单 — /api/v1/search/all 放行")
    void whitelistSearch() throws IOException, ServletException {
        request.setRequestURI("/api/v1/search/all");

        filter.doFilter(request, response, chain);

        assertEquals(200, response.getStatus());
    }

    // ==================== Token 校验测试 ====================

    @Test
    @DisplayName("TC-FILTER-006: 无 Authorization 头 — 返回 401")
    void noAuthorizationHeader() throws IOException, ServletException {
        request.setRequestURI("/api/v1/user/info");

        filter.doFilter(request, response, chain);

        assertEquals(401, response.getStatus());
        assertEquals("application/json;charset=UTF-8", response.getContentType());
        assertTrue(response.getContentAsString().contains("缺少 Authorization 请求头"));
    }

    @Test
    @DisplayName("TC-FILTER-007: Authorization 格式错误 (Basic 而非 Bearer) — 返回 401")
    void invalidAuthorizationFormat() throws IOException, ServletException {
        request.setRequestURI("/api/v1/user/info");
        request.addHeader("Authorization", "Basic dXNlcjpwYXNz");

        filter.doFilter(request, response, chain);

        assertEquals(401, response.getStatus());
        assertTrue(response.getContentAsString().contains("缺少 Authorization 请求头"));
    }

    @Test
    @DisplayName("TC-FILTER-008: Bearer Token 无效 — 返回 401")
    void invalidToken() throws IOException, ServletException {
        request.setRequestURI("/api/v1/user/info");
        request.addHeader("Authorization", "Bearer invalid_token_here");

        filter.doFilter(request, response, chain);

        assertEquals(401, response.getStatus());
        assertTrue(response.getContentAsString().contains("JWT 令牌无效或已过期"));
    }

    @Test
    @DisplayName("Authorization 头为纯 'Bearer ' (无token) — 返回 401")
    void bearerWithoutToken() throws IOException, ServletException {
        request.setRequestURI("/api/v1/user/info");
        request.addHeader("Authorization", "Bearer ");

        filter.doFilter(request, response, chain);

        assertEquals(401, response.getStatus());
    }

    @Test
    @DisplayName("TC-FILTER-009: 请求结束 finally 清理 UserContext")
    void finallyClearsUserContext() throws IOException, ServletException {
        request.setRequestURI("/api/v1/home/carousel");

        filter.doFilter(request, response, chain);

        // Finally 块应该已清理
        assertNull(UserContext.getUsername());
    }
}
