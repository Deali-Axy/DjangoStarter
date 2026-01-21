# 架构与规范

本项目采用清晰的分层目录结构与约定式开发规范，便于团队协作与扩展。

## 目录结构

```
src/
├── apps/                  # 业务应用
├── config/                # Django 配置
├── django_starter/        # 核心框架代码
├── static/                # 静态资源
├── templates/             # 公共模板（不要直接修改）
└── locale/                # i18n
```

## 关键组件

- ModelExt：统一的模型基类，提供软删除与时间戳
- Django-Ninja：API 组织位于 apps/[app]/apis/
- Split Settings：配置拆分在 config/settings/components/

## 开发规范摘要

- 遵循 PEP 8 与类型注解
- Model 字段需提供 verbose_name
- API 使用 Pydantic Schema 与 JwtBearer 鉴权
- 前端模板使用 Tailwind CSS 与语义化 HTML
