import re
import inspect

_under_scorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_under_scorer2 = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(s):
    """
    Is it ironic that this function is written in camel case, yet it
    converts to snake case? hmm..
    """
    subbed = _under_scorer1.sub(r'\1_\2', s)
    return _under_scorer2.sub(r'\1_\2', subbed).lower()


def snake_to_camel(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


if __name__ == '__main__':
    c = snake_to_camel('demo_test')
    s = camel_to_snake(c)
    print(c, s)
