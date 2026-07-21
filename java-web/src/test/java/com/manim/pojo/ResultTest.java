package com.manim.pojo;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Result 统一响应封装 单元测试
 * 对应测试用例: TC-RES-001 ~ TC-RES-005
 */
@DisplayName("Result 统一响应测试")
class ResultTest {

    @Test
    @DisplayName("TC-RES-001: success() 无数据 — code=200, msg=操作成功, data=null")
    void successWithoutData() {
        Result<Void> result = Result.success();

        assertEquals(200, result.getCode());
        assertEquals("操作成功", result.getMsg());
        assertNull(result.getData());
    }

    @Test
    @DisplayName("TC-RES-002: success(T data) — code=200, data为传入对象")
    void successWithData() {
        Result<String> result = Result.success("hello");

        assertEquals(200, result.getCode());
        assertEquals("操作成功", result.getMsg());
        assertEquals("hello", result.getData());
    }

    @Test
    @DisplayName("TC-RES-003: success(msg, data) — 自定义消息和数据")
    void successWithCustomMsgAndData() {
        Map<String, Object> map = new HashMap<>();
        map.put("key", "value");
        Result<Map<String, Object>> result = Result.success("自定义成功", map);

        assertEquals(200, result.getCode());
        assertEquals("自定义成功", result.getMsg());
        assertSame(map, result.getData());
    }

    @Test
    @DisplayName("TC-RES-004: fail(msg) — code=500, data=null")
    void failWithMsg() {
        Result<Void> result = Result.fail("业务错误");

        assertEquals(500, result.getCode());
        assertEquals("业务错误", result.getMsg());
        assertNull(result.getData());
    }

    @Test
    @DisplayName("TC-RES-005: fail(code, msg) — 自定义code和msg")
    void failWithCustomCodeAndMsg() {
        Result<Void> result = Result.fail(400, "参数错误");

        assertEquals(400, result.getCode());
        assertEquals("参数错误", result.getMsg());
        assertNull(result.getData());
    }
}
