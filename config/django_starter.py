def config_django_starter():
    return {
        # 管理后台的配置
        'admin': {
            'site_header': 'DjangoStarter',
            'site_title': 'DjangoStarter',
            'index_title': 'DjangoStarter',
            'list_per_page': 20
        },
        # 第三方登录配置
        'oauth': {
            # 微信企业号配置
            'wechat_work_config': {
                'corp_id': '',
                'secret': ''
            },
        }
    }
