# -*- coding: utf-8 -*-

import os
import logging
import inspect
import pymssql
import sys
# sys.setdefaultencoding('utf8')
# sys.path.append('../Srv_Hana2MSSQL')


class MSSQLDB(object):
    """
    SQLServer Database class
    """

    def __init__(self, host: str, user: str, password: str, database: str,port: str = '1433'):
        ''' Init MSSQLDB class '''
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database
        self.__connection = pymssql.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
            database=self.__database,
            charset='utf8',
            autocommit=True
        )

    def execute_sql(self, sql_str):
        ''' MSSQL database excute sql string '''
        try:
            cursor = self.__connection.cursor()
            # print(sql_str)
            cursor.execute(sql_str)
            self.__connection.commit()
            cursor.close()
        except Exception as e:
            self.__connection.rollback()
            raise e
            #raise Exception('%s\n%s' % (e.message,sql_str))
        # finally:
        #     self.__connection.close()

    def insert_many(self, sql_str, values):
        ''' MSSQL database insert many data '''
        try:
            cursor = self.__connection.cursor()
            # print(sql_str)
            cursor.executemany(sql_str, values)
            self.__connection.commit()
            cursor.close()
        except Exception as e:
            self.__connection.rollback()
            raise e
            # raise Exception('%s\n%s' % (e.message,sql_str))
        pass

    def do_query(self, sql_str) -> list:
        ''' MSSQL database query sql string '''
        try:
            cursor = self.__connection.cursor()
            # print(sql_str)
            cursor.execute(sql_str)
            data = cursor.fetchall()
            # print(type(data))
            return data
        except Exception as e:
            raise e
            # raise Exception('%s\n%s' % (e.message,sql_str))

    def disconnect(self):
        ''' MSSQL database disconnect '''
        try:
            if self.__connection:
                self.__connection.close()
        except Exception as e:
            raise e

    def connect(self):
        ''' MSSQL database disconnect '''
        try:
            self.__connection = pymssql.connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password,
                charset='utf8',
                autocommit=True)
        except Exception as e:
            raise e
