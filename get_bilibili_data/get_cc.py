import tkinter,threading,get_cc_utils          #载入模块
import browser_cookie3
import ctypes
ctypes.windll.shell32.IsUserAnAdmin()
get_cc_utils.cookie = browser_cookie3.firefox()
import os
import re
def get(BV):
    get_cc_utils.downAll(BV)
    files_and_dirs = os.listdir('.')
    matched_files = [f for f in files_and_dirs if os.path.isfile(f) and BV in f]
    cc_text=""
    for file in matched_files:
        print(file)
        cc_file=open(file,"r+",encoding='utf-8')
        tmp=cc_file.read()
        chinese_text = re.findall(r'[\u4e00-\u9fff]+', tmp)
        for text in chinese_text:
            cc_text+=text
            cc_text+=" "
        cc_file.close()
        os.remove(file)
    return  cc_text
