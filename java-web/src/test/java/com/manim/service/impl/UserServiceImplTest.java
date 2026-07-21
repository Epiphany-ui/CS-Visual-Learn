package com.manim.service.impl;

import com.manim.mapper.UserMapper;
import com.manim.pojo.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * UserServiceImpl 单元测试
 * 对应测试用例: TC-AUTH-001 ~ TC-AUTH-010 (Service层)
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("UserService 业务逻辑测试")
class UserServiceImplTest {

    @Mock
    private UserMapper userMapper;

    @InjectMocks
    private UserServiceImpl userService;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = new User();
        testUser.setId(1);
        testUser.setUsername("testUser");
        testUser.setPassword("e10adc3949ba59abbe56e057f20f883e"); // MD5("123456")
        testUser.setNickname("测试用户");
    }

    // ==================== 注册测试 ====================

    @Test
    @DisplayName("TC-AUTH-001: 正常注册 — insert 被执行")
    void registerSuccess() {
        User newUser = new User();
        newUser.setUsername("newuser");
        newUser.setPassword("e10adc3949ba59abbe56e057f20f883e");
        newUser.setNickname("新用户");

        when(userMapper.insert(any(User.class))).thenReturn(1);

        userService.register(newUser);

        verify(userMapper, times(1)).insert(newUser);
    }

    // ==================== 登录测试 ====================

    @Test
    @DisplayName("TC-AUTH-006: 正常登录 — 用户名密码正确返回 User")
    void loginSuccess() {
        when(userMapper.selectOne(any())).thenReturn(testUser);

        User result = userService.login("testUser", "e10adc3949ba59abbe56e057f20f883e");

        assertNotNull(result);
        assertEquals("testUser", result.getUsername());
    }

    @Test
    @DisplayName("TC-AUTH-009: 密码错误 — 返回 null")
    void loginWrongPassword() {
        when(userMapper.selectOne(any())).thenReturn(testUser);

        User result = userService.login("testUser", "wrong_md5_hash");

        assertNull(result);
    }

    @Test
    @DisplayName("TC-AUTH-010: 用户不存在 — 返回 null")
    void loginUserNotFound() {
        when(userMapper.selectOne(any())).thenReturn(null);

        User result = userService.login("nonexist", "any_hash");

        assertNull(result);
    }

    @Test
    @DisplayName("login: username 为 null — 返回 null")
    void loginNullUsername() {
        User result = userService.login(null, "any_hash");
        assertNull(result);
    }

    @Test
    @DisplayName("login: encryptedPassword 为 null — 返回 null")
    void loginNullPassword() {
        User result = userService.login("testUser", null);
        assertNull(result);
    }

    // ==================== 查询测试 ====================

    @Test
    @DisplayName("findByUsername: 用户存在 — 返回 User")
    void findByUsernameExists() {
        when(userMapper.selectOne(any())).thenReturn(testUser);

        User result = userService.findByUsername("testUser");

        assertNotNull(result);
        assertEquals("testUser", result.getUsername());
    }

    @Test
    @DisplayName("findByUsername: 用户不存在 — 返回 null")
    void findByUsernameNotExists() {
        when(userMapper.selectOne(any())).thenReturn(null);

        User result = userService.findByUsername("nonexist");

        assertNull(result);
    }

    @Test
    @DisplayName("getById: 根据ID查询")
    void getById() {
        when(userMapper.selectById(1)).thenReturn(testUser);

        User result = userService.getById(1);

        assertNotNull(result);
        assertEquals(1, result.getId());
    }

    // ==================== 更新资料测试 ====================

    @Test
    @DisplayName("TC-UC-009: updateProfile — 更新昵称")
    void updateProfileNickname() {
        when(userMapper.selectById(1)).thenReturn(testUser);
        when(userMapper.updateById(any(User.class))).thenReturn(1);

        userService.updateProfile(1, "新昵称", null, null);

        verify(userMapper).updateById(testUser);
        assertEquals("新昵称", testUser.getNickname());
    }

    @Test
    @DisplayName("updateProfile: 用户不存在 — 不抛异常")
    void updateProfileUserNotFound() {
        when(userMapper.selectById(999)).thenReturn(null);

        assertDoesNotThrow(() -> userService.updateProfile(999, "昵称", null, null));
        verify(userMapper, never()).updateById(any(User.class));
    }
}
