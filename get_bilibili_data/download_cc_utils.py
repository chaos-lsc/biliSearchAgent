import gzip, requests, json, time, urllib
import http.client
import random

bianma = 'utf-8'

he = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',}
User_Agent_List=[
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',},
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',},
{'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",},
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',},
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',},
{'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; M351 Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',},
{'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/31.0.1650.18 Mobile/11B554a Safari/8536.25',},
]
bili_jct="e1d595b90fe039950646f75a18ef3c0f"
sessdata="e0151c86%2C1752716091%2Ce98ba%2A11CjDZfECIT514IU_OXe1nU9sFo4b1cjvhscqW5Fd75hoOJHC3bbCm5BaZSTm3G8Nkp_0SVjdpczRRamlxWnN0aEwzeDg5Rk5ZSzRwWjdjOWdxZTRqazVyOUtjMDVWQVdGYXlSb3BfMHl0cXczRU0zZ3JIQnAwVjhuX2g4ako5VkFDVE1sY1BLMmJBIIEC"
buvid3="0BCB8828-F13D-AA28-84CB-BB7F354F0E4B79515infoc"
dedeuserid="292903223"
#my_credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3="你的 buvid3", dedeuserid="你的 DedeUserID", ac_time_value="你的 ac_time_value")

cookie = {"SESSDATA": f"{sessdata}",}
cookieDe = {"SESSDATA": "",}

from playwright.sync_api import sync_playwright
import pyperclip
import json

def run_get_cid(url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.get_by_text("{\"code\":0,\"message\":\"0\",\"ttl").click()
        page.locator("body").press("ControlOrMeta+a")
        page.locator("body").press("ControlOrMeta+c")
        # ---------------------
        context.close()
        browser.close()
    return pyperclip.paste()

def run_get_cc(url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.get_by_text("{ \"font_size\": 0.4, \"").click()
        time.sleep(0.2)
        page.locator("body").press("ControlOrMeta+a")
        page.locator("body").press("ControlOrMeta+c")
        # ---------------------
        context.close()
        browser.close()
    return pyperclip.paste()

def setCookie(ck):
    # cookie = {i.split("=")[0]:i.split("=")[1] for i in ck.split(";")}
    global cookie
    cookie = ck


def downAll(bv):
    '''
    传入BV号，下载该BV号下的全部字幕
    '''
    videoList = getVideoList(bv)
    p = 1
    cc_cc_text=""
    all_count=0
    for i in videoList:
        cid = i['cid']
        all_count+=1
        if(all_count>=5):
            break
        cc_cc_text+=downSolo(cid, bv, p, i['part'])
        cc_cc_text+=' \n'
        # 下载该P视频的字幕，part是单P视频名。
        #print ('【任务总进度：%s/%sP】\n'%(p,len(videoList)))
        p += 1
    return cc_cc_text
    #print ('\n\n*** 任务完成 ***\n')


def getVideoList(bv):
    '''
    传入BV号，返回该BV号的视频列表
    '''
    url = 'https://api.bilibili.com/x/player/pagelist?bvid=%s' % bv # 创建URL
    #print ('创建URL',url)
    he=random.choice(User_Agent_List)
    vl = requests.get(url,headers=he,cookies=cookie).json()
    videoList = vl['data']         # Json转换

    return videoList

from pprint import pprint
def downSolo(cid, bv, p, part=''):
    '''
    根据cid，下载单P里的全部语言字幕
    '''
    url = 'https://api.bilibili.com/x/player/wbi/v2?bvid=%s&cid=%s'%(bv,cid)
    #print (url)
    data = requests.get(url, headers=he, cookies=cookie).json()
    cc_type = 0
    subList = data['data']['subtitle']['subtitles']  # 字幕信息列表
    if len(subList) == 0:print('【警告】P%s无字幕！' % p)
    i = 1
    cc_cc_text=""
    for d in subList:
        lan = d['lan']  # 字幕的语言编号（ZH JP EN之类）
        name = bv + ' - P' + str(p) + '：' + rep(part) + ' - ' + lan  # 根据BV号、P数、语言，生成字幕文件名
        subUrl = 'http:' + d['subtitle_url']  # 字幕的URL

        # urllib.request.urlretrieve(subUrl,'%s.json' % name)   # 下载json字幕文件
        response = urllib.request.urlopen(subUrl)  # 不下载了，直接获取内容

        if response.info().get('Content-Encoding') == 'gzip':  # 在响应头中获取编码格式
            j = gzip.decompress(response.read())
        else:
            j = response.read()
        cc_cc_text += jsonToSrt(name, j)

        # print ('P%s 第%s种语言下载完成，进度：%s/%s'%(p,i,i,len(subList)))    #报告任务进度（以该P视频的字幕语言数算）
        i += 1
        time.sleep(0.2)

    return cc_cc_text

def jsonToSrt(fileName,j):
    '''
    传入文件名和json字幕内容，将json输出为Srt字幕文件
    '''

    data = json.loads(j)['body']
    #file = open('%s.srt'%fileName,'w',encoding=bianma)     # 创建srt字幕文件
    i = 1   # Srt字幕的序号计数器
    cc_cc_text=""
    for d in data:
        #f = round(d['from'],3)      # 开始时间 （round(n，3)四舍五入为三位小数）
        #t = round(d['to'],3)        # 结束时间
        c = d['content']            # 字幕内容
        cc_cc_text+=c
        cc_cc_text += " "
        #ff = time.strftime("%H:%M:%S",time.gmtime(f)) + ',' + miao(f)   # 开始时间，秒数转 时:分:秒 格式，加逗号、毫秒修正为三位
        #tt = time.strftime("%H:%M:%S",time.gmtime(t)) + ',' + miao(t)   # 结束时间，处理方式同上

        #srt = str(i) + '\n' + ff + ' ' + '-->' + ' ' + tt + '\n' + c + '\n\n'     # 格式化为Srt字幕
        #file.write(srt)             # 写入文件
        #i += 1                      # 计数器+1
    return cc_cc_text
    #file.close()
    #print ('%s OK.' % fileName)



li = [
    ['/','、'],
    ['\\','、'],
    ['|','、'],
    ['*','X'],
    [':','：'],
    ['?','？'],
    ['<','《'],
    ['>','》'],
    ['\"','“'],
    ['\"','”'],
]

def rep(s=''):
    '''
    根据列表li，去除特殊符号（不能用于文件名的）
    '''
    for i in li:
        s.replace(i[0],i[1])
    return s

def miao(miao):
    '''
    修正毫秒为三位
    '''
    miao = str(miao).partition('.')[2]    # 取小数部分
    miao += '0'*(3-len(miao))       # 补齐三位小数
    return miao
