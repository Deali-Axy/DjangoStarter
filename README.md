# Django Rails 基础框架

这个项目是我为了满足公司安全部门的要求，定制了一个基于Django的Web框架，
功能包括：给DjangoAdmin加上验证码，并且加入登录次数尝试，
屏蔽了RestFramework默认的API主页，使外部访问无法看到所有接口。

后续我会根据实际工作继续添加一些其他功能以方便团队快速搭建应用~


## features

- 自定义访问前缀
- 支持Docker部署
- 支持Uwsgi部署
- 基于SimpleUI定制的管理后台
- 管理后台支持登录验证码和登录尝试次数限制
- 集成RestFramework，默认屏蔽了链接主页，即对外隐藏API
- 对默认的settings进行拆分
- 默认使用Redis缓存

## 文件结构

- apps：所有应用
- apps/core：默认应用，包含已经写好的示例逻辑和后台登录限流逻辑
- config：Django配置
- static：静态文件
- static_collected：运行collectstatic命令后把所有静态文件都保存到这个文件夹
- templates：模板


## 快速开始


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



## TODO

- [ ] 集成IP段限制中间件
- [ ] 集成微信公众号、小程序SDK
- [ ] 集成单点登录认证
- [ ] 集成消息队列


## LICENSE
```
Apache License Version 2.0, January 2004
http://www.apache.org/licenses/
```
