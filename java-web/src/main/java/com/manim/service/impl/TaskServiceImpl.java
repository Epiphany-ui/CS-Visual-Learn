package com.manim.service.impl;

import cn.hutool.http.HttpRequest;
import cn.hutool.http.HttpResponse;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.manim.dto.PythonResponse;
import com.manim.mapper.TaskMapper;
import com.manim.pojo.Task;
import com.manim.service.TaskService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 任务业务实现
 */
@Service
public class TaskServiceImpl implements TaskService {

    private static final Logger log = LoggerFactory.getLogger(TaskServiceImpl.class);

    @Autowired
    private TaskMapper taskMapper;

    @Value("${manim.ai.base-url}")
    private String aiBaseUrl;

    @Value("${manim.ai.generate-endpoint}")
    private String generateEndpoint;

    @Value("${manim.ai.read-timeout}")
    private int readTimeout;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Integer submitTask(Integer userId, String userInput, Integer maxRetry) {
        // 创建任务记录，status=0（处理中）
        Task task = new Task();
        task.setUserId(userId);
        task.setUserInput(userInput);
        task.setStatus(0);
        taskMapper.insert(task);

        // 异步调用 Python 服务渲染
        Integer taskId = task.getId();
        asyncRender(taskId, userInput, maxRetry != null ? maxRetry : 3);

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

    // ==================== 异步调用 Python 服务 ====================

    @Async
    public void asyncRender(Integer taskId, String userInput, Integer maxRetry) {
        try {
            JSONObject requestBody = JSONUtil.createObj()
                    .set("user_input", userInput)
                    .set("max_retry", maxRetry);

            String url = aiBaseUrl + generateEndpoint;
            log.info("调用 Python AI 服务: POST {}, 请求体: {}", url, requestBody);

            HttpResponse response = HttpRequest.post(url)
                    .header("Content-Type", "application/json")
                    .body(requestBody.toString())
                    .timeout(readTimeout)
                    .execute();

            int httpStatus = response.getStatus();
            String responseBody = response.body();
            log.info("Python 服务响应状态码: {}, 响应体: {}", httpStatus, responseBody);

            if (httpStatus != 200) {
                markTaskFailed(taskId, "Python 服务返回异常状态码: " + httpStatus);
                return;
            }

            PythonResponse pythonResp = JSONUtil.toBean(responseBody, PythonResponse.class);
            updateTaskFromPythonResponse(taskId, pythonResp);

        } catch (Exception e) {
            log.error("调用 Python AI 服务异常", e);
            markTaskFailed(taskId, "调用 AI 服务网络异常: " + e.getMessage());
        }
    }

    private void updateTaskFromPythonResponse(Integer taskId, PythonResponse resp) {
        Task task = taskMapper.selectById(taskId);
        if (task == null) return;

        task.setErrorLog(resp.getLog());

        if (resp.isSuccess()) {
            task.setStatus(1);               // 成功
            task.setVideoPath(resp.getVideoPath());
        } else {
            task.setStatus(2);               // 失败
        }
        taskMapper.updateById(task);
    }

    private void markTaskFailed(Integer taskId, String errorMsg) {
        Task task = taskMapper.selectById(taskId);
        if (task == null) return;
        task.setStatus(2);                   // 失败
        task.setErrorLog(errorMsg);
        taskMapper.updateById(task);
    }
}
