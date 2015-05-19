#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, datetime
from apps import recom

from core import Application, make_app_wrappers, request
from core.cache import cache
import logging

log = logging.getLogger('MediaApi')

app = Application()
get, post = make_app_wrappers(app)

