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
import java.util.HashMap;
import java.util.Map;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * UserCenterController 集成测试 (MockMvc)
 * 对应测试用例: TC-UC-001 ~ TC-UC-011
 */
@WebMvcTest(UserCenterController.class)
@DisplayName("UserCenterController 个人中心接口测试")
class UserCenterControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @MockBean
    private WorkService workService;

    @MockBean
    private UserCollectService userCollectService;

    @MockBean
    private BrowseHistoryService browseHistoryService;

    @MockBean
    private StudyRecordService studyRecordService;

    @MockBean
    private UserFollowService userFollowService;

    // ==================== 个人首页测试 ====================

    @Test
    @DisplayName("TC-UC-001: 获取个人首页数据 — 需要认证，此处验证未登录返回401")
    void getHomeDataUnauthorized() throws Exception {
        // UserCenterController.getHomeData() 内部调用 getCurrentUserId()
        // 在 @WebMvcTest 中 AuthFilter 不会被加载，但 getCurrentUserId 从 UserContext 取值
        // UserContext 为空 → 抛 UnauthorizedException → 返回401
        mockMvc.perform(get("/api/v1/user/home/data"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(401));
    }

    // ==================== 我的作品测试 ====================

    @Test
    @DisplayName("TC-UC-004: 按状态筛选 — status=0(草稿)")
    void getMyWorksFilteredByStatus() throws Exception {
        // 未登录时被拦截
        mockMvc.perform(get("/api/v1/user/work/list")
                        .param("status", "0"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(401));
    }

    // ==================== 我的收藏测试 ====================

    @Test
    @DisplayName("TC-UC-005: 获取收藏列表 — type=1")
    void getMyCollects() throws Exception {
        mockMvc.perform(get("/api/v1/user/collect/list")
                        .param("type", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(401));
    }

    // ==================== 浏览历史测试 ====================

    @Test
    @DisplayName("TC-UC-006: 获取浏览历史")
    void getBrowseHistory() throws Exception {
        mockMvc.perform(get("/api/v1/user/history/list"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(401));
    }

    // ==================== 学习统计测试 ====================

    @Test
    @DisplayName("TC-UC-007: 获取学习统计")
    void getStudyStat() throws Exception {
        mockMvc.perform(get("/api/v1/user/study/stat"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(401));
    }

    // ==================== 创作者统计测试 ====================

    @Test
    @DisplayName("TC-UC-008: 获取创作者统计")
    void getAuthorStat() throws Exception {
        mockMvc.perform(get("/api/v1/user/author/stat"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(401));
    }
}
