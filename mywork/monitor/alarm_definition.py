#!/usr/bin/env python

# SIMPLE: ALARM_VARIABLE = (alarmid, "alarm specific problem", "err_msg_format")

# undefined alarm
ALM_BASIC = (9999, "UNKOWN_ISSUE", "")
# system related alarm, alarmid from 10000 to 19999
ALM_NETWORK_ISSUE = (10000, "NETWORK_ISSUE", "")

# data related alarm, alarmid from 20000 to 29999
# poster related from 20000 to 20099
ALM_POSTER_IMAGE_GONE = (20000, "POSTER_IMAGE_GONE", "")

# media related from 20100 to 20199
ALM_MEDIA_OFFLINE = (20100, "MEDIA_OFFINE", "")
ALM_MEDIA_DATA_INVALID = (201001, "INVALID_MEDIA_DATA", "")
ALM_CATEGORY_HAS_BAD_MEDIAS = (201002, "CATEGORY_HAS_BAD_MEDIAS", "")



