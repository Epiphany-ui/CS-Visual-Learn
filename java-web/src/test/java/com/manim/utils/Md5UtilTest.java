package com.manim.utils;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Md5Util 单元测试
 * 对应测试用例: TC-UTIL-005 ~ TC-UTIL-007
 */
@DisplayName("Md5Util 工具类测试")
class Md5UtilTest {

    @Test
    @DisplayName("TC-UTIL-005: MD5加密 — 返回32位十六进制字符串")
    void md5EncryptReturns32Hex() {
        String result = Md5Util.md5("123456");

        assertNotNull(result);
        assertEquals(32, result.length());
        // 验证全是十六进制字符
        assertTrue(result.matches("[0-9a-f]{32}"));
    }

    @Test
    @DisplayName("TC-UTIL-006: 空字符串加密 — 返回MD5(\"\")固定值")
    void md5EmptyString() {
        String result = Md5Util.md5("");

        assertNotNull(result);
        assertEquals(32, result.length());
        // MD5("") 的已知值
        assertEquals("d41d8cd98f00b204e9800998ecf8427e", result);
    }

    @Test
    @DisplayName("TC-UTIL-007: 相同输入产生相同摘要 — 幂等性")
    void md5SameInputSameOutput() {
        String result1 = Md5Util.md5("123456");
        String result2 = Md5Util.md5("123456");

        assertEquals(result1, result2);
    }

    @Test
    @DisplayName("不同输入产生不同摘要")
    void md5DifferentInputDifferentOutput() {
        String result1 = Md5Util.md5("123456");
        String result2 = Md5Util.md5("654321");

        assertNotEquals(result1, result2);
    }
}
