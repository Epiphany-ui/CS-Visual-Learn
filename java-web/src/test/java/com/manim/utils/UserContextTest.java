package com.manim.utils;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * UserContext ThreadLocal 单元测试
 * 对应测试用例: TC-UTIL-008 ~ TC-UTIL-009
 */
@DisplayName("UserContext 工具类测试")
class UserContextTest {

    @AfterEach
    void tearDown() {
        // 每个测试结束后清理 ThreadLocal，防止污染其他测试
        UserContext.remove();
    }

    @Test
    @DisplayName("TC-UTIL-008: setUsername → getUsername → remove → getUsername 生命周期")
    void setGetRemoveLifecycle() {
        // 初始状态应该是 null
        assertNull(UserContext.getUsername());

        // 设置用户名
        UserContext.setUsername("testUser");
        assertEquals("testUser", UserContext.getUsername());

        // 更新用户名
        UserContext.setUsername("anotherUser");
        assertEquals("anotherUser", UserContext.getUsername());

        // remove 后为 null
        UserContext.remove();
        assertNull(UserContext.getUsername());
    }

    @Test
    @DisplayName("TC-UTIL-009: 多线程隔离 — 各自ThreadLocal不受影响")
    void threadIsolation() throws InterruptedException {
        UserContext.setUsername("mainThread");

        final String[] threadResult = new String[1];

        Thread thread = new Thread(() -> {
            // 子线程初始应为 null
            threadResult[0] = UserContext.getUsername();

            // 子线程设置自己的值
            UserContext.setUsername("childThread");
            assertEquals("childThread", UserContext.getUsername());

            UserContext.remove();
        });

        thread.start();
        thread.join();

        // 子线程读到的初始值为 null（隔离）
        assertNull(threadResult[0]);

        // 主线程的值不受子线程影响
        assertEquals("mainThread", UserContext.getUsername());
    }

    @Test
    @DisplayName("remove 未设置过值的 ThreadLocal 不应抛异常")
    void removeWithoutSetShouldNotThrow() {
        assertDoesNotThrow(UserContext::remove);
    }
}
