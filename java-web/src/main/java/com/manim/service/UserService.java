package com.manim.service;

import com.manim.pojo.User;

/**
 * 用户业务接口
 */
public interface UserService {

    /**
     * 根据用户名查询用户
     */
    User findByUsername(String username);

    /**
     * 用户登录校验
     *
     * @param username 用户名
     * @param password 密码（已加密）
     * @return 登录成功返回用户对象，失败返回 null
     */
    User login(String username, String password);

    /**
     * 用户注册
     *
     * @param user 用户对象（含 username + 已加密的 password）
     */
    void register(User user);
}
