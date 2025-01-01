import asyncio
from bilibili_api import video
from bilibili_api import video, ass
import os
from bilibili_api import Credential
#bili_jct:"ee73c0bef8b7c4336d449c9331da9282"
#SESSDATA:"a208c850%2C1751273365%2Cb0771%2A12CjBowBZHhLkjf46o6a465wlyy28hL-qPNn73crACA57n_Q0PwrEjgH-WGMA-f7w60VQSVlR4cWdlMU5pY21HUUlnYVU2ZUZiVW43eFpWSVFaQi10TFd0aWhkd0w2R29RQ2p0OXRlY3F2TGZ0Z1o0RGFGckJsOVNtNVFEczRTWGhEXzFucTg3THBBIIEC"
credential = Credential(sessdata="a208c850%2C1751273365%2Cb0771%2A12CjBowBZHhLkjf46o6a465wlyy28hL-qPNn73crACA57n_Q0PwrEjgH-WGMA-f7w60VQSVlR4cWdlMU5pY21HUUlnYVU2ZUZiVW43eFpWSVFaQi10TFd0aWhkd0w2R29RQ2p0OXRlY3F2TGZ0Z1o0RGFGckJsOVNtNVFEczRTWGhEXzFucTg3THBBIIEC")


async def download(BV) -> None:
    # 实例化 Video 类
    v = video.Video(bvid=BV)
    await ass.make_ass_file_subtitle(obj=v, out="tmp.ass",credential=credential)
    cc_file=open("tmp.ass","r+",encoding='utf-8')
    cc=cc_file.read()
    cc_file.close()
    os.remove("tmp.ass")
    return cc

def get(BV):
    cc=asyncio.run(download(BV))
    return cc
#print(get("BV1uH22YMEoR"))
