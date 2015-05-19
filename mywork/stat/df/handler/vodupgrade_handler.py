#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liupeng'
import logging

from df.datamodel.schema import SCHEMA, DATATYPE, vodupgrade, Base
from base_handler import db_handler
from df.session import engine

logger = logging.getLogger('VodUpgradeHandler')

def registerRequstHander():
    return "schema_vod_upgrade", SCHEMA.schema_vod_upgrade, VodUpgradeHandler


class VodUpgradeHandler(db_handler):
    def __init__(self, op, data_desc, session=None):
        """
    >>> from df.data_descriptor import DataDesc
    >>> desc = DataDesc()
    >>> upgrade = vodupgrade()
    >>> upgrade.toVersion = 'test004'
    >>> upgrade.fromVersion = 'test001'
    >>> upgrade.packageUrl = 'http://test/a.apk'
    >>> upgrade.message = 'test'
    >>> upgrade.customer_id = 1
    >>> upgrade.id = 1
    >>> desc.keys = {'data' : [upgrade]}
    >>> handler = VodUpgradeHandler(None, desc)
    >>> Base.metadata.create_all(engine)
    >>> handler.insert_upgrade()
    >>> data = handler.get_upgrade_by_id(customer_id=1, upgrade_id=1)
    >>> data.count()
    1
    >>> data[0].message
    u'test'
    >>> data[0].packageUrl
    u'http://test/a.apk'
    >>> data[0].toVersion
    u'test004'
    >>> desc.keys = dict(customer_id=1, upgrade_id=1, data=dict(message='change test'))
    >>> handler.data_desc = desc
    >>> handler.update_upgrade()
    >>> data = handler.get_upgrade_by_id(customer_id=1, upgrade_id=1)
    >>> data[0].message
    u'change test'
    >>> desc = DataDesc()
    >>> desc.setKey('customer', 1)
    >>> handler.data_desc = desc
    >>> data = handler.simple_query()
    >>> data[0].toVersion
    u'test004'
    """
        super(VodUpgradeHandler, self).__init__(op, data_desc, session)
        self.query_map = {DATATYPE.data_type_query_all: self.simple_query}
        self.insert_map = {DATATYPE.data_type_initialization: self.insert_upgrade}
        self.update_map = {DATATYPE.data_type_update_by_id: self.update_upgrade}

    def processUpdate(self):
        return self.execute(self.update_map)

    # def processDelete(self):
    #     return self.execute(self.delete_map)

    def processInsert(self):
        return self.execute(self.insert_map)

    def processQuery(self):
        return self.execute(self.query_map)

    def execute(self, func_map):
        if not self.data_desc.getDataType() in func_map:
            raise RuntimeError("can't find {0}".format(self.data_desc.getDataType()))
        executor = func_map[self.data_desc.getDataType()]
        try:
            return executor()
        except Exception:
            logger.exception('Db operator fails')

    def simple_query(self):
        upgrade = vodupgrade()
        kw = {}
        for k, v in self.data_desc.keys.items():
            if hasattr(upgrade, k):
                kw[k] = v

        return apply(self.session.query(vodupgrade).filter_by, (), kw).all()

    def get_upgrade_by_id(self, customer_id, upgrade_id):
        if not customer_id:
            customer_id = self.data_desc.getKey('customer_id')
        if not upgrade_id:
            upgrade_id = self.data_desc.getKey('upgrade_id')
        return self.session.query(vodupgrade).filter_by(id=upgrade_id, customer_id=customer_id)

    def get_update_by_version(self, customer_id, from_version):
        if not customer_id:
            customer_id = self.data_desc.getKey('customer_id')
        if not from_version:
            from_version = self.data_desc.getKey('from_version')
        return self.session.query(vodupgrade).filter_by(
            customer_id=customer_id,
            fromVersion=from_version)

    def update_upgrade(self):
        customer_id = self.data_desc.getKey('customer_id')
        upgrade_id = self.data_desc.getKey('upgrade_id')
        update_data = self.data_desc.getKey('data')

        for k, v in update_data.items():
            if k in ('customer_id', 'upgrade_id'):
                del update_data.k

        self.get_upgrade_by_id(customer_id, upgrade_id).update(update_data)

    def insert_upgrade(self):
        insert_data = self.data_desc.getKey('data')

        for insert in insert_data:
            self.session.add(insert)

if __name__ == '__main__':
    import doctest
    doctest.testmod()