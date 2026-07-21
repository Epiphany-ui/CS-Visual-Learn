package com.manim.service.impl;

import com.manim.exception.BusinessException;
import com.manim.mapper.*;
import com.manim.pojo.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * WorkServiceImpl 单元测试
 * 对应测试用例: TC-WORK-003 ~ TC-WORK-025 (Service 层)
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("WorkService 业务逻辑测试")
class WorkServiceImplTest {

    @Mock
    private WorkMapper workMapper;

    @Mock
    private WorkLikeMapper workLikeMapper;

    @Mock
    private UserCollectMapper userCollectMapper;

    @Mock
    private SandboxDraftMapper sandboxDraftMapper;

    @Mock
    private UserMapper userMapper;

    @InjectMocks
    private WorkServiceImpl workService;

    private Work testWork;

    @BeforeEach
    void setUp() {
        testWork = new Work();
        testWork.setId(1);
        testWork.setUserId(1);
        testWork.setTitle("测试作品");
        testWork.setDescription("测试描述");
        testWork.setManimCode("from manim import *");
        testWork.setIsPublic(1);
        testWork.setLikeCount(5);
        testWork.setViewCount(100);
        testWork.setCollectCount(3);
        testWork.setForkCount(2);
        testWork.setStatus(1);
    }

    // ==================== 查询测试 ====================

    @Test
    @DisplayName("TC-WORK-001: getPublicDetail — 公开作品返回详情，viewCount+1")
    void getPublicDetailSuccess() {
        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workMapper.updateById(any(Work.class))).thenReturn(1);

        Work result = workService.getPublicDetail(1);

        assertNotNull(result);
        assertEquals(101, result.getViewCount()); // viewCount+1
        verify(workMapper).updateById(testWork);
    }

    @Test
    @DisplayName("getPublicDetail: 作品不存在 — 返回 null")
    void getPublicDetailNotFound() {
        when(workMapper.selectById(999)).thenReturn(null);

        Work result = workService.getPublicDetail(999);

        assertNull(result);
    }

    // ==================== 点赞测试 ====================

    @Test
    @DisplayName("TC-WORK-003: toggleLike 点赞 — likeCount+1")
    void toggleLikeAdd() {
        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workLikeMapper.selectOne(any())).thenReturn(null); // 未曾点赞
        when(workLikeMapper.insert(any(WorkLike.class))).thenReturn(1);
        when(workMapper.updateById(any(Work.class))).thenReturn(1);

        boolean result = workService.toggleLike(1, 2, true);

        assertTrue(result);
        assertEquals(6, testWork.getLikeCount()); // 5 + 1
        verify(workLikeMapper).insert(any(WorkLike.class));
    }

    @Test
    @DisplayName("TC-WORK-004: toggleLike 取消点赞 — likeCount-1")
    void toggleLikeRemove() {
        testWork.setLikeCount(5);
        WorkLike existingLike = new WorkLike();
        existingLike.setId(1);
        existingLike.setWorkId(1);
        existingLike.setUserId(2);

        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workLikeMapper.selectOne(any())).thenReturn(existingLike);
        when(workLikeMapper.deleteById(1)).thenReturn(1);
        when(workMapper.updateById(any(Work.class))).thenReturn(1);

        boolean result = workService.toggleLike(1, 2, false);

        assertTrue(result);
        assertEquals(4, testWork.getLikeCount());
        verify(workLikeMapper).deleteById(1);
    }

    @Test
    @DisplayName("TC-WORK-005: toggleLike 重复点赞 — likeCount 不重复增加")
    void toggleLikeDuplicateAdd() {
        WorkLike existingLike = new WorkLike();
        existingLike.setId(1);

        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workLikeMapper.selectOne(any())).thenReturn(existingLike);
        // 已点赞，再次点赞不应 insert 或 update count

        workService.toggleLike(1, 2, true);

        // likeCount 不变
        assertEquals(5, testWork.getLikeCount());
        verify(workLikeMapper, never()).insert(any(WorkLike.class));
    }

    @Test
    @DisplayName("toggleLike: 作品不存在 — 返回 false")
    void toggleLikeWorkNotFound() {
        when(workMapper.selectById(999)).thenReturn(null);

        boolean result = workService.toggleLike(999, 1, true);

        assertFalse(result);
    }

    // ==================== 收藏测试 ====================

    @Test
    @DisplayName("TC-WORK-007: toggleCollect 收藏 — collectCount+1")
    void toggleCollectAdd() {
        when(workMapper.selectById(1)).thenReturn(testWork);
        when(userCollectMapper.selectOne(any())).thenReturn(null);
        when(userCollectMapper.insert(any(UserCollect.class))).thenReturn(1);
        when(workMapper.updateById(any(Work.class))).thenReturn(1);

        boolean result = workService.toggleCollect(1, 2, true);

        assertTrue(result);
        assertEquals(4, testWork.getCollectCount()); // 3 + 1
    }

    @Test
    @DisplayName("TC-WORK-008: toggleCollect 取消收藏 — collectCount-1")
    void toggleCollectRemove() {
        UserCollect existing = new UserCollect();
        existing.setId(1);
        existing.setUserId(2);
        existing.setTargetType(2);
        existing.setTargetId(1);

        when(workMapper.selectById(1)).thenReturn(testWork);
        when(userCollectMapper.selectOne(any())).thenReturn(existing);
        when(userCollectMapper.deleteById(1)).thenReturn(1);
        when(workMapper.updateById(any(Work.class))).thenReturn(1);

        boolean result = workService.toggleCollect(1, 2, false);

        assertTrue(result);
        assertEquals(2, testWork.getCollectCount());
    }

    // ==================== Fork 测试 ====================

    @Test
    @DisplayName("TC-WORK-013: forkWork — 创建Fork副本")
    void forkWorkSuccess() {
        User sourceAuthor = new User();
        sourceAuthor.setId(1);
        sourceAuthor.setNickname("原作者");

        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workMapper.insert(any(Work.class))).thenAnswer(inv -> {
            Work w = inv.getArgument(0);
            w.setId(2); // 模拟自增 ID
            return 1;
        });
        when(workMapper.updateById(testWork)).thenReturn(1);
        when(sandboxDraftMapper.insert(any(SandboxDraft.class))).thenReturn(1);

        Integer forkId = workService.forkWork(1, 3);

        assertNotNull(forkId);
        // 原作品 forkCount+1
        assertEquals(3, testWork.getForkCount()); // 2 + 1
        verify(workMapper, times(1)).insert(any(Work.class));
        verify(sandboxDraftMapper, times(1)).insert(any(SandboxDraft.class));
    }

    @Test
    @DisplayName("TC-WORK-014: forkWork — 作品不存在返回 null")
    void forkWorkNotFound() {
        when(workMapper.selectById(999)).thenReturn(null);

        Integer result = workService.forkWork(999, 1);

        assertNull(result);
    }

    // ==================== 删除测试 ====================

    @Test
    @DisplayName("TC-WORK-018: deleteWork — 删除自己的作品")
    void deleteOwnWork() {
        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workMapper.deleteById(1)).thenReturn(1);

        assertDoesNotThrow(() -> workService.deleteWork(1, 1));
        verify(workMapper).deleteById(1);
    }

    @Test
    @DisplayName("TC-WORK-019: deleteWork — 删除他人作品抛异常")
    void deleteOthersWork() {
        when(workMapper.selectById(1)).thenReturn(testWork);

        BusinessException ex = assertThrows(BusinessException.class,
                () -> workService.deleteWork(1, 999));
        assertEquals("无权删除他人作品", ex.getMessage());
    }

    @Test
    @DisplayName("TC-WORK-020: deleteWork — 作品不存在抛异常")
    void deleteWorkNotFound() {
        when(workMapper.selectById(999)).thenReturn(null);

        BusinessException ex = assertThrows(BusinessException.class,
                () -> workService.deleteWork(999, 1));
        assertEquals("作品不存在", ex.getMessage());
    }

    // ==================== 可见性切换测试 ====================

    @Test
    @DisplayName("TC-WORK-021: toggleVisibility — 公开→私密")
    void toggleVisibilityPublicToPrivate() {
        testWork.setIsPublic(1);
        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workMapper.updateById(any(Work.class))).thenReturn(1);

        workService.toggleVisibility(1, 1);

        assertEquals(0, testWork.getIsPublic());
    }

    @Test
    @DisplayName("TC-WORK-022: toggleVisibility — 私密→公开")
    void toggleVisibilityPrivateToPublic() {
        testWork.setIsPublic(0);
        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workMapper.updateById(any(Work.class))).thenReturn(1);

        workService.toggleVisibility(1, 1);

        assertEquals(1, testWork.getIsPublic());
    }

    @Test
    @DisplayName("toggleVisibility — 无权操作他人作品")
    void toggleVisibilityOthersWork() {
        when(workMapper.selectById(1)).thenReturn(testWork);

        assertThrows(BusinessException.class,
                () -> workService.toggleVisibility(1, 999));
    }

    // ==================== 更新作品测试 ====================

    @Test
    @DisplayName("TC-WORK-023: updateWorkFields — 更新标题")
    void updateWorkTitle() {
        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workMapper.updateById(any(Work.class))).thenReturn(1);

        workService.updateWorkFields(1, 1, "新标题", null);

        assertEquals("新标题", testWork.getTitle());
        assertEquals("测试描述", testWork.getDescription()); // 描述不变
    }

    @Test
    @DisplayName("TC-WORK-024: updateWorkFields — 更新描述")
    void updateWorkDescription() {
        when(workMapper.selectById(1)).thenReturn(testWork);
        when(workMapper.updateById(any(Work.class))).thenReturn(1);

        workService.updateWorkFields(1, 1, null, "新描述");

        assertEquals("测试作品", testWork.getTitle()); // 标题不变
        assertEquals("新描述", testWork.getDescription());
    }
}
