#!/usr/bin/env python

class DataNotFoundException(Exception):
    """ a exception for data not found """
    pass

class DBdataNotFoundException(DataNotFoundException):
    """ data not found from the database """
    pass

