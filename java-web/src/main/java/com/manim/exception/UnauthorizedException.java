package com.manim.exception;

/**
 * 未授权异常 (401)
 * <p>
 * 当 JWT 令牌缺失、无效或过期时抛出，
 * 将被 {@link GlobalExceptionHandler} 捕获后返回 401。
 * </p>
 */
public class UnauthorizedException extends BusinessException {

    public UnauthorizedException(String msg) {
        super(401, msg);
    }

    public UnauthorizedException() {
        this("未登录或令牌已过期，请重新登录");
    }
}
