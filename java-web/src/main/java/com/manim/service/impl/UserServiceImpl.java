package com.manim.service.impl;

import com.manim.mapper.UserMapper;
import com.manim.pojo.User;
import com.manim.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * 用户业务实现
 */
@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    @Override
    public User findByUsername(String username) {
        return userMapper.selectByUsername(username);
    }

    @Override
    public User login(String username, String encryptedPassword) {
        if (username == null || encryptedPassword == null) {
            return null;
        }
        User user = userMapper.selectByUsername(username.trim());
        if (user == null) {
            return null;
        }
        // 密码比对（存入时已是 MD5，此处直接比对密文）
        if (!encryptedPassword.equals(user.getPassword())) {
            return null;
        }
        return user;
    }

    @Override
    public void register(User user) {
        userMapper.insert(user);
    }
}
