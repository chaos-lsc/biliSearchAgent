import requests
import time
import csv
import json
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'  # 改为自己的User-Agent
}


def get(video_id):
    comments = ""
    pages=5
    for page in range(pages):
        url = f'https://api.bilibili.com/x/v2/reply/main?next={page+1}&type=1&oid={video_id}&mode=3'
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()

                if data and 'data' in data and 'replies' in data['data']:
                    for comment in data['data']['replies']:
                        comment_info = {
                            '用户昵称': comment['member']['uname'],
                            '评论内容': comment['content']['message'],
                            '评论层级': '一级评论',
                            '性别': comment['member']['sex'],
                            '用户当前等级': comment['member']['level_info']['current_level'],
                            '点赞数量': comment['like'],
                            '回复时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment['ctime']))
                        }
                        comments +=(comment['content']['message']).strip().replace("\n",'')
                        comments+="\n"
            else:
                print(f'请求失败：{response.status_code}')
        except requests.RequestException as e:
            print(f"请求出错: {e}")

    return f"该视频的评论:{comments}"

def save_comments_to_csv(comments, video_id):
    with open(f'{video_id}.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file,
                                fieldnames=['用户昵称', '性别', '评论内容', '评论层级', '用户当前等级',
                                            '点赞数量', '回复时间'])
        writer.writeheader()
        for comment in comments:
            writer.writerow(comment)
