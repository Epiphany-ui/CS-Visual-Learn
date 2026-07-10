package com.manim.controller;

import cn.hutool.http.HttpRequest;
import cn.hutool.json.JSONArray;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import com.manim.dto.WorkListDTO;
import com.manim.pojo.Result;
import com.manim.pojo.User;
import com.manim.pojo.Work;
import com.manim.service.UserService;
import com.manim.service.WorkService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.stream.Collectors;

@Tag(name = "社区画廊接口")
@RestController
@RequestMapping("/api/v1/gallery")
public class GalleryController {

    private static final Logger log = LoggerFactory.getLogger(GalleryController.class);

    @Autowired
    private WorkService workService;

    @Autowired
    private UserService userService;

    @Value("${manim.ai.base-url}")
    private String aiBaseUrl;

    /**
     * 从 Python 服务获取当前实际存在的视频文件名列表
     */
    private Set<String> fetchExistingFilenames() {
        try {
            String url = aiBaseUrl + "/api/videos/filenames";
            String body = HttpRequest.get(url).timeout(5000).execute().body();
            JSONObject resp = JSONUtil.parseObj(body);
            Object data = resp.get("data");
            if (data instanceof JSONArray) {
                JSONArray arr = (JSONArray) data;
                Set<String> set = new HashSet<>();
                for (int i = 0; i < arr.size(); i++) {
                    set.add(arr.getStr(i));
                }
                return set;
            }
        } catch (Exception e) {
            log.warn("获取 Python 视频文件列表失败，跳过存在性校验：{}", e.getMessage());
        }
        return Collections.emptySet();
    }

    /**
     * 从 video_path 中提取文件名
     */
    private String extractFilename(String videoPath) {
        if (videoPath == null || videoPath.isEmpty()) return null;
        int idx = videoPath.lastIndexOf('/');
        return idx >= 0 ? videoPath.substring(idx + 1) : videoPath;
    }

    @Operation(summary = "获取画廊作品列表/排行榜（自动过滤已删除的视频）")
    @GetMapping("/list")
    public Result<Map<String, Object>> getGalleryList(
            @RequestParam(value = "rankType", defaultValue = "weekly") String rankType,
            @RequestParam(value = "sort", required = false) String sort,
            @RequestParam(value = "category", required = false) String category,
            @RequestParam(value = "page", defaultValue = "1") Integer page,
            @RequestParam(value = "size", defaultValue = "10") Integer size) {

        // 1. 获取实际存在的视频文件名
        Set<String> existingFiles = fetchExistingFilenames();

        // 2. 查询数据库
        List<Work> works = workService.listGallery(rankType, sort, category, page, size);

        // 3. 过滤 + 清理孤立记录
        List<Work> validWorks = new ArrayList<>();
        List<Work> orphanedWorks = new ArrayList<>();
        for (Work w : works) {
            String fn = extractFilename(w.getVideoPath());
            if (existingFiles.isEmpty() || (fn != null && existingFiles.contains(fn))) {
                validWorks.add(w);
            } else {
                orphanedWorks.add(w);
            }
        }

        // 4. 清理孤立记录
        if (!orphanedWorks.isEmpty()) {
            log.info("发现 {} 个孤立作品（视频已丢失），自动清理", orphanedWorks.size());
            for (Work ow : orphanedWorks) {
                try { workService.deleteWork(ow.getId()); } catch (Exception e) {
                    log.warn("清理孤立作品 {} 失败：{}", ow.getId(), e.getMessage());
                }
            }
        }

        // 5. 转为 DTO
        List<WorkListDTO> list = validWorks.stream().map(w -> {
            User author = userService.getById(w.getUserId());
            String authorName = author != null ?
                (author.getNickname() != null ? author.getNickname() : author.getUsername()) :
                "匿名用户";
            String authorAvatar = author != null ? author.getAvatar() : null;
            String createTime = w.getCreateTime() != null ? w.getCreateTime().toString() : null;
            return new WorkListDTO(w.getId(), w.getCover(), w.getTitle(),
                    w.getDescription(), authorName, authorAvatar,
                    w.getLikeCount(), w.getViewCount(),
                    w.getVideoPath(), createTime);
        }).collect(Collectors.toList());

        Map<String, Object> data = new HashMap<>();
        data.put("list", list);
        data.put("total", validWorks.size());
        return Result.success(data);
    }
}
