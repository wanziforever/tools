#!/usr/bin/env python

from msgtype import MsgTypeBase
from eventype import EVENTYPE
from mydef import MyDef

class MyHeader(object):
    def __init__(self):
        self.sender = ""
        self.sender_len = MyDef.MAX_QUEUE_NAME
        self.receiver = ""
        self.receiver_len = MyDef.MAX_QUEUE_NAME
        self.event_type = 0
        self.event_type_len = 3
        self.type = 0
        self.type_len = 6
        self.fixed_header_len = self.sender_len + self.type_len

    def set_header_params(self, params):
        ''' currently not implemented for very little params '''
        pass

    def get_sender(self):
        return self.sender.strip()

    def get_type(self):
        return self.type

    def set_sender(self, sender_qname):
        if len(sender_qname) > MyDef.MAX_QUEUE_NAME:
            self.sender = sender_qname[:MyDef.MAX_QUEUE_NAME]
        else:
            self.sender = sender_qname
        return True
    def set_receiver(self, receiver_qname):
        self.receivere = receiver_qname
        
    def set_type(self, msg_type):
        if not isinstance(msg_type, int):
            print "fail to set message type", msg_type
            return False
        self.type = msg_type
        return True
    def set_eventype(self, evtype):
        if not isinstance(evtype, int):
            print "fail to set event type", evtype
            return False
        self.event_type = evtype
        return True

    def get_eventype(self):
        return self.event_type
        
    def encode(self):
        ''' encode all the header element into a string base data
        each element data will occupy fix lengh of data, and all
        element will have a sequence to build mesasge:
        type[3]||qname[MAX_QUEUE_NAME]

        return: (True, header_string) '''
        s = ""

        evtype_str = str(self.event_type)
        if len(evtype_str) >= self.event_type_len:
            evtype_str = evtype_str[:self.event_type_len]
        else:
            evtype_str += " " * (self.event_type_len - len(evtype_str))
        s += evtype_str
        
        type_str = str(self.type)
        if len(type_str) >= self.type_len:
            type_str = type_str[:self.type_len]
        else:
            type_str += " " * (self.type_len - len(type_str))
        s += type_str

        name_str = ""
        if len(self.sender) >= self.sender_len:
            name_str = self.sender[:self.sender_len]
        else:
            name_str = self.sender + " " * (self.sender_len - len(self.sender))
        s += name_str
        return True, s

    def decode(self, header_str):
        if len(header_str) != self.fixed_header_len:
            print "fail to decode header string, len is not %s"%\
                  self.fiexed_header_len
            return False
        length = 0
        evtype_str = header_str[:self.event_type_len]
        if not evtype_str.strip().isdigit():
            print "fail to decode header string, first %s[%s] char should "\
                  "represent a digit"%(self.event_type_len, evtype_str)
            return False
        self.event_type = int(evtype_str)
        length += self.event_type_len
        type_str = header_str[length:length + self.type_len]
        if not type_str.strip().isdigit():
            print "fail to decode header string, first %s[%s] char should "\
                  "represent a digit"%(self.type_len, type_str)
            print header_str
            return False
        self.type = int(type_str)
        length += self.type_len

        self.sender = header_str[length:]
        return True

class MyMessage(object):
    def __init__(self,
                 evtype=EVENTYPE.TIMEREXPIRE,
                 msgtype=MsgTypeBase.INVALID):
        self.header = MyHeader()
        self.header.set_type(msgtype)
        self.header.set_eventype(evtype)
        self.body = ""

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def set_header(self, type, qname):
        self.header.set_sender(qname)
        self.header.set_type(type)

    def encode_header(self):
        ret, s = self.header.encode()
        return ret, s

    def decode_header(self, header_str):
        return self.header.decode(header_str)

    def cast(self, MyMessageObject):
        self.header = MyMessageObject.get_header()
        self.body = MyMessageObject.get_body()

    def get_body(self):
        return self.body

    def get_header(self):
        return self.header

    def get_msgtype(self):
        return self.header.get_type()

    def get_eventype(self):
        return self.header.get_eventype()

    def build(self):
        pass

    def parse(self):
        pass
