#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from ..datamodel.schema import frontpage_layout
from ..datamodel.schema import category_frontpage_strategy
from ..datamodel.schema import category_navigation
from ..datamodel.schema import category_manager
from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound
import df.data_function
from df.data_descriptor import DataDesc
import time

from base_handler import db_handler
from model_version_filter import filter_model_version
from ..datamodel.schema import model_version

def registerRequstHander():
    return "schema_category_frontpage", SCHEMA.schema_category_frontpage, \
           category_frontpage_handler

def addTimestampToMedias(medias_list, timestamp):
    for media in medias_list:
        media["cached_timestamp"] = timestamp

def addTimestampToFrontpageData(frontpage):
    timestamp = int(time.time())
    addTimestampToMedias(frontpage["categories"], timestamp)
    frontpage["cached_timestamp"] = timestamp

def dataConvertion(tiles):
    ''' convert the typeCode to int anyway '''
    if tiles is None:
        return 
    for tile in tiles:
        if not isinstance(tile["typeCode"], (int, long)):
            if tile["typeCode"] == "":
                tile["typeCode"] = 0
            tile["typeCode"] = int(tile["typeCode"])

class category_frontpage_handler(db_handler):
    def __init__(self,op, data_desc, session=None):
        super(category_frontpage_handler, self).__init__(op,
                                                         data_desc,
                                                         session)
    def convertDate(self, day):
        seconds = (day) * 24 * 60 * 60
        return time.strftime('%Y-%m-%d', time.localtime(seconds))

    def getLayout(self, index):
        identifier, layout_info = self.session.query(frontpage_layout.params,
                                         frontpage_layout.layout_info).\
                      filter(frontpage_layout.layout_index==index).one()
        if layout_info is None:
            return None
        from layout_gen import generateFullLayoutJson
        layout =  generateFullLayoutJson(layout_info)
        #self.convertMediaType(layout)
        return identifier, layout

    def getStrategy(self, navi, date, model_id):
        strategy = self.session.query(category_frontpage_strategy).\
                   filter(category_frontpage_strategy.date==date,
                          category_frontpage_strategy.navigation_id==navi,
                          category_frontpage_strategy.model_id == model_id).one()
        return strategy

    def getCategoryName(self, id):
        category = self.session.query(category_manager).filter(category_manager.category_id==id).all()
        if len(category) == 0:
            return None
        return category[0].name
        
    def getAllLayout(self):
        all_layout = self.session.query(frontpage_layout.layout_index).all()
        return all_layout

    def getAllStrategy(self):
        all_strategy = self.session.query(category_frontpage_strategy).\
                       order_by(category_frontpage_strategy.date).all()
        return all_strategy

    def mergeLayoutAndCategories(self, layout, tiles):
        merge = []
        entry = {}
        for element in layout["element_list"]:
            entry = element.copy()
            for tile in tiles:
                if int(element["id"]) == int(tile["index"]):
                    entry = dict(entry.items() + tile.items())
                    break
            merge.append(entry)
        return merge
        
    def processQuery(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_all_judge_category_strategy == data_type:
            frontpage_info = {}
            date = self.data_desc.getKey(1)
            model_id = self.data_desc.getKey(2)
            try:
                strategy_list = strategy = self.session.query(category_frontpage_strategy).\
                          filter(category_frontpage_strategy.date==date,
                          category_frontpage_strategy.model_id == model_id).all()
            except NoResultFound:
                return None
            return strategy_list
        elif DATATYPE.data_type_all_by_date == data_type:
            frontpage_info = {}
            navi = self.data_desc.getKey(1)
            date = self.data_desc.getKey(2)
            model_id = self.data_desc.getKey(3)
            try:
                strategy = self.getStrategy(navi, date, model_id)
            except NoResultFound:
                return None
            return strategy
        elif DATATYPE.data_type_all_by_navigation_id == data_type:
            navi = self.data_desc.getKey(1)
            model_id = self.data_desc.getKey(2)
            strategies = self.session.query(category_frontpage_strategy).\
                         filter(category_frontpage_strategy.navigation_id==navi).\
                         filter(category_frontpage_strategy.deleted == 0).\
                         filter(category_frontpage_strategy.model_id == model_id).\
                         order_by(category_frontpage_strategy.date).all()      #deleted==0
            return strategies
        if DATATYPE.data_type_all_by_feature_navigation_id == data_type:
            navi = self.data_desc.getKey(1)
            strategies = self.session.query(category_frontpage_strategy).\
                         filter(category_frontpage_strategy.navigation_id==navi).\
                         filter(category_frontpage_strategy.deleted != 1).\
                         order_by(category_frontpage_strategy.date).all()      #deleted==0
            return strategies
        elif DATATYPE.data_type_initialization == data_type:
            # get the stategy which is put to online, if multiple records found
            # just get the first record
            navi_id = int(self.data_desc.getKey(1))
            date = int(self.data_desc.getKey(2))
            model_id = self.data_desc.getKey(3)
            frontpage_info = {}
            try:
                query = self.session.query(category_frontpage_strategy)
                query = query.filter(category_frontpage_strategy.navigation_id == navi_id)
                query = query.filter(category_frontpage_strategy.date == date)
                # li add deleted
                query = query.filter(category_frontpage_strategy.deleted == 0)
                query = query.filter(category_frontpage_strategy.model_id == int(model_id))
                strategy = query.one()
                identifier, layout = self.getLayout(strategy.layout)
                import json
                tiles = json.loads(strategy.tiles)

                merge = self.mergeLayoutAndCategories(layout, tiles)
                dataConvertion(merge)
                frontpage_info = layout
                frontpage_info.pop("element_list")
                frontpage_info["categories"] = merge
                frontpage_info["name"] = strategy.name
                frontpage_info["layoutId"] = identifier
                frontpage_info["show_vender_log"] = strategy.show_vender_log
                addTimestampToFrontpageData(frontpage_info)
            except NoResultFound:
                return []
            return frontpage_info
            
        elif DATATYPE.data_type_all_strategy == data_type:
            return self.getAllStrategy()
        elif DATATYPE.data_type_all_layout == data_type:
            return self.getAllLayout()
        else:
            return None

    def processUpdate(self):
        data_type = self.data_desc.getDataType()

        if DATATYPE.data_type_create_pic_submit==data_type:
            date = self.data_desc.getKey(1)
            navi = self.data_desc.getKey(2)
            model_id = self.data_desc.getKey(3)
            layout_id = self.data_desc.getModifier("layout_id")
            details = self.data_desc.getModifier("details")
            strategy_name = self.data_desc.getModifier("strategy_name")
            audit_result = self.data_desc.getModifier("audit_result")
            deleted = self.data_desc.getModifier("deleted")
            show_vender_log = self.data_desc.getModifier("show_vender_log")
            try:
                strategy = self.getStrategy(navi, date, model_id)
            except NoResultFound:
                return None
            if isinstance(strategy_name, unicode):
                strategy_name = strategy_name.encode('utf-8')
            #############for new requirement##########
            self.session.query(category_frontpage_strategy).\
                        filter(category_frontpage_strategy.date == date,
                               category_frontpage_strategy.navigation_id == navi,
                               category_frontpage_strategy.model_id == model_id).\
                        update({"tiles": details,
                                "name": strategy_name,
                                "model_id": model_id,
                                "audit_result": audit_result,
                                "deleted": deleted,
                                "show_vender_log": show_vender_log})
            self.session.commit()

            data_desc2 = DataDesc(SCHEMA.schema_category_frontpage,
                             DATATYPE.data_type_initialization)
            data_desc2.setKey(1, navi)
            data_desc2.setKey(2, date)
            data_desc2.setKey(3, model_id)
            self.add_notify_descriptor(data_desc2, "reload")
        elif DATATYPE.data_type_for_feature_audit_category == data_type:
            date = self.data_desc.getKey(1)
            navi = self.data_desc.getKey(2)
            deleted = self.data_desc.getModifier("deleted")
            audit_result = self.data_desc.getModifier("audit_result")
            model_id = 0
            try:
                strategy = self.getStrategy(navi, date, model_id)
            except NoResultFound:
                return None
            if isinstance(audit_result, unicode):
                audit_result = audit_result.encode('utf-8')
            #############for new requirement##########
            self.session.query(category_frontpage_strategy).\
                        filter(category_frontpage_strategy.date==date,
                               category_frontpage_strategy.navigation_id==navi).\
                        update({"deleted": deleted,
                                "audit_result": audit_result})
            self.session.commit()

            data_desc2 = DataDesc(SCHEMA.schema_category_frontpage,
                             DATATYPE.data_type_initialization)
            data_desc2.setKey(1, navi)
            data_desc2.setKey(2, date)
            data_desc2.setKey(3, model_id)
            self.add_notify_descriptor(data_desc2, "reload")
            
        elif DATATYPE.data_type_upd_squence == data_type:
            # this data_type is obsolate
            queue = self.data_desc.getModifier("queue")
            for sequence, navi_id in enumerate(queue):
                self.session.query(category_navigation).\
                             filter(category_navigation.navigation_id==navi_id).\
                             update({"sequence": sequence})
            self.session.commit()
        elif DATATYPE.data_type_category_navigation_management == data_type:
            ids = self.data_desc.getKey(1)
            names = self.data_desc.getModifier("names")
            sequences = self.data_desc.getModifier("sequences")
            onlines = self.data_desc.getModifier("onlines")
            for i in range(0, len(ids)):
                self.session.query(category_navigation).\
                             filter(category_navigation.navigation_id==ids[i]).\
                             update({"name":names[i],
                                     "sequence": sequences[i],
                                     "online": onlines[i]})
            self.session.commit()
            dsc = DataDesc(SCHEMA.schema_category_navigation, DATATYPE.data_type_query_all)
            self.add_notify_descriptor(dsc, "reload")
        elif DATATYPE.data_type_del_by_navi_date == data_type:
            navi = self.data_desc.getKey(1)
            date = self.data_desc.getKey(2)
            model_id = self.data_desc.getKey(3)
            try:
                strategy = self.getStrategy(navi, date, model_id)
            except NoResultFound:
                return None
            self.session.query(category_frontpage_strategy).\
                        filter(category_frontpage_strategy.date == date,
                               category_frontpage_strategy.navigation_id == navi,
                               category_frontpage_strategy.model_id == model_id).\
                        update({"deleted": 1})
            self.session.commit()

            data_desc4 = DataDesc(SCHEMA.schema_category_frontpage,
                             DATATYPE.data_type_initialization)
            data_desc4.setKey(1, navi)
            data_desc4.setKey(2, date)
            data_desc4.setKey(3, model_id)
            # self.add_notify_descriptor(data_desc4, "reload")
            self.add_notify_descriptor(data_desc4, "flush_cache")

            

    def processInsert(self):
        data_type = self.data_desc.getDataType()

        if DATATYPE.data_type_create_pic_submit == data_type:
            date = self.data_desc.getKey(1)
            navi = self.data_desc.getKey(2)
            model_id = self.data_desc.getKey(3)

            try:
                strategy = self.getStrategy(navi, date, model_id)
            except NoResultFound:
                strategy = None

            if strategy is not None:
                self.processUpdate()
                return
            
            layout_id = self.data_desc.getModifier("layout_id")
            details = self.data_desc.getModifier("details")
            #strategy_name = self.data_desc.getModifier("strategy_name").decode('utf-8')
            strategy_name = self.data_desc.getModifier("strategy_name")
            deleted = self.data_desc.getModifier("deleted")
            audit_result = self.data_desc.getModifier("audit_result")
            show_vender_log = self.data_desc.getModifier("show_vender_log")
            if isinstance(strategy_name, unicode):
                strategy_name = strategy_name.encode('utf-8')

            strategy = category_frontpage_strategy(date=date,
                                                   convert_date=self.convertDate(int(date)),
                                                   navigation_id=navi,
                                                   name=strategy_name,
                                                   layout=layout_id,
                                                   tiles=details,
                                                   deleted=deleted,
                                                   audit_result=audit_result,
                                                   model_id=model_id,
                                                   show_vender_log=show_vender_log)

            self.session.add(strategy)
            self.session.commit()

            data_desc3 = DataDesc(SCHEMA.schema_category_frontpage,
                             DATATYPE.data_type_initialization)
            data_desc3.setKey(1, navi)
            data_desc3.setKey(2, date)
            data_desc3.setKey(3, model_id)
            self.add_notify_descriptor(data_desc3, "reload")

        elif DATATYPE.data_type_category_navigation_management == data_type:
            ids = self.data_desc.getKey(1)
            names = self.data_desc.getModifier("names")
            sequences = self.data_desc.getModifier("sequences")
            onlines = self.data_desc.getModifier("onlines")
            for i in range(0, len(ids)):
                navi = category_navigation(name=names[i],
                                           sequence=sequences[i],
                                           online=onlines[i])
                self.session.add(navi)
                self.session.commit()
                navi.navigation_id = navi.id
                self.session.merge(navi)
                self.session.commit()
                
