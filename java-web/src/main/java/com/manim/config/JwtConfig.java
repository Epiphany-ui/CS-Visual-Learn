package com.manim.config;

import com.manim.utils.JwtUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import javax.annotation.PostConstruct;

/**
 * JWT 配置初始化
 * <p>
 * 读取 application.yml 中的 jwt.secret 和 jwt.expiration，
 * 在应用启动时注入到 {@link JwtUtil} 静态工具类。
 * </p>
 */
@Configuration
public class JwtConfig {

    private static final Logger log = LoggerFactory.getLogger(JwtConfig.class);

    @Value("${jwt.secret}")
    private String secret;

    @Value("${jwt.expiration}")
    private long expiration;

    @PostConstruct
    public void init() {
        JwtUtil.init(secret, expiration);
        log.info("JWT 配置已注入 JwtUtil");
    }
}
