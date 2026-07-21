package com.manim.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.manim.pojo.User;
import com.manim.service.UserService;
import com.manim.utils.JwtUtil;
import com.manim.utils.UserContext;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * AuthController 集成测试 (MockMvc)
 * 对应测试用例: TC-AUTH-001 ~ TC-AUTH-014
 */
@WebMvcTest(AuthController.class)
@DisplayName("AuthController 用户认证接口测试")
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @BeforeEach
    void setUp() {
        // @WebMvcTest 不会加载 JwtConfig，手动初始化 JwtUtil
        // secret 长度必须 ≥256 bits (32字节) 以满足 HS256 要求
        JwtUtil.init("ManimAI2024TestSecretKeyForJWTTokenGeneration256b!!", 86400000L);
    }

    @AfterEach
    void tearDown() {
        UserContext.remove();
    }

    // ==================== 注册测试 ====================

    @Test
    @DisplayName("TC-AUTH-001: 正常注册 — 返回200含token和用户信息")
    void registerSuccess() throws Exception {
        when(userService.findByUsername("newuser")).thenReturn(null);
        doAnswer(inv -> {
            User u = inv.getArgument(0);
            u.setId(1);
            return null;
        }).when(userService).register(any(User.class));

        mockMvc.perform(post("/api/v1/user/register")
                        .param("username", "newuser")
                        .param("password", "123456")
                        .param("nickname", "新用户"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("注册成功"))
                .andExpect(jsonPath("$.data.username").value("newuser"))
                .andExpect(jsonPath("$.data.nickname").value("新用户"));
    }

    @Test
    @DisplayName("TC-AUTH-002: 用户名为空 — code=500")
    void registerEmptyUsername() throws Exception {
        mockMvc.perform(post("/api/v1/user/register")
                        .param("username", "")
                        .param("password", "123456"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("用户名不能为空"));
    }

    @Test
    @DisplayName("TC-AUTH-003: 密码过短 — code=500")
    void registerShortPassword() throws Exception {
        mockMvc.perform(post("/api/v1/user/register")
                        .param("username", "newuser")
                        .param("password", "12345"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("密码不能少于6位"));
    }

    @Test
    @DisplayName("TC-AUTH-004: 重复注册 — code=500")
    void registerDuplicateUsername() throws Exception {
        User existingUser = new User();
        existingUser.setUsername("existing");

        when(userService.findByUsername("existing")).thenReturn(existingUser);

        mockMvc.perform(post("/api/v1/user/register")
                        .param("username", "existing")
                        .param("password", "123456"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("账号已存在"));
    }

    @Test
    @DisplayName("TC-AUTH-005: nickname为空时默认使用username")
    void registerWithoutNickname() throws Exception {
        when(userService.findByUsername("abc")).thenReturn(null);
        doAnswer(inv -> {
            User u = inv.getArgument(0);
            u.setId(1);
            return null;
        }).when(userService).register(any(User.class));

        mockMvc.perform(post("/api/v1/user/register")
                        .param("username", "abc")
                        .param("password", "123456"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.nickname").value("abc"));
    }

    // ==================== 登录测试 ====================

    @Test
    @DisplayName("TC-AUTH-006: 正常登录 — 返回200含token和用户信息")
    void loginSuccess() throws Exception {
        User user = new User();
        user.setId(1);
        user.setUsername("testUser");
        user.setPassword("e10adc3949ba59abbe56e057f20f883e");
        user.setNickname("测试用户");
        user.setAvatar("/avatar.png");

        when(userService.login(eq("testUser"), anyString())).thenReturn(user);

        mockMvc.perform(post("/api/v1/user/login")
                        .param("username", "testUser")
                        .param("password", "123456"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("登录成功"))
                .andExpect(jsonPath("$.data.userId").value(1))
                .andExpect(jsonPath("$.data.username").value("testUser"))
                .andExpect(jsonPath("$.data.nickname").value("测试用户"));
    }

    @Test
    @DisplayName("TC-AUTH-007: 用户名为空 — code=500")
    void loginEmptyUsername() throws Exception {
        mockMvc.perform(post("/api/v1/user/login")
                        .param("username", "")
                        .param("password", "123456"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("用户名不能为空"));
    }

    @Test
    @DisplayName("TC-AUTH-008: 密码为空 — code=500")
    void loginEmptyPassword() throws Exception {
        mockMvc.perform(post("/api/v1/user/login")
                        .param("username", "testUser")
                        .param("password", ""))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("密码不能为空"));
    }

    @Test
    @DisplayName("TC-AUTH-009/010: 密码错误或用户不存在 — code=500")
    void loginWrongCredentials() throws Exception {
        when(userService.login(eq("testUser"), anyString())).thenReturn(null);

        mockMvc.perform(post("/api/v1/user/login")
                        .param("username", "testUser")
                        .param("password", "wrongpassword"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("用户名或密码错误"));
    }

    // ==================== 退出登录测试 ====================

    @Test
    @DisplayName("TC-AUTH-014: 退出登录 — code=200")
    void logoutSuccess() throws Exception {
        mockMvc.perform(post("/api/v1/user/logout"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
}
