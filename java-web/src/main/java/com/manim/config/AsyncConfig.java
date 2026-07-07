package com.manim.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

/**
 * 异步任务线程池配置
 * <p>
 * 为 {@link org.springframework.scheduling.annotation.Async @Async} 注解
 * 提供专用的线程池，避免异步任务占用 Tomcat 请求线程。
 * </p>
 */
@Configuration
public class AsyncConfig implements AsyncConfigurer {

    /**
     * 获取异步任务执行器
     * <ul>
     *   <li>corePoolSize = 2：核心常驻线程</li>
     *   <li>maxPoolSize = 5：最大线程数</li>
     *   <li>queueCapacity = 20：等待队列容量</li>
     *   <li>threadNamePrefix = manim-async-：线程名前缀，便于日志追踪</li>
     *   <li>awaitTerminationSeconds = 30：关闭时等待任务完成</li>
     * </ul>
     */
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(5);
        executor.setQueueCapacity(20);
        executor.setThreadNamePrefix("manim-async-");
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(30);
        executor.initialize();
        return executor;
    }
}
