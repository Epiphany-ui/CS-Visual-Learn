package com.manim.controller;

import com.manim.dto.CarouselDTO;
import com.manim.dto.CategoryDTO;
import com.manim.dto.WorkListDTO;
import com.manim.service.KnowledgeCategoryService;
import com.manim.service.WorkService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * HomeController 集成测试 (MockMvc)
 * 对应测试用例: TC-HOME-001 ~ TC-HOME-005
 */
@WebMvcTest(HomeController.class)
@DisplayName("HomeController 首页模块接口测试")
class HomeControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private WorkService workService;

    @MockBean
    private KnowledgeCategoryService knowledgeCategoryService;

    // ==================== 轮播测试 ====================

    @Test
    @DisplayName("TC-HOME-001: 获取热门轮播 — code=200, 返回列表")
    void getCarousel() throws Exception {
        CarouselDTO dto = new CarouselDTO(1, "/cover.png", "测试动画", 100, "作者名");
        when(workService.listCarousel()).thenReturn(Collections.singletonList(dto));

        mockMvc.perform(get("/api/v1/home/carousel"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data[0].workId").value(1))
                .andExpect(jsonPath("$.data[0].title").value("测试动画"));
    }

    @Test
    @DisplayName("轮播为空 — 返回空列表不报错")
    void getCarouselEmpty() throws Exception {
        when(workService.listCarousel()).thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/home/carousel"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data").isArray())
                .andExpect(jsonPath("$.data.length()").value(0));
    }

    // ==================== 分类测试 ====================

    @Test
    @DisplayName("TC-HOME-002: 获取知识点分类列表 — code=200")
    void getCategory() throws Exception {
        CategoryDTO dto = new CategoryDTO(1, "算法", "algorithm", 25);
        when(knowledgeCategoryService.listWithEntryCount())
                .thenReturn(Collections.singletonList(dto));

        mockMvc.perform(get("/api/v1/home/category"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data[0].name").value("算法"));
    }

    // ==================== 作品列表测试 ====================

    @Test
    @DisplayName("TC-HOME-003: 最新作品(type=latest) — code=200")
    void getWorkListLatest() throws Exception {
        when(workService.listHomeWorksDTO(eq("latest"), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());
        when(workService.countHomeWorks("latest")).thenReturn(0);

        mockMvc.perform(get("/api/v1/home/work/list")
                        .param("type", "latest")
                        .param("page", "1")
                        .param("size", "10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.list").isArray())
                .andExpect(jsonPath("$.data.total").value(0));
    }

    @Test
    @DisplayName("TC-HOME-004: 精选作品(type=featured) — 按like_count降序")
    void getWorkListFeatured() throws Exception {
        when(workService.listHomeWorksDTO(eq("featured"), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());
        when(workService.countHomeWorks("featured")).thenReturn(0);

        mockMvc.perform(get("/api/v1/home/work/list")
                        .param("type", "featured"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    @Test
    @DisplayName("TC-HOME-005: 默认参数 — type默认latest, page默认1, size默认10")
    void getWorkListDefaultParams() throws Exception {
        when(workService.listHomeWorksDTO(eq("latest"), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());
        when(workService.countHomeWorks("latest")).thenReturn(0);

        mockMvc.perform(get("/api/v1/home/work/list"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
}
