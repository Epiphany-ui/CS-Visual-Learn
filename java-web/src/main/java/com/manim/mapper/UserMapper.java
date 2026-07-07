package com.manim.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.manim.pojo.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

/**
 * 用户数据访问接口
 */
@Mapper
public interface UserMapper extends BaseMapper<User> {

    /**
     * 按用户名查询用户
     */
    User selectByUsername(@Param("username") String username);
}
