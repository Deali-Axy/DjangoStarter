def config_django_starter():
    return {
        # 第三方登录配置
        'OAUTH': {
            # 微信企业号配置
            'WECHAT_WORK_CONFIG': {
                'CORP_ID': '',
                'SECRET': ''
            },
        }
    }
