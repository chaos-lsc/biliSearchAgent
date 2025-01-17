import json
from bilibili_api import search
from collections import Counter
import datetime
from bilibili_api import comment, Credential
from bilibili_api.comment import CommentResourceType, OrderType
from typing import List
from aiohttp.client_exceptions import ClientError, ClientOSError
import asyncio
my_sessdata="a208c850%2C1751273365%2Cb0771%2A12CjBowBZHhLkjf46o6a465wlyy28hL-qPNn73crACA57n_Q0PwrEjgH-WGMA-f7w60VQSVlR4cWdlMU5pY21HUUlnYVU2ZUZiVW43eFpWSVFaQi10TFd0aWhkd0w2R29RQ2p0OXRlY3F2TGZ0Z1o0RGFGckJsOVNtNVFEczRTWGhEXzFucTg3THBBIIEC"
my_bili_jct="ee73c0bef8b7c4336d449c9331da9282"

# https://github.com/Nemo2011/bilibili-api

from bilibili_api import settings

# settings.proxy = "http://127.0.0.1:10080" # 里头填写你的代理地址

# settings.proxy = "http://username:password@your-proxy.com" # 如果需要用户名、密码

# 定义重试装饰器


def retry_request(retries=5, delay=1.0, backoff=1.5):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            nonlocal delay
            attempts = 0
            while attempts < retries:
                try:
                    return await func(*args, **kwargs)
                except (ClientOSError, ClientError) as e:
                    attempts += 1
                    if attempts >= retries:
                        print(f"重试 {retries} 次后失败，不再重试。")
                        raise e
                    print(f"请求失败，{delay}秒后尝试第{attempts + 1}次重试...")
                    await asyncio.sleep(delay)
                    delay *= backoff

        return wrapper

    return decorator


async def get_video_detail_info(keyword: str, page: int):
    result = await search.search(keyword=keyword,
                                 page=page)
    print(f"result: {json.dumps(result, indent=4)}")
    return json.dumps(result)


async def fetch_comments(oid, page_start, page_end):
    type_ = CommentResourceType.VIDEO  # 视频类型
    order = OrderType.TIME  # 按发布时间倒序

    credential = Credential(
        sessdata=my_sessdata,
        bili_jct=my_bili_jct,
        buvid3="",
        dedeuserid="", )

    comments_list = []  # 初始化列表用于存储所有评论的内容

    # 循环遍历指定页码范围
    for page_index in range(page_start, page_end + 1):
        try:
            response = await comment.get_comments(oid, type_, page_index, order, credential=credential)
            # 检查是否有评论或评论是否为空
            if 'replies' not in response or not response['replies']:
                continue  # 如果某一页没有评论，跳过当前循环

            comments_data = response['replies']
            for context in comments_data:
                message = context['content']['message']  # 获取评论内容
                comments_list.append(message)  # 将评论内容添加到列表中
        except Exception as e:
            # 打印错误信息并继续执行
            print(f"An error occurred on page {page_index}: {str(e)}")
            continue  # 发生异常时跳过当前页继续下一页

    return comments_list  # 返回存储评论内容的列表



async def process_search_results(results):
    data_to_write = []

    # 遍历结果
    for result in results:
        if result['data']:  # 检查data列表是否非空
            for item in result['data']:
                tags = item.get('tag', '').split(',')

                oid = item.get('aid', 0),  # 假设视频ID存储在'aid'字段

                comments = ''
                # comments = await fetch_comments(oid, 1, 30)  # 异步获取评论

                processed_data = [
                    item.get('type', '未知类型'),
                    item.get('author', '未知作者'),
                    item.get('typename', '未知分类'),
                    item.get('arcurl', '无链接'),
                    item.get('title', '无标题').replace(
                        '<em class="keyword">', '').replace('</em>', ''),
                    item.get('description', '无描述'),
                    item.get('play', 0),
                    item.get('video_review', 0),
                    item.get('favorites', 0),
                    ', '.join(tags),
                    item.get('comment', 0),
                    comments,
                    datetime.datetime.fromtimestamp(
                        item.get('pubdate', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                ]

                # 获取完整的单个视频信息内容
                headers = ["类型", "作者", "分类", "视频链接", "标题", "描述", "播放量", "弹幕数", "收藏数", "标签",
                           "发布日期", "评论"]

                result_text = '\n'.join(
                    f"{header}: {data}" for header, data in zip(headers, processed_data))

                data_to_write.append(result_text)

    return json.dumps(data_to_write, ensure_ascii=False)


# @retry_request(retries=5, delay=1, backoff=1.5)
async def bilibili_detail_pipiline(keywords: List, page: int):
    all_results = []  # 初始化一个列表来存储所有关键词和页面的结果
    get_result=[]
    for keyword in keywords:  # 遍历关键词

        keyword_results = []

        for page in range(page):  # 循环从第1页到第10页
            # 根据关键字和页数获取页面中信息
            result = await search.search(keyword=keyword, page=page)
            # print(f"result: {json.dumps(result, indent=4, ensure_ascii=False)}")
            # 根据result字段获取详细信息
            keyword_results.extend(result.get('result', []))  # 累积当前关键词的所有页面的结果

            real_data = await process_search_results(keyword_results)

            all_results.append({
                "keyword": keyword,
                "real_data": real_data
            })
        import re
        #print(len(real_data.split("类型")))
        pages=real_data.split("类型")

        for page in pages:
            pattern = r'视频链接: ([^"]*)\\n标题'
            matches = re.findall(pattern, page)
            if(len(matches)>=1):
                try:
                    AV = matches[0].replace("http://www.bilibili.com/video/av", "")
                    BV = abv_switch.av2bv(int(AV))
                    AV=int(AV)
                    get_result.append([page, BV,AV])
                except:
                    continue
        return get_result

from pprint import pprint
from get_bilibili_data import abv_switch
def get_pages(key_word,page):
    if(len(key_word)<=6):
        key_word+=key_word
    import asyncio
    # asyncio.run(get_video_detail_info(keyword="ChatGLM3-6B模型的本地部署", page=1))
    get_result=asyncio.run(bilibili_detail_pipiline(keywords=[key_word],
                                         page=page))
    return get_result

from pprint import pprint
if __name__ == '__main__':
    pprint(get("神经网络",1))