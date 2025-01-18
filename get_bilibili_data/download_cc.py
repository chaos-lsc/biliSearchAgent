import tkinter,threading,download_cc_utils          #载入模块
import browser_cookie3

download_cc_utils.cookie = browser_cookie3.firefox()



def get(BV):
    cc_text=download_cc_utils.downAll(BV)
    return cc_text

#print(get("BV11T42117FY"))