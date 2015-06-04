# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import logging
# import fileutil
# import os
# from core.settings import settings

# logging.getLogger().setLevel(logging.INFO) # defaults to INFO level

# log_base_dir = '/var/log'

# def add_console_handler(level, format=('[%(levelname)s] %(message)s')):
#     handler = logging.StreamHandler()
#     handler.setFormatter(logging.Formatter(format))
#     logging.getLogger().addHandler(handler)
    
# def add_file_handler(file_path,
#                      level,
#                      format=('[%(asctime)s] [%(levelname)s] [%(process)d:%(threadName)s] '
#                              '[%(name)s:%(funcName)s:%(lineno)d]\n%(message)s')):
#     # create parent dir_path if not exist
#     dir_path = os.path.dirname(file_path)
#     try:
#         fileutil.create_dir_if_not_exist(dir_path)
#     except OSError, e:
#         print 'failed to create dir {0}: {1}'.format(dir_path, e.message)
#         return
    
#     # add handler
#     logger = logging.getLogger()
#     info_file_handler = logging.FileHandler(file_path)
#     info_file_handler.setLevel(level)
#     info_file_handler.setFormatter(logging.Formatter(format))
#     logger.addHandler(info_file_handler)

# def set_level(level):
#     logger = logging.getLogger()
#     logger.setLevel(level)


    
