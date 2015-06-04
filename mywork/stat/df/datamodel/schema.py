#!/usr/bin/env python
'''
ATTENTION: THE FILE IS GENERATED AUTOMATICLY, DO NOT MODIFIY IT MANUALLY
'''
from base import Base
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Text, SmallInteger, Float, DateTime

def enum(start=0, *sequential):
    enums = dict(zip(sequential, range(start, len(sequential)+start)))
    return type('Enum', (), enums)
    
class userDevice(Base):
    type = Column(String(64), nullable=False, index=True)
    code = Column(String(255), nullable=False, index=True)

class resource(Base):
    url = Column(String(256), nullable=False)
    type = Column(Integer, nullable=False)

class userLogin(Base):
    loginType = Column(String(16), nullable=False)
    userId = Column(Integer, nullable=False)
    loginInfo = Column(String(256), nullable=False)

class vodupgrade(Base):
    packageUrl = Column(String(256), nullable=False)
    fromVersion = Column(String(64), nullable=False)
    toVersion = Column(String(64), nullable=False)
    message = Column(String(512), nullable=False)
    packageName = Column(String(256), nullable=False)
    fileSize = Column(Integer, nullable=False)
    toVersion_name = Column(String(20), nullable=False)

class frontpage_strategy(Base):
    date = Column(Integer, nullable=False, index=True)
    tiles = Column(String(4096), nullable=True)
    layout = Column(Integer, nullable=False)
    convert_date = Column(String(64), nullable=True)
    front_name = Column(String(50), nullable=True)
    model_id = Column(Integer, nullable=True, index=True)
    show_vender_log = Column(String(50), nullable=True)

class frontpage_layout(Base):
    layout_index = Column(Integer, nullable=False, index=True)
    layout_info = Column(String(1024), nullable=True)
    params = Column(String(256), nullable=True)
    image = Column(String(512), nullable=True)

class category_manager(Base):
    category_id = Column(Integer, nullable=True, index=True)
    name = Column(String(128), nullable=False, index=True)
    category_info = Column(String(1024), nullable=True)
    provider_id = Column(Integer, nullable=True, index=True)

class category_frontpage_strategy(Base):
    navigation_id = Column(Integer, nullable=True, index=True)
    strategy_id = Column(Integer, nullable=True, index=True)
    date = Column(Integer, nullable=False, index=True)
    name = Column(String(256), nullable=True)
    tiles = Column(String(4096), nullable=True)
    layout = Column(Integer, nullable=False)
    convert_date = Column(String(64), nullable=True)
    model_id = Column(Integer, nullable=True, index=True)
    audit_result = Column(String(64), nullable=True)
    show_vender_log = Column(String(50), nullable=True)

class category_navigation(Base):
    navigation_id = Column(Integer, nullable=True, index=True)
    name = Column(String(128), nullable=False)
    sequence = Column(Integer, nullable=True)
    online = Column(Integer, nullable=True)
    model_id = Column(Integer, nullable=True, index=True)

class category_aggregation(Base):
    aggregation_id = Column(Integer, nullable=True, index=True)
    name = Column(String(128), nullable=False)
    field_name = Column(String(128), nullable=True)
    categories = Column(String(1000), nullable=True)
    provider_id = Column(Integer, nullable=True, index=True)

class topic_category(Base):
    strategy_id = Column(Integer, nullable=True, index=True)
    type_name = Column(String(256), nullable=True)
    pic_link = Column(String(1024), nullable=True)
    online = Column(Integer, nullable=True)
    summary = Column(String(1024), nullable=True)
    provider_id = Column(Integer, nullable=True, index=True)

class topic_info(Base):
    strategy_id = Column(Integer, nullable=True, index=True)
    pic_link = Column(String(1024), nullable=True)
    music_link = Column(String(1024), nullable=True)
    medias = Column(String(10240), nullable=True)

class area_apps(Base):
    app_name = Column(String(128), nullable=False)
    package_name = Column(String(1024), nullable=False)
    pic_url = Column(String(1024), nullable=False)
    media_type = Column(Integer, nullable=False, default=0)
    height = Column(Integer, nullable=False, default=0)
    width = Column(Integer, nullable=False, default=0)
    xpos = Column(Integer, nullable=False, default=0)
    ypos = Column(Integer, nullable=False, default=0)

class Basic_Vender(Base):
    name = Column(String(128), nullable=False)
    code = Column(String(128), nullable=True)
    level = Column(SmallInteger, nullable=False)
    video_play_method = Column(String(128), nullable=True)
    video_play_package = Column(String(128), nullable=True)
    video_play_param = Column(String(512), nullable=True)
    pic_link = Column(String(1024), nullable=True)
    application_package = Column(String(512), nullable=True)
    status = Column(Integer, nullable=False, default=1)
    online = Column(SmallInteger, nullable=False, default=1)
    o_application_packages = Column(String(1024), nullable=True)
    video_play_version = Column(String(1024), nullable=True)

class Basic_Media_Entertainer_Rel(Base):
    media_id = Column(BigInteger, nullable=False, index=True)
    entertainer_id = Column(BigInteger, nullable=False, index=True)
    type = Column(SmallInteger, nullable=False)

class Basic_Video_Entertainer_Rel(Base):
    video_id = Column(BigInteger, nullable=False, index=True)
    entertainer_id = Column(BigInteger, nullable=False, index=True)
    type = Column(SmallInteger, nullable=False)

class Basic_Media_Category_Rel(Base):
    media_id = Column(BigInteger, nullable=False, index=True)
    category_id = Column(BigInteger, nullable=False, index=True)

class Basic_Category(Base):
    name = Column(String(128), nullable=False)
    parent_id = Column(BigInteger, nullable=True, index=True)
    is_series = Column(SmallInteger, nullable=True)
    is_collected = Column(SmallInteger, nullable=True)

class Basic_Media(Base):
    title = Column(String(250), nullable=False, index=True)
    escape_title = Column(String(250), nullable=False, index=True)
    origin_name = Column(String(256), nullable=True)
    tag = Column(String(1024), nullable=True)
    aka = Column(String(512), nullable=True)
    summary = Column(Text, nullable=True)
    definition = Column(String(128), nullable=True)
    pubdate = Column(DateTime, nullable=True)
    rate = Column(Float, nullable=True)
    is_clip = Column(SmallInteger, nullable=True)
    is_3d = Column(SmallInteger, nullable=True, default=0)
    next_update_time = Column(String(256), nullable=True)
    available = Column(SmallInteger, nullable=False, default=1)
    online = Column(SmallInteger, nullable=False, default=0)
    season_id = Column(SmallInteger, nullable=True)
    total = Column(SmallInteger, nullable=True)
    total_season = Column(SmallInteger, nullable=True)
    current = Column(Integer, nullable=True)
    country = Column(String(256), nullable=True)
    language = Column(String(512), nullable=True)
    updatefrq = Column(String(128), nullable=True)
    image_post_url = Column(String(1024), nullable=True)
    image_icon_url = Column(String(1024), nullable=True)
    image_rec_url = Column(String(1024), nullable=True)
    default_play_source = Column(BigInteger, nullable=True)
    search_index = Column(BigInteger, nullable=True, index=True)

class Basic_Entertainer(Base):
    country = Column(String(128), nullable=True)
    origin_name = Column(String(128), nullable=True)
    stagename = Column(String(128), nullable=False, index=True)
    aka = Column(String(512), nullable=True)
    birthday = Column(String(64), nullable=True)
    biography = Column(Text, nullable=True)
    gender = Column(SmallInteger, nullable=True)
    career = Column(String(512), nullable=True)
    works = Column(Text, nullable=True)

class Basic_Video(Base):
    media_id = Column(BigInteger, nullable=False, index=True)
    title = Column(String(256), nullable=False)
    escape_title = Column(String(256), nullable=False)
    series = Column(Integer, nullable=True, index=True)
    summary = Column(Text, nullable=True)
    pubdate = Column(String(64), nullable=True)
    time_length = Column(Integer, nullable=True)
    available = Column(SmallInteger, nullable=False, default=1)
    online = Column(SmallInteger, nullable=False, default=1)
    image_post_url = Column(String(1024), nullable=True)
    image_icon_url = Column(String(1024), nullable=True)
    image_rec_url = Column(String(1024), nullable=True)

class Basic_Asset(Base):
    vender_id = Column(BigInteger, nullable=False, index=True)
    type = Column(SmallInteger, nullable=False)
    ref_id = Column(BigInteger, nullable=False, index=True)
    video_play_url = Column(String(512), nullable=True)
    video_swf_url = Column(String(512), nullable=True)
    video_m3u8_url = Column(String(512), nullable=True)
    video_quality = Column(String(128), nullable=True, index=True)
    fee = Column(SmallInteger, nullable=True)
    video_play_param = Column(String(1024), nullable=True)
    image_post_url = Column(String(1024), nullable=True)
    image_icon_url = Column(String(1024), nullable=True)
    small_image_post_url = Column(String(1024), nullable=True)
    small_image_icon_url = Column(String(1024), nullable=True)
    vender_update_time = Column(String(32), nullable=True)
    vender_category = Column(String(16), nullable=True)
    ref_source_id = Column(String(40), nullable=True, index=True)
    data_source = Column(String(200), nullable=True)
    is_only = Column(SmallInteger, nullable=True)
    available = Column(SmallInteger, nullable=False, default=1)
    online = Column(SmallInteger, nullable=False, default=1)

class Basic_UserHistory(Base):
    user_id = Column(BigInteger, nullable=False, index=True)
    media_id = Column(BigInteger, nullable=False, index=True)
    video_id = Column(BigInteger, nullable=False, index=True)
    view_duration = Column(BigInteger, nullable=False)

class Basic_UserCollect(Base):
    user_id = Column(String(128), nullable=False, index=True)
    media_id = Column(BigInteger, nullable=False, index=True)
    type = Column(SmallInteger, nullable=False)

class Basic_UserSettings(Base):
    user_id = Column(BigInteger, nullable=False, index=True)
    type = Column(String(2), nullable=True)
    item = Column(String(128), nullable=False)
    value = Column(String(256), nullable=False)

class vender_attr_mapping(Base):
    vender_id = Column(BigInteger, nullable=False, index=True)
    type = Column(String(100), nullable=False, index=True)
    self_attr_value = Column(String(256), nullable=True)
    mapping_attr_value = Column(String(256), nullable=True)

class user_center_layout(Base):
    title = Column(String(200), nullable=False)
    icon_url = Column(String(512), nullable=False)
    media_type = Column(Integer, nullable=False, default=-1)
    collect_type = Column(Integer, nullable=False, default=-1)
    width = Column(Integer, nullable=False, default=0)
    height = Column(Integer, nullable=False, default=0)
    xpos = Column(Integer, nullable=False, default=0)
    ypos = Column(Integer, nullable=False, default=0)

class video_startup(Base):
    provider_id = Column(Integer, nullable=True)
    startup_type = Column(String(512), nullable=True)
    params = Column(String(1024), nullable=True)

class oss_user(Base):
    name = Column(String(200), nullable=False)
    role = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=0)
    scope = Column(String(1024), nullable=True)
    convert_scope = Column(String(1024), nullable=True)
    staffId = Column(BigInteger, nullable=True, index=True)
    password = Column(String(1024), nullable=True)

class media_collections(Base):
    name = Column(String(200), nullable=False)
    collect_id = Column(BigInteger, nullable=False, index=True)
    medias1 = Column(String(2048), nullable=True)
    medias2 = Column(String(2048), nullable=True)
    medias3 = Column(String(2048), nullable=True)

class new7days(Base):
    category_type = Column(String(256), nullable=True)
    category_type2 = Column(String(256), nullable=True)
    type_code = Column(Integer, nullable=True, index=True)
    all_name = Column(String(256), nullable=True)
    other_name = Column(String(256), nullable=True)

class medias_update_record(Base):
    title = Column(String(250), nullable=True)
    category_name = Column(String(256), nullable=True)
    child_category_name = Column(String(1024), nullable=True)
    media_id = Column(BigInteger, nullable=False, index=True)
    actor_name = Column(String(256), nullable=True)
    director_name = Column(String(256), nullable=True)
    rate = Column(Float, nullable=True)
    play_times = Column(BigInteger, nullable=True)
    vender = Column(String(250), nullable=True)
    vender_status = Column(String(250), nullable=True)
    definition = Column(String(128), nullable=True)
    total = Column(SmallInteger, nullable=True)
    current = Column(Integer, nullable=True)
    pubdate = Column(String(64), nullable=True)
    time_length = Column(String(64), nullable=True)
    online = Column(String(64), nullable=True)
    country = Column(String(256), nullable=True)
    summary = Column(Text, nullable=True)
    image_icon_url = Column(String(1024), nullable=True)
    onoff_vender = Column(String(64), nullable=True)

class oss_preview(Base):
    mac = Column(String(256), nullable=True, index=True)
    date = Column(Integer, nullable=False, index=True)
    convert_date = Column(String(64), nullable=True)

class cpsection(Base):
    device_id = Column(String(128), nullable=False, index=True)
    is_cpsection_activated = Column(Integer, nullable=False)

class startup_bg(Base):
    startup_url = Column(String(1024), nullable=True)
    bg_url = Column(String(1024), nullable=True)
    vision_startup_url = Column(String(1024), nullable=True)
    vision_bg_url = Column(String(1024), nullable=True)
    date = Column(Integer, nullable=False, index=True)
    convert_date = Column(String(64), nullable=True)

class batch_audit_media(Base):
    taskid = Column(Integer, nullable=False, index=True)
    file_path = Column(String(1024), nullable=True)
    description = Column(String(1024), nullable=True)
    title = Column(String(250), nullable=True)
    status = Column(String(1024), nullable=True)
    complete_time = Column(Integer, nullable=True)

class monitor_data(Base):
    monitor_type = Column(String(128), nullable=False)
    total = Column(Integer, nullable=False)
    total_success = Column(Integer, nullable=False)
    total_fail = Column(Integer, nullable=False)
    success_rate = Column(Float, nullable=False)
    longest_time = Column(Integer, nullable=False)
    average_time = Column(Integer, nullable=False)
    success_average_time = Column(Integer, nullable=False)
    fail_average_time = Column(Integer, nullable=False)

class model_version(Base):
    name = Column(String(128), nullable=True)
    version = Column(String(1024), nullable=False)
    model_id = Column(Integer, nullable=False, index=True)

class feature_navigation(Base):
    provider_id = Column(Integer, nullable=True, index=True)
    name = Column(String(128), nullable=False)
    feature_navigation_id = Column(Integer, nullable=True, index=True)

class model_deviceid(Base):
    devid = Column(String(128), nullable=False)
    model = Column(String(128), nullable=False)
    devid = Column(String(128), nullable=False)
    is_4k = Column(Integer, nullable=False, index=True)

class frontpage_static_strategy(Base):
    static_file_name = Column(String(128), nullable=False)
    devid = Column(String(128), nullable=False)
    version = Column(String(128), nullable=False)

# following code is used to define the default schemas
SCHEMA = enum(1000,
    "schema_userDevice", 	# 1000
    "schema_resource", 	# 1001
    "schema_userLogin", 	# 1002
    "schema_vodupgrade", 	# 1003
    "schema_frontpage_strategy", 	# 1004
    "schema_frontpage_layout", 	# 1005
    "schema_category_manager", 	# 1006
    "schema_category_frontpage_strategy", 	# 1007
    "schema_category_navigation", 	# 1008
    "schema_category_aggregation", 	# 1009
    "schema_topic_category", 	# 1010
    "schema_topic_info", 	# 1011
    "schema_area_apps", 	# 1012
    "schema_Basic_Vender", 	# 1013
    "schema_Basic_Media_Entertainer_Rel", 	# 1014
    "schema_Basic_Video_Entertainer_Rel", 	# 1015
    "schema_Basic_Media_Category_Rel", 	# 1016
    "schema_Basic_Category", 	# 1017
    "schema_Basic_Media", 	# 1018
    "schema_Basic_Entertainer", 	# 1019
    "schema_Basic_Video", 	# 1020
    "schema_Basic_Asset", 	# 1021
    "schema_Basic_UserHistory", 	# 1022
    "schema_Basic_UserCollect", 	# 1023
    "schema_Basic_UserSettings", 	# 1024
    "schema_vender_attr_mapping", 	# 1025
    "schema_user_center_layout", 	# 1026
    "schema_video_startup", 	# 1027
    "schema_oss_user", 	# 1028
    "schema_media_collections", 	# 1029
    "schema_new7days", 	# 1030
    "schema_medias_update_record", 	# 1031
    "schema_oss_preview", 	# 1032
    "schema_cpsection", 	# 1033
    "schema_startup_bg", 	# 1034
    "schema_batch_audit_media", 	# 1035
    "schema_monitor_data", 	# 1036
    "schema_model_version", 	# 1037
    "schema_feature_navigation", 	# 1038
    "schema_model_deviceid", 	# 1039
    "schema_frontpage_static_strategy", 	# 1040
    "schema_default_end", 	# 1041,
    # following are user defined schema
    "schema_frontpage", 	# 1042
    "schema_category_frontpage", 	# 1043
    "schema_Basic_Media_model", 	# 1044
    "schema_areapps", 	# 1045
    "schema_video_manage", 	# 1046
    "schema_search", 	# 1047
    "schema_usercenter", 	# 1048
    "schema_category_management", 	# 1049
    "schema_recent_medias", 	# 1050
    "schema_topic_manage", 	# 1051
    "schema_video_startup_manage", 	# 1052
    "schema_vod_upgrade", 	# 1053
    "schema_user_device", 	# 1054
    "schema_media_collections_manage", 	# 1055
    "schema_master_view", 	# 1056
    "schema_vender", 	# 1057
    "schema_modelversion", 	# 1058
    "schema_recom", 	# 1059
    )

# following code is used to define the data type
DATATYPE = enum(2000,
    "data_type_all_by_id", 	# 2000,
    "data_type_all_by_type", 	# 2001,
    "data_type_all_by_code", 	# 2002,
    "data_type_all_by_date", 	# 2003,
    "data_type_all_by_model_id", 	# 2004,
    "data_type_all_by_layout_index", 	# 2005,
    "data_type_all_by_category_id", 	# 2006,
    "data_type_all_by_name", 	# 2007,
    "data_type_all_by_provider_id", 	# 2008,
    "data_type_all_by_navigation_id", 	# 2009,
    "data_type_all_by_strategy_id", 	# 2010,
    "data_type_all_by_aggregation_id", 	# 2011,
    "data_type_all_by_media_id", 	# 2012,
    "data_type_all_by_entertainer_id", 	# 2013,
    "data_type_all_by_video_id", 	# 2014,
    "data_type_all_by_parent_id", 	# 2015,
    "data_type_all_by_title", 	# 2016,
    "data_type_all_by_escape_title", 	# 2017,
    "data_type_all_by_search_index", 	# 2018,
    "data_type_all_by_stagename", 	# 2019,
    "data_type_all_by_series", 	# 2020,
    "data_type_all_by_vender_id", 	# 2021,
    "data_type_all_by_ref_id", 	# 2022,
    "data_type_all_by_video_quality", 	# 2023,
    "data_type_all_by_ref_source_id", 	# 2024,
    "data_type_all_by_user_id", 	# 2025,
    "data_type_all_by_staffId", 	# 2026,
    "data_type_all_by_collect_id", 	# 2027,
    "data_type_all_by_type_code", 	# 2028,
    "data_type_all_by_mac", 	# 2029,
    "data_type_all_by_device_id", 	# 2030,
    "data_type_all_by_taskid", 	# 2031,
    "data_type_all_by_feature_navigation_id", 	# 2032,
    "data_type_all_by_is_4k", 	# 2033,
    # following are user defined data type
    "data_type_query_filter", 	# 2034,
    "data_type_query_all", 	# 2035,
    "data_type_query_number_of", 	# 2036,
    "data_type_update_by_id", 	# 2037,
    "data_type_insert_record", 	# 2038,
    "data_type_del_by_id", 	# 2039,
    "data_type_initialization", 	# 2040,
    "data_type_all_strategy", 	# 2041,
    "data_type_all_layout", 	# 2042,
    "data_type_create_pic", 	# 2043,
    "data_type_create_pic_submit", 	# 2044,
    "data_type_query_by_media_id", 	# 2045,
    "data_type_query_by_video_id", 	# 2046,
    "data_type_usercenter_favorite", 	# 2047,
    "data_type_usercenter_query_favorite_index", 	# 2048,
    "data_type_usercenter_query_favorite_byuidtype", 	# 2049,
    "data_type_usercenter_query_favorite_newvideo", 	# 2050,
    "data_type_usercenter_query_updatedvideos_by_mediaids", 	# 2051,
    "data_type_usercenter_history", 	# 2052,
    "data_type_usercenter_query_history", 	# 2053,
    "data_type_usercenter_query_history_index", 	# 2054,
    "data_type_usercenter_layout", 	# 2055,
    "data_type_usercenter_query_layout", 	# 2056,
    "data_type_query_by_name", 	# 2057,
    "data_type_query_by_time", 	# 2058,
    "get_list_page_model", 	# 2059,
    "get_detail_page_model", 	# 2060,
    "get_media_by_ids", 	# 2061,
    "data_type_create_category", 	# 2062,
    "data_type_qurey_by_all_condition", 	# 2063,
    "data_type_by_type_media_id", 	# 2064,
    "data_type_count", 	# 2065,
    "data_type_query_all_media_info", 	# 2066,
    "data_type_query_pararent_category", 	# 2067,
    "data_type_all_vidio_venders", 	# 2068,
    "data_type_update_name_by_topic_id", 	# 2069,
    "data_type_update_pic_by_topic_id", 	# 2070,
    "data_type_save_topic", 	# 2071,
    "data_type_save_detail_by_topic_id", 	# 2072,
    "data_type_qurey_by_topic_condition", 	# 2073,
    "data_type_save_topic_media_info", 	# 2074,
    "data_type_query_topic_media_by_strategy", 	# 2075,
    "data_type_del_by_strategy_id", 	# 2076,
    "data_type_update_video_startup", 	# 2077,
    "get_latest_media_model", 	# 2078,
    "data_type_upd_squence", 	# 2079,
    "data_type_get_device_id_by_type", 	# 2080,
    "data_type_create_device_id_by_type", 	# 2081,
    "data_type_category_navigation_management", 	# 2082,
    "data_type_query_pinyin_cache", 	# 2083,
    "data_type_query_pinyin", 	# 2084,
    "data_type_query_t9", 	# 2085,
    "data_type_query_t9_cache", 	# 2086,
    "data_type_query_t9_cache", 	# 2087,
    "data_type_query_t9_cache", 	# 2088,
    "data_type_del_by_collect_id", 	# 2089,
    "data_type_update_by_collect_id", 	# 2090,
    "data_type_query_all_vender_list", 	# 2091,
    "data_type_query_media_by_online", 	# 2092,
    "data_type_update_basic_media", 	# 2093,
    "data_type_update_basic_asset", 	# 2094,
    "data_type_update_basic_category", 	# 2095,
    "data_type_update_basic_entertainer", 	# 2096,
    "data_type_del_by_navi_date", 	# 2097,
    "data_type_del_by_date", 	# 2098,
    "get_master_view_all_infor", 	# 2099,
    "data_type_del_by_cateogry_id", 	# 2100,
    "data_type_for_console", 	# 2101,
    "data_type_for_preview", 	# 2102,
    "data_type_all_judge_category_strategy", 	# 2103,
    "data_type_for_feature_audit_category", 	# 2104,
    "data_type_all_by_home_recommend", 	# 2105,
    "data_type_all_max_search_index", 	# 2106
    )

cache_policy = {
"%s::%s"%(SCHEMA.schema_frontpage,
             DATATYPE.data_type_initialization):3600,
"%s::%s"%(SCHEMA.schema_search,
             DATATYPE.data_type_query_pinyin_cache):14400,
"%s::%s"%(SCHEMA.schema_search,
             DATATYPE.data_type_query_all):3600,
"%s::%s"%(SCHEMA.schema_search,
             DATATYPE.data_type_query_t9_cache):7200,
"%s::%s"%(SCHEMA.schema_areapps,
             DATATYPE.data_type_query_all):0,
"%s::%s"%(SCHEMA.schema_Basic_Vender,
             DATATYPE.data_type_query_all):3600,
"%s::%s"%(SCHEMA.schema_category_frontpage,
             DATATYPE.data_type_initialization):3600,
"%s::%s"%(SCHEMA.schema_category_navigation,
             DATATYPE.data_type_query_all):3600,
"%s::%s"%(SCHEMA.schema_Basic_Media_model,
             DATATYPE.get_detail_page_model):3600,
"%s::%s"%(SCHEMA.schema_recent_medias,
             DATATYPE.data_type_query_by_time):3600,
"%s::%s"%(SCHEMA.schema_Basic_Media_model,
             DATATYPE.get_media_by_ids):3600,
"%s::%s"%(SCHEMA.schema_new7days,
             DATATYPE.data_type_all_by_type_code):3600,
"%s::%s"%(SCHEMA.schema_category_management,
             DATATYPE.data_type_query_filter):3600,
"%s::%s"%(SCHEMA.schema_search,
             DATATYPE.get_list_page_model):3600,
"%s::%s"%(SCHEMA.schema_master_view,
             DATATYPE.get_master_view_all_infor):600,
"%s::%s"%(SCHEMA.schema_startup_bg,
             DATATYPE.data_type_all_by_date):3600,
"%s::%s"%(SCHEMA.schema_media_collections,
             DATATYPE.data_type_all_by_collect_id):3600,
"%s::%s"%(SCHEMA.schema_Basic_Media_model,
             DATATYPE.get_list_page_model):3600,
"%s::%s"%(SCHEMA.schema_model_version,
             DATATYPE.data_type_query_all):3600,
"%s::%s"%(SCHEMA.schema_model_deviceid,
             DATATYPE.data_type_query_all):3600,
"%s::%s"%(SCHEMA.schema_Basic_Category,
             DATATYPE.data_type_all_by_id):3600,
"%s::%s"%(SCHEMA.schema_frontpage_static_strategy,
             DATATYPE.data_type_query_all):3600
}

def get_cache_policy(schema, data_type):
    return cache_policy.get("%s::%s"%(schema, data_type), None)