# Author: Harold.Duan
# This module is sbo windows service implements.

__version__ = '0.0.1.dev'
__author__ = 'Harold.Duan'
__all__ = ['logger', 'run']

import inspect
import os
from os import path
import logging
from logging import Logger
import time
import xlrd
from xlrd.book import Book
from datetime import datetime
from shutil import copyfile, move
from db import new_mcp, Microphone


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


logger = _get_logger()


def _read_xls_file(folder_path: str, file_name: str) -> Microphone:
    ''' Read excel test '''
    try:
        file_path = os.path.join(folder_path,file_name)
        if file_path:
            (shortname, _) = os.path.splitext(file_name)
            xls_data = xlrd.open_workbook(file_path)
            # print(type(xls_data))
            # print(xls_data)
            tab_data = xls_data.sheet_by_index(0)
            # print(tab_data)
            # print(tab_data.ncols)
            # print(tab_data.nrows)
            # temp = tab_data.col_values(1)
            # print(temp)
            if tab_data.ncols >= 2 or tab_data.nrows >= 4:
                mcp = new_mcp()
                mcp.emodle = shortname
                i = 1
                while i < tab_data.ncols:
                    col_data = tab_data.col_values(i)
                    line = mcp.new_line()
                    line.freq = col_data[0]
                    line.lsen = col_data[1]
                    line.lthd = col_data[2]
                    line.lhd = col_data[3]
                    i += 1
                mcp.save()
                temp_info = ('File [%s] has %i rows data saved...\r' % (shortname,len(mcp.lines)))
                logger.info(temp_info)
            return xls_data
    except Exception as e:
        raise e


def __get_time_stamp() -> str:
    ''' Get current time stamp str '''
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    print(time_stamp)
    stamp = ("".join(time_stamp.split()[0].split(
        "-"))+"".join(time_stamp.split()[1].split(":"))).replace('.', '')
    return stamp


def _backup_xls_file(folder_path: str, file_name: str, backup_name: str):
    ''' Backup excel files '''
    try:
        if os.path.exists(folder_path):
            backup_dir = os.path.join(folder_path, 'Backups')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            source = os.path.join(folder_path, file_name)
            target = os.path.join(backup_dir, backup_name)
            # copyfile(source,target)
            move(source, target)
    except Exception as e:
        raise e


def __file_filter(f: str) -> bool:
    ''' Filter for files '''
    try:
        # (filepath,tempfilename) = os.path.split(f)
        (_, extension) = os.path.splitext(f)
        return (extension.upper() == '.XLS' or extension.upper() == '.XLSX')
    except Exception as e:
        raise e


def _do(folder_path: str):
    ''' Get excel datas '''
    try:
        files = []
        if folder_path:
            # temp = os.listdir(folder_path)
            # f = temp[0]
            # print(os.path.splitext(f)[-1][1:])
            # print(type(temp[0]))
            # files = list(filter(__file_filter,os.listdir(folder_path)))
            files = list(filter(lambda f: (os.path.splitext(f)[-1][1:].upper() == 'XLS'
                                           or os.path.splitext(f)[-1][1:].upper() == 'XLSX'), os.listdir(folder_path)))
        # print(files)
        is_err = False
        for f in files:
            try:
                # file_path = os.path.join(folder_path, f)
                temp_info = ('Start processing file [%s]...\r' % f)
                logger.info(temp_info)
                _read_xls_file(folder_path,f)
            except Exception as e:
                logger.exception(e)
                is_err = True
            finally:
                # fname = os.path.splitext(f)[0]
                # fext = os.path.splitext(f)[-1][1:]
                (fname, fext) = os.path.splitext(f)
                timestamp = __get_time_stamp()
                print(fname + '_error')
                # temp =
                backup_file = '%s_%s%s' % \
                    ((fname + '_error') if is_err else fname, timestamp, fext)
                _backup_xls_file(folder_path, f, backup_file)
                temp_info = ('Complete processed file [%s]!\r' % f)
                logger.info(temp_info)
    except Exception as e:
        raise e
    pass


def run():
    try:
        # mcp = new_mcp()
        # print(type(mcp.lines))
        # print(mcp.create_date)
        # line = mcp.new_line()
        # line.freq = 1.0
        # line.lsen = 2.0
        # line.lthd = 3.0
        # line.lhd = 4.0
        # line = mcp.new_line()
        # line.freq = 2.0
        # line.lsen = 4.0
        # line.lthd = 6.0
        # line.lhd = 8.0
        # mcp.save()
        # print(__get_time_stamp())
        _do('D:\\DEMO\\兴科迪')
    except Exception as e:
        logger.exception(e)
