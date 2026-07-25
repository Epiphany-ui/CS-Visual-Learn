package com.manim.controller;

import com.manim.pojo.*;
import com.manim.service.*;
import com.manim.utils.UserContext;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * AiSandboxController 集成测试 (MockMvc)
 * 对应测试用例: TC-AI-001 ~ TC-AI-016
 */
@WebMvcTest(AiSandboxController.class)
@DisplayName("AiSandboxController AI沙箱接口测试")
class AiSandboxControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AiService aiService;

    @MockBean
    private TaskService taskService;

    @MockBean
    private SandboxDraftService sandboxDraftService;

    @MockBean
    private WorkService workService;

    @MockBean
    private UserService userService;

    @BeforeEach
    void setUp() {
        // @WebMvcTest 不会加载 AuthFilter，手动设置 UserContext 模拟已登录
        UserContext.setUsername("testUser");
    }

    @AfterEach
    void tearDown() {
        UserContext.remove();
    }

    // ==================== AI生成代码测试 ====================

    @Test
    @DisplayName("TC-AI-001: AI生成代码 — 正常生成返回200")
    void generateCodeSuccess() throws Exception {
        Map<String, Object> mockResult = new HashMap<>();
        mockResult.put("code", "from manim import *\n...");
        mockResult.put("explanation", "这段代码...");

        when(aiService.generateCode(eq("画一个旋转的正方形"), isNull()))
                .thenReturn(mockResult);

        mockMvc.perform(post("/api/v1/ai/generate/code")
                        .param("userPrompt", "画一个旋转的正方形"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.code").exists());
    }

    @Test
    @DisplayName("TC-AI-002: userPrompt为空 — code=500")
    void generateCodeEmptyPrompt() throws Exception {
        mockMvc.perform(post("/api/v1/ai/generate/code")
                        .param("userPrompt", ""))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("userPrompt 不能为空"));
    }

    // ==================== AI修复代码测试 ====================

    @Test
    @DisplayName("TC-AI-003: AI修复代码 — 正常修复返回200")
    void fixCodeSuccess() throws Exception {
        Map<String, Object> mockResult = new HashMap<>();
        mockResult.put("fixedCode", "from manim import *\n...");
        mockResult.put("changes", "修复了语法错误");

        when(aiService.fixCode(eq("syntax error"), eq("bad code")))
                .thenReturn(mockResult);

        mockMvc.perform(post("/api/v1/ai/fix/code")
                        .param("errorLog", "syntax error")
                        .param("oldCode", "bad code"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    @Test
    @DisplayName("TC-AI-004: errorLog为空 — code=500")
    void fixCodeEmptyErrorLog() throws Exception {
        mockMvc.perform(post("/api/v1/ai/fix/code")
                        .param("errorLog", "")
                        .param("oldCode", "some code"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("errorLog 不能为空"));
    }

    @Test
    @DisplayName("TC-AI-005: oldCode为空 — code=500")
    void fixCodeEmptyOldCode() throws Exception {
        mockMvc.perform(post("/api/v1/ai/fix/code")
                        .param("errorLog", "some error")
                        .param("oldCode", ""))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("oldCode 不能为空"));
    }

    // ==================== 发布作品测试 ====================

    @Test
    @DisplayName("TC-AI-013: 发布作品 — 完整信息返回200")
    void publishWorkSuccess() throws Exception {
        // 模拟已登录用户
        User mockUser = new User();
        mockUser.setId(1);
        mockUser.setUsername("testUser");

        when(userService.findByUsername(anyString())).thenReturn(mockUser);

        Work savedWork = new Work();
        savedWork.setId(10);

        when(workService.saveWork(any(Work.class))).thenReturn(10);

        mockMvc.perform(post("/api/v1/work/publish")
                        .param("workTitle", "测试作品")
                        .param("workDesc", "描述")
                        .param("tagList", "数学,几何")
                        .param("isPublic", "true")
                        .param("code", "from manim import *")
                        .param("previewUrl", "/preview.mp4"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.publishedWorkId").value(10));
    }

    @Test
    @DisplayName("TC-AI-014: workTitle为空 — code=500")
    void publishWorkEmptyTitle() throws Exception {
        mockMvc.perform(post("/api/v1/work/publish")
                        .param("workTitle", "")
                        .param("isPublic", "true")
                        .param("code", "from manim import *"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("workTitle 不能为空"));
    }

    @Test
    @DisplayName("TC-AI-015: code为空 — code=500")
    void publishWorkEmptyCode() throws Exception {
        mockMvc.perform(post("/api/v1/work/publish")
                        .param("workTitle", "测试")
                        .param("isPublic", "true")
                        .param("code", ""))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("code 不能为空"));
    }
}
