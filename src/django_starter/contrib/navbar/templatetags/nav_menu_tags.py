from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_nav_menu():
    """获取导航菜单配置的模板标签（原始标签，保留用于兼容）"""
    return settings.NAV_MENU


@register.inclusion_tag('django_starter/components/sidebar_menu.html', takes_context=True)
def render_sidebar_menu(context):
    """
    渲染侧边栏菜单
    处理权限检查和激活状态
    """
    request = context.get('request')
    user = context.get('user')
    nav_menu = getattr(settings, 'NAV_MENU', [])
    processed_menu = []

    if not request:
        return {'menu_sections': []}

    # 获取当前路由信息
    resolver_match = getattr(request, 'resolver_match', None)
    current_app = getattr(resolver_match, 'app_name', '') if resolver_match else ''
    
    for section in nav_menu:
        # 处理每个 section
        processed_section = {
            'heading': section.get('heading'),
            'items': []
        }
        
        for item in section.get('items', []):
            # 1. 权限检查
            permissions = item.get('permissions', [])
            if not check_permissions(user, permissions):
                continue
                
            # 2. 激活状态检查
            is_active = False
            match_app = item.get('match_app')
            if match_app and match_app == current_app:
                is_active = True
            
            # 复制 item 并添加 active 状态
            # 注意：这里 item['url'] 可能是 lazy object，在模板渲染时会自动求值
            processed_item = item.copy()
            processed_item['is_active'] = is_active
            processed_section['items'].append(processed_item)
            
        # 只有当 section 有可见项时才显示
        if processed_section['items']:
            processed_menu.append(processed_section)
            
    return {
        'menu_sections': processed_menu,
        'request': request  # 传递 request 以便模板中可能用到
    }


def check_permissions(user, permissions):
    """
    检查用户是否满足权限列表
    支持 'is_authenticated', '!is_authenticated' 和标准 Django perms
    """
    if not permissions:
        return True
        
    for perm in permissions:
        if perm == 'is_authenticated':
            if not user or not user.is_authenticated:
                return False
        elif perm == '!is_authenticated':
            if user and user.is_authenticated:
                return False
        # 假设其他字符串是 Django permission codename
        elif user and not user.has_perm(perm):
            return False
            
    return True
