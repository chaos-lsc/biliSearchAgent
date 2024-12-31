import json
import requests

# 头部
headers = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"
}

def get(BV):
    # url地址
    url = f"https://api.bilibili.com/x/v2/reply/main?type=1&oid={BV}&mode=3"

    response = requests.get(url, headers=headers)
    html_str = response.content.decode()
 
    #print(url)
    import re

    # 假设你的长字符串存储在text变量中
    text = html_str
    """
    这里是你的长字符串，包含多个"message":"xxx"格式的数据。
    """

    # 正则表达式模式，匹配 "message":"任意字符" 直到遇到逗号或字符串结束
    #pattern = r'"message":"(.*?)(?=,|")'
    pattern = r'"message":"([^"]*)"'
    # 使用re.findall查找所有匹配项
    matches = re.findall(pattern, text)

    # 打印所有匹配的message内容
    count = 0
    result=matches
    for match in matches:
        #print(match)
        count += 1
    return matches

if __name__ == '__main__':
    print(get("BV12t4y1X7oA"))