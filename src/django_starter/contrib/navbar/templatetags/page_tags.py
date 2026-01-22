# app/templatetags/page_tags.py
from django import template

register = template.Library()

def _normalize_breadcrumbs(breadcrumbs):
    if breadcrumbs is None:
        return []
        
    processed_breadcrumbs = []
    for item in breadcrumbs:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            processed_breadcrumbs.append({
                'text': item[0],
                'url': item[1],
                'icon': None
            })
        else:
            processed_breadcrumbs.append(item)
    return processed_breadcrumbs

@register.inclusion_tag('django_starter/components/page_header.html')
def page_header(title, breadcrumbs=None, show_title=True, show_breadcrumbs=True):
    """
    渲染标准页面标题和面包屑导航
    
    :param title: 页面主标题
    :param breadcrumbs: 面包屑导航列表
    :param show_title: 是否显示标题区域，默认为 True
    :param show_breadcrumbs: 是否显示面包屑导航，默认为 True
    """
    return {
        'title': title,
        'breadcrumbs': _normalize_breadcrumbs(breadcrumbs),
        'show_title': show_title,
        'show_breadcrumbs': show_breadcrumbs,
    }

@register.inclusion_tag('django_starter/components/breadcrumbs_items.html')
def render_breadcrumbs(breadcrumbs, show_icon=False):
    """
    仅渲染面包屑导航列表项 (<li>...</li>)
    用于 navbar 等需要单独显示面包屑的地方
    
    :param show_icon: 是否显示图标，默认为 False
    """
    return {
        'breadcrumbs': _normalize_breadcrumbs(breadcrumbs),
        'show_icon': show_icon,
    }
