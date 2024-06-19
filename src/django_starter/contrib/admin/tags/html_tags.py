from typing import Optional
from django.utils.html import format_html


def image(url, alt_text='', width: Optional[int] = None, height: Optional[int] = None):
    size = ''
    if width:
        size += f'width={width} '
    if height:
        size += f'height={height} '
    return format_html('<img src="{}" {} alt="{}" />', url, size, alt_text)


def link(url, text, target='_self'):
    return format_html('<a href="{}" target="{}">{}</a>', url, target, text)


# todo 未测试
def script(src):
    return format_html('<script src="{}"></script>', src)


# todo 未测试
def style(css):
    return format_html('<style>{}</style>', css)


# todo 未测试
def div(content, class_name=None, id_name=None):
    class_attr = f' class="{class_name}"' if class_name else ''
    id_attr = f' id="{id_name}"' if id_name else ''
    return format_html('<div{}{}>{}</div>', class_attr, id_attr, content)


# todo 未测试
def span(content, class_name=None):
    class_attr = f' class="{class_name}"' if class_name else ''
    return format_html('<span{}>{}</span>', class_attr, content)
