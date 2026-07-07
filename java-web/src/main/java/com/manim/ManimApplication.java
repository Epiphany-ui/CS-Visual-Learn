package com.manim;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Manim 动画自动生成系统 — 应用启动入口
 * <p>
 * 功能：
 * <ul>
 *   <li>提供 REST API 供 Vue 前端调用</li>
 *   <li>异步调用 Python AI 服务生成 Manim 动画视频</li>
 *   <li>JWT 认证 + ThreadLocal 用户上下文</li>
 *   <li>全局异常统一处理</li>
 * </ul>
 * </p>
 */
@SpringBootApplication
@EnableAsync
public class ManimApplication {

    public static void main(String[] args) {
        SpringApplication.run(ManimApplication.class, args);
    }
}
