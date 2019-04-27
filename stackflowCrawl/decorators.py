# -*- coding: utf-8 -*-


def validate_value(func):
    def wrapper_value_error(*arg, **kw):
        value, key = func(*arg, **kw)
        if not value:
            raise ValueError(
                "{} must have a {}".format(arg[0].__class__.__name__, key)
            )
        else:
            return value
    return wrapper_value_error
