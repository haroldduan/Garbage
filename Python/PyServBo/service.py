# Author: Harold.Duan
# This module is sbo windows service implements.

__version__ = "0.0.1.dev"
__author__ = "Harold.Duan"
__all__ = ['logger', 'run']

import os
from os import path
# import sys
# sys.path.append(path.abspath(path.dirname(__file__)))
import inspect
import logging
from logging import Logger
import time
import json
from decimal import Decimal
from sqlalchemy import Column, String, DECIMAL, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import Schema, fields, post_load
from requests import request, post


def _get_logger(name='service') -> Logger:
    ''' Get logging Logger instance '''
    try:
        str_time = time.strftime('%Y%m%d', time.localtime())
        log_name = 'service_%s.log' % str_time
        # log_name = '%s.log' % name
        logger = logging.getLogger('[%s_log]' % name)
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = path.abspath(path.dirname(this_file))
        folder_path = path.join(dirpath, 'LOG')
        if not path.exists(folder_path):
            os.makedirs(folder_path)
        handler = logging.FileHandler(
            path.join(folder_path, log_name), encoding='utf-8')
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    except Exception as ex:
        print(ex)


def _get_conf() -> dict:
    ''' get configuration info by conf '''
    try:
        cur_path = path.abspath(path.dirname(__file__))
        cur_path = os.path.join(cur_path, 'conf.json')
        # print(cur_path)
        if not cur_path:
            raise Exception('Conf file path is invalid!')
        if not os.path.exists(cur_path):
            raise Exception('Conf file is not exist!')
        # ret_val = Configuration()
        with open(cur_path, 'r') as f:
            ret_val = json.load(f)
        return ret_val
    except Exception as e:
        raise e


Base = declarative_base()


class Item(Base):
    ''' define class Revaluation Item '''

    def __init__(self):
        """ constructor """
        # self.__item_code = ''
        # self.__warehouse = ''
        # self.__price = 0.0
        # self.__price_diff = 0.0

    # @property
    # def item_code(self) -> str:
    #     return self.__item_code

    # @item_code.setter
    # def item_code(self, value: str):
    #     self.__item_code = value

    # @property
    # def warehouse(self) -> str:
    #     return self.__warehouse

    # @warehouse.setter
    # def warehouse(self, value: str):
    #     self.__warehouse = value

    # @property
    # def price_diff(self) -> float:
    #     return self.__price_diff

    # @price_diff.setter
    # def price_diff(self, value: float):
    #     self.__price_diff = value

    # @property
    # def price(self) -> float:
    #     return self.__price

    # @price.setter
    # def price(self, value: float):
    #     self.__price = value

    __tablename__ = "AVA_IM_OPRC"

    item_code = Column('ItemCode', String(50), primary_key=True)
    warehouse = Column('Warehouse', String(8), primary_key=True)
    price = Column('Price', DECIMAL(19, 6))
    price_diff = Column('PriceDiff', DECIMAL(19, 6))


class ItemSchema(Schema):
    ''' define Items serializable schema class '''
    item_code = fields.String(load_from='item_code', dump_to='item_code')
    warehouse = fields.String(
        load_from='warehouse_code', dump_to='warehouse_code')
    price = fields.Decimal(load_from='price', dump_to='price',
                           default=None, allow_none=True, as_string=True)
    price_diff = fields.Decimal(
        load_from='price_diff', dump_to='price_diff', default=None, allow_none=True, as_string=True)


class Revaluation(object):
    ''' define class Revaluation '''

    def __init__(self):
        """ constructor """
        self.__company_db = ''
        self.__items = []

    @property
    def company_db(self) -> str:
        return self.__company_db

    @company_db.setter
    def company_db(self, value: str):
        self.__company_db = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value: list):
        self.__items = value


class RevaluationSchema(Schema):
    ''' define Revaluation serializable schema class '''
    company_db = fields.String(load_from='company_db', dump_to='company_db')
    items = fields.Nested(ItemSchema, dump_to='items',
                          many=True, allow_none=True)


_conf = _get_conf()
logger = _get_logger()


def _get_reval_datas() -> str:
    try:
        str_driver = 'mssql+pymssql://%s:%s@%s/%s' % \
            (_conf['db_user'], _conf['db_passwd'],
             _conf['db_server'], _conf['db_company'])
        engine = create_engine(str_driver, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        items = session.query(Item).all()
        reval = Revaluation()
        reval.company_db = _conf['db_company']
        reval.items = items
        schema = RevaluationSchema()
        ret_val = schema.dumps(reval, ensure_ascii=False)
        return ret_val
    except Exception as e:
        raise e
    pass


def run():
    try:
        url = _conf['api_addr']
        json_data = _get_reval_datas()
        temp = 'Get datas from [%s]:\r[\r%s\r]\rSent to [%s]...\r' % \
            (_conf['db_company'], json_data, url)
        logger.info(temp)
        head = {'Content-Type': 'application/json'}
        ret = post(url=url, data=json_data, headers=head)
        if ret.status_code == 200:
            ret_val = ret.json()
        else:
            ret_val = {'code': 999,
                       'message': 'WebAPI is invalid!', 'data': ''}
        temp = 'Receipt datas from [%s]:\r[\r%s\r]!\r\n' % \
            (url, ret_val)
        logger.info(temp)
    except Exception as e:
        logger.exception(e)


run()
