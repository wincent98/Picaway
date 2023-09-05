import os
import re
import argparse
import requests
import json
from logger import getLogger
from MatchInfo import MatchInfo 
import yaml
logger=getLogger()

# 读取配置文件
config=None
with open("config.yml", "r", encoding="utf-8") as yaml_file:
    config = yaml.safe_load(yaml_file)
yaml_file.close()
directory = config["scan"]["directory"]
md_regex=re.compile(config["scan"]["match"]["md_regex"])
pic_regex = re.compile(config["scan"]["match"]["pic_regex"])
result_filepath = config["scan"]["match"]["result_filepath"]
# 打开输出文件
output_file = open(result_filepath, "w", encoding="utf-8")
matches=[]
# 遍历目录下的所有文件和子目录
for root, dirs, files in os.walk(directory):
    for filename in files:
        # 如果是Markdown文件，读取内容并匹配图片链接
        if md_regex.match(filename):
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                picUrls = pic_regex.findall(content)
                if len(picUrls)>0:
                    matchInfo=MatchInfo(filepath,picUrls)
                    matches.append(matchInfo)
# 序列化对象列表为 JSON
serialized_list = [match.to_dict() for match in matches]
json.dump(serialized_list,output_file,indent=4,ensure_ascii=False)
# 关闭输出文件
output_file.close()
logger.info("图片扫描完成, 请检查是否有不需要迁移的图片, 然后再执行migrate脚本上传")