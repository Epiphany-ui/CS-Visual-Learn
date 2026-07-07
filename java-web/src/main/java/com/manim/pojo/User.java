package com.manim.pojo;

import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonFormat;

import java.time.LocalDateTime;

/**
 * 系统登录用户实体
 * <p>
 * 对应 database.sql 中 user 表结构：
 * id, username, password, create_time
 * </p>
 */
@TableName("user")
public class User {

    /** 用户id（INT自增） */
    @TableId(type = IdType.AUTO)
    private Integer id;

    /** 登录账号，唯一不可重复 */
    private String username;

    /** 登录密码（序列化时忽略，不返回给前端） */
    @JsonIgnore
    private String password;

    /** 创建时间 */
    @TableField(fill = FieldFill.INSERT)
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;

    // ===== getters & setters =====

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public LocalDateTime getCreateTime() {
        return createTime;
    }

    public void setCreateTime(LocalDateTime createTime) {
        this.createTime = createTime;
    }
}
