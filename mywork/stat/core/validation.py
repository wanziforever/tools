#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'shaoguojian@video-tx.com'


from core import request
from common.errors import ArgMissingError, PermissionDeniedError
import functools
import doctest
import inspect


def params_required(*args, **kwargs):
    """
    source: query, cookie, form, file
    validation: None
    """
    def wrapper(func):
        @functools.wraps(func)
        def _wrapper(*func_args, **func_kwargs):
            source = kwargs.get('source', 'query')
            for param in args:
                if source == 'query':
                    p = request.query.get(param)
                elif source == 'cookie':
                    p = request.cookies.get(param)
                elif source == 'form':
                    p = request.forms.get(param)
                elif source == 'file':
                    p = request.files.get(param)
                if p is None:
                    raise ArgMissingError(param)
                # TODO: validate params
                #if validations is None or not isinstance(validations, dict):
                #    continue
                #validation = validations.get(param, None)
                #if validation is None:
                #    continue
            return func(*func_args, **func_kwargs)
        argspec = inspect.getargspec(func)
        if 'db' in argspec.args:
            _wrapper.inject_db = True
        return _wrapper
    return wrapper


def json_required(*args, **kwargs):
    def wrapper(func):
        @functools.wraps(func)
        def _wrapper(*func_args, **func_kwargs):
            data = request.json
            if data is None:
                raise ArgMissingError('json argument')
            if isinstance(data, dict):
                data = [data]
            if isinstance(data, list):
                for d in data:
                    if isinstance(d, dict):
                        for key in args:
                            if key not in d:
                                raise ArgMissingError(key)
                        # TODO: validate keys
            return func(*func_args, **func_kwargs)
        argspec = inspect.getargspec(func)
        if 'db' in argspec.args:
            _wrapper.inject_db = True
        return _wrapper
    return wrapper


def verify_current_customer(customer_id):
    if request.customer_id != customer_id:
        raise PermissionDeniedError(msg='invalid customer')


@params_required('param')
def test_param_required():
    """
    >>> request.query = {'param1': 'value1'}
    >>> test_param_required()
    Traceback (most recent call last):
    ArgMissingError: [ARG_MISSING] "param" is required. (_status_code="400", param="param")
    >>> request.query['param'] = 'value'
    >>> test_param_required()
    """
    pass


if __name__ == '__main__':
    doctest.testmod()