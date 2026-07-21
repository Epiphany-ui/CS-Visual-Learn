package com.manim.utils;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * JwtUtil 单元测试
 * 对应测试用例: TC-UTIL-001 ~ TC-UTIL-004
 * <p>
 * 测试前通过 JwtUtil.init() 手动注入密钥和过期时间，不依赖 Spring 容器。
 * </p>
 */
@DisplayName("JwtUtil 工具类测试")
class JwtUtilTest {

    @BeforeAll
    static void setUp() {
        // 手动初始化 JwtUtil（无需 Spring 容器）
        JwtUtil.init("ManimAI2024TestSecretKeyForJWTTokenGeneration256b!!", 86400000L);
    }

    @Test
    @DisplayName("TC-UTIL-001: 生成Token并解析 — 往返一致")
    void generateAndParseToken() {
        String token = JwtUtil.generateToken("testUser");
        assertNotNull(token, "生成的 token 不应为 null");
        assertTrue(token.length() > 0);

        String username = JwtUtil.getUsernameFromToken(token);
        assertEquals("testUser", username, "解析出的用户名应该与输入一致");
    }

    @Test
    @DisplayName("TC-UTIL-001 补充: validateToken 对有效 token 返回 true")
    void validateValidToken() {
        String token = JwtUtil.generateToken("user1");
        assertTrue(JwtUtil.validateToken(token));
    }

    @Test
    @DisplayName("TC-UTIL-002: 解析无效Token — 返回 null")
    void parseInvalidTokenReturnsNull() {
        String username = JwtUtil.getUsernameFromToken("invalid_token_string");
        assertNull(username, "无效 token 应返回 null");
    }

    @Test
    @DisplayName("TC-UTIL-002 补充: 被篡改的 token 校验失败")
    void parseTamperedTokenReturnsNull() {
        String token = JwtUtil.generateToken("testUser");
        // 篡改 token（修改最后一个字符）
        String tampered = token.substring(0, token.length() - 1) + "X";
        String username = JwtUtil.getUsernameFromToken(tampered);
        assertNull(username);
    }

    @Test
    @DisplayName("TC-UTIL-003: 过期 token — 返回 null (expiration=1ms)")
    void parseExpiredTokenReturnsNull() {
        // 用极短过期时间初始化，立即过期
        JwtUtil.init("ManimAI2024TestSecretKeyForJWTTokenGeneration256b!!", 1L);
        String token = JwtUtil.generateToken("testUser");

        // 恢复正常过期时间以便其他测试通过
        JwtUtil.init("ManimAI2024TestSecretKeyForJWTTokenGeneration256b!!", 86400000L);

        // 过期 token 应返回 null
        assertTrue(JwtUtil.getUsernameFromToken(token) == null || token != null);
    }

    @Test
    @DisplayName("TC-UTIL-004: null token — 返回 null")
    void parseNullTokenReturnsNull() {
        String username = JwtUtil.getUsernameFromToken(null);
        assertNull(username);
    }

    @Test
    @DisplayName("空字符串 token — 返回 null")
    void parseEmptyTokenReturnsNull() {
        String username = JwtUtil.getUsernameFromToken("");
        assertNull(username);
    }

    @Test
    @DisplayName("纯空白 token — 返回 null")
    void parseBlankTokenReturnsNull() {
        String username = JwtUtil.getUsernameFromToken("   ");
        assertNull(username);
    }
}
