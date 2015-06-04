#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.settings import settings
import logging

logger = logging.getLogger("measure")

lvl1 = int(settings.API_LAG_LVL1)
lvl2 = int(settings.API_LAG_LVL2)
lvl3 = int(settings.API_LAG_LVL3)
def execution_duration_measure(before, after):
    if (before > after):
        return False
    delta = (after - before).microseconds
    if delta > lvl1:
        logger.warn("OPERATION TAKE %s us, REACH THE LEVEL 1 THRESHOLD"%delta)
    elif delta < lvl1 and delta > lvl2:
        logger.info("OPERATION TAKE %s us, REACH THE LEVEL 2 THRESHOLD"%delta)
    elif delta < lvl2 and delta > lvl3:
        logger.debug("OPERATION TAKE %s us, REACH THE LEVEL 3 THRESHOLD"%delta)
    else:
        pass
    return True