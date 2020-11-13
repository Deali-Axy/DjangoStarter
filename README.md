# Django Starter 基础框架

这个项目是我为了满足公司安全部门的要求，定制了一个基于Django的Web框架，
功能包括：给DjangoAdmin加上验证码，并且加入登录次数尝试，
屏蔽了RestFramework默认的API主页，使外部访问无法看到所有接口。

后续我会根据实际工作继续添加一些其他功能以方便团队快速搭建应用~


## features


- admin后台安全限制中间件（需手动启用）
- 非debug模式下管理员可以查看报错信息（需手动启用）
- 自定义访问前缀
- 支持Docker部署（使用`docker-compose`方式）
- 支持Uwsgi部署，支持Uwsgi自动重启
- 默认启用`CORS_ALLOW`实现接口跨域
- 基于SimpleUI定制的管理后台
- 管理后台支持登录验证码和登录尝试次数限制
- 集成RestFramework，默认屏蔽了链接主页，即对外隐藏API
- 对默认的`settings`进行拆分
- 默认使用Redis缓存
- 优化`drf_yasg`的Swagger分组和文档显示效果（显示分组说明、接口说明等）


## 文件结构

- apps：所有应用
- apps/core：默认应用，包含已经写好的示例逻辑和后台登录限流逻辑
- config：Django配置
- static：静态文件
- static_collected：运行collectstatic命令后把所有静态文件都保存到这个文件夹
- templates：模板


## 快速开始

### 安装依赖

```python
pip install -r requirements.txt
```

### 迁移数据库

```
python manage.py makemigrations
python manage.py migrate
```


### 配置Redis缓存

请先在本机安装Redis服务，即可正常使用


### 配置URL前缀

在环境变量中指定`URL_PREFIX`地址前缀

部署应用需要在`docker-compose.yml`文件中修改这个环境变量

运行应用后，会自动在所有URL前加上前缀，如管理后台的地址

添加URL前缀之前：

```
http://127.0.0.1/admin
```

添加URL前缀（如 test）之后：

```
http://127.0.0.1/test/admin
```


### 开始写业务逻辑

- **根据实际业务在`apps`包中创建一个新的应用（推荐）**
- ~~在默认应用`apps/core`里写~~（不推荐）

使用`django-admin`命令创建app：

```bash
cd apps
django-admin startapp your_app_name
```

仿照`apps/core`里的逻辑进行业务开发，每个App需要完成以下代码开发：
- `models.py`
- `serializers.py`
- `viewsets.py`

之后在`urls.py`中注册路由，代码参考`apps/core/urls.py`。

需要在Django后台进行管理的话，在`admin.py`中进行注册，参考`apps/core/admin.py`。


## 配置

### 配置Django后台网站名称

编辑`apps/core/admin.py`文件，修改这三行代码：

```python
admin.site.site_header = 'DjangoStart 管理后台'
admin.site.site_title = 'DjangoStart 管理后台'
admin.site.index_title = 'DjangoStart 管理后台'
```

>PS: 本项目的后台界面基于SimpleUI，更多Django后台配置方法请参考SimpleUI官方文档。


### 配置App在后台显示的名称

编辑每个App目录下的`apps.py`文件，在`[AppName]Config`类里配置`verbose_name`，然后在App目录下的`__init__.py`中，设置`default_app_config`即可，具体参照`apps/core`的代码。


### 配置app在swagger中的说明

编辑`config/swagger.py`文件，在`CustomOpenAPISchemaGenerator`类的`get_schema`方法中配置`swagger.tags`即可。


### 限流配置

编辑`config/rest_framework.py`文件 ，参照注释说明修改`DEFAULT_THROTTLE_RATES`节点即可。


### 配置启用*admin后台安全限制中间件*

编辑`config/settings.py`文件，在`MIDDLEWARE`节点中添加`middleware/admin_secure.AdminSecureMiddleware`即可。

### 配置启用*非debug模式下管理员可以查看报错信息*

编辑`config/settings.py`文件，在`MIDDLEWARE`节点中添加`middleware/user_base_exception.UserBasedExceptionMiddleware`即可。


### Uwsgi自动重启

在`uwsgi.ini`配置文件中，本项目已经配置了监控`readme.md`文件，文件变化就会自动重启服务器，因此在生产环境中可以通过修改`readme.md`文件实现优雅的uwsgi服务重启。


## TODO

- [x] 集成IP段限制中间件
- [ ] 集成微信公众号、小程序SDK
- [ ] 集成单点登录认证
- [x] 集成消息队列
- [ ] 进一步优化`settings`拆分
- [ ] 完善项目单元测试
- [ ] 使用自动构建部署工具实现快速
- [ ] 实现自动的业务代码生成器

## 相关博文

公众号专辑：[Django开发精选](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI3MjQ5ODU0Mg==&action=getalbum&album_id=1409752252860022785&subscene=126&scenenote=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI3MjQ5ODU0Mg%3D%3D%26mid%3D2247485662%26idx%3D1%26sn%3D3dfeb8a077220afb3607abcf9dc03eb9%26chksm%3Deb30e2dfdc476bc94ad3d4314591eeb74b1a3340aaff763af81e8aa3aeb13433ad63d14f382c%26scene%3D126%26sessionid%3D1594189969%26key%3D6d309a22c00ffb6bef9cc0b9cd5a125d1e6e57036758e1406e9eb444f50e9b700fbfbda8deaa1bfc431da4096bcd3b716f4f3fbaf30d1cb13aa779da9a32cd5cb7dabfd8d4069be6e23c19759f34c9e5%26ascene%3D1%26uin%3DMjQ1NzIyMjgw%26devicetype%3DWindows%2B10%2Bx64%26version%3D62090523%26lang%3Dzh_CN%26exportkey%3DA41f2%252BxPyxQC8LkTcD3p2O0%253D%26pass_ticket%3DtRJAFFF0qD2j0C9V0754yCDjHLxEraPHwEk%252BG2geCzI%253D%26winzoom%3D1.25#wechat_redirect)

知乎专栏：[程序设计实验室](https://www.zhihu.com/column/deali)

- [聊聊Django应用的部署和性能的那些事儿](https://zhuanlan.zhihu.com/p/152679805)
- [给Django Admin添加验证码和多次登录尝试限制](https://zhuanlan.zhihu.com/p/138955540)
- [Python后端日常操作之在Django中「强行」使用MVVM设计模式](https://zhuanlan.zhihu.com/p/136571773)
- [Python后端必须知道的Django的信号机制！](https://zhuanlan.zhihu.com/p/135361621)
- [一小时完成后台开发：DjangoRestFramework开发实践](https://zhuanlan.zhihu.com/p/113367282)
- [Django快速开发实践：Drf框架和xadmin配置指北](https://zhuanlan.zhihu.com/p/100135134)


## LICENSE
```
Apache License Version 2.0, January 2004
http://www.apache.org/licenses/
```
