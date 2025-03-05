from dataclasses import dataclass


@dataclass
class Uri:
    title: str
    url: str


# 相关博客列表
BLOGS = [
    Uri('项目完成小结：使用DjangoStarter v3和Taro开发的微信小程序', 'https://www.cnblogs.com/deali/p/18411349'),
    Uri('项目完成小结 - Django-React-Docker-Swag部署配置', 'https://www.cnblogs.com/deali/p/16961771.html'),
    Uri('DjangoAdmin使用合集，它的功能比你想象的强大！', 'https://www.cnblogs.com/deali/p/16678014.html'),
    Uri('轻量级消息队列 Django-Q 轻度体验', 'https://www.cnblogs.com/deali/p/16644989.html'),
    Uri('Django数据库性能优化之 - 使用Python集合操作', 'https://www.cnblogs.com/deali/p/16449011.html'),
    Uri('如何优雅地在django项目里生成不重复的ID？', 'https://www.cnblogs.com/deali/p/18593862'),
    Uri('新版的Django Docker部署方案，多阶段构建、自动处理前端依赖', 'https://www.cnblogs.com/deali/p/18357853'),
]

# 相关项目列表
PROJECTS = [
    Uri('SiteDirectory', 'https://github.com/Deali-Axy/SiteDirectory'),
    Uri('CodePackager', 'https://github.com/star-plan/code-packager'),
    Uri('django / channels', 'https://github.com/django/channels'),
    Uri('excel_to_model', 'https://github.com/Deali-Axy/excel_to_model'),
]
