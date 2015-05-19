__author__ = 'liupeng'

from df.datamodel.schema import SCHEMA, DATATYPE, userDevice
from base_handler import db_handler

def registerRequstHander():
    return "schema_user_device", SCHEMA.schema_user_device, UserDeviceHandler


class UserDeviceHandler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(UserDeviceHandler, self).__init__(op, data_desc, session)

    def processQuery(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_get_device_id_by_type == data_type:
            device_type = self.data_desc.getKey('device_type')
            code = self.data_desc.getKey('code')
            customer_id = self.data_desc.getKey('customer_id')
            return self.session.query(userDevice).filter_by(customer_id=customer_id,
                                                            type=device_type,
                                                            code=code).all()
    def processInsert(self):
        data_type = self.data_desc.getDataType()
        if DATATYPE.data_type_create_device_id_by_type == data_type:
            device_type = self.data_desc.getKey('device_type')
            code = self.data_desc.getKey('code')
            customer_id = self.data_desc.getKey('customer_id')
            device = userDevice(type=device_type, code=code, customer_id=customer_id)
            self.session.add(device)
            #have to flush to get incremental id
            # due to the flush cannot insert data into database for unkown read
            # use commit  instead
            self.session.commit()
            self.session.flush()
            return device.id
