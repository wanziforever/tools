#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Condition(object):
    op_mapping = {'eq':'==',
                  'ne':'!=',
                  'lt':'<',
                  'le':'<=',
                  'gt':'>',
                  'ge':'>='}
    def __init__(self, name, given, op):
        self.name = name
        self.value1 = given
        self.value2 = ''
        self.op = op

    def compute(self, to_compare):
        # print "condition::compute enter with", to_compare
        self.value2 = to_compare
        real_op = Condition.op_mapping.get(self.op, None)
        if real_op is None:
            return False
        compare = "'{1}' {2} '{0}'".format(self.value1, self.value2, real_op)
        return eval(compare)

    def __repr__(self):
        s = ""
        s += "name:%s, "%self.name
        s += "value1:%s, "%self.value1
        s += "value2:%s, "%self.value2
        s += "op: %s"%self.op
        return s
        
class Filter(object):
    def __init__(self, filter_dict):
        self.conditions = []
        self.conj = ''
        self.oppsite = False
        self.parse(filter_dict.get('filter', {}))
        self.setResult(filter_dict.get('ret', ''))

    def __repr__(self):
        s = ""
        s += "conditions:" + repr(self.conditions)
        return s
        
    def setResult(self, ret):
        self.ret = ret

    def parse(self, d):
        conditions = d.get("conditions", [])
        for c in conditions:
            condition = self.genCondition(c)
            if condition is None:
                continue
            # print "parse: ", repr(condition)
            self.conditions.append(condition)
        self.conj = d.get('conj', 'and')
        self.opposite = d.get('oppsite', 'False')

    def genCondition(self, d):
        name = d.get('name', '')
        if len(name.strip()) == 0:
            return None
        value = d.get('value', '')
        op = d.get('op', 'eq')[:2]
        return Condition(name, value, op)

    def getfilterResult(self, to_compare):
        # print "getfilterResult enter with to_compare", to_compare
        r = self.compute(to_compare)
        # print "compute result is ", r

        if self.opposite.upper() == "TRUE":
            r = not r

        # print "last result is ", r
        if r is False:
            return None
        return self.ret
        
    def findCondition(self, name):
        for c in self.conditions:
            if c.name == name:
                return c
        return None
    
    def compute(self, to_compare):
        ''' default to and operation '''
        if not isinstance(to_compare, dict):
            raise Exception("to_compare should be Dict type")
        ret = False
        if self.conj == 'or':
            ret = self.computeOr(to_compare)
        else:
            ret = self.computeAnd(to_compare)
        return ret

    def computeAnd(self, to_compare):
        # print "computeAnd enter"
        # print "conditions", self.conditions
        for c in self.conditions:
            if not c.name in to_compare:
                # print "%s not exist in %s"%(c.name, str(to_compare))
                return False
            
            ret_each = c.compute(to_compare[c.name])
            if ret_each is False:
                return False
        return True

    def computeOr(self, to_compare):
        # print "computeOr enter"
        # print "conditions", self.conditions
        for c in self.conditions:
            if not c.name in to_compare:
                return False
            ret_each = c.compute(to_compare[c.name])
            if ret_each is True:
                return True
        return False

def filter_model_version(input, model, version):
    ret = None
    if not input:
        return ret
    filters = json.loads(input)
    to_compare = {'model': model, 'version':version}
    # print "how many filters: ", len(filters['filters'])
    for filter_dict in filters['filters']:
        f = Filter(filter_dict)
        ret = f.getfilterResult(to_compare)
        if ret is not None:
            # print "not None", ret
            return ret
    return ret