package com.manim.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.manim.mapper.TaskMapper;
import com.manim.pojo.Task;
import com.manim.service.TaskService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 任务业务实现
 */
@Service
public class TaskServiceImpl implements TaskService {

    private static final Logger log = LoggerFactory.getLogger(TaskServiceImpl.class);

    @Autowired
    private TaskMapper taskMapper;

    @Autowired
    private RenderTaskService renderTaskService;

    @Override
    public Integer submitTask(Integer userId, String userInput, Integer maxRetry) {
        /*
         * 1. 创建任务记录，status=0（处理中）
         * 2. 异步调用 Python AI 服务渲染视频（通过 RenderTaskService 代理，确保 @Async 生效）
         * 3. 立即返回任务 ID，不阻塞当前请求
         */
        Task task = new Task();
        task.setUserId(userId);
        task.setUserInput(userInput);
        task.setStatus(0);
        taskMapper.insert(task);

        Integer taskId = task.getId();
        renderTaskService.asyncRender(taskId, userInput, maxRetry != null ? maxRetry : 3);

        return taskId;
    }

    @Override
    public Task getTaskById(Integer id) {
        return taskMapper.selectById(id);
    }

    @Override
    public List<Task> listTasksByUserId(Integer userId) {
        QueryWrapper<Task> qw = new QueryWrapper<>();
        qw.eq("user_id", userId)
           .orderByDesc("create_time");
        return taskMapper.selectList(qw);
    }
}
