package com.manim.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * SpringDoc OpenAPI (Swagger) 配置
 * <p>
 * 生成 API 接口文档，启动后访问 {@code /swagger-ui.html} 可查看。
 * </p>
 */
@Configuration
public class SwaggerConfig {

    /**
     * 自定义 OpenAPI 文档信息
     * <p>
     * 包括接口标题、版本号、描述、联系人以及许可证信息，
     * 展示在 Swagger UI 页面顶部。
     * </p>
     */
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Manim 动画自动生成引擎 API")
                        .version("1.0.0")
                        .description("Java 后端业务接口，支持动画任务提交、状态查询、历史记录管理")
                        .contact(new Contact()
                                .name("Manim AI Team")
                                .email("team@manim-ai.local"))
                        .license(new License()
                                .name("MIT")
                                .url("https://opensource.org/licenses/MIT")));
    }
}
