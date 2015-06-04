#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from ..datamodel.schema import frontpage_layout
from ..datamodel.schema import frontpage_strategy
from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound
import df.data_function
from df.data_descriptor import DataDesc
import time
from core.settings import settings
from ..exceptions import NoSupportDataType
from apps.share.image_utils import genPicUrl

from base_handler import db_handler

from model_version_filter import filter_model_version
from ..datamodel.schema import model_version

def registerRequstHander():
    return "schema_frontpage", SCHEMA.schema_frontpage, frontpage_handler

def addTimestampToMedias(medias_list, timestamp):
        for media in medias_list:
            media["cached_timestamp"] = timestamp

def addTimestampToFrontpageData(frontpage):
    timestamp = int(time.time())
    addTimestampToMedias(frontpage["medias"], timestamp)
    frontpage["cached_timestamp"] = timestamp

def dataConvertion(tiles):
    ''' convert the typeCode to int anyway '''
    if tiles is None:
        return 
    for tile in tiles:
        if not isinstance(tile["typeCode"], (int, long)):
            if not tile["typeCode"] == "":
                tile["typeCode"] = int(tile["typeCode"])
            else:
                tile["typeCode"] = 0

class frontpage_handler(db_handler):
    def __init__(self,op, data_desc, session=None):
        super(frontpage_handler, self).__init__(op, data_desc, session)

    def getLayout(self, index):
        '''get the layout information from database, the layout
        information is stored as XML, use layout generation tool
        to get a json format layout, the layout information only
        contain the number of poster number and position for each
        poster
        the function also return the layout identifier information,
        which is used by VIDAA to identify which layout is used,
        since VIDAA will not care the position of each poster
        '''
        identifier, layout_info = self.session.query(frontpage_layout.params,
                                         frontpage_layout.layout_info).\
                      filter(frontpage_layout.layout_index==index).one()
        if layout_info is None:
            return None
        from layout_gen import generateFullLayoutJson
        layout =  generateFullLayoutJson(layout_info)
        #self.convertMediaType(layout)
        return identifier, layout

    def convertDate(self, day):
        seconds = (day) * 24 * 60 * 60
        return time.strftime('%Y-%m-%d', time.localtime(seconds))

    def getStrategy(self, date, model_id):
        #print "get strategy enter date is %d"%date
        #li add deleted because yuqi statitic
        strategy = self.session.query(frontpage_strategy).\
                   filter(frontpage_strategy.date == date).\
                   filter(frontpage_strategy.model_id == model_id).\
                   filter(frontpage_strategy.deleted == 0).one()
        
        return strategy

    def get_strategy_by_day(self, date):
        strategy = self.session.query(frontpage_strategy).\
                   filter(frontpage_strategy.date == date).\
                   filter(frontpage_strategy.deleted == 0).one()
        
        return strategy

    def get_preview_strategy(self, date, model_id):
        #print "get strategy enter date is %d"%date
        #li add deleted because yuqi statitic
        strategy_list = self.session.query(frontpage_strategy).\
                   filter(frontpage_strategy.date == date).\
                   filter(frontpage_strategy.model_id == model_id).\
                   filter(frontpage_strategy.deleted == 0).all()
        
        return strategy_list

    def getAllLayout(self):
        all_layout = self.session.query(frontpage_layout.layout_index).all()
        return all_layout

    def mergeLayoutAndMedias(self, layout, tiles):
        merge = []
        for element in layout["element_list"]:
            entry = element.copy()
            for tile in tiles:
                if int(element["id"]) == int(tile["index"]):
                    entry = dict(entry.items() + tile.items())
                    break
            merge.append(entry)
        return merge

#delete =0 is need
    def getAllStrategy(self, model_id):
        all_strategy = self.session.query(frontpage_strategy).\
                        filter(frontpage_strategy.deleted == 0).\
                        filter(frontpage_strategy.model_id == int(model_id)).\
                       order_by(frontpage_strategy.date).all()
        return all_strategy

    def getReloadDesc(self, schema, dataType, date, model_id):
        data_desc2 = DataDesc(schema, dataType)
        data_desc2.setKey(1, date)
        data_desc2.setKey(2, model_id)
        return data_desc2

    def processQuery(self):
        data_type = self.data_desc.getDataType()
        #print "frontpage_handler::processQuery with data_type ", data_type
        if DATATYPE.data_type_initialization == data_type:
            frontpage_info = {}
            day = self.data_desc.getKey(1)
            model_id = self.data_desc.getKey(2)
            #print "get frontpage request for day ", day
            try:
                strategy = self.getStrategy(day,model_id)
                identifier, layout = self.getLayout(strategy.layout)
                import json
                tiles = json.loads(strategy.tiles)
                merge = self.mergeLayoutAndMedias(layout, tiles)
                dataConvertion(merge)
                frontpage_info["medias"] = merge
                frontpage_info["layoutId"] = identifier
                frontpage_info["front_name"] = strategy.front_name
                frontpage_info["show_vender_log"] = strategy.show_vender_log
                addTimestampToFrontpageData(frontpage_info)
                
            except NoResultFound:
                return []
            return frontpage_info
        elif DATATYPE.data_type_all_strategy == data_type:
            model_id = self.data_desc.getKey(1)
            return self.getAllStrategy(model_id)
        elif DATATYPE.data_type_all_layout == data_type:
            return self.getAllLayout()
        elif DATATYPE.data_type_for_preview == data_type:
            day = self.data_desc.getKey(1)
            model_id = self.data_desc.getKey(2)
            return self.get_preview_strategy(day, model_id)
        else:
            raise NoSupportDataType

    def processUpdate(self):
        data_type = self.data_desc.getDataType()

        if DATATYPE.data_type_create_pic_submit == data_type:
            date = self.data_desc.getKey(1)
            layout_id = self.data_desc.getModifier("layout_id")
            details = self.data_desc.getModifier("details")
            front_name = self.data_desc.getModifier("front_name")
            model_id = self.data_desc.getModifier('model_id')
            show_vender_log = self.data_desc.getModifier('show_vender_log')
            try:
                strategy = self.getStrategy(date, model_id)
            except NoResultFound, e:
                raise e
            
            self.session.query(frontpage_strategy).\
                         filter(frontpage_strategy.date == date).\
                         filter(frontpage_strategy.model_id == model_id).\
                         update({"tiles": details, "front_name": front_name, "model_id": model_id, "show_vender_log": show_vender_log})
            self.session.commit()
            data_desc2 = self.getReloadDesc(self.data_desc.getSchema(),
                                            DATATYPE.data_type_initialization, date, model_id)
            self.add_notify_descriptor(data_desc2, "reload")
        elif DATATYPE.data_type_del_by_date == data_type:
            date = self.data_desc.getKey(1)
            model_id = self.data_desc.getKey(2)
            try:
                strategy = self.getStrategy(date, model_id)
            except NoResultFound:
                return None
            
            self.session.query(frontpage_strategy).\
                         filter(frontpage_strategy.date == date).\
                         filter(frontpage_strategy.model_id == model_id).\
                         update({"deleted": 1})
            self.session.commit()
            data_desc2 = self.getReloadDesc(self.data_desc.getSchema(),
                                            DATATYPE.data_type_initialization, date, model_id)
            self.add_notify_descriptor(data_desc2, "flush_cache")

            
    def processInsert(self):
        data_type = self.data_desc.getDataType()
        
        if DATATYPE.data_type_create_pic_submit==data_type:
            date = self.data_desc.getKey(1)
            layout_id = self.data_desc.getModifier("layout_id")
            details = self.data_desc.getModifier("details")
            front_name = self.data_desc.getModifier("front_name")
            model_id = self.data_desc.getModifier('model_id')
            show_vender_log = self.data_desc.getModifier('show_vender_log')
            found=True
            try:
                self.getStrategy(date, model_id)
            except NoResultFound:
                found = False
            if found:
                return self.processUpdate()
            
            strategy = frontpage_strategy(date=date,
                                          convert_date=self.convertDate(int(date)),
                                          tiles=details,
                                          front_name=front_name,
                                          layout=layout_id,
                                          model_id=model_id,
                                          show_vender_log=show_vender_log)
            self.session.add(strategy)
            self.session.commit()
            data_desc2 = self.getReloadDesc(self.data_desc.getSchema(),
                                            DATATYPE.data_type_initialization, date, model_id)
            self.add_notify_descriptor(data_desc2, "reload")
