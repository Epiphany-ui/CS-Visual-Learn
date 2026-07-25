-- 社区与学习路径基础打通：作品关联来源标签
ALTER TABLE work ADD COLUMN knowledge_slug VARCHAR(255) DEFAULT NULL COMMENT '关联知识点slug' AFTER source_work_id;
ALTER TABLE work ADD COLUMN path_id VARCHAR(50) DEFAULT NULL COMMENT '关联学习路径ID' AFTER knowledge_slug;
