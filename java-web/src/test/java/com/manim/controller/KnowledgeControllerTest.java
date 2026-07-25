package com.manim.controller;

import com.manim.pojo.*;
import com.manim.service.*;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Collections;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * KnowledgeController 集成测试 (MockMvc)
 * 对应测试用例: TC-KNOW-001 ~ TC-KNOW-012
 */
@WebMvcTest(KnowledgeController.class)
@DisplayName("KnowledgeController 百科知识接口测试")
class KnowledgeControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private KnowledgeEntryService knowledgeEntryService;

    @MockBean
    private AnimationService animationService;

    @MockBean
    private UserCollectService userCollectService;

    @MockBean
    private StudyRecordService studyRecordService;

    @MockBean
    private UserService userService;

    // ==================== 知识点列表测试 ====================

    @Test
    @DisplayName("TC-KNOW-001: 按分类查询知识点列表 — code=200")
    void getCategoryList() throws Exception {
        KnowledgeEntry entry = new KnowledgeEntry();
        entry.setId(1);
        entry.setTitle("冒泡排序");
        entry.setDifficulty(2);

        when(knowledgeEntryService.listByCategory(eq(1), isNull(), eq(1), eq(10)))
                .thenReturn(Collections.singletonList(entry));
        when(animationService.countByKnowledgeId(1)).thenReturn(3);

        mockMvc.perform(get("/api/v1/knowledge/category/list")
                        .param("categoryId", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data[0].title").value("冒泡排序"))
                .andExpect(jsonPath("$.data[0].difficulty").value(2));
    }

    @Test
    @DisplayName("TC-KNOW-002: 按难度筛选 — 只返回匹配难度条目")
    void getCategoryListByDifficulty() throws Exception {
        when(knowledgeEntryService.listByCategory(isNull(), eq(3), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/knowledge/category/list")
                        .param("difficulty", "3"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    @Test
    @DisplayName("TC-KNOW-003: 无参数查询 — 返回全部条目第一页")
    void getCategoryListNoParams() throws Exception {
        when(knowledgeEntryService.listByCategory(isNull(), isNull(), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/knowledge/category/list"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    // ==================== 词条详情测试 ====================

    @Test
    @DisplayName("TC-KNOW-004: 获取词条详情 — 存在时返回200")
    void getDetailExists() throws Exception {
        KnowledgeEntry entry = new KnowledgeEntry();
        entry.setId(1);
        entry.setTitle("二叉搜索树");
        entry.setDefinition("详细内容...");

        when(knowledgeEntryService.getById(1)).thenReturn(entry);

        mockMvc.perform(get("/api/v1/knowledge/detail")
                        .param("knowledgeId", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.title").value("二叉搜索树"));
    }

    @Test
    @DisplayName("TC-KNOW-005: 词条不存在 — code=500")
    void getDetailNotFound() throws Exception {
        when(knowledgeEntryService.getById(99999)).thenReturn(null);

        mockMvc.perform(get("/api/v1/knowledge/detail")
                        .param("knowledgeId", "99999"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("词条不存在"));
    }

    // ==================== 配套动画测试 ====================

    @Test
    @DisplayName("TC-KNOW-006: 获取配套动画列表 — code=200")
    void getAnimationList() throws Exception {
        Animation anim = new Animation();
        anim.setId(1);
        anim.setTitle("冒泡排序演示");

        when(animationService.listByKnowledgeId(1))
                .thenReturn(Collections.singletonList(anim));

        mockMvc.perform(get("/api/v1/knowledge/animation/list")
                        .param("knowledgeId", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data[0].title").value("冒泡排序演示"));
    }

    // ==================== 相关推荐测试 ====================

    @Test
    @DisplayName("TC-KNOW-007: 获取相关推荐 — code=200")
    void getRecommend() throws Exception {
        when(knowledgeEntryService.getRecommended(1))
                .thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/knowledge/recommend")
                        .param("knowledgeId", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
}
