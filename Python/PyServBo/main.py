# Author: Harold.Duan
# This module is sbo windows service startup.

__version__ = "0.0.1.dev"
__author__ = "Harold.Duan"
# __all__ = []

from service import run

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(e)