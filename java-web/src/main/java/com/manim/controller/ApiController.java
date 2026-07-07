package com.manim.controller;

import com.manim.exception.BusinessException;
import com.manim.exception.UnauthorizedException;
import com.manim.pojo.Result;
import com.manim.pojo.Task;
import com.manim.pojo.User;
import com.manim.service.TaskService;
import com.manim.service.UserService;
import com.manim.utils.UserContext;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 动画任务接口
 * <p>
 * 当前登录用户由 {@link com.manim.filter.AuthFilter} 解析 JWT 后写入
 * {@link UserContext}，Controller 直接从中获取。
 * </p>
 */
@Tag(name = "动画任务接口")
@RestController
@RequestMapping("/api")
public class ApiController {

    @Autowired
    private TaskService taskService;

    @Autowired
    private UserService userService;

    /**
     * 从 UserContext 获取当前用户 ID
     */
    private Integer getCurrentUserId() {
        String username = UserContext.getUsername();
        if (username == null) {
            throw new UnauthorizedException("未登录或登录已过期");
        }
        User user = userService.findByUsername(username);
        if (user == null) {
            throw new UnauthorizedException("当前用户不存在");
        }
        return user.getId();
    }

    @Operation(summary = "提交生成任务")
    @PostMapping("/submit")
    public Result<Integer> submit(
            @Parameter(description = "动画需求文本", required = true)
            @RequestParam("userInput") String userInput,
            @Parameter(description = "最大重试次数（默认 3）")
            @RequestParam(value = "maxRetry", required = false, defaultValue = "3") Integer maxRetry) {

        if (userInput == null || userInput.trim().isEmpty()) {
            throw new BusinessException("userInput 不能为空");
        }

        Integer userId = getCurrentUserId();
        Integer taskId = taskService.submitTask(userId, userInput.trim(), maxRetry);
        return Result.success(taskId);
    }

    @Operation(summary = "查询单条任务（Vue 轮询用）")
    @GetMapping("/task/status/{id}")
    public Result<Task> getTaskStatus(
            @Parameter(description = "任务 ID", required = true)
            @PathVariable("id") Integer id) {

        Integer userId = getCurrentUserId();
        Task task = taskService.getTaskById(id);
        if (task == null) {
            throw new BusinessException("任务不存在");
        }
        // 校验任务归属
        if (!task.getUserId().equals(userId)) {
            throw new BusinessException("无权访问该任务");
        }
        return Result.success(task);
    }

    @Operation(summary = "查询当前用户全部历史任务")
    @GetMapping("/task/list")
    public Result<List<Task>> listTasks() {
        Integer userId = getCurrentUserId();
        List<Task> taskList = taskService.listTasksByUserId(userId);
        return Result.success(taskList);
    }
}
