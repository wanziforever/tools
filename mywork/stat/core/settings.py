#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
settings for root app and sub-apps

@author: Shao Guojian
"""

from common.types import Properties
from common import util
import os
from apps import get_app_dirs, get_app_base_dir, get_root_dir
import doctest


class Settings(Properties):
    """
    >>> p = {'db.username':'root', 'db.host':'localhost'}
    >>> settings = Settings(properties=p)
    >>> settings['db.username']
    'root'
    >>> settings['DB_USERNAME']
    'root'
    >>> settings.DB_USERNAME
    'root'
    >>> settings['db.username1']
    Traceback (most recent call last):
    KeyError: 'db.username1'
    >>> settings.DB_USERNAME1 is None
    True
    >>> p2 = {'db.username':'adam'}
    >>> settings2 = Settings(properties=p2)
    >>> settings.merge(settings2)
    >>> settings.DB_USERNAME
    'root'
    >>> settings.DB_HOST
    'localhost'
    >>> settings.merge(settings2, override=True)
    >>> settings.DB_USERNAME
    'adam'
    >>> settings.DB_HOST
    'localhost'
    >>> settings.set_default('db.name', 'jamdeo')
    'jamdeo'
    >>> settings.DB_NAME
    'jamdeo'
    >>> settings.set_default('db.username', 'root1')
    'adam'
    >>> settings.DB_USERNAME
    'adam'
    """
    # def __init__(self, *args, **kwargs):
    #     super(Settings, self).__init__(*args, **kwargs)
        
    def __getattr__(self, key):
        return self.get(key)
    
    def set_property(self, key, value, override=False):
        if isinstance(value, basestring):
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.isdigit():
                value = int(value)
        super(Settings, self).set_property(key, value, override)
        super(Settings, self).set_property(key.upper().replace('.', '_'), value, override)
        
    def set_default(self, key, default=None):
        if key in self:
            return self[key]
        else:
            self.set_property(key, default, False)
            return self[key]


def get_global_settings():
    # load core properties
    global_config_file = '/srv/jamdeo-cloud/jamdeo-cloud.properties'
    return Settings(global_config_file)


def get_app_settings_from_dir(base_dir):
    # load local app properties
    local_config_file = os.path.join(base_dir, 'app.properties.local')
    local_settings = Settings(local_config_file)
    # load app properties
    app_config_file = os.path.join(base_dir, 'app.properties')
    app_settings = Settings(app_config_file)
    # override app properties with local properties
    local_settings.merge(app_settings, False)
    return local_settings


def get_app_settings():
    app_settings = []
    # load core properties first
    app_settings.append(get_app_settings_from_dir(os.path.dirname(__file__)))
    # load root app properties
    app_settings.append(get_app_settings_from_dir(get_root_dir()))
    # load sub app properties
    app_dirs = get_app_dirs()
    for app_dir in app_dirs:
        app_settings.append(get_app_settings_from_dir(app_dir))
    return app_settings


def merge_app_settings(settings):
    for app_settings in get_app_settings():
        # do not override existing properties
        settings.merge(app_settings)

settings = get_global_settings()
merge_app_settings(settings)

def get_version():
    '''if setting.VERSION is a number, setting.VERSION will be a integer,
    but if the setting.VERSION is null, it will be a string, so just wrap it
    to string in all case, it is configured to 0, just ignore it as null'''
    if settings.VERSION == None:
        return ""
    version_str = str(settings.VERSION)
    if version_str == "0":
        version_str = ""
    return version_str

if __name__ == '__main__':
    doctest.testmod()
    
