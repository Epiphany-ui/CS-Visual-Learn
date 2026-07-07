package com.manim.utils;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.MalformedJwtException;
import io.jsonwebtoken.UnsupportedJwtException;
import io.jsonwebtoken.security.Keys;
import io.jsonwebtoken.security.SecurityException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * JWT 令牌工具类（纯静态）
 * <p>
 * 提供令牌的生成、解析与校验功能。
 * 密钥和过期时间由 {@link com.manim.config.JwtConfig} 在应用启动时注入。
 * </p>
 */
public class JwtUtil {

    private static final Logger log = LoggerFactory.getLogger(JwtUtil.class);

    /** HMAC-SHA 密钥 */
    private static SecretKey secretKey;

    /** 令牌过期时间（毫秒） */
    private static long expiration;

    /**
     * 初始化（由 JwtConfig 在应用启动时调用一次）
     */
    public static void init(String secret, long expirationMillis) {
        secretKey = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        expiration = expirationMillis;
        log.info("JwtUtil 初始化完成，过期时间: {}ms", expiration);
    }

    /**
     * 生成 JWT 令牌
     *
     * @param username 用户名（存在 subject 中）
     * @return JWT 字符串
     */
    public static String generateToken(String username) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + expiration);

        return Jwts.builder()
                .subject(username)
                .issuedAt(now)
                .expiration(expiryDate)
                .signWith(secretKey)
                .compact();
    }

    /**
     * 解析并校验令牌，返回 Claims
     *
     * @param token JWT 字符串
     * @return Claims；无效/过期返回 null
     */
    public static Claims parseToken(String token) {
        if (token == null || token.trim().isEmpty()) {
            return null;
        }
        try {
            return Jwts.parser()
                    .verifyWith(secretKey)
                    .build()
                    .parseSignedClaims(token.trim())
                    .getPayload();
        } catch (ExpiredJwtException e) {
            log.warn("JWT 已过期: {}", e.getMessage());
        } catch (SecurityException | MalformedJwtException e) {
            log.warn("JWT 签名校验失败: {}", e.getMessage());
        } catch (UnsupportedJwtException e) {
            log.warn("不支持的 JWT 格式: {}", e.getMessage());
        } catch (IllegalArgumentException e) {
            log.warn("JWT 参数异常: {}", e.getMessage());
        }
        return null;
    }

    /**
     * 校验令牌是否有效
     */
    public static boolean validateToken(String token) {
        return parseToken(token) != null;
    }

    /**
     * 从令牌中获取用户名
     *
     * @param token JWT 字符串
     * @return 用户名；无效返回 null
     */
    public static String getUsernameFromToken(String token) {
        Claims claims = parseToken(token);
        return claims != null ? claims.getSubject() : null;
    }
}
