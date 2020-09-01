# -*- coding: utf-8 -*-
# Author: Harold.Duan
# This module is sbo windows service implements.

from typing import List
__version__ = '0.0.1.dev'
__author__ = 'Harold.Duan'
__all__ = ['conf', 'database', 'new_mcp']

import sys
import json
import os
from os import path
from datetime import datetime, date
from db.mssql import MSSQLDB


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


conf = _get_conf()
database = MSSQLDB(conf['db_server'], conf['db_user'],
                   conf['db_passwd'], conf['db_company'])


class MicrophoneLine(object):
    ''' Class Microphone Line define '''

    def __init__(self, docentry: int, line_id: int):
        ''' Constructor '''
        self.__docentry: int = 0
        self.__line_id: int = -1
        self.__freq: float = 0.0
        self.__lsen: float = 0.0
        self.__lthd: float = 0.0
        self.__lhd: float = 0.0
        if docentry > 0:
            self.__docentry = docentry
        if line_id > 0:
            self.__line_id = line_id

    @property
    def docentry(self) -> int:
        return self.__docentry

    @property
    def line_id(self) -> int:
        return self.__line_id

    @property
    def freq(self) -> float:
        return self.__freq

    @freq.setter
    def freq(self, value: float):
        self.__freq = value

    @property
    def lsen(self) -> float:
        return self.__lsen

    @lsen.setter
    def lsen(self, value: float):
        self.__lsen = value

    @property
    def lthd(self) -> float:
        return self.__lthd

    @lthd.setter
    def lthd(self, value: float):
        self.__lthd = value

    @property
    def lhd(self) -> float:
        return self.__lhd

    @lhd.setter
    def lhd(self, value: float):
        self.__lhd = value


MicrophoneLines = List[MicrophoneLine]


class Microphone(object):
    ''' Class Microphone define '''

    def __init__(self, docentry: int):
        ''' Constructor '''
        try:
            self.__docentry: int = 0
            self.__create_date: date = datetime.today()
            self.__emodle: str = ''
            self.__inpeople: str = 'U009'
            self.__remarks: str = 'Test'
            self.__lines: MicrophoneLines = []
            if docentry > 0:
                self.__docentry = docentry
        except Exception as e:
            raise e

    @property
    def docentry(self) -> int:
        return self.__docentry

    @property
    def create_date(self) -> date:
        return self.__create_date

    @create_date.setter
    def create_date(self, value: date):
        self.__create_date = value

    @property
    def emodle(self) -> str:
        return self.__emodle

    @emodle.setter
    def emodle(self, value: str):
        self.__emodle = value

    @property
    def inpeople(self) -> str:
        return self.__inpeople

    @inpeople.setter
    def inpeople(self, value: str):
        self.__inpeople = value

    @property
    def remarks(self) -> str:
        return self.__remarks

    @remarks.setter
    def remarks(self, value: str):
        self.__remarks = value

    @property
    def lines(self) -> MicrophoneLines:
        try:
            return self.__lines
        except Exception as e:
            raise e

    def new_line(self) -> MicrophoneLine:
        ''' New MicrophoneLine in lines '''
        try:
            line = MicrophoneLine(self.docentry, len(self.lines) + 1)
            self.lines.append(line)
            return line
        except Exception as e:
            raise e

    def __insert_parent_record(self):
        ''' Insert parent record - Microphone '''
        try:
            sql_insert_parent = "insert into \"@AVA_TEST_MKF1\" (DocEntry,DocNum,Period,Instance,Series,Handwrtten,Canceled,Object,\
LogInst,UserSign,Transfered,Status,DataSource,RequestStatus,Creator,\
U_Cdate,U_Emodle,U_Inpeople,U_Rmark) \
values (%i,%i,56,0,-1,'N','N','AVA_TETS_MKF',\
null,'40','N','O','I','W','U009',\
'%s','%s','%s','%s')"
            sql_insert_parent = sql_insert_parent % \
                (self.docentry,self.docentry,str(self.create_date)[0:-3],self.emodle,self.inpeople,self.remarks)
            # print(sql_insert_parent)
            # print(str(self.create_date)[0:-3])
            database.execute_sql(sql_insert_parent)
        except Exception as e:
            raise e

    def __insert_child_records(self):
        ''' Insert child record - MicrophoneLine '''
        try:
            sql_insert_child = "insert into \"@AVA_TEST_MKF2\" (DocEntry,LineId,VisOrder,Object,U_Freq,U_LSen,U_LTHD,U_LHD) \
values (%s,%s,%s,%s,%s,%s,%s,%s)"
            values = [(x.docentry,x.line_id,x.line_id - 1,'AVA_TETS_MKF',x.freq,x.lsen,x.lthd,x.lhd) for x in self.lines if len(self.lines) > 0]
            database.insert_many(sql_insert_child,values)
        except Exception as e:
            raise e

    def __update_key(self):
        ''' Update ONNM key record '''
        try:
            sql_update_key = "update ONNM set AutoKey = %i where ObjectCode = 'AVA_TETS_MKF' "
            sql_update_key = sql_update_key % (self.docentry + 1)
            database.execute_sql(sql_update_key)
        except Exception as e:
            raise e


    def save(self):
        ''' Save data '''
        try:
            self.__insert_parent_record()
            self.__insert_child_records()
            self.__update_key()
        except Exception as e:
            raise e
        finally:
            pass


def new_mcp() -> Microphone:
    ''' New Microphone instance '''
    try:
        sql_next_entry = "select AutoKey from ONNM where ObjectCode = 'AVA_TETS_MKF '"
        next_entry = database.do_query(sql_next_entry)
        docentry = 1
        if len(next_entry) > 0:
            docentry = next_entry[0][0]
        # print(docentry)
        return Microphone(docentry)
    except Exception as e:
        raise e
