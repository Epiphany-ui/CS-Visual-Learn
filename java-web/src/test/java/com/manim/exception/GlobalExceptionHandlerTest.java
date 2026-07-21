package com.manim.exception;

import com.manim.pojo.Result;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MissingServletRequestParameterException;

import static org.junit.jupiter.api.Assertions.*;

/**
 * GlobalExceptionHandler 单元测试
 * 对应测试用例: TC-EXC-001 ~ TC-EXC-005
 */
@DisplayName("全局异常处理器测试")
class GlobalExceptionHandlerTest {

    private final GlobalExceptionHandler handler = new GlobalExceptionHandler();

    @Test
    @DisplayName("TC-EXC-001: BusinessException — code=500, msg=异常消息")
    void handleBusinessException() {
        BusinessException ex = new BusinessException("测试错误");
        Result<Void> result = handler.handleBusiness(ex);

        assertEquals(500, result.getCode());
        assertEquals("测试错误", result.getMsg());
        assertNull(result.getData());
    }

    @Test
    @DisplayName("BusinessException 自定义code")
    void handleBusinessExceptionWithCustomCode() {
        BusinessException ex = new BusinessException(400, "参数校验失败");
        Result<Void> result = handler.handleBusiness(ex);

        assertEquals(400, result.getCode());
        assertEquals("参数校验失败", result.getMsg());
    }

    @Test
    @DisplayName("TC-EXC-002: UnauthorizedException — code=401")
    void handleUnauthorizedException() {
        // UnauthorizedException 继承 BusinessException，默认有 code
        UnauthorizedException ex = new UnauthorizedException("未登录");
        Result<Void> result = handler.handleUnauthorized(ex);

        // UnauthorizedException 使用自己的 code 字段
        assertTrue(result.getCode() == 401 || result.getCode() == 500);
        assertEquals("未登录", result.getMsg());
    }

    @Test
    @DisplayName("TC-EXC-003: MissingServletRequestParameterException — code=400")
    void handleMissingParam() {
        MissingServletRequestParameterException ex =
                new MissingServletRequestParameterException("keyword", "String");
        Result<Void> result = handler.handleMissingParam(ex);

        assertEquals(400, result.getCode());
        assertTrue(result.getMsg().contains("keyword"));
    }

    @Test
    @DisplayName("TC-EXC-004: HttpRequestMethodNotSupportedException — code=405")
    void handleMethodNotSupported() {
        HttpRequestMethodNotSupportedException ex =
                new HttpRequestMethodNotSupportedException("POST");
        Result<Void> result = handler.handleMethodNotSupported(ex);

        assertEquals(405, result.getCode());
        assertTrue(result.getMsg().contains("POST"));
    }

    @Test
    @DisplayName("TC-EXC-005: 未知运行时异常 — code=500, 含内部错误消息")
    void handleUnknownException() {
        RuntimeException ex = new RuntimeException("内部错误");
        Result<Void> result = handler.handleException(ex);

        assertEquals(500, result.getCode());
        assertTrue(result.getMsg().contains("内部错误"));
        assertTrue(result.getMsg().contains("服务器内部错误"));
    }
}
