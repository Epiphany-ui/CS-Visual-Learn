package com.manim.controller;

import com.manim.dto.WorkListDTO;
import com.manim.pojo.User;
import com.manim.pojo.Work;
import com.manim.service.UserService;
import com.manim.service.WorkService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Collections;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * GalleryController 集成测试 (MockMvc)
 * 对应测试用例: TC-GAL-001 ~ TC-GAL-005
 */
@WebMvcTest(GalleryController.class)
@DisplayName("GalleryController 社区画廊接口测试")
class GalleryControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private WorkService workService;

    @MockBean
    private UserService userService;

    @Test
    @DisplayName("TC-GAL-001: 默认排行榜(weekly) — code=200")
    void getGalleryDefaultRank() throws Exception {
        when(workService.listGallery(eq("weekly"), isNull(), isNull(), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/gallery/list"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.list").isArray())
                .andExpect(jsonPath("$.data.total").value(0));
    }

    @Test
    @DisplayName("TC-GAL-002: 按时间排序(sort=time) — code=200")
    void getGallerySortByTime() throws Exception {
        when(workService.listGallery(anyString(), eq("time"), isNull(), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/gallery/list")
                        .param("sort", "time"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    @Test
    @DisplayName("TC-GAL-003: 按点赞排序(sort=likes) — code=200")
    void getGallerySortByLikes() throws Exception {
        when(workService.listGallery(anyString(), eq("likes"), isNull(), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/gallery/list")
                        .param("sort", "likes"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    @Test
    @DisplayName("TC-GAL-004: 按分类筛选(category=几何) — 只返回匹配标签作品")
    void getGalleryFilterByCategory() throws Exception {
        when(workService.listGallery(anyString(), isNull(), eq("几何"), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/gallery/list")
                        .param("category", "几何"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    @Test
    @DisplayName("TC-GAL-005: 分页 — page=2, size=5")
    void getGalleryPagination() throws Exception {
        when(workService.listGallery(anyString(), isNull(), isNull(), eq(2), eq(5)))
                .thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/gallery/list")
                        .param("page", "2")
                        .param("size", "5"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    @Test
    @DisplayName("画廊列表包含完整作品信息(Fork来源)")
    void getGalleryWithForkInfo() throws Exception {
        Work work = new Work();
        work.setId(1);
        work.setUserId(1);
        work.setTitle("测试作品");
        work.setLikeCount(10);
        work.setViewCount(100);
        work.setSourceWorkId(null);

        User author = new User();
        author.setId(1);
        author.setNickname("作者");
        author.setAvatar(null);

        when(workService.listGallery(anyString(), isNull(), isNull(), eq(1), eq(10)))
                .thenReturn(Collections.singletonList(work));
        when(userService.getById(1)).thenReturn(author);

        mockMvc.perform(get("/api/v1/gallery/list"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.list[0].title").value("测试作品"))
                .andExpect(jsonPath("$.data.list[0].authorName").value("作者"));
    }
}
