package com.manim.service;

import com.manim.pojo.Task;

import java.util.List;

/**
 * 任务业务接口
 */
public interface TaskService {

    /**
     * 提交新任务（入库后异步生成）
     *
     * @param userId    所属用户ID
     * @param userInput 用户需求文本
     * @param maxRetry  最大重试次数（默认 3，传给 Python 服务）
     * @return 新任务 ID
     */
    Integer submitTask(Integer userId, String userInput, Integer maxRetry);

    /**
     * 根据 ID 查询任务
     */
    Task getTaskById(Integer id);

    /**
     * 查询指定用户的全部历史任务（按创建时间倒序）
     */
    List<Task> listTasksByUserId(Integer userId);
}
