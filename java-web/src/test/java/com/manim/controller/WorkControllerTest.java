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
 * WorkController 集成测试 (MockMvc)
 * 对应测试用例: TC-WORK-001 ~ TC-WORK-029
 */
@WebMvcTest(WorkController.class)
@DisplayName("WorkController 作品互动接口测试")
class WorkControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private WorkService workService;

    @MockBean
    private WorkCommentService workCommentService;

    @MockBean
    private UserFollowService userFollowService;

    @MockBean
    private UserService userService;

    // ==================== 作品详情测试 ====================

    @Test
    @DisplayName("TC-WORK-001: 获取公开作品详情 — code=200")
    void getPublicDetail() throws Exception {
        Work work = new Work();
        work.setId(1);
        work.setTitle("测试动画");
        work.setIsPublic(1);
        work.setViewCount(100);

        when(workService.getPublicDetail(1)).thenReturn(work);

        mockMvc.perform(get("/api/v1/work/public/detail")
                        .param("workId", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.title").value("测试动画"));
    }

    @Test
    @DisplayName("TC-WORK-002: 作品不存在 — code=500")
    void getPublicDetailNotFound() throws Exception {
        when(workService.getPublicDetail(99999)).thenReturn(null);

        mockMvc.perform(get("/api/v1/work/public/detail")
                        .param("workId", "99999"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("作品不存在"));
    }

    // ==================== 评论测试 ====================

    @Test
    @DisplayName("TC-WORK-009: 获取评论列表 — code=200")
    void getCommentList() throws Exception {
        WorkComment comment = new WorkComment();
        comment.setId(1);
        comment.setContent("不错!");

        when(workCommentService.listByWorkId(1))
                .thenReturn(Collections.singletonList(comment));

        mockMvc.perform(get("/api/v1/work/comment/list")
                        .param("workId", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data[0].content").value("不错!"));
    }

    @Test
    @DisplayName("TC-WORK-012: 评论内容为空 — code=500")
    void addCommentEmptyContent() throws Exception {
        mockMvc.perform(post("/api/v1/work/comment/add")
                        .param("workId", "1")
                        .param("content", ""))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("评论内容不能为空"));
    }

    // ==================== 创作者主页测试 ====================

    @Test
    @DisplayName("TC-WORK-026: 获取创作者主页 — code=200")
    void getAuthorHome() throws Exception {
        User author = new User();
        author.setId(2);
        author.setNickname("创作者");
        author.setAvatar("/avatar.png");
        author.setIntro("简介");

        when(userService.getById(2)).thenReturn(author);
        when(workService.listByUser(eq(2), eq(1), eq(1), eq(100)))
                .thenReturn(Collections.emptyList());
        when(userFollowService.getFollowerCount(2)).thenReturn(10);

        mockMvc.perform(get("/api/v1/user/author/home")
                        .param("authorId", "2"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.authorInfo.nickname").value("创作者"))
                .andExpect(jsonPath("$.data.workCount").value(0))
                .andExpect(jsonPath("$.data.followerCount").value(10));
    }

    @Test
    @DisplayName("TC-WORK-027: 创作者不存在 — code=500")
    void getAuthorHomeNotFound() throws Exception {
        when(userService.getById(99999)).thenReturn(null);

        mockMvc.perform(get("/api/v1/user/author/home")
                        .param("authorId", "99999"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("创作者不存在"));
    }

    // ==================== 用户查询测试 ====================

    @Test
    @DisplayName("TC-WORK-028: 根据用户名查用户 — code=200")
    void getUserInfoByUsername() throws Exception {
        User user = new User();
        user.setId(1);
        user.setUsername("test1");
        user.setNickname("测试用户");
        user.setAvatar("/avatar.png");
        user.setIntro("个人简介");

        when(userService.findByUsername("test1")).thenReturn(user);

        mockMvc.perform(get("/api/v1/user/info-by-username")
                        .param("username", "test1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.username").value("test1"))
                .andExpect(jsonPath("$.data.nickname").value("测试用户"));
    }

    @Test
    @DisplayName("TC-WORK-029: 用户不存在 — code=500")
    void getUserInfoByUsernameNotFound() throws Exception {
        when(userService.findByUsername("nonexist")).thenReturn(null);

        mockMvc.perform(get("/api/v1/user/info-by-username")
                        .param("username", "nonexist"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("用户不存在"));
    }
}
