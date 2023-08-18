import os
import re
import requests
import json
from logger import getLogger
from MatchInfo import MatchInfo 
logger=getLogger()

picgoServerUrl="http://127.0.0.1:36677/upload"
def uploadByPicgo(matchInfo):
    name=matchInfo.filepath
    data={
        "list":matchInfo.picUrls
    }
    logger.info(f"{name}: 开始上传")
    res=requests.post(picgoServerUrl,json=data)
    resObj=json.loads(res.text)
    if res.status_code!=200 or resObj["success"]==False:
        logger.error(f"{name}: 上传失败, {res}")
        return False
    logger.info(f"{name}: 上传成功, {res.text}")
    return resObj["result"]

# 反序列化
output_file = open("output.json", "r", encoding="utf-8")

load_data=json.load(output_file)
matches=[MatchInfo.from_dict(data) for data in load_data]
logger.info("开始执行, 可能会耗费较长时间, 请勿关闭程序!!")
# 按文件分组上传图片并替换原始url
for match in matches:
    # 上传文件内所有图片
    picsNew=uploadByPicgo(match)
    if picsNew==False:
        continue
    # 批量替换
    with open(match.filepath, "r", encoding="utf-8") as f:
        content = f.read()
        for search_text, replace_text in zip(match.picUrls, picsNew):
            content=content.replace(search_text, replace_text)
        with open(match.filepath, "w", encoding="utf-8") as ff:
            ff.write(content)
        ff.close()
        logger.info(f"{match.filepath}: 替换完成")
    f.close()
logger.info("全部替换完成!!")