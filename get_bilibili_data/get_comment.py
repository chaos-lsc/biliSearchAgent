import json
import aiohttp
import asyncio
import re


async def get(BV):
    # url地址
    url = f"https://api.bilibili.com/x/v2/reply/main?type=1&oid={BV}&mode=3"
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_str = await response.text()

    # 正则表达式模式，匹配 "message":"任意字符" 直到遇到逗号或字符串结束
    pattern = r'"message":"([^"]*)"'
    # 使用re.findall查找所有匹配项
    matches = re.findall(pattern, html_str)

    # 打印所有匹配的message内容
    count = 0
    result = matches
    for match in matches:
        count += 1
    return matches


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    matches = loop.run_until_complete(get("BV12t4y1X7oA"))
    print(matches)