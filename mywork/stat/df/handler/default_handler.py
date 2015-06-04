#!/usr/bin/env python

from sqlalchemy.orm.exc import NoResultFound
from ..datamodel.schema import SCHEMA, DATATYPE
from base_handler import db_handler
from common.dbutil import slice_query
from ..exceptions import NoSupportDataType
from ..data_descriptor import InvalidKeyException
    
class userDevice_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(userDevice_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import userDevice
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("userDevice_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(userDevice).filter(userDevice.id==id).all()
                else:
                    q = self.session.query(userDevice).filter(userDevice.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "userDevice_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_type == data_type:
            try:
                type = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("userDevice_handler", "type")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(userDevice).filter(userDevice.type==type).all()
                else:
                    q = self.session.query(userDevice).filter(userDevice.type==type)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "userDevice_handler: no record found for data_type_all_by_type"
                raise e
    
        elif DATATYPE.data_type_all_by_code == data_type:
            try:
                code = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("userDevice_handler", "code")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(userDevice).filter(userDevice.code==code).all()
                else:
                    q = self.session.query(userDevice).filter(userDevice.code==code)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "userDevice_handler: no record found for data_type_all_by_code"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(userDevice).all()
                else:
                    q = self.session.query(userDevice)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "userDevice_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "userDevice donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import userDevice
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("userDevice_handler", "id")
            try:
                self.session.query(userDevice).filter(userDevice.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "userDevice_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import userDevice
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = userDevice(**self.data_desc.modifier)
            except:
                print "fail to initialize the userDevice instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "userDevice process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "userDevice process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import userDevice
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "userDevice_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("userDevice_handler", "id")
            try:
                ret = self.session.query(userDevice).filter(userDevice.id==id).count()
                return ret
            except NoResultFound, e:
                print "userDevice_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_type == data_type:
            try:
                type = self.data_desc.getKey(1)
            except:
                print "userDevice_handler: type parameters is required for data_type_all_bytype"
                raise InvalidKeyException("userDevice_handler", "type")
            try:
                ret = self.session.query(userDevice).filter(userDevice.type==type).count()
                return ret
            except NoResultFound, e:
                print "userDevice_handler: no record found for data_type_all_by_type"
                raise e
    
        elif DATATYPE.data_type_all_by_code == data_type:
            try:
                code = self.data_desc.getKey(1)
            except:
                print "userDevice_handler: code parameters is required for data_type_all_bycode"
                raise InvalidKeyException("userDevice_handler", "code")
            try:
                ret = self.session.query(userDevice).filter(userDevice.code==code).count()
                return ret
            except NoResultFound, e:
                print "userDevice_handler: no record found for data_type_all_by_code"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(userDevice).count()
                return ret
            except NoResultFound, e:
                print "userDevice_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "userDevice donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import userDevice
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "userDevice_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("userDevice_handler", "id")
            try:
                self.session.query(userDevice).filter(userDevice.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "userDevice_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class resource_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(resource_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import resource
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("resource_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(resource).filter(resource.id==id).all()
                else:
                    q = self.session.query(resource).filter(resource.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "resource_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(resource).all()
                else:
                    q = self.session.query(resource)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "resource_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "resource donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import resource
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("resource_handler", "id")
            try:
                self.session.query(resource).filter(resource.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "resource_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import resource
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = resource(**self.data_desc.modifier)
            except:
                print "fail to initialize the resource instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "resource process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "resource process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import resource
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "resource_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("resource_handler", "id")
            try:
                ret = self.session.query(resource).filter(resource.id==id).count()
                return ret
            except NoResultFound, e:
                print "resource_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(resource).count()
                return ret
            except NoResultFound, e:
                print "resource_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "resource donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import resource
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "resource_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("resource_handler", "id")
            try:
                self.session.query(resource).filter(resource.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "resource_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class userLogin_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(userLogin_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import userLogin
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("userLogin_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(userLogin).filter(userLogin.id==id).all()
                else:
                    q = self.session.query(userLogin).filter(userLogin.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "userLogin_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(userLogin).all()
                else:
                    q = self.session.query(userLogin)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "userLogin_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "userLogin donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import userLogin
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("userLogin_handler", "id")
            try:
                self.session.query(userLogin).filter(userLogin.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "userLogin_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import userLogin
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = userLogin(**self.data_desc.modifier)
            except:
                print "fail to initialize the userLogin instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "userLogin process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "userLogin process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import userLogin
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "userLogin_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("userLogin_handler", "id")
            try:
                ret = self.session.query(userLogin).filter(userLogin.id==id).count()
                return ret
            except NoResultFound, e:
                print "userLogin_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(userLogin).count()
                return ret
            except NoResultFound, e:
                print "userLogin_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "userLogin donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import userLogin
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "userLogin_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("userLogin_handler", "id")
            try:
                self.session.query(userLogin).filter(userLogin.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "userLogin_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class vodupgrade_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(vodupgrade_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import vodupgrade
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vodupgrade_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vodupgrade).filter(vodupgrade.id==id).all()
                else:
                    q = self.session.query(vodupgrade).filter(vodupgrade.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vodupgrade_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vodupgrade).all()
                else:
                    q = self.session.query(vodupgrade)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vodupgrade_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "vodupgrade donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import vodupgrade
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vodupgrade_handler", "id")
            try:
                self.session.query(vodupgrade).filter(vodupgrade.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "vodupgrade_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import vodupgrade
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = vodupgrade(**self.data_desc.modifier)
            except:
                print "fail to initialize the vodupgrade instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "vodupgrade process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "vodupgrade process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import vodupgrade
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "vodupgrade_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("vodupgrade_handler", "id")
            try:
                ret = self.session.query(vodupgrade).filter(vodupgrade.id==id).count()
                return ret
            except NoResultFound, e:
                print "vodupgrade_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(vodupgrade).count()
                return ret
            except NoResultFound, e:
                print "vodupgrade_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "vodupgrade donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import vodupgrade
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "vodupgrade_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("vodupgrade_handler", "id")
            try:
                self.session.query(vodupgrade).filter(vodupgrade.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "vodupgrade_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class frontpage_strategy_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(frontpage_strategy_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("frontpage_strategy_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(frontpage_strategy).filter(frontpage_strategy.id==id).all()
                else:
                    q = self.session.query(frontpage_strategy).filter(frontpage_strategy.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "frontpage_strategy_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_date == data_type:
            try:
                date = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("frontpage_strategy_handler", "date")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(frontpage_strategy).filter(frontpage_strategy.date==date).all()
                else:
                    q = self.session.query(frontpage_strategy).filter(frontpage_strategy.date==date)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "frontpage_strategy_handler: no record found for data_type_all_by_date"
                raise e
    
        elif DATATYPE.data_type_all_by_model_id == data_type:
            try:
                model_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("frontpage_strategy_handler", "model_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(frontpage_strategy).filter(frontpage_strategy.model_id==model_id).all()
                else:
                    q = self.session.query(frontpage_strategy).filter(frontpage_strategy.model_id==model_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "frontpage_strategy_handler: no record found for data_type_all_by_model_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(frontpage_strategy).all()
                else:
                    q = self.session.query(frontpage_strategy)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "frontpage_strategy_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "frontpage_strategy donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("frontpage_strategy_handler", "id")
            try:
                self.session.query(frontpage_strategy).filter(frontpage_strategy.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "frontpage_strategy_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = frontpage_strategy(**self.data_desc.modifier)
            except:
                print "fail to initialize the frontpage_strategy instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "frontpage_strategy process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "frontpage_strategy process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "frontpage_strategy_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("frontpage_strategy_handler", "id")
            try:
                ret = self.session.query(frontpage_strategy).filter(frontpage_strategy.id==id).count()
                return ret
            except NoResultFound, e:
                print "frontpage_strategy_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_date == data_type:
            try:
                date = self.data_desc.getKey(1)
            except:
                print "frontpage_strategy_handler: date parameters is required for data_type_all_bydate"
                raise InvalidKeyException("frontpage_strategy_handler", "date")
            try:
                ret = self.session.query(frontpage_strategy).filter(frontpage_strategy.date==date).count()
                return ret
            except NoResultFound, e:
                print "frontpage_strategy_handler: no record found for data_type_all_by_date"
                raise e
    
        elif DATATYPE.data_type_all_by_model_id == data_type:
            try:
                model_id = self.data_desc.getKey(1)
            except:
                print "frontpage_strategy_handler: model_id parameters is required for data_type_all_bymodel_id"
                raise InvalidKeyException("frontpage_strategy_handler", "model_id")
            try:
                ret = self.session.query(frontpage_strategy).filter(frontpage_strategy.model_id==model_id).count()
                return ret
            except NoResultFound, e:
                print "frontpage_strategy_handler: no record found for data_type_all_by_model_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(frontpage_strategy).count()
                return ret
            except NoResultFound, e:
                print "frontpage_strategy_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "frontpage_strategy donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "frontpage_strategy_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("frontpage_strategy_handler", "id")
            try:
                self.session.query(frontpage_strategy).filter(frontpage_strategy.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "frontpage_strategy_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class frontpage_layout_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(frontpage_layout_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import frontpage_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("frontpage_layout_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(frontpage_layout).filter(frontpage_layout.id==id).all()
                else:
                    q = self.session.query(frontpage_layout).filter(frontpage_layout.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "frontpage_layout_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_layout_index == data_type:
            try:
                layout_index = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("frontpage_layout_handler", "layout_index")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(frontpage_layout).filter(frontpage_layout.layout_index==layout_index).all()
                else:
                    q = self.session.query(frontpage_layout).filter(frontpage_layout.layout_index==layout_index)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "frontpage_layout_handler: no record found for data_type_all_by_layout_index"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(frontpage_layout).all()
                else:
                    q = self.session.query(frontpage_layout)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "frontpage_layout_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "frontpage_layout donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import frontpage_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("frontpage_layout_handler", "id")
            try:
                self.session.query(frontpage_layout).filter(frontpage_layout.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "frontpage_layout_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import frontpage_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = frontpage_layout(**self.data_desc.modifier)
            except:
                print "fail to initialize the frontpage_layout instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "frontpage_layout process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "frontpage_layout process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import frontpage_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "frontpage_layout_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("frontpage_layout_handler", "id")
            try:
                ret = self.session.query(frontpage_layout).filter(frontpage_layout.id==id).count()
                return ret
            except NoResultFound, e:
                print "frontpage_layout_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_layout_index == data_type:
            try:
                layout_index = self.data_desc.getKey(1)
            except:
                print "frontpage_layout_handler: layout_index parameters is required for data_type_all_bylayout_index"
                raise InvalidKeyException("frontpage_layout_handler", "layout_index")
            try:
                ret = self.session.query(frontpage_layout).filter(frontpage_layout.layout_index==layout_index).count()
                return ret
            except NoResultFound, e:
                print "frontpage_layout_handler: no record found for data_type_all_by_layout_index"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(frontpage_layout).count()
                return ret
            except NoResultFound, e:
                print "frontpage_layout_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "frontpage_layout donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import frontpage_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "frontpage_layout_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("frontpage_layout_handler", "id")
            try:
                self.session.query(frontpage_layout).filter(frontpage_layout.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "frontpage_layout_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class category_manager_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(category_manager_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import category_manager
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_manager_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_manager).filter(category_manager.id==id).all()
                else:
                    q = self.session.query(category_manager).filter(category_manager.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_category_id == data_type:
            try:
                category_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_manager_handler", "category_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_manager).filter(category_manager.category_id==category_id).all()
                else:
                    q = self.session.query(category_manager).filter(category_manager.category_id==category_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_all_by_category_id"
                raise e
    
        elif DATATYPE.data_type_all_by_name == data_type:
            try:
                name = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_manager_handler", "name")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_manager).filter(category_manager.name==name).all()
                else:
                    q = self.session.query(category_manager).filter(category_manager.name==name)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_all_by_name"
                raise e
    
        elif DATATYPE.data_type_all_by_provider_id == data_type:
            try:
                provider_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_manager_handler", "provider_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_manager).filter(category_manager.provider_id==provider_id).all()
                else:
                    q = self.session.query(category_manager).filter(category_manager.provider_id==provider_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_all_by_provider_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_manager).all()
                else:
                    q = self.session.query(category_manager)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "category_manager donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import category_manager
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_manager_handler", "id")
            try:
                self.session.query(category_manager).filter(category_manager.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "category_manager_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import category_manager
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = category_manager(**self.data_desc.modifier)
            except:
                print "fail to initialize the category_manager instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "category_manager process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "category_manager process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import category_manager
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "category_manager_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("category_manager_handler", "id")
            try:
                ret = self.session.query(category_manager).filter(category_manager.id==id).count()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_category_id == data_type:
            try:
                category_id = self.data_desc.getKey(1)
            except:
                print "category_manager_handler: category_id parameters is required for data_type_all_bycategory_id"
                raise InvalidKeyException("category_manager_handler", "category_id")
            try:
                ret = self.session.query(category_manager).filter(category_manager.category_id==category_id).count()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_all_by_category_id"
                raise e
    
        elif DATATYPE.data_type_all_by_name == data_type:
            try:
                name = self.data_desc.getKey(1)
            except:
                print "category_manager_handler: name parameters is required for data_type_all_byname"
                raise InvalidKeyException("category_manager_handler", "name")
            try:
                ret = self.session.query(category_manager).filter(category_manager.name==name).count()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_all_by_name"
                raise e
    
        elif DATATYPE.data_type_all_by_provider_id == data_type:
            try:
                provider_id = self.data_desc.getKey(1)
            except:
                print "category_manager_handler: provider_id parameters is required for data_type_all_byprovider_id"
                raise InvalidKeyException("category_manager_handler", "provider_id")
            try:
                ret = self.session.query(category_manager).filter(category_manager.provider_id==provider_id).count()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_all_by_provider_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(category_manager).count()
                return ret
            except NoResultFound, e:
                print "category_manager_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "category_manager donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import category_manager
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "category_manager_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("category_manager_handler", "id")
            try:
                self.session.query(category_manager).filter(category_manager.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "category_manager_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class category_frontpage_strategy_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(category_frontpage_strategy_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import category_frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_frontpage_strategy_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.id==id).all()
                else:
                    q = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_navigation_id == data_type:
            try:
                navigation_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_frontpage_strategy_handler", "navigation_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.navigation_id==navigation_id).all()
                else:
                    q = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.navigation_id==navigation_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_navigation_id"
                raise e
    
        elif DATATYPE.data_type_all_by_strategy_id == data_type:
            try:
                strategy_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_frontpage_strategy_handler", "strategy_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.strategy_id==strategy_id).all()
                else:
                    q = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.strategy_id==strategy_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_strategy_id"
                raise e
    
        elif DATATYPE.data_type_all_by_date == data_type:
            try:
                date = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_frontpage_strategy_handler", "date")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.date==date).all()
                else:
                    q = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.date==date)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_date"
                raise e
    
        elif DATATYPE.data_type_all_by_model_id == data_type:
            try:
                model_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_frontpage_strategy_handler", "model_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.model_id==model_id).all()
                else:
                    q = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.model_id==model_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_model_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_frontpage_strategy).all()
                else:
                    q = self.session.query(category_frontpage_strategy)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "category_frontpage_strategy donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import category_frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_frontpage_strategy_handler", "id")
            try:
                self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import category_frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = category_frontpage_strategy(**self.data_desc.modifier)
            except:
                print "fail to initialize the category_frontpage_strategy instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "category_frontpage_strategy process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "category_frontpage_strategy process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import category_frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "category_frontpage_strategy_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("category_frontpage_strategy_handler", "id")
            try:
                ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.id==id).count()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_navigation_id == data_type:
            try:
                navigation_id = self.data_desc.getKey(1)
            except:
                print "category_frontpage_strategy_handler: navigation_id parameters is required for data_type_all_bynavigation_id"
                raise InvalidKeyException("category_frontpage_strategy_handler", "navigation_id")
            try:
                ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.navigation_id==navigation_id).count()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_navigation_id"
                raise e
    
        elif DATATYPE.data_type_all_by_strategy_id == data_type:
            try:
                strategy_id = self.data_desc.getKey(1)
            except:
                print "category_frontpage_strategy_handler: strategy_id parameters is required for data_type_all_bystrategy_id"
                raise InvalidKeyException("category_frontpage_strategy_handler", "strategy_id")
            try:
                ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.strategy_id==strategy_id).count()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_strategy_id"
                raise e
    
        elif DATATYPE.data_type_all_by_date == data_type:
            try:
                date = self.data_desc.getKey(1)
            except:
                print "category_frontpage_strategy_handler: date parameters is required for data_type_all_bydate"
                raise InvalidKeyException("category_frontpage_strategy_handler", "date")
            try:
                ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.date==date).count()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_date"
                raise e
    
        elif DATATYPE.data_type_all_by_model_id == data_type:
            try:
                model_id = self.data_desc.getKey(1)
            except:
                print "category_frontpage_strategy_handler: model_id parameters is required for data_type_all_bymodel_id"
                raise InvalidKeyException("category_frontpage_strategy_handler", "model_id")
            try:
                ret = self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.model_id==model_id).count()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_model_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(category_frontpage_strategy).count()
                return ret
            except NoResultFound, e:
                print "category_frontpage_strategy_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "category_frontpage_strategy donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import category_frontpage_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "category_frontpage_strategy_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("category_frontpage_strategy_handler", "id")
            try:
                self.session.query(category_frontpage_strategy).filter(category_frontpage_strategy.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "category_frontpage_strategy_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class category_navigation_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(category_navigation_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import category_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_navigation_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_navigation).filter(category_navigation.id==id).all()
                else:
                    q = self.session.query(category_navigation).filter(category_navigation.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_navigation_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_navigation_id == data_type:
            try:
                navigation_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_navigation_handler", "navigation_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_navigation).filter(category_navigation.navigation_id==navigation_id).all()
                else:
                    q = self.session.query(category_navigation).filter(category_navigation.navigation_id==navigation_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_navigation_handler: no record found for data_type_all_by_navigation_id"
                raise e
    
        elif DATATYPE.data_type_all_by_model_id == data_type:
            try:
                model_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_navigation_handler", "model_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_navigation).filter(category_navigation.model_id==model_id).all()
                else:
                    q = self.session.query(category_navigation).filter(category_navigation.model_id==model_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_navigation_handler: no record found for data_type_all_by_model_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_navigation).all()
                else:
                    q = self.session.query(category_navigation)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_navigation_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "category_navigation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import category_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_navigation_handler", "id")
            try:
                self.session.query(category_navigation).filter(category_navigation.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "category_navigation_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import category_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = category_navigation(**self.data_desc.modifier)
            except:
                print "fail to initialize the category_navigation instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "category_navigation process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "category_navigation process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import category_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "category_navigation_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("category_navigation_handler", "id")
            try:
                ret = self.session.query(category_navigation).filter(category_navigation.id==id).count()
                return ret
            except NoResultFound, e:
                print "category_navigation_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_navigation_id == data_type:
            try:
                navigation_id = self.data_desc.getKey(1)
            except:
                print "category_navigation_handler: navigation_id parameters is required for data_type_all_bynavigation_id"
                raise InvalidKeyException("category_navigation_handler", "navigation_id")
            try:
                ret = self.session.query(category_navigation).filter(category_navigation.navigation_id==navigation_id).count()
                return ret
            except NoResultFound, e:
                print "category_navigation_handler: no record found for data_type_all_by_navigation_id"
                raise e
    
        elif DATATYPE.data_type_all_by_model_id == data_type:
            try:
                model_id = self.data_desc.getKey(1)
            except:
                print "category_navigation_handler: model_id parameters is required for data_type_all_bymodel_id"
                raise InvalidKeyException("category_navigation_handler", "model_id")
            try:
                ret = self.session.query(category_navigation).filter(category_navigation.model_id==model_id).count()
                return ret
            except NoResultFound, e:
                print "category_navigation_handler: no record found for data_type_all_by_model_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(category_navigation).count()
                return ret
            except NoResultFound, e:
                print "category_navigation_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "category_navigation donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import category_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "category_navigation_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("category_navigation_handler", "id")
            try:
                self.session.query(category_navigation).filter(category_navigation.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "category_navigation_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class category_aggregation_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(category_aggregation_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import category_aggregation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_aggregation_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_aggregation).filter(category_aggregation.id==id).all()
                else:
                    q = self.session.query(category_aggregation).filter(category_aggregation.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_aggregation_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_aggregation_id == data_type:
            try:
                aggregation_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_aggregation_handler", "aggregation_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_aggregation).filter(category_aggregation.aggregation_id==aggregation_id).all()
                else:
                    q = self.session.query(category_aggregation).filter(category_aggregation.aggregation_id==aggregation_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_aggregation_handler: no record found for data_type_all_by_aggregation_id"
                raise e
    
        elif DATATYPE.data_type_all_by_provider_id == data_type:
            try:
                provider_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_aggregation_handler", "provider_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_aggregation).filter(category_aggregation.provider_id==provider_id).all()
                else:
                    q = self.session.query(category_aggregation).filter(category_aggregation.provider_id==provider_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_aggregation_handler: no record found for data_type_all_by_provider_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(category_aggregation).all()
                else:
                    q = self.session.query(category_aggregation)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "category_aggregation_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "category_aggregation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import category_aggregation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("category_aggregation_handler", "id")
            try:
                self.session.query(category_aggregation).filter(category_aggregation.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "category_aggregation_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import category_aggregation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = category_aggregation(**self.data_desc.modifier)
            except:
                print "fail to initialize the category_aggregation instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "category_aggregation process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "category_aggregation process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import category_aggregation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "category_aggregation_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("category_aggregation_handler", "id")
            try:
                ret = self.session.query(category_aggregation).filter(category_aggregation.id==id).count()
                return ret
            except NoResultFound, e:
                print "category_aggregation_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_aggregation_id == data_type:
            try:
                aggregation_id = self.data_desc.getKey(1)
            except:
                print "category_aggregation_handler: aggregation_id parameters is required for data_type_all_byaggregation_id"
                raise InvalidKeyException("category_aggregation_handler", "aggregation_id")
            try:
                ret = self.session.query(category_aggregation).filter(category_aggregation.aggregation_id==aggregation_id).count()
                return ret
            except NoResultFound, e:
                print "category_aggregation_handler: no record found for data_type_all_by_aggregation_id"
                raise e
    
        elif DATATYPE.data_type_all_by_provider_id == data_type:
            try:
                provider_id = self.data_desc.getKey(1)
            except:
                print "category_aggregation_handler: provider_id parameters is required for data_type_all_byprovider_id"
                raise InvalidKeyException("category_aggregation_handler", "provider_id")
            try:
                ret = self.session.query(category_aggregation).filter(category_aggregation.provider_id==provider_id).count()
                return ret
            except NoResultFound, e:
                print "category_aggregation_handler: no record found for data_type_all_by_provider_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(category_aggregation).count()
                return ret
            except NoResultFound, e:
                print "category_aggregation_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "category_aggregation donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import category_aggregation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "category_aggregation_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("category_aggregation_handler", "id")
            try:
                self.session.query(category_aggregation).filter(category_aggregation.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "category_aggregation_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class topic_category_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(topic_category_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import topic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("topic_category_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(topic_category).filter(topic_category.id==id).all()
                else:
                    q = self.session.query(topic_category).filter(topic_category.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "topic_category_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_strategy_id == data_type:
            try:
                strategy_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("topic_category_handler", "strategy_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(topic_category).filter(topic_category.strategy_id==strategy_id).all()
                else:
                    q = self.session.query(topic_category).filter(topic_category.strategy_id==strategy_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "topic_category_handler: no record found for data_type_all_by_strategy_id"
                raise e
    
        elif DATATYPE.data_type_all_by_provider_id == data_type:
            try:
                provider_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("topic_category_handler", "provider_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(topic_category).filter(topic_category.provider_id==provider_id).all()
                else:
                    q = self.session.query(topic_category).filter(topic_category.provider_id==provider_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "topic_category_handler: no record found for data_type_all_by_provider_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(topic_category).all()
                else:
                    q = self.session.query(topic_category)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "topic_category_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "topic_category donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import topic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("topic_category_handler", "id")
            try:
                self.session.query(topic_category).filter(topic_category.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "topic_category_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import topic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = topic_category(**self.data_desc.modifier)
            except:
                print "fail to initialize the topic_category instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "topic_category process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "topic_category process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import topic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "topic_category_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("topic_category_handler", "id")
            try:
                ret = self.session.query(topic_category).filter(topic_category.id==id).count()
                return ret
            except NoResultFound, e:
                print "topic_category_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_strategy_id == data_type:
            try:
                strategy_id = self.data_desc.getKey(1)
            except:
                print "topic_category_handler: strategy_id parameters is required for data_type_all_bystrategy_id"
                raise InvalidKeyException("topic_category_handler", "strategy_id")
            try:
                ret = self.session.query(topic_category).filter(topic_category.strategy_id==strategy_id).count()
                return ret
            except NoResultFound, e:
                print "topic_category_handler: no record found for data_type_all_by_strategy_id"
                raise e
    
        elif DATATYPE.data_type_all_by_provider_id == data_type:
            try:
                provider_id = self.data_desc.getKey(1)
            except:
                print "topic_category_handler: provider_id parameters is required for data_type_all_byprovider_id"
                raise InvalidKeyException("topic_category_handler", "provider_id")
            try:
                ret = self.session.query(topic_category).filter(topic_category.provider_id==provider_id).count()
                return ret
            except NoResultFound, e:
                print "topic_category_handler: no record found for data_type_all_by_provider_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(topic_category).count()
                return ret
            except NoResultFound, e:
                print "topic_category_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "topic_category donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import topic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "topic_category_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("topic_category_handler", "id")
            try:
                self.session.query(topic_category).filter(topic_category.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "topic_category_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class topic_info_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(topic_info_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import topic_info
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("topic_info_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(topic_info).filter(topic_info.id==id).all()
                else:
                    q = self.session.query(topic_info).filter(topic_info.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "topic_info_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_strategy_id == data_type:
            try:
                strategy_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("topic_info_handler", "strategy_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(topic_info).filter(topic_info.strategy_id==strategy_id).all()
                else:
                    q = self.session.query(topic_info).filter(topic_info.strategy_id==strategy_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "topic_info_handler: no record found for data_type_all_by_strategy_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(topic_info).all()
                else:
                    q = self.session.query(topic_info)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "topic_info_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "topic_info donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import topic_info
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("topic_info_handler", "id")
            try:
                self.session.query(topic_info).filter(topic_info.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "topic_info_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import topic_info
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = topic_info(**self.data_desc.modifier)
            except:
                print "fail to initialize the topic_info instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "topic_info process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "topic_info process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import topic_info
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "topic_info_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("topic_info_handler", "id")
            try:
                ret = self.session.query(topic_info).filter(topic_info.id==id).count()
                return ret
            except NoResultFound, e:
                print "topic_info_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_strategy_id == data_type:
            try:
                strategy_id = self.data_desc.getKey(1)
            except:
                print "topic_info_handler: strategy_id parameters is required for data_type_all_bystrategy_id"
                raise InvalidKeyException("topic_info_handler", "strategy_id")
            try:
                ret = self.session.query(topic_info).filter(topic_info.strategy_id==strategy_id).count()
                return ret
            except NoResultFound, e:
                print "topic_info_handler: no record found for data_type_all_by_strategy_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(topic_info).count()
                return ret
            except NoResultFound, e:
                print "topic_info_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "topic_info donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import topic_info
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "topic_info_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("topic_info_handler", "id")
            try:
                self.session.query(topic_info).filter(topic_info.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "topic_info_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class area_apps_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(area_apps_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import area_apps
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("area_apps_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(area_apps).filter(area_apps.id==id).all()
                else:
                    q = self.session.query(area_apps).filter(area_apps.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "area_apps_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(area_apps).all()
                else:
                    q = self.session.query(area_apps)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "area_apps_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "area_apps donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import area_apps
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("area_apps_handler", "id")
            try:
                self.session.query(area_apps).filter(area_apps.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "area_apps_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import area_apps
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = area_apps(**self.data_desc.modifier)
            except:
                print "fail to initialize the area_apps instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "area_apps process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "area_apps process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import area_apps
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "area_apps_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("area_apps_handler", "id")
            try:
                ret = self.session.query(area_apps).filter(area_apps.id==id).count()
                return ret
            except NoResultFound, e:
                print "area_apps_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(area_apps).count()
                return ret
            except NoResultFound, e:
                print "area_apps_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "area_apps donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import area_apps
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "area_apps_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("area_apps_handler", "id")
            try:
                self.session.query(area_apps).filter(area_apps.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "area_apps_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_Vender_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_Vender_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_Vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Vender_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Vender).filter(Basic_Vender.id==id).all()
                else:
                    q = self.session.query(Basic_Vender).filter(Basic_Vender.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Vender_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Vender).all()
                else:
                    q = self.session.query(Basic_Vender)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Vender_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Vender donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_Vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Vender_handler", "id")
            try:
                self.session.query(Basic_Vender).filter(Basic_Vender.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_Vender_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_Vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_Vender(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_Vender instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_Vender process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_Vender process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_Vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Vender_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_Vender_handler", "id")
            try:
                ret = self.session.query(Basic_Vender).filter(Basic_Vender.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Vender_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_Vender).count()
                return ret
            except NoResultFound, e:
                print "Basic_Vender_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Vender donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_Vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Vender_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_Vender_handler", "id")
            try:
                self.session.query(Basic_Vender).filter(Basic_Vender.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_Vender_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_Media_Entertainer_Rel_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_Media_Entertainer_Rel_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_Media_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_Entertainer_Rel_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.id==id).all()
                else:
                    q = self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_Entertainer_Rel_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.media_id==media_id).all()
                else:
                    q = self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_entertainer_id == data_type:
            try:
                entertainer_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_Entertainer_Rel_handler", "entertainer_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.entertainer_id==entertainer_id).all()
                else:
                    q = self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.entertainer_id==entertainer_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_all_by_entertainer_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media_Entertainer_Rel).all()
                else:
                    q = self.session.query(Basic_Media_Entertainer_Rel)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Media_Entertainer_Rel donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_Media_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_Entertainer_Rel_handler", "id")
            try:
                self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_Media_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_Media_Entertainer_Rel(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_Media_Entertainer_Rel instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_Media_Entertainer_Rel process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_Media_Entertainer_Rel process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_Media_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_Entertainer_Rel_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_Media_Entertainer_Rel_handler", "id")
            try:
                ret = self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_Entertainer_Rel_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("Basic_Media_Entertainer_Rel_handler", "media_id")
            try:
                ret = self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_entertainer_id == data_type:
            try:
                entertainer_id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_Entertainer_Rel_handler: entertainer_id parameters is required for data_type_all_byentertainer_id"
                raise InvalidKeyException("Basic_Media_Entertainer_Rel_handler", "entertainer_id")
            try:
                ret = self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.entertainer_id==entertainer_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_all_by_entertainer_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_Media_Entertainer_Rel).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Media_Entertainer_Rel donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_Media_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_Entertainer_Rel_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_Media_Entertainer_Rel_handler", "id")
            try:
                self.session.query(Basic_Media_Entertainer_Rel).filter(Basic_Media_Entertainer_Rel.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_Media_Entertainer_Rel_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_Video_Entertainer_Rel_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_Video_Entertainer_Rel_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_Video_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Video_Entertainer_Rel_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.id==id).all()
                else:
                    q = self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_video_id == data_type:
            try:
                video_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Video_Entertainer_Rel_handler", "video_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.video_id==video_id).all()
                else:
                    q = self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.video_id==video_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_all_by_video_id"
                raise e
    
        elif DATATYPE.data_type_all_by_entertainer_id == data_type:
            try:
                entertainer_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Video_Entertainer_Rel_handler", "entertainer_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.entertainer_id==entertainer_id).all()
                else:
                    q = self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.entertainer_id==entertainer_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_all_by_entertainer_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Video_Entertainer_Rel).all()
                else:
                    q = self.session.query(Basic_Video_Entertainer_Rel)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Video_Entertainer_Rel donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_Video_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Video_Entertainer_Rel_handler", "id")
            try:
                self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_Video_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_Video_Entertainer_Rel(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_Video_Entertainer_Rel instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_Video_Entertainer_Rel process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_Video_Entertainer_Rel process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_Video_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Video_Entertainer_Rel_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_Video_Entertainer_Rel_handler", "id")
            try:
                ret = self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_video_id == data_type:
            try:
                video_id = self.data_desc.getKey(1)
            except:
                print "Basic_Video_Entertainer_Rel_handler: video_id parameters is required for data_type_all_byvideo_id"
                raise InvalidKeyException("Basic_Video_Entertainer_Rel_handler", "video_id")
            try:
                ret = self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.video_id==video_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_all_by_video_id"
                raise e
    
        elif DATATYPE.data_type_all_by_entertainer_id == data_type:
            try:
                entertainer_id = self.data_desc.getKey(1)
            except:
                print "Basic_Video_Entertainer_Rel_handler: entertainer_id parameters is required for data_type_all_byentertainer_id"
                raise InvalidKeyException("Basic_Video_Entertainer_Rel_handler", "entertainer_id")
            try:
                ret = self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.entertainer_id==entertainer_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_all_by_entertainer_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_Video_Entertainer_Rel).count()
                return ret
            except NoResultFound, e:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Video_Entertainer_Rel donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_Video_Entertainer_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Video_Entertainer_Rel_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_Video_Entertainer_Rel_handler", "id")
            try:
                self.session.query(Basic_Video_Entertainer_Rel).filter(Basic_Video_Entertainer_Rel.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_Video_Entertainer_Rel_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_Media_Category_Rel_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_Media_Category_Rel_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_Media_Category_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_Category_Rel_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.id==id).all()
                else:
                    q = self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_Category_Rel_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.media_id==media_id).all()
                else:
                    q = self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_category_id == data_type:
            try:
                category_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_Category_Rel_handler", "category_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.category_id==category_id).all()
                else:
                    q = self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.category_id==category_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_all_by_category_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media_Category_Rel).all()
                else:
                    q = self.session.query(Basic_Media_Category_Rel)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Media_Category_Rel donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_Media_Category_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_Category_Rel_handler", "id")
            try:
                self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_Media_Category_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_Media_Category_Rel(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_Media_Category_Rel instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_Media_Category_Rel process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_Media_Category_Rel process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_Media_Category_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_Category_Rel_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_Media_Category_Rel_handler", "id")
            try:
                ret = self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_Category_Rel_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("Basic_Media_Category_Rel_handler", "media_id")
            try:
                ret = self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_category_id == data_type:
            try:
                category_id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_Category_Rel_handler: category_id parameters is required for data_type_all_bycategory_id"
                raise InvalidKeyException("Basic_Media_Category_Rel_handler", "category_id")
            try:
                ret = self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.category_id==category_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_all_by_category_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_Media_Category_Rel).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Media_Category_Rel donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_Media_Category_Rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_Category_Rel_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_Media_Category_Rel_handler", "id")
            try:
                self.session.query(Basic_Media_Category_Rel).filter(Basic_Media_Category_Rel.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_Media_Category_Rel_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_Category_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_Category_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_Category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Category_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Category).filter(Basic_Category.id==id).all()
                else:
                    q = self.session.query(Basic_Category).filter(Basic_Category.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Category_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_parent_id == data_type:
            try:
                parent_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Category_handler", "parent_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Category).filter(Basic_Category.parent_id==parent_id).all()
                else:
                    q = self.session.query(Basic_Category).filter(Basic_Category.parent_id==parent_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Category_handler: no record found for data_type_all_by_parent_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Category).all()
                else:
                    q = self.session.query(Basic_Category)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Category_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Category donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_Category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Category_handler", "id")
            try:
                self.session.query(Basic_Category).filter(Basic_Category.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_Category_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_Category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_Category(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_Category instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_Category process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_Category process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_Category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Category_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_Category_handler", "id")
            try:
                ret = self.session.query(Basic_Category).filter(Basic_Category.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Category_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_parent_id == data_type:
            try:
                parent_id = self.data_desc.getKey(1)
            except:
                print "Basic_Category_handler: parent_id parameters is required for data_type_all_byparent_id"
                raise InvalidKeyException("Basic_Category_handler", "parent_id")
            try:
                ret = self.session.query(Basic_Category).filter(Basic_Category.parent_id==parent_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Category_handler: no record found for data_type_all_by_parent_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_Category).count()
                return ret
            except NoResultFound, e:
                print "Basic_Category_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Category donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_Category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Category_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_Category_handler", "id")
            try:
                self.session.query(Basic_Category).filter(Basic_Category.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_Category_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_Media_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_Media_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_Media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media).filter(Basic_Media.id==id).all()
                else:
                    q = self.session.query(Basic_Media).filter(Basic_Media.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_title == data_type:
            try:
                title = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_handler", "title")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media).filter(Basic_Media.title==title).all()
                else:
                    q = self.session.query(Basic_Media).filter(Basic_Media.title==title)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_all_by_title"
                raise e
    
        elif DATATYPE.data_type_all_by_escape_title == data_type:
            try:
                escape_title = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_handler", "escape_title")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media).filter(Basic_Media.escape_title==escape_title).all()
                else:
                    q = self.session.query(Basic_Media).filter(Basic_Media.escape_title==escape_title)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_all_by_escape_title"
                raise e
    
        elif DATATYPE.data_type_all_by_search_index == data_type:
            try:
                search_index = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_handler", "search_index")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media).filter(Basic_Media.search_index==search_index).all()
                else:
                    q = self.session.query(Basic_Media).filter(Basic_Media.search_index==search_index)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_all_by_search_index"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Media).all()
                else:
                    q = self.session.query(Basic_Media)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Media donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_Media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Media_handler", "id")
            try:
                self.session.query(Basic_Media).filter(Basic_Media.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_Media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_Media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_Media(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_Media instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_Media process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_Media process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_Media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_Media_handler", "id")
            try:
                ret = self.session.query(Basic_Media).filter(Basic_Media.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_title == data_type:
            try:
                title = self.data_desc.getKey(1)
            except:
                print "Basic_Media_handler: title parameters is required for data_type_all_bytitle"
                raise InvalidKeyException("Basic_Media_handler", "title")
            try:
                ret = self.session.query(Basic_Media).filter(Basic_Media.title==title).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_all_by_title"
                raise e
    
        elif DATATYPE.data_type_all_by_escape_title == data_type:
            try:
                escape_title = self.data_desc.getKey(1)
            except:
                print "Basic_Media_handler: escape_title parameters is required for data_type_all_byescape_title"
                raise InvalidKeyException("Basic_Media_handler", "escape_title")
            try:
                ret = self.session.query(Basic_Media).filter(Basic_Media.escape_title==escape_title).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_all_by_escape_title"
                raise e
    
        elif DATATYPE.data_type_all_by_search_index == data_type:
            try:
                search_index = self.data_desc.getKey(1)
            except:
                print "Basic_Media_handler: search_index parameters is required for data_type_all_bysearch_index"
                raise InvalidKeyException("Basic_Media_handler", "search_index")
            try:
                ret = self.session.query(Basic_Media).filter(Basic_Media.search_index==search_index).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_all_by_search_index"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_Media).count()
                return ret
            except NoResultFound, e:
                print "Basic_Media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Media donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_Media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Media_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_Media_handler", "id")
            try:
                self.session.query(Basic_Media).filter(Basic_Media.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_Media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_Entertainer_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_Entertainer_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_Entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Entertainer_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Entertainer).filter(Basic_Entertainer.id==id).all()
                else:
                    q = self.session.query(Basic_Entertainer).filter(Basic_Entertainer.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Entertainer_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_stagename == data_type:
            try:
                stagename = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Entertainer_handler", "stagename")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Entertainer).filter(Basic_Entertainer.stagename==stagename).all()
                else:
                    q = self.session.query(Basic_Entertainer).filter(Basic_Entertainer.stagename==stagename)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Entertainer_handler: no record found for data_type_all_by_stagename"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Entertainer).all()
                else:
                    q = self.session.query(Basic_Entertainer)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Entertainer_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Entertainer donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_Entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Entertainer_handler", "id")
            try:
                self.session.query(Basic_Entertainer).filter(Basic_Entertainer.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_Entertainer_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_Entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_Entertainer(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_Entertainer instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_Entertainer process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_Entertainer process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_Entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Entertainer_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_Entertainer_handler", "id")
            try:
                ret = self.session.query(Basic_Entertainer).filter(Basic_Entertainer.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Entertainer_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_stagename == data_type:
            try:
                stagename = self.data_desc.getKey(1)
            except:
                print "Basic_Entertainer_handler: stagename parameters is required for data_type_all_bystagename"
                raise InvalidKeyException("Basic_Entertainer_handler", "stagename")
            try:
                ret = self.session.query(Basic_Entertainer).filter(Basic_Entertainer.stagename==stagename).count()
                return ret
            except NoResultFound, e:
                print "Basic_Entertainer_handler: no record found for data_type_all_by_stagename"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_Entertainer).count()
                return ret
            except NoResultFound, e:
                print "Basic_Entertainer_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Entertainer donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_Entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Entertainer_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_Entertainer_handler", "id")
            try:
                self.session.query(Basic_Entertainer).filter(Basic_Entertainer.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_Entertainer_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_Video_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_Video_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_Video
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Video_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Video).filter(Basic_Video.id==id).all()
                else:
                    q = self.session.query(Basic_Video).filter(Basic_Video.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Video_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Video_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Video).filter(Basic_Video.media_id==media_id).all()
                else:
                    q = self.session.query(Basic_Video).filter(Basic_Video.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Video_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_series == data_type:
            try:
                series = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Video_handler", "series")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Video).filter(Basic_Video.series==series).all()
                else:
                    q = self.session.query(Basic_Video).filter(Basic_Video.series==series)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Video_handler: no record found for data_type_all_by_series"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Video).all()
                else:
                    q = self.session.query(Basic_Video)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Video_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Video donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_Video
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Video_handler", "id")
            try:
                self.session.query(Basic_Video).filter(Basic_Video.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_Video_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_Video
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_Video(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_Video instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_Video process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_Video process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_Video
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Video_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_Video_handler", "id")
            try:
                ret = self.session.query(Basic_Video).filter(Basic_Video.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Video_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "Basic_Video_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("Basic_Video_handler", "media_id")
            try:
                ret = self.session.query(Basic_Video).filter(Basic_Video.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Video_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_series == data_type:
            try:
                series = self.data_desc.getKey(1)
            except:
                print "Basic_Video_handler: series parameters is required for data_type_all_byseries"
                raise InvalidKeyException("Basic_Video_handler", "series")
            try:
                ret = self.session.query(Basic_Video).filter(Basic_Video.series==series).count()
                return ret
            except NoResultFound, e:
                print "Basic_Video_handler: no record found for data_type_all_by_series"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_Video).count()
                return ret
            except NoResultFound, e:
                print "Basic_Video_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Video donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_Video
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Video_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_Video_handler", "id")
            try:
                self.session.query(Basic_Video).filter(Basic_Video.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_Video_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_Asset_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_Asset_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_Asset
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Asset_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Asset).filter(Basic_Asset.id==id).all()
                else:
                    q = self.session.query(Basic_Asset).filter(Basic_Asset.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Asset_handler", "vender_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Asset).filter(Basic_Asset.vender_id==vender_id).all()
                else:
                    q = self.session.query(Basic_Asset).filter(Basic_Asset.vender_id==vender_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_id == data_type:
            try:
                ref_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Asset_handler", "ref_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Asset).filter(Basic_Asset.ref_id==ref_id).all()
                else:
                    q = self.session.query(Basic_Asset).filter(Basic_Asset.ref_id==ref_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_ref_id"
                raise e
    
        elif DATATYPE.data_type_all_by_video_quality == data_type:
            try:
                video_quality = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Asset_handler", "video_quality")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Asset).filter(Basic_Asset.video_quality==video_quality).all()
                else:
                    q = self.session.query(Basic_Asset).filter(Basic_Asset.video_quality==video_quality)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_video_quality"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_source_id == data_type:
            try:
                ref_source_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Asset_handler", "ref_source_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Asset).filter(Basic_Asset.ref_source_id==ref_source_id).all()
                else:
                    q = self.session.query(Basic_Asset).filter(Basic_Asset.ref_source_id==ref_source_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_ref_source_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_Asset).all()
                else:
                    q = self.session.query(Basic_Asset)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Asset donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_Asset
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_Asset_handler", "id")
            try:
                self.session.query(Basic_Asset).filter(Basic_Asset.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_Asset_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_Asset
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_Asset(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_Asset instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_Asset process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_Asset process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_Asset
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Asset_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_Asset_handler", "id")
            try:
                ret = self.session.query(Basic_Asset).filter(Basic_Asset.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                print "Basic_Asset_handler: vender_id parameters is required for data_type_all_byvender_id"
                raise InvalidKeyException("Basic_Asset_handler", "vender_id")
            try:
                ret = self.session.query(Basic_Asset).filter(Basic_Asset.vender_id==vender_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_id == data_type:
            try:
                ref_id = self.data_desc.getKey(1)
            except:
                print "Basic_Asset_handler: ref_id parameters is required for data_type_all_byref_id"
                raise InvalidKeyException("Basic_Asset_handler", "ref_id")
            try:
                ret = self.session.query(Basic_Asset).filter(Basic_Asset.ref_id==ref_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_ref_id"
                raise e
    
        elif DATATYPE.data_type_all_by_video_quality == data_type:
            try:
                video_quality = self.data_desc.getKey(1)
            except:
                print "Basic_Asset_handler: video_quality parameters is required for data_type_all_byvideo_quality"
                raise InvalidKeyException("Basic_Asset_handler", "video_quality")
            try:
                ret = self.session.query(Basic_Asset).filter(Basic_Asset.video_quality==video_quality).count()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_video_quality"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_source_id == data_type:
            try:
                ref_source_id = self.data_desc.getKey(1)
            except:
                print "Basic_Asset_handler: ref_source_id parameters is required for data_type_all_byref_source_id"
                raise InvalidKeyException("Basic_Asset_handler", "ref_source_id")
            try:
                ret = self.session.query(Basic_Asset).filter(Basic_Asset.ref_source_id==ref_source_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_all_by_ref_source_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_Asset).count()
                return ret
            except NoResultFound, e:
                print "Basic_Asset_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_Asset donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_Asset
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_Asset_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_Asset_handler", "id")
            try:
                self.session.query(Basic_Asset).filter(Basic_Asset.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_Asset_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_UserHistory_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_UserHistory_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_UserHistory
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserHistory_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.id==id).all()
                else:
                    q = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_user_id == data_type:
            try:
                user_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserHistory_handler", "user_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.user_id==user_id).all()
                else:
                    q = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.user_id==user_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_user_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserHistory_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.media_id==media_id).all()
                else:
                    q = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_video_id == data_type:
            try:
                video_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserHistory_handler", "video_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.video_id==video_id).all()
                else:
                    q = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.video_id==video_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_video_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserHistory).all()
                else:
                    q = self.session.query(Basic_UserHistory)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_UserHistory donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_UserHistory
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserHistory_handler", "id")
            try:
                self.session.query(Basic_UserHistory).filter(Basic_UserHistory.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_UserHistory
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_UserHistory(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_UserHistory instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_UserHistory process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_UserHistory process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_UserHistory
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_UserHistory_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_UserHistory_handler", "id")
            try:
                ret = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_user_id == data_type:
            try:
                user_id = self.data_desc.getKey(1)
            except:
                print "Basic_UserHistory_handler: user_id parameters is required for data_type_all_byuser_id"
                raise InvalidKeyException("Basic_UserHistory_handler", "user_id")
            try:
                ret = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.user_id==user_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_user_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "Basic_UserHistory_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("Basic_UserHistory_handler", "media_id")
            try:
                ret = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_video_id == data_type:
            try:
                video_id = self.data_desc.getKey(1)
            except:
                print "Basic_UserHistory_handler: video_id parameters is required for data_type_all_byvideo_id"
                raise InvalidKeyException("Basic_UserHistory_handler", "video_id")
            try:
                ret = self.session.query(Basic_UserHistory).filter(Basic_UserHistory.video_id==video_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_video_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_UserHistory).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserHistory_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_UserHistory donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_UserHistory
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_UserHistory_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_UserHistory_handler", "id")
            try:
                self.session.query(Basic_UserHistory).filter(Basic_UserHistory.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_UserHistory_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_UserCollect_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_UserCollect_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_UserCollect
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserCollect_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserCollect).filter(Basic_UserCollect.id==id).all()
                else:
                    q = self.session.query(Basic_UserCollect).filter(Basic_UserCollect.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserCollect_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_user_id == data_type:
            try:
                user_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserCollect_handler", "user_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserCollect).filter(Basic_UserCollect.user_id==user_id).all()
                else:
                    q = self.session.query(Basic_UserCollect).filter(Basic_UserCollect.user_id==user_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserCollect_handler: no record found for data_type_all_by_user_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserCollect_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserCollect).filter(Basic_UserCollect.media_id==media_id).all()
                else:
                    q = self.session.query(Basic_UserCollect).filter(Basic_UserCollect.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserCollect_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserCollect).all()
                else:
                    q = self.session.query(Basic_UserCollect)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserCollect_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_UserCollect donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_UserCollect
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserCollect_handler", "id")
            try:
                self.session.query(Basic_UserCollect).filter(Basic_UserCollect.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_UserCollect_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_UserCollect
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_UserCollect(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_UserCollect instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_UserCollect process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_UserCollect process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_UserCollect
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_UserCollect_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_UserCollect_handler", "id")
            try:
                ret = self.session.query(Basic_UserCollect).filter(Basic_UserCollect.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserCollect_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_user_id == data_type:
            try:
                user_id = self.data_desc.getKey(1)
            except:
                print "Basic_UserCollect_handler: user_id parameters is required for data_type_all_byuser_id"
                raise InvalidKeyException("Basic_UserCollect_handler", "user_id")
            try:
                ret = self.session.query(Basic_UserCollect).filter(Basic_UserCollect.user_id==user_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserCollect_handler: no record found for data_type_all_by_user_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "Basic_UserCollect_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("Basic_UserCollect_handler", "media_id")
            try:
                ret = self.session.query(Basic_UserCollect).filter(Basic_UserCollect.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserCollect_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_UserCollect).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserCollect_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_UserCollect donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_UserCollect
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_UserCollect_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_UserCollect_handler", "id")
            try:
                self.session.query(Basic_UserCollect).filter(Basic_UserCollect.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_UserCollect_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class Basic_UserSettings_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(Basic_UserSettings_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import Basic_UserSettings
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserSettings_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserSettings).filter(Basic_UserSettings.id==id).all()
                else:
                    q = self.session.query(Basic_UserSettings).filter(Basic_UserSettings.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserSettings_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_user_id == data_type:
            try:
                user_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserSettings_handler", "user_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserSettings).filter(Basic_UserSettings.user_id==user_id).all()
                else:
                    q = self.session.query(Basic_UserSettings).filter(Basic_UserSettings.user_id==user_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserSettings_handler: no record found for data_type_all_by_user_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(Basic_UserSettings).all()
                else:
                    q = self.session.query(Basic_UserSettings)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "Basic_UserSettings_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_UserSettings donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import Basic_UserSettings
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("Basic_UserSettings_handler", "id")
            try:
                self.session.query(Basic_UserSettings).filter(Basic_UserSettings.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "Basic_UserSettings_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import Basic_UserSettings
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = Basic_UserSettings(**self.data_desc.modifier)
            except:
                print "fail to initialize the Basic_UserSettings instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "Basic_UserSettings process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "Basic_UserSettings process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import Basic_UserSettings
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_UserSettings_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("Basic_UserSettings_handler", "id")
            try:
                ret = self.session.query(Basic_UserSettings).filter(Basic_UserSettings.id==id).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserSettings_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_user_id == data_type:
            try:
                user_id = self.data_desc.getKey(1)
            except:
                print "Basic_UserSettings_handler: user_id parameters is required for data_type_all_byuser_id"
                raise InvalidKeyException("Basic_UserSettings_handler", "user_id")
            try:
                ret = self.session.query(Basic_UserSettings).filter(Basic_UserSettings.user_id==user_id).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserSettings_handler: no record found for data_type_all_by_user_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(Basic_UserSettings).count()
                return ret
            except NoResultFound, e:
                print "Basic_UserSettings_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "Basic_UserSettings donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import Basic_UserSettings
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "Basic_UserSettings_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("Basic_UserSettings_handler", "id")
            try:
                self.session.query(Basic_UserSettings).filter(Basic_UserSettings.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "Basic_UserSettings_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class vender_attr_mapping_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(vender_attr_mapping_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vender_attr_mapping_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id).all()
                else:
                    q = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vender_attr_mapping_handler", "vender_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.vender_id==vender_id).all()
                else:
                    q = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.vender_id==vender_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_type == data_type:
            try:
                type = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vender_attr_mapping_handler", "type")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.type==type).all()
                else:
                    q = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.type==type)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_type"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vender_attr_mapping).all()
                else:
                    q = self.session.query(vender_attr_mapping)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "vender_attr_mapping donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vender_attr_mapping_handler", "id")
            try:
                self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = vender_attr_mapping(**self.data_desc.modifier)
            except:
                print "fail to initialize the vender_attr_mapping instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "vender_attr_mapping process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "vender_attr_mapping process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "vender_attr_mapping_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("vender_attr_mapping_handler", "id")
            try:
                ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id).count()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                print "vender_attr_mapping_handler: vender_id parameters is required for data_type_all_byvender_id"
                raise InvalidKeyException("vender_attr_mapping_handler", "vender_id")
            try:
                ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.vender_id==vender_id).count()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_type == data_type:
            try:
                type = self.data_desc.getKey(1)
            except:
                print "vender_attr_mapping_handler: type parameters is required for data_type_all_bytype"
                raise InvalidKeyException("vender_attr_mapping_handler", "type")
            try:
                ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.type==type).count()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_type"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(vender_attr_mapping).count()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "vender_attr_mapping donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "vender_attr_mapping_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("vender_attr_mapping_handler", "id")
            try:
                self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class user_center_layout_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(user_center_layout_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import user_center_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("user_center_layout_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(user_center_layout).filter(user_center_layout.id==id).all()
                else:
                    q = self.session.query(user_center_layout).filter(user_center_layout.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "user_center_layout_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(user_center_layout).all()
                else:
                    q = self.session.query(user_center_layout)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "user_center_layout_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "user_center_layout donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import user_center_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("user_center_layout_handler", "id")
            try:
                self.session.query(user_center_layout).filter(user_center_layout.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "user_center_layout_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import user_center_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = user_center_layout(**self.data_desc.modifier)
            except:
                print "fail to initialize the user_center_layout instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "user_center_layout process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "user_center_layout process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import user_center_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "user_center_layout_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("user_center_layout_handler", "id")
            try:
                ret = self.session.query(user_center_layout).filter(user_center_layout.id==id).count()
                return ret
            except NoResultFound, e:
                print "user_center_layout_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(user_center_layout).count()
                return ret
            except NoResultFound, e:
                print "user_center_layout_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "user_center_layout donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import user_center_layout
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "user_center_layout_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("user_center_layout_handler", "id")
            try:
                self.session.query(user_center_layout).filter(user_center_layout.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "user_center_layout_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class video_startup_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(video_startup_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import video_startup
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("video_startup_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(video_startup).filter(video_startup.id==id).all()
                else:
                    q = self.session.query(video_startup).filter(video_startup.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "video_startup_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(video_startup).all()
                else:
                    q = self.session.query(video_startup)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "video_startup_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "video_startup donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import video_startup
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("video_startup_handler", "id")
            try:
                self.session.query(video_startup).filter(video_startup.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "video_startup_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import video_startup
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = video_startup(**self.data_desc.modifier)
            except:
                print "fail to initialize the video_startup instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "video_startup process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "video_startup process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import video_startup
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "video_startup_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("video_startup_handler", "id")
            try:
                ret = self.session.query(video_startup).filter(video_startup.id==id).count()
                return ret
            except NoResultFound, e:
                print "video_startup_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(video_startup).count()
                return ret
            except NoResultFound, e:
                print "video_startup_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "video_startup donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import video_startup
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "video_startup_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("video_startup_handler", "id")
            try:
                self.session.query(video_startup).filter(video_startup.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "video_startup_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class oss_user_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(oss_user_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_user_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_user).filter(oss_user.id==id).all()
                else:
                    q = self.session.query(oss_user).filter(oss_user.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_staffId == data_type:
            try:
                staffId = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_user_handler", "staffId")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_user).filter(oss_user.staffId==staffId).all()
                else:
                    q = self.session.query(oss_user).filter(oss_user.staffId==staffId)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_all_by_staffId"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_user).all()
                else:
                    q = self.session.query(oss_user)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "oss_user donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_user_handler", "id")
            try:
                self.session.query(oss_user).filter(oss_user.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "oss_user_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = oss_user(**self.data_desc.modifier)
            except:
                print "fail to initialize the oss_user instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "oss_user process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "oss_user process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "oss_user_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("oss_user_handler", "id")
            try:
                ret = self.session.query(oss_user).filter(oss_user.id==id).count()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_staffId == data_type:
            try:
                staffId = self.data_desc.getKey(1)
            except:
                print "oss_user_handler: staffId parameters is required for data_type_all_bystaffId"
                raise InvalidKeyException("oss_user_handler", "staffId")
            try:
                ret = self.session.query(oss_user).filter(oss_user.staffId==staffId).count()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_all_by_staffId"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(oss_user).count()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "oss_user donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "oss_user_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("oss_user_handler", "id")
            try:
                self.session.query(oss_user).filter(oss_user.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "oss_user_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class media_collections_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(media_collections_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import media_collections
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("media_collections_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(media_collections).filter(media_collections.id==id).all()
                else:
                    q = self.session.query(media_collections).filter(media_collections.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "media_collections_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_collect_id == data_type:
            try:
                collect_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("media_collections_handler", "collect_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(media_collections).filter(media_collections.collect_id==collect_id).all()
                else:
                    q = self.session.query(media_collections).filter(media_collections.collect_id==collect_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "media_collections_handler: no record found for data_type_all_by_collect_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(media_collections).all()
                else:
                    q = self.session.query(media_collections)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "media_collections_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "media_collections donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import media_collections
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("media_collections_handler", "id")
            try:
                self.session.query(media_collections).filter(media_collections.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "media_collections_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import media_collections
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = media_collections(**self.data_desc.modifier)
            except:
                print "fail to initialize the media_collections instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "media_collections process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "media_collections process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import media_collections
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "media_collections_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("media_collections_handler", "id")
            try:
                ret = self.session.query(media_collections).filter(media_collections.id==id).count()
                return ret
            except NoResultFound, e:
                print "media_collections_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_collect_id == data_type:
            try:
                collect_id = self.data_desc.getKey(1)
            except:
                print "media_collections_handler: collect_id parameters is required for data_type_all_bycollect_id"
                raise InvalidKeyException("media_collections_handler", "collect_id")
            try:
                ret = self.session.query(media_collections).filter(media_collections.collect_id==collect_id).count()
                return ret
            except NoResultFound, e:
                print "media_collections_handler: no record found for data_type_all_by_collect_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(media_collections).count()
                return ret
            except NoResultFound, e:
                print "media_collections_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "media_collections donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import media_collections
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "media_collections_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("media_collections_handler", "id")
            try:
                self.session.query(media_collections).filter(media_collections.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "media_collections_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class new7days_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(new7days_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import new7days
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("new7days_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(new7days).filter(new7days.id==id).all()
                else:
                    q = self.session.query(new7days).filter(new7days.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "new7days_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_type_code == data_type:
            try:
                type_code = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("new7days_handler", "type_code")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(new7days).filter(new7days.type_code==type_code).all()
                else:
                    q = self.session.query(new7days).filter(new7days.type_code==type_code)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "new7days_handler: no record found for data_type_all_by_type_code"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(new7days).all()
                else:
                    q = self.session.query(new7days)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "new7days_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "new7days donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import new7days
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("new7days_handler", "id")
            try:
                self.session.query(new7days).filter(new7days.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "new7days_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import new7days
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = new7days(**self.data_desc.modifier)
            except:
                print "fail to initialize the new7days instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "new7days process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "new7days process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import new7days
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "new7days_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("new7days_handler", "id")
            try:
                ret = self.session.query(new7days).filter(new7days.id==id).count()
                return ret
            except NoResultFound, e:
                print "new7days_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_type_code == data_type:
            try:
                type_code = self.data_desc.getKey(1)
            except:
                print "new7days_handler: type_code parameters is required for data_type_all_bytype_code"
                raise InvalidKeyException("new7days_handler", "type_code")
            try:
                ret = self.session.query(new7days).filter(new7days.type_code==type_code).count()
                return ret
            except NoResultFound, e:
                print "new7days_handler: no record found for data_type_all_by_type_code"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(new7days).count()
                return ret
            except NoResultFound, e:
                print "new7days_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "new7days donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import new7days
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "new7days_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("new7days_handler", "id")
            try:
                self.session.query(new7days).filter(new7days.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "new7days_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class medias_update_record_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(medias_update_record_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("medias_update_record_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(medias_update_record).filter(medias_update_record.id==id).all()
                else:
                    q = self.session.query(medias_update_record).filter(medias_update_record.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("medias_update_record_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(medias_update_record).filter(medias_update_record.media_id==media_id).all()
                else:
                    q = self.session.query(medias_update_record).filter(medias_update_record.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(medias_update_record).all()
                else:
                    q = self.session.query(medias_update_record)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "medias_update_record donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("medias_update_record_handler", "id")
            try:
                self.session.query(medias_update_record).filter(medias_update_record.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "medias_update_record_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = medias_update_record(**self.data_desc.modifier)
            except:
                print "fail to initialize the medias_update_record instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "medias_update_record process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "medias_update_record process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "medias_update_record_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("medias_update_record_handler", "id")
            try:
                ret = self.session.query(medias_update_record).filter(medias_update_record.id==id).count()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "medias_update_record_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("medias_update_record_handler", "media_id")
            try:
                ret = self.session.query(medias_update_record).filter(medias_update_record.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(medias_update_record).count()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "medias_update_record donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "medias_update_record_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("medias_update_record_handler", "id")
            try:
                self.session.query(medias_update_record).filter(medias_update_record.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "medias_update_record_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class oss_preview_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(oss_preview_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import oss_preview
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_preview_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_preview).filter(oss_preview.id==id).all()
                else:
                    q = self.session.query(oss_preview).filter(oss_preview.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_preview_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_mac == data_type:
            try:
                mac = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_preview_handler", "mac")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_preview).filter(oss_preview.mac==mac).all()
                else:
                    q = self.session.query(oss_preview).filter(oss_preview.mac==mac)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_preview_handler: no record found for data_type_all_by_mac"
                raise e
    
        elif DATATYPE.data_type_all_by_date == data_type:
            try:
                date = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_preview_handler", "date")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_preview).filter(oss_preview.date==date).all()
                else:
                    q = self.session.query(oss_preview).filter(oss_preview.date==date)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_preview_handler: no record found for data_type_all_by_date"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_preview).all()
                else:
                    q = self.session.query(oss_preview)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_preview_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "oss_preview donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import oss_preview
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_preview_handler", "id")
            try:
                self.session.query(oss_preview).filter(oss_preview.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "oss_preview_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import oss_preview
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = oss_preview(**self.data_desc.modifier)
            except:
                print "fail to initialize the oss_preview instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "oss_preview process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "oss_preview process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import oss_preview
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "oss_preview_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("oss_preview_handler", "id")
            try:
                ret = self.session.query(oss_preview).filter(oss_preview.id==id).count()
                return ret
            except NoResultFound, e:
                print "oss_preview_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_mac == data_type:
            try:
                mac = self.data_desc.getKey(1)
            except:
                print "oss_preview_handler: mac parameters is required for data_type_all_bymac"
                raise InvalidKeyException("oss_preview_handler", "mac")
            try:
                ret = self.session.query(oss_preview).filter(oss_preview.mac==mac).count()
                return ret
            except NoResultFound, e:
                print "oss_preview_handler: no record found for data_type_all_by_mac"
                raise e
    
        elif DATATYPE.data_type_all_by_date == data_type:
            try:
                date = self.data_desc.getKey(1)
            except:
                print "oss_preview_handler: date parameters is required for data_type_all_bydate"
                raise InvalidKeyException("oss_preview_handler", "date")
            try:
                ret = self.session.query(oss_preview).filter(oss_preview.date==date).count()
                return ret
            except NoResultFound, e:
                print "oss_preview_handler: no record found for data_type_all_by_date"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(oss_preview).count()
                return ret
            except NoResultFound, e:
                print "oss_preview_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "oss_preview donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import oss_preview
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "oss_preview_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("oss_preview_handler", "id")
            try:
                self.session.query(oss_preview).filter(oss_preview.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "oss_preview_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class cpsection_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(cpsection_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import cpsection
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("cpsection_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(cpsection).filter(cpsection.id==id).all()
                else:
                    q = self.session.query(cpsection).filter(cpsection.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "cpsection_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_device_id == data_type:
            try:
                device_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("cpsection_handler", "device_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(cpsection).filter(cpsection.device_id==device_id).all()
                else:
                    q = self.session.query(cpsection).filter(cpsection.device_id==device_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "cpsection_handler: no record found for data_type_all_by_device_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(cpsection).all()
                else:
                    q = self.session.query(cpsection)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "cpsection_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "cpsection donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import cpsection
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("cpsection_handler", "id")
            try:
                self.session.query(cpsection).filter(cpsection.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "cpsection_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import cpsection
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = cpsection(**self.data_desc.modifier)
            except:
                print "fail to initialize the cpsection instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "cpsection process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "cpsection process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import cpsection
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "cpsection_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("cpsection_handler", "id")
            try:
                ret = self.session.query(cpsection).filter(cpsection.id==id).count()
                return ret
            except NoResultFound, e:
                print "cpsection_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_device_id == data_type:
            try:
                device_id = self.data_desc.getKey(1)
            except:
                print "cpsection_handler: device_id parameters is required for data_type_all_bydevice_id"
                raise InvalidKeyException("cpsection_handler", "device_id")
            try:
                ret = self.session.query(cpsection).filter(cpsection.device_id==device_id).count()
                return ret
            except NoResultFound, e:
                print "cpsection_handler: no record found for data_type_all_by_device_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(cpsection).count()
                return ret
            except NoResultFound, e:
                print "cpsection_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "cpsection donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import cpsection
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "cpsection_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("cpsection_handler", "id")
            try:
                self.session.query(cpsection).filter(cpsection.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "cpsection_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class startup_bg_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(startup_bg_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import startup_bg
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("startup_bg_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(startup_bg).filter(startup_bg.id==id).all()
                else:
                    q = self.session.query(startup_bg).filter(startup_bg.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "startup_bg_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_date == data_type:
            try:
                date = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("startup_bg_handler", "date")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(startup_bg).filter(startup_bg.date==date).all()
                else:
                    q = self.session.query(startup_bg).filter(startup_bg.date==date)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "startup_bg_handler: no record found for data_type_all_by_date"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(startup_bg).all()
                else:
                    q = self.session.query(startup_bg)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "startup_bg_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "startup_bg donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import startup_bg
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("startup_bg_handler", "id")
            try:
                self.session.query(startup_bg).filter(startup_bg.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "startup_bg_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import startup_bg
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = startup_bg(**self.data_desc.modifier)
            except:
                print "fail to initialize the startup_bg instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "startup_bg process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "startup_bg process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import startup_bg
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "startup_bg_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("startup_bg_handler", "id")
            try:
                ret = self.session.query(startup_bg).filter(startup_bg.id==id).count()
                return ret
            except NoResultFound, e:
                print "startup_bg_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_date == data_type:
            try:
                date = self.data_desc.getKey(1)
            except:
                print "startup_bg_handler: date parameters is required for data_type_all_bydate"
                raise InvalidKeyException("startup_bg_handler", "date")
            try:
                ret = self.session.query(startup_bg).filter(startup_bg.date==date).count()
                return ret
            except NoResultFound, e:
                print "startup_bg_handler: no record found for data_type_all_by_date"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(startup_bg).count()
                return ret
            except NoResultFound, e:
                print "startup_bg_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "startup_bg donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import startup_bg
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "startup_bg_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("startup_bg_handler", "id")
            try:
                self.session.query(startup_bg).filter(startup_bg.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "startup_bg_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class batch_audit_media_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(batch_audit_media_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import batch_audit_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("batch_audit_media_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(batch_audit_media).filter(batch_audit_media.id==id).all()
                else:
                    q = self.session.query(batch_audit_media).filter(batch_audit_media.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "batch_audit_media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_taskid == data_type:
            try:
                taskid = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("batch_audit_media_handler", "taskid")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(batch_audit_media).filter(batch_audit_media.taskid==taskid).all()
                else:
                    q = self.session.query(batch_audit_media).filter(batch_audit_media.taskid==taskid)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "batch_audit_media_handler: no record found for data_type_all_by_taskid"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(batch_audit_media).all()
                else:
                    q = self.session.query(batch_audit_media)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "batch_audit_media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "batch_audit_media donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import batch_audit_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("batch_audit_media_handler", "id")
            try:
                self.session.query(batch_audit_media).filter(batch_audit_media.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "batch_audit_media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import batch_audit_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = batch_audit_media(**self.data_desc.modifier)
            except:
                print "fail to initialize the batch_audit_media instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "batch_audit_media process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "batch_audit_media process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import batch_audit_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "batch_audit_media_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("batch_audit_media_handler", "id")
            try:
                ret = self.session.query(batch_audit_media).filter(batch_audit_media.id==id).count()
                return ret
            except NoResultFound, e:
                print "batch_audit_media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_taskid == data_type:
            try:
                taskid = self.data_desc.getKey(1)
            except:
                print "batch_audit_media_handler: taskid parameters is required for data_type_all_bytaskid"
                raise InvalidKeyException("batch_audit_media_handler", "taskid")
            try:
                ret = self.session.query(batch_audit_media).filter(batch_audit_media.taskid==taskid).count()
                return ret
            except NoResultFound, e:
                print "batch_audit_media_handler: no record found for data_type_all_by_taskid"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(batch_audit_media).count()
                return ret
            except NoResultFound, e:
                print "batch_audit_media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "batch_audit_media donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import batch_audit_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "batch_audit_media_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("batch_audit_media_handler", "id")
            try:
                self.session.query(batch_audit_media).filter(batch_audit_media.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "batch_audit_media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class monitor_data_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(monitor_data_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import monitor_data
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("monitor_data_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(monitor_data).filter(monitor_data.id==id).all()
                else:
                    q = self.session.query(monitor_data).filter(monitor_data.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "monitor_data_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(monitor_data).all()
                else:
                    q = self.session.query(monitor_data)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "monitor_data_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "monitor_data donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import monitor_data
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("monitor_data_handler", "id")
            try:
                self.session.query(monitor_data).filter(monitor_data.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "monitor_data_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import monitor_data
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = monitor_data(**self.data_desc.modifier)
            except:
                print "fail to initialize the monitor_data instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "monitor_data process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "monitor_data process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import monitor_data
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "monitor_data_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("monitor_data_handler", "id")
            try:
                ret = self.session.query(monitor_data).filter(monitor_data.id==id).count()
                return ret
            except NoResultFound, e:
                print "monitor_data_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(monitor_data).count()
                return ret
            except NoResultFound, e:
                print "monitor_data_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "monitor_data donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import monitor_data
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "monitor_data_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("monitor_data_handler", "id")
            try:
                self.session.query(monitor_data).filter(monitor_data.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "monitor_data_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class model_version_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(model_version_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import model_version
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("model_version_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(model_version).filter(model_version.id==id).all()
                else:
                    q = self.session.query(model_version).filter(model_version.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "model_version_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_model_id == data_type:
            try:
                model_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("model_version_handler", "model_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(model_version).filter(model_version.model_id==model_id).all()
                else:
                    q = self.session.query(model_version).filter(model_version.model_id==model_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "model_version_handler: no record found for data_type_all_by_model_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(model_version).all()
                else:
                    q = self.session.query(model_version)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "model_version_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "model_version donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import model_version
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("model_version_handler", "id")
            try:
                self.session.query(model_version).filter(model_version.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "model_version_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import model_version
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = model_version(**self.data_desc.modifier)
            except:
                print "fail to initialize the model_version instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "model_version process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "model_version process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import model_version
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "model_version_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("model_version_handler", "id")
            try:
                ret = self.session.query(model_version).filter(model_version.id==id).count()
                return ret
            except NoResultFound, e:
                print "model_version_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_model_id == data_type:
            try:
                model_id = self.data_desc.getKey(1)
            except:
                print "model_version_handler: model_id parameters is required for data_type_all_bymodel_id"
                raise InvalidKeyException("model_version_handler", "model_id")
            try:
                ret = self.session.query(model_version).filter(model_version.model_id==model_id).count()
                return ret
            except NoResultFound, e:
                print "model_version_handler: no record found for data_type_all_by_model_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(model_version).count()
                return ret
            except NoResultFound, e:
                print "model_version_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "model_version donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import model_version
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "model_version_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("model_version_handler", "id")
            try:
                self.session.query(model_version).filter(model_version.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "model_version_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class feature_navigation_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(feature_navigation_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import feature_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("feature_navigation_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(feature_navigation).filter(feature_navigation.id==id).all()
                else:
                    q = self.session.query(feature_navigation).filter(feature_navigation.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "feature_navigation_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_provider_id == data_type:
            try:
                provider_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("feature_navigation_handler", "provider_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(feature_navigation).filter(feature_navigation.provider_id==provider_id).all()
                else:
                    q = self.session.query(feature_navigation).filter(feature_navigation.provider_id==provider_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "feature_navigation_handler: no record found for data_type_all_by_provider_id"
                raise e
    
        elif DATATYPE.data_type_all_by_feature_navigation_id == data_type:
            try:
                feature_navigation_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("feature_navigation_handler", "feature_navigation_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(feature_navigation).filter(feature_navigation.feature_navigation_id==feature_navigation_id).all()
                else:
                    q = self.session.query(feature_navigation).filter(feature_navigation.feature_navigation_id==feature_navigation_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "feature_navigation_handler: no record found for data_type_all_by_feature_navigation_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(feature_navigation).all()
                else:
                    q = self.session.query(feature_navigation)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "feature_navigation_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "feature_navigation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import feature_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("feature_navigation_handler", "id")
            try:
                self.session.query(feature_navigation).filter(feature_navigation.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "feature_navigation_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import feature_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = feature_navigation(**self.data_desc.modifier)
            except:
                print "fail to initialize the feature_navigation instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "feature_navigation process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "feature_navigation process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import feature_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "feature_navigation_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("feature_navigation_handler", "id")
            try:
                ret = self.session.query(feature_navigation).filter(feature_navigation.id==id).count()
                return ret
            except NoResultFound, e:
                print "feature_navigation_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_provider_id == data_type:
            try:
                provider_id = self.data_desc.getKey(1)
            except:
                print "feature_navigation_handler: provider_id parameters is required for data_type_all_byprovider_id"
                raise InvalidKeyException("feature_navigation_handler", "provider_id")
            try:
                ret = self.session.query(feature_navigation).filter(feature_navigation.provider_id==provider_id).count()
                return ret
            except NoResultFound, e:
                print "feature_navigation_handler: no record found for data_type_all_by_provider_id"
                raise e
    
        elif DATATYPE.data_type_all_by_feature_navigation_id == data_type:
            try:
                feature_navigation_id = self.data_desc.getKey(1)
            except:
                print "feature_navigation_handler: feature_navigation_id parameters is required for data_type_all_byfeature_navigation_id"
                raise InvalidKeyException("feature_navigation_handler", "feature_navigation_id")
            try:
                ret = self.session.query(feature_navigation).filter(feature_navigation.feature_navigation_id==feature_navigation_id).count()
                return ret
            except NoResultFound, e:
                print "feature_navigation_handler: no record found for data_type_all_by_feature_navigation_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(feature_navigation).count()
                return ret
            except NoResultFound, e:
                print "feature_navigation_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "feature_navigation donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import feature_navigation
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "feature_navigation_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("feature_navigation_handler", "id")
            try:
                self.session.query(feature_navigation).filter(feature_navigation.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "feature_navigation_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class model_deviceid_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(model_deviceid_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import model_deviceid
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("model_deviceid_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(model_deviceid).filter(model_deviceid.id==id).all()
                else:
                    q = self.session.query(model_deviceid).filter(model_deviceid.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "model_deviceid_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_is_4k == data_type:
            try:
                is_4k = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("model_deviceid_handler", "is_4k")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(model_deviceid).filter(model_deviceid.is_4k==is_4k).all()
                else:
                    q = self.session.query(model_deviceid).filter(model_deviceid.is_4k==is_4k)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "model_deviceid_handler: no record found for data_type_all_by_is_4k"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(model_deviceid).all()
                else:
                    q = self.session.query(model_deviceid)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "model_deviceid_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "model_deviceid donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import model_deviceid
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("model_deviceid_handler", "id")
            try:
                self.session.query(model_deviceid).filter(model_deviceid.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "model_deviceid_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import model_deviceid
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = model_deviceid(**self.data_desc.modifier)
            except:
                print "fail to initialize the model_deviceid instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "model_deviceid process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "model_deviceid process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import model_deviceid
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "model_deviceid_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("model_deviceid_handler", "id")
            try:
                ret = self.session.query(model_deviceid).filter(model_deviceid.id==id).count()
                return ret
            except NoResultFound, e:
                print "model_deviceid_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_is_4k == data_type:
            try:
                is_4k = self.data_desc.getKey(1)
            except:
                print "model_deviceid_handler: is_4k parameters is required for data_type_all_byis_4k"
                raise InvalidKeyException("model_deviceid_handler", "is_4k")
            try:
                ret = self.session.query(model_deviceid).filter(model_deviceid.is_4k==is_4k).count()
                return ret
            except NoResultFound, e:
                print "model_deviceid_handler: no record found for data_type_all_by_is_4k"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(model_deviceid).count()
                return ret
            except NoResultFound, e:
                print "model_deviceid_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "model_deviceid donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import model_deviceid
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "model_deviceid_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("model_deviceid_handler", "id")
            try:
                self.session.query(model_deviceid).filter(model_deviceid.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "model_deviceid_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class frontpage_static_strategy_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(frontpage_static_strategy_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import frontpage_static_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("frontpage_static_strategy_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(frontpage_static_strategy).filter(frontpage_static_strategy.id==id).all()
                else:
                    q = self.session.query(frontpage_static_strategy).filter(frontpage_static_strategy.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "frontpage_static_strategy_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(frontpage_static_strategy).all()
                else:
                    q = self.session.query(frontpage_static_strategy)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "frontpage_static_strategy_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "frontpage_static_strategy donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import frontpage_static_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("frontpage_static_strategy_handler", "id")
            try:
                self.session.query(frontpage_static_strategy).filter(frontpage_static_strategy.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "frontpage_static_strategy_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import frontpage_static_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = frontpage_static_strategy(**self.data_desc.modifier)
            except:
                print "fail to initialize the frontpage_static_strategy instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "frontpage_static_strategy process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "frontpage_static_strategy process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import frontpage_static_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "frontpage_static_strategy_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("frontpage_static_strategy_handler", "id")
            try:
                ret = self.session.query(frontpage_static_strategy).filter(frontpage_static_strategy.id==id).count()
                return ret
            except NoResultFound, e:
                print "frontpage_static_strategy_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(frontpage_static_strategy).count()
                return ret
            except NoResultFound, e:
                print "frontpage_static_strategy_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "frontpage_static_strategy donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import frontpage_static_strategy
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "frontpage_static_strategy_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("frontpage_static_strategy_handler", "id")
            try:
                self.session.query(frontpage_static_strategy).filter(frontpage_static_strategy.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "frontpage_static_strategy_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
def default_db_get(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_userDevice == schema:
        handler = userDevice_handler("get", data_desc)
    elif SCHEMA.schema_resource == schema:
        handler = resource_handler("get", data_desc)
    elif SCHEMA.schema_userLogin == schema:
        handler = userLogin_handler("get", data_desc)
    elif SCHEMA.schema_vodupgrade == schema:
        handler = vodupgrade_handler("get", data_desc)
    elif SCHEMA.schema_frontpage_strategy == schema:
        handler = frontpage_strategy_handler("get", data_desc)
    elif SCHEMA.schema_frontpage_layout == schema:
        handler = frontpage_layout_handler("get", data_desc)
    elif SCHEMA.schema_category_manager == schema:
        handler = category_manager_handler("get", data_desc)
    elif SCHEMA.schema_category_frontpage_strategy == schema:
        handler = category_frontpage_strategy_handler("get", data_desc)
    elif SCHEMA.schema_category_navigation == schema:
        handler = category_navigation_handler("get", data_desc)
    elif SCHEMA.schema_category_aggregation == schema:
        handler = category_aggregation_handler("get", data_desc)
    elif SCHEMA.schema_topic_category == schema:
        handler = topic_category_handler("get", data_desc)
    elif SCHEMA.schema_topic_info == schema:
        handler = topic_info_handler("get", data_desc)
    elif SCHEMA.schema_area_apps == schema:
        handler = area_apps_handler("get", data_desc)
    elif SCHEMA.schema_Basic_Vender == schema:
        handler = Basic_Vender_handler("get", data_desc)
    elif SCHEMA.schema_Basic_Media_Entertainer_Rel == schema:
        handler = Basic_Media_Entertainer_Rel_handler("get", data_desc)
    elif SCHEMA.schema_Basic_Video_Entertainer_Rel == schema:
        handler = Basic_Video_Entertainer_Rel_handler("get", data_desc)
    elif SCHEMA.schema_Basic_Media_Category_Rel == schema:
        handler = Basic_Media_Category_Rel_handler("get", data_desc)
    elif SCHEMA.schema_Basic_Category == schema:
        handler = Basic_Category_handler("get", data_desc)
    elif SCHEMA.schema_Basic_Media == schema:
        handler = Basic_Media_handler("get", data_desc)
    elif SCHEMA.schema_Basic_Entertainer == schema:
        handler = Basic_Entertainer_handler("get", data_desc)
    elif SCHEMA.schema_Basic_Video == schema:
        handler = Basic_Video_handler("get", data_desc)
    elif SCHEMA.schema_Basic_Asset == schema:
        handler = Basic_Asset_handler("get", data_desc)
    elif SCHEMA.schema_Basic_UserHistory == schema:
        handler = Basic_UserHistory_handler("get", data_desc)
    elif SCHEMA.schema_Basic_UserCollect == schema:
        handler = Basic_UserCollect_handler("get", data_desc)
    elif SCHEMA.schema_Basic_UserSettings == schema:
        handler = Basic_UserSettings_handler("get", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("get", data_desc)
    elif SCHEMA.schema_user_center_layout == schema:
        handler = user_center_layout_handler("get", data_desc)
    elif SCHEMA.schema_video_startup == schema:
        handler = video_startup_handler("get", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("get", data_desc)
    elif SCHEMA.schema_media_collections == schema:
        handler = media_collections_handler("get", data_desc)
    elif SCHEMA.schema_new7days == schema:
        handler = new7days_handler("get", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("get", data_desc)
    elif SCHEMA.schema_oss_preview == schema:
        handler = oss_preview_handler("get", data_desc)
    elif SCHEMA.schema_cpsection == schema:
        handler = cpsection_handler("get", data_desc)
    elif SCHEMA.schema_startup_bg == schema:
        handler = startup_bg_handler("get", data_desc)
    elif SCHEMA.schema_batch_audit_media == schema:
        handler = batch_audit_media_handler("get", data_desc)
    elif SCHEMA.schema_monitor_data == schema:
        handler = monitor_data_handler("get", data_desc)
    elif SCHEMA.schema_model_version == schema:
        handler = model_version_handler("get", data_desc)
    elif SCHEMA.schema_feature_navigation == schema:
        handler = feature_navigation_handler("get", data_desc)
    elif SCHEMA.schema_model_deviceid == schema:
        handler = model_deviceid_handler("get", data_desc)
    elif SCHEMA.schema_frontpage_static_strategy == schema:
        handler = frontpage_static_strategy_handler("get", data_desc)
    
    else:
        print "default_db_get donot support schema ", schema
        return None
    return handler
    
def default_db_update(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_userDevice == schema:
        handler = userDevice_handler("upd", data_desc)
    elif SCHEMA.schema_resource == schema:
        handler = resource_handler("upd", data_desc)
    elif SCHEMA.schema_userLogin == schema:
        handler = userLogin_handler("upd", data_desc)
    elif SCHEMA.schema_vodupgrade == schema:
        handler = vodupgrade_handler("upd", data_desc)
    elif SCHEMA.schema_frontpage_strategy == schema:
        handler = frontpage_strategy_handler("upd", data_desc)
    elif SCHEMA.schema_frontpage_layout == schema:
        handler = frontpage_layout_handler("upd", data_desc)
    elif SCHEMA.schema_category_manager == schema:
        handler = category_manager_handler("upd", data_desc)
    elif SCHEMA.schema_category_frontpage_strategy == schema:
        handler = category_frontpage_strategy_handler("upd", data_desc)
    elif SCHEMA.schema_category_navigation == schema:
        handler = category_navigation_handler("upd", data_desc)
    elif SCHEMA.schema_category_aggregation == schema:
        handler = category_aggregation_handler("upd", data_desc)
    elif SCHEMA.schema_topic_category == schema:
        handler = topic_category_handler("upd", data_desc)
    elif SCHEMA.schema_topic_info == schema:
        handler = topic_info_handler("upd", data_desc)
    elif SCHEMA.schema_area_apps == schema:
        handler = area_apps_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_Vender == schema:
        handler = Basic_Vender_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_Media_Entertainer_Rel == schema:
        handler = Basic_Media_Entertainer_Rel_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_Video_Entertainer_Rel == schema:
        handler = Basic_Video_Entertainer_Rel_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_Media_Category_Rel == schema:
        handler = Basic_Media_Category_Rel_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_Category == schema:
        handler = Basic_Category_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_Media == schema:
        handler = Basic_Media_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_Entertainer == schema:
        handler = Basic_Entertainer_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_Video == schema:
        handler = Basic_Video_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_Asset == schema:
        handler = Basic_Asset_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_UserHistory == schema:
        handler = Basic_UserHistory_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_UserCollect == schema:
        handler = Basic_UserCollect_handler("upd", data_desc)
    elif SCHEMA.schema_Basic_UserSettings == schema:
        handler = Basic_UserSettings_handler("upd", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("upd", data_desc)
    elif SCHEMA.schema_user_center_layout == schema:
        handler = user_center_layout_handler("upd", data_desc)
    elif SCHEMA.schema_video_startup == schema:
        handler = video_startup_handler("upd", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("upd", data_desc)
    elif SCHEMA.schema_media_collections == schema:
        handler = media_collections_handler("upd", data_desc)
    elif SCHEMA.schema_new7days == schema:
        handler = new7days_handler("upd", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("upd", data_desc)
    elif SCHEMA.schema_oss_preview == schema:
        handler = oss_preview_handler("upd", data_desc)
    elif SCHEMA.schema_cpsection == schema:
        handler = cpsection_handler("upd", data_desc)
    elif SCHEMA.schema_startup_bg == schema:
        handler = startup_bg_handler("upd", data_desc)
    elif SCHEMA.schema_batch_audit_media == schema:
        handler = batch_audit_media_handler("upd", data_desc)
    elif SCHEMA.schema_monitor_data == schema:
        handler = monitor_data_handler("upd", data_desc)
    elif SCHEMA.schema_model_version == schema:
        handler = model_version_handler("upd", data_desc)
    elif SCHEMA.schema_feature_navigation == schema:
        handler = feature_navigation_handler("upd", data_desc)
    elif SCHEMA.schema_model_deviceid == schema:
        handler = model_deviceid_handler("upd", data_desc)
    elif SCHEMA.schema_frontpage_static_strategy == schema:
        handler = frontpage_static_strategy_handler("upd", data_desc)
    
    else:
        print "default_db_update donot support schema ", schema
        return None
    return handler
    
def default_db_insert(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_userDevice == schema:
        handler = userDevice_handler("insr", data_desc)
    elif SCHEMA.schema_resource == schema:
        handler = resource_handler("insr", data_desc)
    elif SCHEMA.schema_userLogin == schema:
        handler = userLogin_handler("insr", data_desc)
    elif SCHEMA.schema_vodupgrade == schema:
        handler = vodupgrade_handler("insr", data_desc)
    elif SCHEMA.schema_frontpage_strategy == schema:
        handler = frontpage_strategy_handler("insr", data_desc)
    elif SCHEMA.schema_frontpage_layout == schema:
        handler = frontpage_layout_handler("insr", data_desc)
    elif SCHEMA.schema_category_manager == schema:
        handler = category_manager_handler("insr", data_desc)
    elif SCHEMA.schema_category_frontpage_strategy == schema:
        handler = category_frontpage_strategy_handler("insr", data_desc)
    elif SCHEMA.schema_category_navigation == schema:
        handler = category_navigation_handler("insr", data_desc)
    elif SCHEMA.schema_category_aggregation == schema:
        handler = category_aggregation_handler("insr", data_desc)
    elif SCHEMA.schema_topic_category == schema:
        handler = topic_category_handler("insr", data_desc)
    elif SCHEMA.schema_topic_info == schema:
        handler = topic_info_handler("insr", data_desc)
    elif SCHEMA.schema_area_apps == schema:
        handler = area_apps_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_Vender == schema:
        handler = Basic_Vender_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_Media_Entertainer_Rel == schema:
        handler = Basic_Media_Entertainer_Rel_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_Video_Entertainer_Rel == schema:
        handler = Basic_Video_Entertainer_Rel_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_Media_Category_Rel == schema:
        handler = Basic_Media_Category_Rel_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_Category == schema:
        handler = Basic_Category_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_Media == schema:
        handler = Basic_Media_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_Entertainer == schema:
        handler = Basic_Entertainer_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_Video == schema:
        handler = Basic_Video_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_Asset == schema:
        handler = Basic_Asset_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_UserHistory == schema:
        handler = Basic_UserHistory_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_UserCollect == schema:
        handler = Basic_UserCollect_handler("insr", data_desc)
    elif SCHEMA.schema_Basic_UserSettings == schema:
        handler = Basic_UserSettings_handler("insr", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("insr", data_desc)
    elif SCHEMA.schema_user_center_layout == schema:
        handler = user_center_layout_handler("insr", data_desc)
    elif SCHEMA.schema_video_startup == schema:
        handler = video_startup_handler("insr", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("insr", data_desc)
    elif SCHEMA.schema_media_collections == schema:
        handler = media_collections_handler("insr", data_desc)
    elif SCHEMA.schema_new7days == schema:
        handler = new7days_handler("insr", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("insr", data_desc)
    elif SCHEMA.schema_oss_preview == schema:
        handler = oss_preview_handler("insr", data_desc)
    elif SCHEMA.schema_cpsection == schema:
        handler = cpsection_handler("insr", data_desc)
    elif SCHEMA.schema_startup_bg == schema:
        handler = startup_bg_handler("insr", data_desc)
    elif SCHEMA.schema_batch_audit_media == schema:
        handler = batch_audit_media_handler("insr", data_desc)
    elif SCHEMA.schema_monitor_data == schema:
        handler = monitor_data_handler("insr", data_desc)
    elif SCHEMA.schema_model_version == schema:
        handler = model_version_handler("insr", data_desc)
    elif SCHEMA.schema_feature_navigation == schema:
        handler = feature_navigation_handler("insr", data_desc)
    elif SCHEMA.schema_model_deviceid == schema:
        handler = model_deviceid_handler("insr", data_desc)
    elif SCHEMA.schema_frontpage_static_strategy == schema:
        handler = frontpage_static_strategy_handler("insr", data_desc)
    
    else:
        print "default_db_insert donot support schema ", schema
        return None
    return handler
    
def default_db_count(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_userDevice == schema:
        handler = userDevice_handler("count", data_desc)
    elif SCHEMA.schema_resource == schema:
        handler = resource_handler("count", data_desc)
    elif SCHEMA.schema_userLogin == schema:
        handler = userLogin_handler("count", data_desc)
    elif SCHEMA.schema_vodupgrade == schema:
        handler = vodupgrade_handler("count", data_desc)
    elif SCHEMA.schema_frontpage_strategy == schema:
        handler = frontpage_strategy_handler("count", data_desc)
    elif SCHEMA.schema_frontpage_layout == schema:
        handler = frontpage_layout_handler("count", data_desc)
    elif SCHEMA.schema_category_manager == schema:
        handler = category_manager_handler("count", data_desc)
    elif SCHEMA.schema_category_frontpage_strategy == schema:
        handler = category_frontpage_strategy_handler("count", data_desc)
    elif SCHEMA.schema_category_navigation == schema:
        handler = category_navigation_handler("count", data_desc)
    elif SCHEMA.schema_category_aggregation == schema:
        handler = category_aggregation_handler("count", data_desc)
    elif SCHEMA.schema_topic_category == schema:
        handler = topic_category_handler("count", data_desc)
    elif SCHEMA.schema_topic_info == schema:
        handler = topic_info_handler("count", data_desc)
    elif SCHEMA.schema_area_apps == schema:
        handler = area_apps_handler("count", data_desc)
    elif SCHEMA.schema_Basic_Vender == schema:
        handler = Basic_Vender_handler("count", data_desc)
    elif SCHEMA.schema_Basic_Media_Entertainer_Rel == schema:
        handler = Basic_Media_Entertainer_Rel_handler("count", data_desc)
    elif SCHEMA.schema_Basic_Video_Entertainer_Rel == schema:
        handler = Basic_Video_Entertainer_Rel_handler("count", data_desc)
    elif SCHEMA.schema_Basic_Media_Category_Rel == schema:
        handler = Basic_Media_Category_Rel_handler("count", data_desc)
    elif SCHEMA.schema_Basic_Category == schema:
        handler = Basic_Category_handler("count", data_desc)
    elif SCHEMA.schema_Basic_Media == schema:
        handler = Basic_Media_handler("count", data_desc)
    elif SCHEMA.schema_Basic_Entertainer == schema:
        handler = Basic_Entertainer_handler("count", data_desc)
    elif SCHEMA.schema_Basic_Video == schema:
        handler = Basic_Video_handler("count", data_desc)
    elif SCHEMA.schema_Basic_Asset == schema:
        handler = Basic_Asset_handler("count", data_desc)
    elif SCHEMA.schema_Basic_UserHistory == schema:
        handler = Basic_UserHistory_handler("count", data_desc)
    elif SCHEMA.schema_Basic_UserCollect == schema:
        handler = Basic_UserCollect_handler("count", data_desc)
    elif SCHEMA.schema_Basic_UserSettings == schema:
        handler = Basic_UserSettings_handler("count", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("count", data_desc)
    elif SCHEMA.schema_user_center_layout == schema:
        handler = user_center_layout_handler("count", data_desc)
    elif SCHEMA.schema_video_startup == schema:
        handler = video_startup_handler("count", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("count", data_desc)
    elif SCHEMA.schema_media_collections == schema:
        handler = media_collections_handler("count", data_desc)
    elif SCHEMA.schema_new7days == schema:
        handler = new7days_handler("count", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("count", data_desc)
    elif SCHEMA.schema_oss_preview == schema:
        handler = oss_preview_handler("count", data_desc)
    elif SCHEMA.schema_cpsection == schema:
        handler = cpsection_handler("count", data_desc)
    elif SCHEMA.schema_startup_bg == schema:
        handler = startup_bg_handler("count", data_desc)
    elif SCHEMA.schema_batch_audit_media == schema:
        handler = batch_audit_media_handler("count", data_desc)
    elif SCHEMA.schema_monitor_data == schema:
        handler = monitor_data_handler("count", data_desc)
    elif SCHEMA.schema_model_version == schema:
        handler = model_version_handler("count", data_desc)
    elif SCHEMA.schema_feature_navigation == schema:
        handler = feature_navigation_handler("count", data_desc)
    elif SCHEMA.schema_model_deviceid == schema:
        handler = model_deviceid_handler("count", data_desc)
    elif SCHEMA.schema_frontpage_static_strategy == schema:
        handler = frontpage_static_strategy_handler("count", data_desc)
    
    else:
        print "default_db_count donot support schema ", schema
        return None
    return handler
    
def default_db_delete(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_userDevice == schema:
        handler = userDevice_handler("del", data_desc)
    elif SCHEMA.schema_resource == schema:
        handler = resource_handler("del", data_desc)
    elif SCHEMA.schema_userLogin == schema:
        handler = userLogin_handler("del", data_desc)
    elif SCHEMA.schema_vodupgrade == schema:
        handler = vodupgrade_handler("del", data_desc)
    elif SCHEMA.schema_frontpage_strategy == schema:
        handler = frontpage_strategy_handler("del", data_desc)
    elif SCHEMA.schema_frontpage_layout == schema:
        handler = frontpage_layout_handler("del", data_desc)
    elif SCHEMA.schema_category_manager == schema:
        handler = category_manager_handler("del", data_desc)
    elif SCHEMA.schema_category_frontpage_strategy == schema:
        handler = category_frontpage_strategy_handler("del", data_desc)
    elif SCHEMA.schema_category_navigation == schema:
        handler = category_navigation_handler("del", data_desc)
    elif SCHEMA.schema_category_aggregation == schema:
        handler = category_aggregation_handler("del", data_desc)
    elif SCHEMA.schema_topic_category == schema:
        handler = topic_category_handler("del", data_desc)
    elif SCHEMA.schema_topic_info == schema:
        handler = topic_info_handler("del", data_desc)
    elif SCHEMA.schema_area_apps == schema:
        handler = area_apps_handler("del", data_desc)
    elif SCHEMA.schema_Basic_Vender == schema:
        handler = Basic_Vender_handler("del", data_desc)
    elif SCHEMA.schema_Basic_Media_Entertainer_Rel == schema:
        handler = Basic_Media_Entertainer_Rel_handler("del", data_desc)
    elif SCHEMA.schema_Basic_Video_Entertainer_Rel == schema:
        handler = Basic_Video_Entertainer_Rel_handler("del", data_desc)
    elif SCHEMA.schema_Basic_Media_Category_Rel == schema:
        handler = Basic_Media_Category_Rel_handler("del", data_desc)
    elif SCHEMA.schema_Basic_Category == schema:
        handler = Basic_Category_handler("del", data_desc)
    elif SCHEMA.schema_Basic_Media == schema:
        handler = Basic_Media_handler("del", data_desc)
    elif SCHEMA.schema_Basic_Entertainer == schema:
        handler = Basic_Entertainer_handler("del", data_desc)
    elif SCHEMA.schema_Basic_Video == schema:
        handler = Basic_Video_handler("del", data_desc)
    elif SCHEMA.schema_Basic_Asset == schema:
        handler = Basic_Asset_handler("del", data_desc)
    elif SCHEMA.schema_Basic_UserHistory == schema:
        handler = Basic_UserHistory_handler("del", data_desc)
    elif SCHEMA.schema_Basic_UserCollect == schema:
        handler = Basic_UserCollect_handler("del", data_desc)
    elif SCHEMA.schema_Basic_UserSettings == schema:
        handler = Basic_UserSettings_handler("del", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("del", data_desc)
    elif SCHEMA.schema_user_center_layout == schema:
        handler = user_center_layout_handler("del", data_desc)
    elif SCHEMA.schema_video_startup == schema:
        handler = video_startup_handler("del", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("del", data_desc)
    elif SCHEMA.schema_media_collections == schema:
        handler = media_collections_handler("del", data_desc)
    elif SCHEMA.schema_new7days == schema:
        handler = new7days_handler("del", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("del", data_desc)
    elif SCHEMA.schema_oss_preview == schema:
        handler = oss_preview_handler("del", data_desc)
    elif SCHEMA.schema_cpsection == schema:
        handler = cpsection_handler("del", data_desc)
    elif SCHEMA.schema_startup_bg == schema:
        handler = startup_bg_handler("del", data_desc)
    elif SCHEMA.schema_batch_audit_media == schema:
        handler = batch_audit_media_handler("del", data_desc)
    elif SCHEMA.schema_monitor_data == schema:
        handler = monitor_data_handler("del", data_desc)
    elif SCHEMA.schema_model_version == schema:
        handler = model_version_handler("del", data_desc)
    elif SCHEMA.schema_feature_navigation == schema:
        handler = feature_navigation_handler("del", data_desc)
    elif SCHEMA.schema_model_deviceid == schema:
        handler = model_deviceid_handler("del", data_desc)
    elif SCHEMA.schema_frontpage_static_strategy == schema:
        handler = frontpage_static_strategy_handler("del", data_desc)
    
    else:
        print "default_db_insert donot support schema ", schema
        return None
    return handler
    