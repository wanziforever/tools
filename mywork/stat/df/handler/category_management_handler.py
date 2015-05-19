#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from ..datamodel.schema import category_manager
from ..datamodel.schema import category_aggregation
from ..datamodel.schema import category_navigation
from ..datamodel.schema import SCHEMA, DATATYPE
from sqlalchemy.orm.exc import NoResultFound
import df.data_function
from df.data_descriptor import DataDesc
from base_handler import db_handler

import logging
log = logging.getLogger(__name__)

def registerRequstHander():
    return "schema_category_management", SCHEMA.schema_category_management, \
           category_management_handler


class category_management_handler(db_handler):
    def __init__(self,op, data_desc, session=None):
        super(category_management_handler, self).__init__(op,
                                                         data_desc,
                                                         session)
        
    def processQuery(self):
        data_type = self.data_desc.getDataType()
        #print "frontpage_handler::processQuery with data_type ", data_type
        if DATATYPE.data_type_query_all == data_type:
            try:
                categories = self.session.query(category_manager).all()
            except NoResultFound:
                return None
            rows = []
            
            for category in categories:
                ids, filters = self.unPackXML(category.category_info)
                c = {"id":category.category_id,
                     "name":category.name,
                     "categories": ids.split("_"),
                     "filters": filters}
                rows.append(c)
            return rows
        elif DATATYPE.data_type_all_by_category_id == data_type:
            id = self.data_desc.getKey(1)
            try:
                category = self.session.query(category_manager).\
                           filter(category_manager.category_id==id).one()
            except NoResultFound:
                return None
            ids, filters = self.unPackXML(category.category_info)
            return {"id":category.category_id,
                    "name":category.name,
                    "categories": ids.split("_"),
                    "filters": filters}
        elif DATATYPE.data_type_all_by_id ==data_type:
            id = self.data_desc.getKey(1)
            try:
                category = self.session.query(category_manager).\
                           filter(category_manager.id==id).one()
            except NoResultFound:
                return None
            ids, filters = self.unPackXML(category.category_info)
            return {"id":category.category_id,
                    "name":category.name,
                    "categories": ids.split("_"),
                    "filters": filters}
        elif DATATYPE.data_type_query_filter == data_type:
            category_id = self.data_desc.getKey(1)
            try:
                category = self.session.query(category_manager).\
                           filter(category_manager.category_id == category_id).one()
            except NoResultFound:
                return None
            ids, filters = self.unPackXML(category.category_info)
            filters =  {"id":category.category_id,
                    "name":category.name,
                    "categories": ids.split("_"),
                    "filters": filters}

            if filters is None:
                return None

            if not filters.has_key("filters"):
                return None
        
            for filter in filters["filters"]:
                new_values = []
                for id in filter["values"]:
                    aggregation = self.session.query(category_aggregation).\
                           filter(category_aggregation.aggregation_id == id).all()
                    if len(aggregation) == 0:
                        return None
                    new_values.append([aggregation[0].name, id])
                filter["values"] = new_values
            return filters
        elif DATATYPE.data_type_all_by_provider_id == data_type:
            provider_id = self.data_desc.getKey(1)
            try:
                categories = self.session.query(category_manager).\
                            filter(category_manager.provider_id == provider_id).all()
            except NoResultFound:
                return None
            rows = []
            
            for category in categories:
                ids, filters = self.unPackXML(category.category_info)
                c = {"id":category.category_id,
                     "name":category.name,
                     "categories": ids.split("_"),
                     "filters": filters}
                rows.append(c)
            return rows  
        elif DATATYPE.data_type_all_by_navigation_id == data_type:
            navigation_id = self.data_desc.getKey(1)
            model_id = self.data_desc.getKey(2)
            try:
                navi_list = self.session.query(category_navigation).\
                           filter(category_navigation.navigation_id == navigation_id).\
                           filter(category_navigation.model_id == model_id).all()
            except NoResultFound:
                return []
            return navi_list
        else:
            log.debug("unkown data type")
            return None

    def unPackXML(self, xml_string):
        from xml.dom import minidom
        from xml.dom.minidom import getDOMImplementation, Node, Document
        #print "----", xml_string
        if len(xml_string) == 0:
            return []
        doc = minidom.parseString(xml_string.encode('utf-8'))
        filters = doc.getElementsByTagName("filter")
        ids = doc.getElementsByTagName("ids")
        
        filter_list = []
                
        for filter in filters:
            f = {}
            f["name"] = filter.getAttribute("name")
            f["field_name"] = filter.getAttribute("field_name")
            values = []
            for value in filter.childNodes:
                if len(value.childNodes) == 0:
                    continue
                values.append(value.childNodes[0].nodeValue)
            #f["values"] = ",".join(values)
            f["values"] = values
            filter_list.append(f)
        return ids[0].childNodes[0].nodeValue, filter_list
            
    def packToXML(self, categories, filters):
        from xml.dom.minidom import Document
        doc = Document()
        categories_xml = doc.createElement("categories")
        ids_xml = doc.createElement("ids")
        t = doc.createTextNode("_".join(categories))
        ids_xml.appendChild(t)
        categories_xml.appendChild(ids_xml)
        filters_xml = doc.createElement("filters")
        for filter in filters:
            filter_xml = doc.createElement("filter")
            filter_xml.setAttribute("name", filter["name"])
            filter_xml.setAttribute("field_name", filter["field_name"])
            lvl2_categories = filter["values"].split(",")
            for c in lvl2_categories:
                n = doc.createElement("value")
                t = doc.createTextNode(c)
                n.appendChild(t)
                filter_xml.appendChild(n)
            filters_xml.appendChild(filter_xml)
        categories_xml.appendChild(filters_xml)
        doc.appendChild(categories_xml)
        return doc.toxml()

    def processUpdate(self):
        #log.debug("category_management_handler process update enter")
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_update_by_id == data_type:
            category_id = self.data_desc.getKey(1)
            category_id2 = self.data_desc.getModifier("category_id2")
            filters = self.data_desc.getModifier("filters")
            categories = self.data_desc.getModifier("categories")
            category_name = self.data_desc.getModifier("category_name")
            content = self.packToXML(categories, filters)
            self.session.query(category_manager).\
                         filter(category_manager.category_id==category_id).\
                         update({"name":category_name,
                                 "category_id":category_id2,
                                 "category_info":content})
            self.session.commit()

            data_desc3 = DataDesc(SCHEMA.schema_category_management,
                             DATATYPE.data_type_query_filter)
            data_desc3.setKey(1, category_id)
            self.add_notify_descriptor(data_desc3, "reload")
            
    def processInsert(self):
        #log.debug("category_management_handler process insert enter")
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_create_category == data_type:
            # category_name = self.data_desc.getKey(1)
            category_name = self.data_desc.getModifier("category_name")
            category_id = self.data_desc.getModifier("category_id")
            filters = self.data_desc.getModifier("filters")
            categories = self.data_desc.getModifier("categories")
            provider_id = self.data_desc.getModifier("provider_id")
            content = self.packToXML(categories, filters)
            cat_mgnt = category_manager()
            cat_mgnt.name = category_name
            cat_mgnt.category_info = content
            cat_mgnt.category_id = category_id
            cat_mgnt.provider_id = provider_id
            self.session.add(cat_mgnt)
            self.session.commit()
            # cat_mgnt.category_id = cat_mgnt.id
            # self.session.merge(cat_mgnt)
            # self.session.commit()
            
    def processDelete(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_del_by_cateogry_id == data_type:
            category_id = self.data_desc.getKey(1)
            try:
                 self.session.query(category_manager).filter(category_manager.category_id == category_id).delete()
                 self.session.commit()
            except NoResultFound:
                return None