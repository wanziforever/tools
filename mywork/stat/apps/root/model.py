#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import Base
from sqlalchemy import Column, String, Integer, BigInteger, Boolean


class Customer(Base):
    company = Column(String(64), nullable=False)
    url = Column(String(256))
    description = Column(String(512))
    address = Column(String(256))


class Role(Base):
    name = Column(String(32), nullable=False)
    customer_id = Column(BigInteger, nullable=False, index=True)


class User(Base):
    customer_id = Column(BigInteger, nullable=False, index=True)
    role_id = Column(BigInteger, nullable=False)
    name = Column(String(64), nullable=False)
    passwd = Column(String(128), nullable=False)
    nick_name = Column(String(32), nullable=False)
    phone = Column(String(32))
    email = Column(String(128), nullable=False, index=True)


class Asset(Base):
    customer_id = Column(Integer, nullable=False, index=True)
    file_size = Column(BigInteger, nullable=False)
    file_type = Column(String(16), nullable=False)
    asset_type = Column(String(32), nullable=False)
    file_key = Column(String(256), nullable=False)
    file_url = Column(String(256), nullable=False, default='')


class Modules(Base):
    customerId = Column(Integer, nullable=False, index=True)
    modules = Column(String(256), nullable = False)


class Permission(Base):
    module_name = Column(String(64), nullable=False)
    function_name = Column(String(64), nullable=False)
    customerId = Column(BigInteger)
    roleId = Column(BigInteger)
    permission = Column(Boolean, nullable=False)
