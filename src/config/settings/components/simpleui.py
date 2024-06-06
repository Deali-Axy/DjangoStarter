from config.settings.components.common import URL_PREFIX

# SimpleUI 配置
SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'  # 默认主题
# SIMPLEUI_LOGO = f'/{URL_PREFIX}static/admin/images/custom_logo.png'
SIMPLEUI_HOME_PAGE = f'/{URL_PREFIX}django-starter/admin/extend_home/'
SIMPLEUI_HOME_ICON = 'fa fa-home'
SIMPLEUI_HOME_INFO = False  # 显示服务器信息
SIMPLEUI_HOME_QUICK = True  # 快速操作
SIMPLEUI_HOME_ACTION = True  # 最近动作
SIMPLEUI_ANALYSIS = False  # 关闭使用分析
SIMPLEUI_STATIC_OFFLINE = True  # 离线模式
SIMPLEUI_ICON = {
    'Core': 'fa fa-cat',
    '令牌': 'fa fa-lock',
    '认证令牌': 'fa fa-lock',
}
