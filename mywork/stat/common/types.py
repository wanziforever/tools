#!/usr/bin/python
# -*- coding: UTF-8 -*-

from errors import ResourceNotFoundError, ArgMissingError, ArgError
import doctest
import functools
import inspect
import os
import logging

#log = logging.getLogger(__name__)

class Dict(dict):
    '''
    A Dict object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.

    >>> o = Dict(a=1)
    >>> o.a
    1
    >>> o['a']
    1
    >>> o.a = 2
    >>> o['a']
    2
    >>> del o.a
    >>> o.a
    Traceback (most recent call last):
    ...
    AttributeError: 'a'
    >>> del o.b
    Traceback (most recent call last):
    ...
    AttributeError: 'b'
    '''
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError(k)

    @staticmethod
    def get_and_del_from_dict(d, key, default=None):
        '''
        if specified key exist in dict,
        the value should be returned and deleted in the dict
        >>> d = { 'a' : 1 }
        >>> Dict.get_and_del_from_dict(d, 'a')
        1
        >>> 'a' in d
        False

        if specified key does not exist in dict,
        should return the default value
        >>> Dict.get_and_del_from_dict({}, 'a', 2)
        2
        '''
        if key in d:
            value = d[key]
            del d[key]
            return value
        else:
            return default

    def get_and_del(self, key, default=None):
        '''
        if specified key exist in dict,
        the value should be returned and deleted in the dict
        >>> d = Dict(a=1)
        >>> d.get_and_del('a')
        1
        >>> 'a' in d
        False

        if specified key does not exist in dict,
        should return the default value
        >>> d = Dict()
        >>> d.get_and_del('a', 2)
        2
        '''
        return Dict.get_and_del_from_dict(self, key, default)

class CiDict(Dict):
    '''
    >>> d = CiDict(a='111')
    >>> d['a']
    '111'
    >>> d.a
    '111'
    >>> d['A']
    '111'
    >>> d.A
    '111'

    >>> d.b = '222'
    >>> d['b']
    '222'
    >>> d.b
    '222'
    >>> d['B']
    '222'
    >>> d.B
    '222'
    '''
    def __getitem__(self, key):
        return super(CiDict, self).__getitem__(key.lower())

    def __setitem__(self, key, value):
        super(CiDict, self).__setitem__(key.lower(), value)

class Function(object):
    def __init__(self, func=None):
        self._decorate_or_call = self._decorate
        if func:
            self._decorate(func)

    def __call__(self, *args, **kw):
        return self._decorate_or_call(*args, **kw)

    def __get__(self, instance, instancetype):
        # wrap the current functor with Function1
        # no matter the current functor is Function1 or Function2
        return BoundedFunction(self, instance)

    def __str__(self):
        return '<Function %s>' % self.__name__

    def get_original_lineno(self):
        return self._func.get_original_lineno() if isinstance(self._func, Function) else self._func.func_code.co_firstlineno

    def _call(self, *args, **kw):
        return self._func(*args, **kw)

    def _convert_to_arg_dict(self, *args, **kw):
        # verify that there aren't too many args
        if len(args) > len(self.params):
            raise ArgError('TOO_MANY_ARGS', 'Function1 %s takes at most %d arguments (%d given).' \
                    % (self._func.__name__, len(self.params), len(args)))

        # convert to dict
        d = Dict(self.optional_params)
        d.update(kw)
        for i in range(len(args)):
            d[self.params[i]] = args[i]

        # verify that all required params are specified
        for p in self.required_params:
            if p not in d:
                raise ArgMissingError(p)

        return d

    def _convert_to_arg_list(self, d):
        args = []
        for param in self.required_params:
            arg = d.get(param)
            if arg is None:
                raise ArgMissingError(param)
            args.append(arg)
        for param, default in self.optional_params:
            args.append(d.get(param, default))
        return args

    def _decorate(self, func):
        self._func = func
        functools.update_wrapper(self, func, updated=[])
        if isinstance(func, Function):
            functools.update_wrapper(self, func, ['params', 'required_params', 'optional_params'], [])
        else:
            self._parse_params(func)
        self._decorate_or_call = self._call
        return self

    def _parse_params(self, func):
        self.params, nouse, nouse, defaults = inspect.getargspec(func) #@UnusedVariable
        if defaults is None:
            self.required_params = self.params
            self.optional_params = []
        else:
            self.required_params = self.params[:-len(defaults)]
            self.optional_params = [(self.params[-1 - i], defaults[-1 - i]) for i in range(len(defaults))]
            self.optional_params.reverse()

class BoundedFunction(Function):
    def __init__(self, func, instance):
        self._decorate(func)
        self._instance = instance

    def __call__(self, *args, **kw):
        args = [self._instance] + list(args)
        return self._func(*args, **kw)

class Properties(Dict):

    def __init__(self, file_path='', check_file=False, override=False, properties=None):
        self._check_file = check_file
        self._override = override
        self._load(file_path)
        if isinstance(properties, dict):
            for k, v in properties.items():
                self.set_property(k, v, self._override)

    def _load(self, file_path):
        if not os.path.isfile(file_path):
            if self._check_file:
                raise ResourceNotFoundError('FILE', file_path)
            else:
                #log.warn('properties file {0} is not found'.format(file_path))
                return

        with open(file_path, 'r') as f:
            for l in f:
                l = l.strip()
                if len(l) == 0 or l[0] == '#':
                    continue
                parts = l.split('=', 1)
                key = parts[0].strip()
                value = parts[1].strip()
                self.set_property(key, value, self._override)

    def set_property(self, key, value, override=False):
        if not override and key in self:
            #log.debug('property {0} already exists'.format(key))
            return
        self[key] = value

    def merge(self, properties, override=False):
        for k, v in properties.items():
            self.set_property(k, v, override)


if __name__ == '__main__':
    doctest.testmod()
