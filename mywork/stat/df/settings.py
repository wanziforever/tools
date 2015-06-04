#!/usr/bin/env python

import os
from core.settings import Settings

def loadDataSettings():
    current_dir = os.path.dirname(__file__)
    config_file = os.path.join(current_dir, 'app.properties')
    data_settings = Settings(config_file)
    return data_settings

data_settings = loadDataSettings()

