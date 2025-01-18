from langgraph.types import PregelTask
import requests
import winreg as reg
import winreg
import ctypes
import os
import sys

# 获取当前工作目录
current_dir = os.getcwd()
sys.path.append(current_dir)
import os
import sys

# 获取当前工作目录
current_dir = os.getcwd()
sys.path.append(f"{current_dir}\\get_bilibili_data")
import get_pages
import random
import download_cc

def get(key,page_num):
    FailCount = 0
    CCFailCount = 0
    pages = get_pages.get(key, page_num)
    result=""
    for page in pages:
        try:
            BV = page[1]
            is_useful=page[3]
            if(is_useful==True):
                try:
                    cc = download_cc.get(BV)  # 第一种CC
                except:
                    CCFailCount += 1
                    print(f"FailCountf:{CCFailCount}")
                try:
                    print(cc)
                except:
                    print("CC FAIL")
                    cc=""
                result+=f"{page[0]} {cc}"
                result += "\n"
        except:
            print(f"FailCount:{FailCount}")
#get("七岁的理想",5)