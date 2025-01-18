import tkinter,threading,get_cc_utils          #载入模块
import browser_cookie3
import ctypes
ctypes.windll.shell32.IsUserAnAdmin()
get_cc_utils.cookie = browser_cookie3.firefox()
import os
import re
import time
from bilibili_api import *
from bilibili_api import Credential
bili_jct="e1d595b90fe039950646f75a18ef3c0f"
sessdata="e0151c86%2C1752716091%2Ce98ba%2A11CjDZfECIT514IU_OXe1nU9sFo4b1cjvhscqW5Fd75hoOJHC3bbCm5BaZSTm3G8Nkp_0SVjdpczRRamlxWnN0aEwzeDg5Rk5ZSzRwWjdjOWdxZTRqazVyOUtjMDVWQVdGYXlSb3BfMHl0cXczRU0zZ3JIQnAwVjhuX2g4ako5VkFDVE1sY1BLMmJBIIEC"
buvid3="0BCB8828-F13D-AA28-84CB-BB7F354F0E4B79515infoc"
dedeuserid="292903223"
credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3="你的 buvid3", dedeuserid="你的 DedeUserID", ac_time_value="你的 ac_time_value")
def get_old(BV):
    get_cc_utils.downAll(BV)
    files_and_dirs = os.listdir('.')
    matched_files = [f for f in files_and_dirs if os.path.isfile(f) and BV in f]
    cc_text=""
    for file in matched_files:
        cc_file=open(file,"r+",encoding='utf-8')
        tmp=cc_file.read()
        chinese_text = re.findall(r'[\u4e00-\u9fff]+', tmp)
        for text in chinese_text:
            cc_text+=text
            cc_text+=" "
        cc_file.close()
        os.remove(file)
    return  cc_text
def get(BV):
    v = video.Video(BV)  # 初始化视频对象
    sync(ass.make_ass_file_danmakus_protobuf(
        credential=credential,
        obj=v,  # 生成弹幕文件的对象
        page=0,  # 哪一个分 P (从 0 开始)
        out=f"{BV}.ass"  # 输出文件地址
    ))
    file=open(f"{BV}.ass","r+",encoding='utf-8')
    cc_text=""
    tmp=file.read()
    chinese_text = re.findall(r'[\u4e00-\u9fff]+', tmp)
    for text in chinese_text:
        cc_text += text
        cc_text += " "
    file.close()
    return cc_text


