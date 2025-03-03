import re

from django import template

register = template.Library()


@register.simple_tag
def current_url_re_match(request, pattern):
    return re.match(pattern, request.path)


@register.simple_tag(takes_context=True)
def nav_menu_class(context, menu_name):
    request = context['request']
    if re.match(f'^/{menu_name}/', request.path):
        return 'block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500'
    return 'block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700'


@register.simple_tag(takes_context=True)
def nav_menu_aria(context, menu_name):
    request = context['request']
    if re.match(f'^/{menu_name}/', request.path):
        return 'aria-current="page"'
    return ''
