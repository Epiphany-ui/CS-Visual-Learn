package com.manim.config;

import com.manim.filter.AuthFilter;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 过滤器注册配置
 * <p>
 * 将 {@link AuthFilter} 注册到 /api/* 路径，
 * 白名单内的 /api/register 和 /api/login 不受 token 校验。
 * </p>
 */
@Configuration
public class FilterConfig {

    @Bean
    public FilterRegistrationBean<AuthFilter> authFilterRegistration() {
        FilterRegistrationBean<AuthFilter> registration = new FilterRegistrationBean<>();
        registration.setFilter(new AuthFilter());
        registration.addUrlPatterns("/api/*");
        registration.setOrder(1);
        registration.setName("authFilter");
        return registration;
    }
}
