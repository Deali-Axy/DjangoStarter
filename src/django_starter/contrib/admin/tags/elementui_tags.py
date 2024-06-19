from django.utils.html import format_html


def el_tag(color_type, content):
    """
    生成 ElementUI 的 tag 组件

    :param color_type: success, info, warning, danger
    :param content:
    :return:
    """
    type_class = '' if len(color_type) == 0 else f'el-tag--{color_type}'

    return format_html(
        '<div class="el-tag el-tag--small {} el-tag--light">{}</div>',
        type_class, content
    )


# todo 未测试
def el_button(type, content, plain=False, round=False, circle=False):
    """
    生成 ElementUI 的 button 组件

    :param type: primary, success, warning, danger, info, text
    :param content: 按钮内容
    :param plain: 是否朴素按钮
    :param round: 是否圆角按钮
    :param circle: 是否圆形按钮
    :return: HTML 字符串
    """
    type_class = f'el-button--{type}' if type else ''
    plain_class = 'is-plain' if plain else ''
    round_class = 'is-round' if round else ''
    circle_class = 'is-circle' if circle else ''
    return format_html(
        '<button class="el-button {} {} {} {}">{}</button>',
        type_class, plain_class, round_class, circle_class, content
    )


# todo 未测试
def el_alert(title, type, description='', closable=True, center=False, close_text=''):
    """
    生成 ElementUI 的 alert 组件

    :param title: 标题
    :param type: success, warning, info, error
    :param description: 描述
    :param closable: 是否可关闭
    :param center: 文字是否居中
    :param close_text: 关闭按钮自定义文本
    :return: HTML 字符串
    """
    closable_attr = 'true' if closable else 'false'
    center_class = 'is-center' if center else ''
    return format_html(
        '<div class="el-alert el-alert--{} {}" '
        'closable="{}" close-text="{}">'
        '<span class="el-alert__title">{}</span>'
        '<p class="el-alert__description">{}</p>'
        '</div>',
        type, center_class, closable_attr, close_text, title, description
    )


# todo 未测试
def el_card(header, body):
    """
    生成 ElementUI 的 card 组件

    :param header: 卡片头部内容
    :param body: 卡片主体内容
    :return: HTML 字符串
    """
    return format_html(
        '<div class="el-card">'
        '<div class="el-card__header">{}</div>'
        '<div class="el-card__body">{}</div>'
        '</div>',
        header, body
    )
