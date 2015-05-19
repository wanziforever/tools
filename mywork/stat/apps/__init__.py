import os
import importlib

def get_app_names():
    dir_path = os.path.dirname(__file__)
    return [d for d in os.listdir(dir_path) 
            if os.path.isdir(os.path.join(dir_path, d)) and d != 'root']
    
def get_app_dirs():
    dir_path = os.path.dirname(__file__)
    app_names = get_app_names()
    return [ os.path.join(dir_path, app_name) for app_name in app_names ]

def get_app_dirs_dict():
    dir_path = os.path.dirname(__file__)
    app_names = get_app_names()
    return dict([(app_name, os.path.join(dir_path, app_name)) for app_name in app_names])

def get_app_base_dir():
    return os.path.dirname(__file__)

def get_root_name():
    default_root_name = 'root'
    if os.path.isdir(os.path.join(os.path.dirname(__file__), default_root_name)):
        return default_root_name
    return None

def get_root_dir():
    root_name = get_root_name()
    if root_name is None:
        return None
    return os.path.join(os.path.dirname(__file__), root_name)

