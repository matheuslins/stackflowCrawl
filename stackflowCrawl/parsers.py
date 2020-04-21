import re


_re_nonspaces = re.compile(u'[^\s]+|\n', flags=re.UNICODE)
_re_norm_CR = re.compile(u'(?:\s*\n\s*)+', flags=re.UNICODE)


def normalize_spaces(value):
    cleared_value = u' '.join(_re_nonspaces.findall(value))
    return _re_norm_CR.sub(u'\n', cleared_value).strip()


def convert_items_to_int(items):
    return [int(item) for item in items]


def convert_to_int(item):
    if item:
        if isinstance(item[0], str):
            return int(item[0])
        return item
