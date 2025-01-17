from pprint import pprint

from get_bilibili_data import get_pages
from get_bilibili_data import get_cc
from get_bilibili_data import get_comment
import concurrent.futures
from tqdm import tqdm
def get(key, page_num):
    def process_page(page):
        video_data = page[0]
        BV = page[1]
        AV=page[2]
        try:
            cc = get_cc.get(BV)
        except:
            cc = "没有字幕"
        comment = get_comment.get(AV)
        return [video_data, cc, comment]

    datas = []
    pages = get_pages.get(key, page_num)

    # 使用tqdm创建进度条
    with tqdm(total=len(pages), desc="Processing") as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_page, page) for page in pages]
            for future in concurrent.futures.as_completed(futures):
                data = future.result()
                datas.append(data)
                # 每完成一个任务，进度条前进一格
                pbar.update(1)

    return datas
