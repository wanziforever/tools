import os
import logging

from core.settings import settings
from common.log import set_level, add_console_handler, add_file_handler

log_base_dir = '/home/denny/log'

def init_log(mod, prefix):
    # since the infor level log will also print to debug level log,
    # so no need to assign the info level specified file?
    debug_log_file = os.path.join(log_base_dir, mod, '%s-debug.log' % (prefix))
    info_log_file = os.path.join(log_base_dir, mod, '%s-info.log' % (prefix))
    #info_log_file = os.path.join(log_base_dir, mod, '%s-info.log' % (prefix))
    #error_log_file = os.path.join(log_base_dir, mod, '%s-error.log' % (prefix))
    log_level = settings.LOG_LEVEL.upper()
    le = logging.getLevelName(log_level)
    # if need judge level_list = [0, 10, 20, 30, 40, 50]?
    set_level(le)

    if settings.LOG_CONSOLE is True:
        add_console_handler(logging.DEBUG)
    if le <= logging.DEBUG:
        add_file_handler(debug_log_file, logging.DEBUG, need_rotate=True)
    if le <= logging.INFO:
        add_file_handler(info_log_file, logging.INFO, need_rotate=True)
    #add_file_handler(info_log_file, logging.INFO)
    #add_file_handler(error_log_file, logging.ERROR)
