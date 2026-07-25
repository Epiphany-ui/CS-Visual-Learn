package com.manim.controller;

import com.manim.service.SearchService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.HashMap;
import java.util.Map;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * SearchController 集成测试 (MockMvc)
 * 对应测试用例: TC-SRCH-001 ~ TC-SRCH-004
 */
@WebMvcTest(SearchController.class)
@DisplayName("SearchController 全局搜索接口测试")
class SearchControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SearchService searchService;

    @Test
    @DisplayName("TC-SRCH-001: 关键字搜索 — code=200, 返回四类结果")
    void searchAllWithKeyword() throws Exception {
        Map<String, Object> mockResult = new HashMap<>();
        mockResult.put("knowledge", java.util.Collections.emptyList());
        mockResult.put("works", java.util.Collections.emptyList());
        mockResult.put("templates", java.util.Collections.emptyList());
        mockResult.put("users", java.util.Collections.emptyList());

        when(searchService.searchAll(eq("排序"), eq(1), eq(10))).thenReturn(mockResult);

        mockMvc.perform(get("/api/v1/search/all")
                        .param("keyword", "排序")
                        .param("page", "1")
                        .param("size", "10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.knowledge").exists())
                .andExpect(jsonPath("$.data.works").exists())
                .andExpect(jsonPath("$.data.templates").exists())
                .andExpect(jsonPath("$.data.users").exists());
    }

    @Test
    @DisplayName("TC-SRCH-002: 缺少keyword参数 — code=400")
    void searchAllMissingKeyword() throws Exception {
        mockMvc.perform(get("/api/v1/search/all"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(400))
                .andExpect(jsonPath("$.msg").value("缺少必填参数: keyword"));
    }

    @Test
    @DisplayName("TC-SRCH-003: 无匹配结果 — 返回空列表")
    void searchAllNoResults() throws Exception {
        Map<String, Object> emptyResult = new HashMap<>();
        emptyResult.put("knowledge", java.util.Collections.emptyList());
        emptyResult.put("works", java.util.Collections.emptyList());
        emptyResult.put("templates", java.util.Collections.emptyList());
        emptyResult.put("users", java.util.Collections.emptyList());

        when(searchService.searchAll(eq("不存在的内容xyz"), anyInt(), anyInt()))
                .thenReturn(emptyResult);

        mockMvc.perform(get("/api/v1/search/all")
                        .param("keyword", "不存在的内容xyz"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    @Test
    @DisplayName("TC-SRCH-004: 分页边界 — page=999 返回空")
    void searchAllLargePage() throws Exception {
        Map<String, Object> emptyResult = new HashMap<>();
        emptyResult.put("knowledge", java.util.Collections.emptyList());
        emptyResult.put("works", java.util.Collections.emptyList());
        emptyResult.put("templates", java.util.Collections.emptyList());
        emptyResult.put("users", java.util.Collections.emptyList());

        when(searchService.searchAll(eq("test"), eq(999), eq(10))).thenReturn(emptyResult);

        mockMvc.perform(get("/api/v1/search/all")
                        .param("keyword", "test")
                        .param("page", "999"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
}
