from dataclasses import dataclass


@dataclass
class Uri:
    title: str
    url: str
    description: str = ''


# 相关博客列表
BLOGS = [
    Uri('项目完成小结：使用DjangoStarter v3和Taro开发的微信小程序', 'https://www.cnblogs.com/deali/p/18411349'),
    Uri('项目完成小结 - Django-React-Docker-Swag部署配置', 'https://www.cnblogs.com/deali/p/16961771.html'),
    Uri('DjangoAdmin使用合集，它的功能比你想象的强大！', 'https://www.cnblogs.com/deali/p/16678014.html'),
    Uri('轻量级消息队列 Django-Q 轻度体验', 'https://www.cnblogs.com/deali/p/16644989.html'),
    Uri('Django数据库性能优化之 - 使用Python集合操作', 'https://www.cnblogs.com/deali/p/16449011.html'),
    Uri('如何优雅地在django项目里生成不重复的ID？', 'https://www.cnblogs.com/deali/p/18593862')
]

# 相关项目列表
PROJECTS = [
    Uri('SiteDirectory', 'https://github.com/Deali-Axy/SiteDirectory', '一个基于Django的网站目录管理系统，支持多级分类和标签管理'),
    Uri('CodePackager', 'https://github.com/star-plan/code-packager', '代码打包工具，帮助开发者快速整理和分享代码片段'),
    Uri('django / channels', 'https://github.com/django/channels', 'Django的WebSocket支持库，为Django提供异步和实时通信功能'),
    Uri('excel_to_model', 'https://github.com/Deali-Axy/excel_to_model', 'Excel数据导入工具，支持将Excel数据快速导入Django模型'),
]
