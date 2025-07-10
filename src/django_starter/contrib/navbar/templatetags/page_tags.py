# app/templatetags/page_tags.py
from django import template

register = template.Library()

@register.inclusion_tag('django_starter/components/page_header.html')
def page_header(title, breadcrumbs=None):
    """
    渲染标准页面标题和面包屑导航
    
    :param title: 页面主标题
    :param breadcrumbs: 面包屑导航列表，格式为：
        [
            {'text': '主页', 'url': '/admin/', 'icon': 'fa-solid fa-house'},
            {'text': '视频中台', 'url': '/admin/video/', 'icon': 'fa-solid fa-video'},
            {'text': '批量生成设备ID', 'url': None, 'icon': 'fa-solid fa-gears'},
        ]
        
        icon参数可选，如不提供则不显示图标
    """
    if breadcrumbs is None:
        breadcrumbs = []
        
    # 兼容旧格式 [(name, url), ...]
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
            
    return {
        'title': title,
        'breadcrumbs': processed_breadcrumbs,
    }
