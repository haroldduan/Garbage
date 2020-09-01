# Author: Harold.Duan
# This module is sbo windows service startup.

__version__ = "0.0.1.dev"
__author__ = "Harold.Duan"
# __all__ = []

import threading
import time
import uuid
from service import run, logger

TASKS = []
TASK_ID = ''


def task_do():
    while len(TASKS) > 0:
        try:
            TASK_ID = TASKS[0]
            logger.info("Task instance [%s] is running begin..." % TASK_ID)
            run()
        except Exception as e:
            logger.exception(e)
        finally:
            logger.info("Task instance [%s] is running end!\r\n" % TASK_ID)
            TASKS.remove(TASK_ID)
            TASK_ID = ''

def task_run():
    try:
        timer = threading.Timer(60, task_run)
        timer.start()
        TASKS.append(str(uuid.uuid1()))
        if not TASK_ID:
            task_do()
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    try:
        logger.info('Win sevice is starting...\r\n')
        timer = threading.Timer(60, task_run)
        timer.start()
    except Exception as e:
        logger.exception(e)