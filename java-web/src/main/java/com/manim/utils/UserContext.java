package com.manim.utils;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 * 当前请求用户上下文（ThreadLocal）
 * <p>
 * 在 Filter 中将 JWT 中解析出的用户名存入此处，
 * Controller / Service 层可直接通过 {@link #getUsername()} 获取当前登录用户，
 * 避免在方法参数中层层传递。
 * </p>
 */
public class UserContext {

    private static final ThreadLocal<String> USERNAME_HOLDER = new ThreadLocal<>();

    /** 管理员用户名列表（与前端保持一致） */
    private static final Set<String> ADMIN_USERNAMES = new HashSet<>(Arrays.asList("admin"));

    /**
     * 设置当前请求的用户名
     */
    public static void setUsername(String username) {
        USERNAME_HOLDER.set(username);
    }

    /**
     * 获取当前请求的用户名
     */
    public static String getUsername() {
        return USERNAME_HOLDER.get();
    }

    /**
     * 当前用户是否为管理员
     */
    public static boolean isAdmin() {
        String username = getUsername();
        return username != null && ADMIN_USERNAMES.contains(username);
    }

    /**
     * 清理当前请求的用户上下文（请求结束时在 Filter 中调用）
     */
    public static void remove() {
        USERNAME_HOLDER.remove();
    }
}
