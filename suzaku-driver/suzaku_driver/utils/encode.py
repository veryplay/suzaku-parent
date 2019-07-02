#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six

def to_utf8(text):
    """Encode Unicode to UTF-8, return bytes unchanged.

    :param text: text content : str
    
    Raise TypeError if text is not a bytes string or a Unicode string.

    .. versionadded:: 3.5
    """
    if isinstance(text, six.binary_type):
        return text
    elif isinstance(text, six.text_type):
        return text.encode('utf-8')
    else:
        raise TypeError("bytes or Unicode expected, got %(text)s"
                        % {"text" : type(text).__name__})