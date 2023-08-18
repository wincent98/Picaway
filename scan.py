import os
import re
import argparse
import requests
import json
from logger import getLogger
from MatchInfo import MatchInfo 
logger=getLogger()



# # 创建 ArgumentParser 对象
# parser = argparse.ArgumentParser()

# # 添加参数
# parser.add_argument('--dir', help='需要扫描的目录路径')

# # 解析参数
# args = parser.parse_args()

# # 获取参数值
# directory = args.dir
directory = 'C:\\Users\\admin\\AppData\\Local\\YNote\\Data\\'
# directory='./'
# 匹配Markdown文件的正则表达式
md_regex = re.compile(r".*\.md$")

# 匹配图片链接的正则表达式
# img_regex = re.compile(r"!\[.*\]\((.*?)\)")
img_regex = re.compile(r"!\[.*?\]\((.*?(?:sinaimg\.cn).*?)\)")

# 打开输出文件
output_file = open("output.json", "w", encoding="utf-8")
matches=[]
# 遍历目录下的所有文件和子目录
for root, dirs, files in os.walk(directory):
    for filename in files:
        # 如果是Markdown文件，读取内容并匹配图片链接
        if md_regex.match(filename):
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                picUrls = img_regex.findall(content)
                if len(picUrls)>0:
                    matchInfo=MatchInfo(filepath,picUrls)
                    matches.append(matchInfo)
# matches_sorted=sorted(matches,key=lambda item:item.url)
# for match in matches:
#     output_file.write(match.toString() + "\n")
# 序列化对象列表为 JSON
serialized_list = [match.to_dict() for match in matches]
json.dump(serialized_list,output_file,indent=4,ensure_ascii=False)
# 关闭输出文件
output_file.close()
logger.info("图片扫描完成, 请检查是否有不需要迁移的图片, 然后再执行migrate脚本上传")

        