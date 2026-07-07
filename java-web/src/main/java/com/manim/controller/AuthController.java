package com.manim.controller;

import com.manim.exception.BusinessException;
import com.manim.pojo.Result;
import com.manim.pojo.User;
import com.manim.service.UserService;
import com.manim.utils.JwtUtil;
import com.manim.utils.Md5Util;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 用户账号接口（白名单，无须 token）
 */
@Tag(name = "用户账号接口")
@RestController
@RequestMapping("/api")
public class AuthController {

    @Autowired
    private UserService userService;

    @Operation(summary = "用户注册")
    @PostMapping("/register")
    public Result<Map<String, Object>> register(
            @RequestParam("username") String username,
            @RequestParam("password") String password) {

        if (username == null || username.trim().isEmpty()) {
            throw new BusinessException("用户名不能为空");
        }
        if (password == null || password.length() < 6) {
            throw new BusinessException("密码不能少于6位");
        }

        // 校验账号是否重复
        User exist = userService.findByUsername(username.trim());
        if (exist != null) {
            throw new BusinessException("账号已存在");
        }

        // MD5 加密 + 创建用户
        String encryptedPwd = Md5Util.md5(password);
        User user = new User();
        user.setUsername(username.trim());
        user.setPassword(encryptedPwd);
        userService.register(user);

        // 生成 JWT 令牌（claim 中是用户名）
        String token = JwtUtil.generateToken(user.getUsername());

        Map<String, Object> data = new HashMap<>();
        data.put("token", token);
        data.put("username", user.getUsername());
        data.put("userId", user.getId());

        return Result.success("注册成功", data);
    }

    @Operation(summary = "用户登录")
    @PostMapping("/login")
    public Result<Map<String, Object>> login(
            @RequestParam("username") String username,
            @RequestParam("password") String password) {

        if (username == null || username.trim().isEmpty()) {
            throw new BusinessException("用户名不能为空");
        }
        if (password == null || password.isEmpty()) {
            throw new BusinessException("密码不能为空");
        }

        // 查询用户 + MD5 密码匹配
        User user = userService.login(username.trim(), Md5Util.md5(password));
        if (user == null) {
            throw new BusinessException("用户名或密码错误");
        }

        // 生成 JWT 令牌（claim 中是用户名）
        String token = JwtUtil.generateToken(user.getUsername());

        Map<String, Object> data = new HashMap<>();
        data.put("token", token);
        data.put("username", user.getUsername());
        data.put("userId", user.getId());

        return Result.success("登录成功", data);
    }
}
