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
from ..datamodel.schema import category_frontpage_strategy
from ..datamodel.schema import category_navigation

def registerRequstHander():
    return "schema_modelversion", SCHEMA.schema_modelversion, modelversion_handler

class modelversion_handler(db_handler):
    def __init__(self,op, data_desc, session=None):
        super(modelversion_handler, self).__init__(op, data_desc, session)

    def get_strategy(self, fmodel_id):
        strategy_list = self.session.query(frontpage_strategy).\
                   filter(frontpage_strategy.model_id == fmodel_id).\
                   filter(frontpage_strategy.deleted == 0).all()
        return strategy_list

    def get_category_strategy(self,fmodel_id):
        category_strategy_list = self.session.query(category_frontpage_strategy).\
                   filter(category_frontpage_strategy.model_id == fmodel_id).\
                   filter(category_frontpage_strategy.audit_result == '').\
                   filter(category_frontpage_strategy.deleted == 0).all()
        return category_strategy_list

    def get_category_navigation(self,fmodel_id):
        category_navigation_list = self.session.query(category_navigation).\
                   filter(category_navigation.model_id == fmodel_id).all()
        return category_navigation_list

    def insert_frontpage_strategy(self, fmodel_id, model_id):
        f_strategy_list = self.get_strategy(fmodel_id)
        for s in f_strategy_list:
            strategy = frontpage_strategy(
                             layout=s.layout,
                             tiles=s.tiles,
                             date=s.date,
                             convert_date=s.convert_date,
                             front_name=s.front_name,
                             model_id=model_id,
                             show_vender_log=s.show_vender_log)
            self.session.add(strategy)

    def insert_category_frontpage_strategy(self, fmodel_id, model_id):
        f_category_strategy_list = self.get_category_strategy(fmodel_id)
        for cs in f_category_strategy_list:
            category_stategy = category_frontpage_strategy(
                                            name=cs.name,
                                            navigation_id=cs.navigation_id,
                                            layout=cs.layout,
                                            tiles=cs.tiles,
                                            date=cs.date,
                                            convert_date=cs.convert_date,
                                            audit_result=cs.audit_result,
                                            model_id=model_id,
                                            show_vender_log=cs.show_vender_log)
            self.session.add(category_stategy)

    def insert_category_navigation(self, fmodel_id, model_id):
        category_navigation_list = self.get_category_navigation(fmodel_id)
        for cn in category_navigation_list:
            navigation = category_navigation(
                                  navigation_id=cn.navigation_id,
                                  name=cn.name,
                                  sequence=cn.sequence,
                                  online=cn.online,
                                  model_id=model_id)
            self.session.add(navigation)

    def insert_model_version(self, details):
        mversion = model_version(
                            model_id=details.get('model_id'),
                            version=details.get('version'),
                            name=details.get('name'))
        self.session.add(mversion)

    def delete_frontpage_strategy(self, model_id):
        f_strategy_list = self.get_strategy(model_id)
        for s in f_strategy_list:
            self.session.query(frontpage_strategy).filter(frontpage_strategy.id == s.id).delete()

    def delete_category_frontpage_strategy(self, model_id):
        f_category_strategy_list = self.get_category_strategy(model_id)
        for cs in f_category_strategy_list:
            self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.id == cs.id).delete()

    def delete_category_navigation(self, model_id):
        category_navigation_list = self.get_category_navigation(model_id)
        for cn in category_navigation_list:
            self.session.query(category_navigation).filter(category_navigation.id == cn.id).delete()

    def delete_model_version(self, id):
        self.session.query(model_version).filter(model_version.id == id).delete()
            
    def processInsert(self):
        data_type = self.data_desc.getDataType()
        
        if DATATYPE.data_type_insert_record==data_type:
            fmodel_id = self.data_desc.getKey(1)
            details = self.data_desc.getModifier("details")
            model_id = details.get('model_id')
            try:
                self.insert_frontpage_strategy(fmodel_id, model_id)
                self.insert_category_frontpage_strategy(fmodel_id, model_id)
                self.insert_category_navigation(fmodel_id, model_id)
                self.insert_model_version(details)
            except NoResultFound:
                return None
            self.session.commit()
            data_desc = DataDesc(SCHEMA.schema_model_version, DATATYPE.data_type_query_all)
            self.add_notify_descriptor(data_desc, "reload")

    def processDelete(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_del_by_id == data_type:
            id = self.data_desc.getKey(1)
            model_id = self.data_desc.getKey(2)
            try:
                self.delete_frontpage_strategy(model_id)
                self.delete_category_frontpage_strategy(model_id)
                self.delete_category_navigation(model_id)
                self.delete_model_version(id)
            except NoResultFound:
                return None
            self.session.commit()
            data_desc = DataDesc(SCHEMA.schema_model_version, DATATYPE.data_type_query_all)
            self.add_notify_descriptor(data_desc, "reload")