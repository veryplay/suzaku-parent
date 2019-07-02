#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six
import inspect

_BUILTIN_MODULES = ('builtins', '__builtin__', '__builtins__', 'exceptions')

def get_method_self(method):
    """Gets the ``self`` object attached to this method (or none)."""
    if not inspect.ismethod(method):
        return None
    try:
        return six.get_method_self(method)
    except AttributeError:
        return None

def get_class_name(obj, fully_qualified=True, truncate_builtins=True):
    """Get class name for object.

    If object is a type, returns name of the type. If object is a bound
    method or a class method, returns its ``self`` object's class name.
    If object is an instance of class, returns instance's class name.
    Else, name of the type of the object is returned. If fully_qualified
    is True, returns fully qualified name of the type. For builtin types,
    just name is returned. TypeError is raised if can't get class name from
    object.
    """
    if inspect.isfunction(obj):
        raise TypeError("Can't get class name.")

    if inspect.ismethod(obj):
        obj = get_method_self(obj)
    if not isinstance(obj, six.class_types):
        obj = type(obj)
    if truncate_builtins:
        try:
            built_in = obj.__module__ in _BUILTIN_MODULES
        except AttributeError:  # nosec
            pass
        else:
            if built_in:
                return obj.__name__
    if fully_qualified and hasattr(obj, '__module__'):
        return '%s.%s' % (obj.__module__, obj.__name__)
    else:
        return obj.__name__