import requests
import json
from logger import getLogger
from MatchInfo import MatchInfo 
from PicInfo import PicInfo 
import yaml
logger=getLogger()

# 读取配置文件
config=None
with open("config.yml", "r", encoding="utf-8") as yaml_file:
    config = yaml.safe_load(yaml_file)
yaml_file.close()
picgo_server_url=config["migrate"]["picgo"]["server_url"]
result_filepath = config["scan"]["match"]["result_filepath"]

def uploadByPicgo(matchInfo):
    name=matchInfo.filepath
    logger.info(f"{name}: 开始上传")
    picInfoList=[]
    #改为单个图片上传
    for pic in matchInfo.picUrls:
        data={
            "list":[pic]
        }
        res=requests.post(picgo_server_url,json=data)
        resObj=json.loads(res.text)
        if res.status_code!=200 or resObj["success"]==False:
            logger.error(f"{name}: 上传失败,{pic}, {res.text}")
            continue
        logger.info(f"{name}: 上传成功,{pic}, {res.text}")
        newPic=resObj["result"][0]
        picInfo=PicInfo(pic,newPic)
        picInfoList.append(picInfo)
    return picInfoList

# 反序列化
output_file = open(result_filepath, "r", encoding="utf-8")

load_data=json.load(output_file)
matches=[MatchInfo.from_dict(data) for data in load_data]
logger.info("开始执行, 可能会耗费较长时间, 请勿关闭程序!!")
picCnt=0
# 按文件分组上传图片并替换原始url
for match in matches:
    # 上传文件内所有图片
    picInfoList=uploadByPicgo(match)
    if len(picInfoList)==0:
        continue
    # 批量替换
    with open(match.filepath, "r", encoding="utf-8") as f:
        content = f.read()
        # 匹配的是markdown格式, 上传返回也是markdown格式, 所以直接替换
        for picInfo in picInfoList:
            content=content.replace(picInfo.oldPic, picInfo.newPic)
        with open(match.filepath, "w", encoding="utf-8") as ff:
            ff.write(content)
        ff.close()
        logger.info(f"{match.filepath}: 替换完成")
        picCnt+=len(picInfoList)
    f.close()
logger.info(f"{picCnt}个图片替换完成!!")