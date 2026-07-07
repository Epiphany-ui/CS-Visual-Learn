package com.manim.exception;

/**
 * 通用业务异常
 * <p>
 * 当业务逻辑校验失败时抛出，将被 {@link GlobalExceptionHandler} 捕获
 * 并自动封装为 {@link com.manim.pojo.Result} 返回前端。
 * </p>
 */
public class BusinessException extends RuntimeException {

    /** 业务响应码（对应 Result.code） */
    private final int code;

    /**
     * @param code 响应码（200-成功，500-业务失败，其他自定义）
     * @param msg  错误描述
     */
    public BusinessException(int code, String msg) {
        super(msg);
        this.code = code;
    }

    /**
     * 便捷构造：默认 code=500
     */
    public BusinessException(String msg) {
        this(500, msg);
    }

    public int getCode() {
        return code;
    }
}
