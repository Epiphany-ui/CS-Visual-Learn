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
 * TemplateController 集成测试 (MockMvc)
 * 对应测试用例: TC-TPL-001 ~ TC-TPL-016
 */
@WebMvcTest(TemplateController.class)
@DisplayName("TemplateController 模板创作接口测试")
class TemplateControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TemplateService templateService;

    @MockBean
    private TaskService taskService;

    @MockBean
    private WorkService workService;

    @MockBean
    private UserService userService;

    // ==================== 模板列表测试 ====================

    @Test
    @DisplayName("TC-TPL-001: 获取全部模板 — code=200")
    void getTemplateListAll() throws Exception {
        Template tmpl = new Template();
        tmpl.setId(1);
        tmpl.setName("排序算法");

        when(templateService.listByCategory(isNull(), eq(1), eq(10)))
                .thenReturn(Collections.singletonList(tmpl));

        mockMvc.perform(get("/api/v1/template/list"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data[0].name").value("排序算法"));
    }

    @Test
    @DisplayName("TC-TPL-002: 按分类获取模板 — code=200")
    void getTemplateListByCategory() throws Exception {
        when(templateService.listByCategory(eq("数学"), eq(1), eq(10)))
                .thenReturn(Collections.emptyList());

        mockMvc.perform(get("/api/v1/template/list")
                        .param("category", "数学"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }

    // ==================== 模板详情测试 ====================

    @Test
    @DisplayName("TC-TPL-003: 获取模板详情 — 存在时返回200")
    void getTemplateDetailExists() throws Exception {
        Template tmpl = new Template();
        tmpl.setId(1);
        tmpl.setName("排序算法模板");

        when(templateService.getById(1)).thenReturn(tmpl);

        mockMvc.perform(get("/api/v1/template/detail")
                        .param("templateId", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.name").value("排序算法模板"));
    }

    @Test
    @DisplayName("TC-TPL-004: 模板不存在 — code=500")
    void getTemplateDetailNotFound() throws Exception {
        when(templateService.getById(99999)).thenReturn(null);

        mockMvc.perform(get("/api/v1/template/detail")
                        .param("templateId", "99999"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("模板不存在"));
    }

    // ==================== 导出测试 ====================

    @Test
    @DisplayName("TC-TPL-012: 导出MP4 — code=200")
    void exportMp4() throws Exception {
        Work work = new Work();
        work.setId(1);
        work.setVideoPath("/videos/test.mp4");

        when(workService.getById(1)).thenReturn(work);

        mockMvc.perform(get("/api/v1/work/export")
                        .param("workId", "1")
                        .param("exportType", "mp4"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.downloadUrl").value("/videos/test.mp4"));
    }

    @Test
    @DisplayName("TC-TPL-013: 导出代码 — downloadUrl指向代码接口")
    void exportCode() throws Exception {
        Work work = new Work();
        work.setId(1);

        when(workService.getById(1)).thenReturn(work);

        mockMvc.perform(get("/api/v1/work/export")
                        .param("workId", "1")
                        .param("exportType", "code"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.data.downloadUrl").value("/api/v1/work/code/1"));
    }

    @Test
    @DisplayName("TC-TPL-014: 不支持的导出格式 — code=500")
    void exportUnsupportedType() throws Exception {
        Work work = new Work();
        work.setId(1);

        when(workService.getById(1)).thenReturn(work);

        mockMvc.perform(get("/api/v1/work/export")
                        .param("workId", "1")
                        .param("exportType", "pdf"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("不支持的导出类型: pdf"));
    }

    @Test
    @DisplayName("TC-TPL-015: 导出 — 作品不存在")
    void exportWorkNotFound() throws Exception {
        when(workService.getById(99999)).thenReturn(null);

        mockMvc.perform(get("/api/v1/work/export")
                        .param("workId", "99999")
                        .param("exportType", "mp4"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(500))
                .andExpect(jsonPath("$.msg").value("作品不存在"));
    }
}
