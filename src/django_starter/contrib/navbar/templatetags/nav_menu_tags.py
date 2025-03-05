from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_nav_menu():
    """获取导航菜单配置的模板标签"""
    return settings.NAV_MENU
