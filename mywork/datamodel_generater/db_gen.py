#!/usr/bin/env python

from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation, Node

FIELD_TYPES = ("String", "Integer", "Boolean", "BigInteger",
               "Text", "Float", "SmallInteger", "DateTime")

class Table(object):
    def __init__(self, name):
        self.native_name = name
        self.table_name = name
        self.fields = []
        self.key = ""
        self.indexs = []
        self.data_types = []
    def appendField(self, child):
        self.fields.append(child)
    def repr(self):
        s = "table name: %s\n"%self.name
        for field in self.fields:
            s += field.repr() + "\n"
        return s

class Field(object):
    def __init__(self, name, type):
        self.name = name
        if type not in FIELD_TYPES:
            print "invalid type provided %s"%type
            raise ValueError
        self.base_type = type
        self.length = 0
        self.isIndex = False
        self.nullable = False
        self.hasDefault = False
        self.default = ""
        self.hasCollation = False
        self.collation = ""
        self.desc = ""
        
    def __getattr__(self, key):
        """
        only type attribute will get in this function
        """
        if key == "type":
            if self.base_type == "String":
                if self.hasCollation:
                    s = "String(%d, collation=\'%s\')"%(self.length, self.collation)
                else:
                    s = "String(%d)"%(self.length)
                
                return s
            else:
                return self.base_type
        else:
            print "invalid key ", key
            raise AttributeError
        
    def setLength(self, len):
        self.length = len

    def setIndex(self):
        self.isIndex = True
        self.nullable = False

    def setNullable(self):
        self.nullable = True

    def setDefault(self, value):
        if self.base_type == "String":
            self.default = "'%s'"%value
        else:
            self.default = value
        self.hasDefault = True

    def setCollation(self, value):
        self.collation = value
        self.hasCollation = True

    def setDesc(self, desc):
        self.desc = desc

    def repr(self):
        s = "name: %s, type=%s"%(self.name, self.type)
        if self.length > 0:
            s = s + ", length=%d"%self.length
        return s

class DataType(object):
    def __init__(self, name):
        self.name = name

    def repr(self):
        s = self.name
        return s

class UserSchema(object):
    def __init__(self, name):
        self.name = name

    def repr(self):
        s = self.name
        return s

class cachePolicy(object):
    def __init__(self, schema):
        self.schema = schema
        self.policies = []
    def validate(self):
        ''' maybe check the schema exist '''
        return True
    def addPolicy(self, data_type, time):
        self.policies.append((data_type, time))
    def getPolicies(self):
        return self.policies
    
    
def getFields(table):
    fields = []
    for field in table.childNodes:
        if field.nodeType == Node.TEXT_NODE:
            continue
        name =  field.getAttribute("name")
        type = field.getAttribute("type")
        f = Field(name, type)
        if type == "String":
            len = int(field.getAttribute("length"))
            f.setLength(len)

        if field.getAttribute("index"):
            isIndex = field.getAttribute("index")
            if isIndex == "True":
                f.setIndex()

        if field.hasAttribute("nullable"):
            nullable = field.getAttribute("nullable")
            if nullable == "True":
                f.setNullable()

        if field.getAttribute("default"):
            default = field.getAttribute("default")
            f.setDefault(default)

        if field.getAttribute("collation"):
            collation = field.getAttribute("collation")
            f.setCollation(collation)
        if field.getAttribute("descrip"):
            desc = field.getAttribute("descrip")
            f.setDesc(desc)

        fields.append(f)
    return fields

def genTablePY(table, f):
    s = """
class %s(Base):\n"""%table.table_name
    for field in table.fields:
        token = []
        token.append(field.type)
        token.append("nullable=%s"%str(field.nullable))
        if field.isIndex: token.append("index=True")
        if field.hasDefault: token.append("default=%s"%field.default)
        s += "    %s"%field.name + " = Column("+ ", ".join(token) + ")\n"
        
    f.write(s)

def genSchema(tables, user_schemas, f):
    start_num = 1000
    schema_counter = 0
    s = "\n# following code is used to define the default schemas\n"
    s += "SCHEMA = enum(%s,\n"%start_num
    default_schemas = ["    \"schema_%s\", \t# %s"%(table.table_name, i+start_num) \
                       for i, table in enumerate(tables)];
    default_schemas.append("    \"schema_default_end\", \t# %s"%(len(tables)+start_num))
    d = "\n".join(default_schemas)
    s += d
    user_defined_start = len(tables) + start_num + 1
    user_schemas = ["    \"%s\", \t# %s"%(schema.name, i + user_defined_start) \
                    for i, schema in enumerate(user_schemas)]
    if user_schemas is not None and not len(user_schemas) == 0:
        s += ",\n    # following are user defined schema\n"
        d = "\n".join(user_schemas)
        s += d
    s += "\n    )\n"
    f.write(s)

def genDataType(tables, user_data_types, f):
    start_num = 2000
    s = "\n# following code is used to define the data type\n"
    s += "DATATYPE = enum(%s,\n"%start_num
    default_data_types = []
    default_data_types.append("data_type_all_by_id")
    for table in tables:
        for field in table.indexs:
            data_type = "data_type_all_by_%s"%field.name
            if data_type not in default_data_types:
                default_data_types.append(data_type)
    s += ",\n".join(["    \"%s\", \t# %s"%(d, i+start_num) \
                     for i, d in enumerate(default_data_types)])
    if user_data_types is not None and not len(user_data_types) == 0:
        s += ",\n    # following are user defined data type\n"
        user_defined_start = len(default_data_types) + start_num
        s += ",\n".join(["    \"%s\", \t# %s"%(d.name, i + user_defined_start) \
                         for i, d in enumerate(user_data_types)])
    s += "\n    )\n"
    f.write(s)

def genCachePolicies(cachePolicies, f):
    s = "\ncache_policy = {\n"
    pstr = '''"%s::%s"%(SCHEMA.{0},
             DATATYPE.{1}):{2}'''
    #pstr = "{0}, {1}, {2}"
    pstr_list = []
    for p in cachePolicies:
        for dt, time in p.getPolicies():
            pstr_list.append(pstr.format(p.schema, dt, time))
    s += ",\n".join(pstr_list)
    s += "\n}\n"

    s += '''\ndef get_cache_policy(schema, data_type):
    return cache_policy.get("%s::%s"%(schema, data_type), None)'''
    
    f.write(s)

def genTitle(f):
    s = """#!/usr/bin/env python
'''
ATTENTION: THE FILE IS GENERATED AUTOMATICLY, DO NOT MODIFIY IT MANUALLY
'''
from base import Base
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Text, SmallInteger, Float, DateTime

def enum(start=0, *sequential):
    enums = dict(zip(sequential, range(start, len(sequential)+start)))
    return type('Enum', (), enums)
    """
    f.write(s)

def genDatatypeProcessQueryClauseForTable(table):
    processQueryClause = '''
    def processQuery(self):
        from ..datamodel.schema import {0}
        data_type = self.data_desc.getDataType()
    '''.format(table.table_name)
    s = '''
        {2} DATATYPE.data_type_all_by_{1} == data_type:
            try:
                {1} = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("{0}_handler", "{1}")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query({0}).filter({0}.{1}=={1}).all()
                else:
                    q = self.session.query({0}).filter({0}.{1}=={1})
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "{0}_handler: no record found for data_type_all_by_{1}"
                raise e
    '''
    ifOrElif = "if"
    ret = ""
    for key in ["id"] + [field.name for field in table.indexs]:
        clause = s.format(table.table_name, key, ifOrElif)
        ret += clause
        ifOrElif = "elif"
    ret += '''
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query({0}).all()
                else:
                    q = self.session.query({0})
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "{0}_handler: no record found for data_type_query_all"
                raise e
    '''.format(table.table_name)
    ret += '''
        else:
            print "{0} donot support DataType ", data_type
            raise NoSupportDataType
       '''.format(table.table_name)
    ret = processQueryClause + ret
    return ret

def genDatatypeProcessCountClauseForTable(table):
    processAmountClause = '''
    def processCount(self):
        from ..datamodel.schema import {0}
        data_type = self.data_desc.getDataType()
    '''.format(table.table_name)
    s = '''
        {2} DATATYPE.data_type_all_by_{1} == data_type:
            try:
                {1} = self.data_desc.getKey(1)
            except:
                print "{0}_handler: {1} parameters is required for data_type_all_by{1}"
                raise InvalidKeyException("{0}_handler", "{1}")
            try:
                ret = self.session.query({0}).filter({0}.{1}=={1}).count()
                return ret
            except NoResultFound, e:
                print "{0}_handler: no record found for data_type_all_by_{1}"
                raise e
    '''
    ifOrElif = "if"
    ret = ""
    for key in ["id"] + [field.name for field in table.indexs]:
        clause = s.format(table.table_name, key, ifOrElif)
        ret += clause
        ifOrElif = "elif"

    ret += '''
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query({0}).count()
                return ret
            except NoResultFound, e:
                print "{0}_handler: no record found for data_type_query_all"
                raise e
    '''.format(table.table_name)
    ret += '''
        else:
            print "{0} donot support DataType ", data_type
            raise NoSupportDataType           
       '''.format(table.table_name)
    ret = processAmountClause + ret
    return ret

def genDatatypeProcessUpdateClauseForTable(table):
    processUpdateClause = '''
    def processUpdate(self):
        from ..datamodel.schema import {0}
        data_type = self.data_desc.getDataType()
    '''.format(table.table_name)
    s = '''
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("{0}_handler", "id")
            try:
                self.session.query({0}).filter({0}.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "{0}_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       '''.format(table.table_name)
    processUpdateClause += s
    return processUpdateClause

def genDatatypeProcessDeleteClauseForTable(table):
    processDeleteClause = '''
    def processDelete(self):
        from ..datamodel.schema import {0}
        data_type = self.data_desc.getDataType()
    '''.format(table.table_name)
    s = '''
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "{0}_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("{0}_handler", "id")
            try:
                self.session.query({0}).filter({0}.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "{0}_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       '''.format(table.table_name)
    processDeleteClause += s
    return processDeleteClause

def genDatatypeProcessInsertClauseForTable(table):
    processInsertClause = '''
    def processInsert(self):
        from ..datamodel.schema import {0}
        data_type = self.data_desc.getDataType()
    '''.format(table.table_name)
    s = '''
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = {0}(**self.data_desc.modifier)
            except:
                print "fail to initialize the {0} instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "{0} process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "{0} process insert donot support DataType ", data_type
            return None
       '''.format(table.table_name)
    processInsertClause += s
    return processInsertClause

def genDBgetFunction(tables):
    default_db_get_str = '''
def default_db_get(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    '''
    ifclause = '''{0} SCHEMA.schema_{1} == schema:
        handler = {1}_handler("get", data_desc)
    '''
    ifOrElif = "if"
    for table in tables:
        clause = ifclause.format(ifOrElif, table.table_name)
        default_db_get_str += clause
        ifOrElif = "elif"

    default_db_get_str += '''
    else:
        print "default_db_get donot support schema ", schema
        return None
    return handler
    '''
    return default_db_get_str

def getDBupdFunction(tables):
    default_db_upd_str = '''
def default_db_update(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    '''
    ifclause = '''{0} SCHEMA.schema_{1} == schema:
        handler = {1}_handler("upd", data_desc)
    '''
    ifOrElif = "if"
    for table in tables:
        clause = ifclause.format(ifOrElif, table.table_name)
        default_db_upd_str += clause
        ifOrElif = "elif"

    default_db_upd_str += '''
    else:
        print "default_db_update donot support schema ", schema
        return None
    return handler
    '''
    return default_db_upd_str

def getDBcountFunction(tables):
    default_db_count_str = '''
def default_db_count(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    '''
    ifclause = '''{0} SCHEMA.schema_{1} == schema:
        handler = {1}_handler("count", data_desc)
    '''
    ifOrElif = "if"
    for table in tables:
        clause = ifclause.format(ifOrElif, table.table_name)
        default_db_count_str += clause
        ifOrElif = "elif"

    default_db_count_str += '''
    else:
        print "default_db_count donot support schema ", schema
        return None
    return handler
    '''
    return default_db_count_str

def getDBisrFunction(tables):
    default_db_isr_str = '''
def default_db_insert(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    '''
    ifclause = '''{0} SCHEMA.schema_{1} == schema:
        handler = {1}_handler("insr", data_desc)
    '''
    ifOrElif = "if"
    for table in tables:
        clause = ifclause.format(ifOrElif, table.table_name)
        default_db_isr_str += clause
        ifOrElif = "elif"

    default_db_isr_str += '''
    else:
        print "default_db_insert donot support schema ", schema
        return None
    return handler
    '''
    return default_db_isr_str

def genDBdelFunction(tables):
    default_db_del_str = '''
def default_db_delete(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    '''
    ifclause = '''{0} SCHEMA.schema_{1} == schema:
        handler = {1}_handler("del", data_desc)
    '''
    ifOrElif = "if"
    for table in tables:
        clause = ifclause.format(ifOrElif, table.table_name)
        default_db_del_str += clause
        ifOrElif = "elif"

    default_db_del_str += '''
    else:
        print "default_db_insert donot support schema ", schema
        return None
    return handler
    '''
    return default_db_del_str

def genDBfunctions(tables, f):
    clause = ""
    clause += genDBgetFunction(tables)
    clause += getDBupdFunction(tables)
    clause += getDBisrFunction(tables)
    clause += getDBcountFunction(tables)
    clause += genDBdelFunction(tables)
    f.write(clause)
    
def genDefaultHandler(tables, f):
    title = '''#!/usr/bin/env python

from sqlalchemy.orm.exc import NoResultFound
from ..datamodel.schema import SCHEMA, DATATYPE
from base_handler import db_handler
from common.dbutil import slice_query
from ..exceptions import NoSupportDataType
from ..data_descriptor import InvalidKeyException
    '''
    f.write(title)
    
    s = '''
class {0}_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super({0}_handler, self).__init__(op, data_desc, session)
        '''
    for table in tables:
        clause = ""
        clause += genDatatypeProcessQueryClauseForTable(table)
        clause += genDatatypeProcessUpdateClauseForTable(table)
        clause += genDatatypeProcessInsertClauseForTable(table)
        clause += genDatatypeProcessCountClauseForTable(table)
        clause += genDatatypeProcessDeleteClauseForTable(table)
        print "generate default handler for table ", table.table_name
        handler = s.format(table.table_name)
        f.write(handler+clause)
    
# --- MAIN START ---
tables = []
user_data_types = []
user_schemas = []
if __name__ == "__main__":
    schema_output_file = "./schema.py"
    handler_output_file = "../handler/default_handler.py"
    doc = minidom.parse("./datamodel.xml")

    # ******* Table definition SETUP ********
    dict_tables = doc.getElementsByTagName("table")
    for dict_table in dict_tables:
        print "generating table %s"%dict_table.getAttribute("name")
        table = Table(dict_table.getAttribute("name"))
        for field in getFields(dict_table):
            table.appendField(field)
            if field.isIndex:
                table.indexs.append(field)
        tables.append(table)
    # ***************** END **********************

    f = open(schema_output_file, "w")

    genTitle(f)

    # ******* System Table Structure Generation ********
    for table in tables:
        genTablePY(table, f)
    # ***************** END ****************************    

    # ********* System Schema Generation ***************
    dict_user_schemas = doc.getElementsByTagName("Schema")
    for item in dict_user_schemas:
        print "generating user defined schema ", item.getAttribute("name")
        user_schema = UserSchema(item.getAttribute("name"))
        user_schemas.append(user_schema)

    genSchema(tables, user_schemas, f)
    # ***************** END ****************************

    # ********* System Data Type Generation ***********
    dict_data_types = doc.getElementsByTagName("DataType")
    for  item in dict_data_types:
        print "generating DataType ", item.getAttribute("name")
        data_type = DataType(item.getAttribute("name"))
        user_data_types.append(data_type)
        
    genDataType(tables, user_data_types, f)
    # ***************** END ****************************
    # ********* system cache policy Generation *********
    dict_cache_policies = doc.getElementsByTagName("cachePolicy")
    cachePolicies = []
    for item in dict_cache_policies:
        schema = item.getAttribute("schema")
        print "generating cachePolicy ", schema
        cp = cachePolicy(schema)
        for policy in item.childNodes:
            if policy.nodeType == Node.TEXT_NODE:
                continue
            cache_time = policy.getAttribute("time")
            data_type = policy.childNodes[0].nodeValue
            cp.addPolicy(data_type, cache_time)
        if cp.validate() is False:
            print "fail to validate the cachePolicy %s", repr(cp)
            continue
        cachePolicies.append(cp)
    genCachePolicies(cachePolicies, f)
        
    # ***************** END ****************************

    f.close()

    print "going to generate default request handlers to default_handler.py"
    f = open(handler_output_file, "w")
    genDefaultHandler(tables, f)
    genDBfunctions(tables, f)
    f.close()

    print "All Done!"
