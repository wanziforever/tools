#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import settings
import os

def get_file_from_fs(path):
    return os.path.join(settings.STORE_BASE_DIR, path)

CATEGORIES = ['tv','movie','other','entertainment', 'anime']
CATEGORIE_IDS = [1001,1004,1100,1002,1005]
CATEGORIES_SEARCH = ['tv_ext', 'entertainment_ext', 'movie_ext', 'anime_ext']

def get_category_name_by_id(cat_id):
    try:
        index = CATEGORIE_IDS.index(int(cat_id))
        return  CATEGORIES[index]
    except:
        return None

def get_category_id_by_name(cat_name):
    try:
        index = CATEGORIES.index(cat_name)
        return  CATEGORIE_IDS[index]
    except:
        return None

        