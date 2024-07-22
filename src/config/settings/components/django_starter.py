class ProjectInfo(object):
    def __init__(self, name: str, description: str = ''):
        self.name = name
        self.description = description


project_info = ProjectInfo('DjangoStarter')

# DjangoStarter 框架配置
DJANGO_STARTER = {
    'project_info': {
        'name': project_info.name,
        'description': project_info.description,
    },
    # 管理后台的配置
    'admin': {
        'site_header': project_info.name,
        'site_title': project_info.name,
        'index_title': project_info.name,
        'list_per_page': 20
    },
    # 认证配置
    'auth': {
        # JWT 配置
        'jwt': {
            # 算法
            'algo': 'HS256',
            # 随机的salt密钥，只有token生成者（同时也是校验者）自己能有，用于校验生成的token是否合法
            'salt': 'CUeeG5Ez56d2GCd5pfqvkXwVMGTvzdwo',
            # token 有效时间 （单位：秒）
            'lifetime': 12 * 60 * 60,
        }
    },
    # 第三方登录配置
    'oauth2': {
        # 微信登录配置
        'wechat': {
            'enabled': False,
            'app_id': '',
            'secret': '',
            'redirect_uri': '',
        },
        # 企业微信配置
        'wecom': {
            'enabled': False,
            'corp_id': '',
            'secret': '',
            'redirect_uri': '',
        },
        # 微信小程序配置
        'weapp': {
            'enabled': False,
            'appid': '',
            'secret': ''
        }
    }
}
