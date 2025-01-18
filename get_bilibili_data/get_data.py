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
    result=[]
    for page in pages:
        try:
            BV = page[1]
            is_useful=page[3]
            if(is_useful==True):
                try:
                    cc = download_cc.get(BV)  # 第一种CC
                except:
                    CCFailCount += 1
                #tmp=cc
                #cc=handle_cc.handle(cc)
                #if(cc==-1):
                #    cc=tmp
                page[4]=page[4].replace("\\","")
                result.append(f'{f"视频名:{page[4]}",f"BV号:{page[1]}",f"内容:{cc}"}')
        except:
            print(f"FailCount:{FailCount}")
            FailCount+=1
    return result
#from pprint import pprint
#pprint(get("七岁的理想",3))