import get_data
from pprint import pprint
key="深度学习"
page=1
datas=get_data.get(key,page)
pprint(datas)
# file=open("sample.txt","w+",encoding='utf-8')
# file.write(f"{datas}")
# file.flush()
