import requests
from logger import getLogger
logger=getLogger()

# 图片URL列表
image_urls = [
    # "https://dubbo.apache.org/imgs/user/dubbo-architecture-roadmap.jpg",
    #         "https://dubbo.apache.org/imgs/architecture.png",
            "https://dubbo.apache.org/imgs/user/dubbo-properties-override.jpg",
            "https://dubbo.apache.org/imgs/user/dubbo-config-override.jpg",
            "https://dubbo.apache.org/imgs/user/stub.jpg",
            "https://dubbo.apache.org/imgs/dev/consistent-hash.jpg",
            "https://dubbo.apache.org/imgs/dev/consistent-hash-invoker.jpg",
            "https://dubbo.apache.org/imgs/dev/consistent-hash-data-incline.jpg"
    # 添加更多图片URL
]

# 指定保存图片的目录
save_directory = "downloaded_images/"

# 循环遍历图片URL列表
for i, image_url in enumerate(image_urls):
    # 发送GET请求获取图片数据
    response = requests.get(image_url)

    # 检查响应状态码，确保请求成功
    if response.status_code == 200:
        # 从响应中获取图片数据
        image_data = response.content

        # 构造保存图片的文件路径
        file_name = f"image_{i + 1}.jpg"  # 可以根据需要修改文件名
        file_path = save_directory + file_name

        # 保存图片到本地文件
        with open(file_path, "wb") as image_file:
            image_file.write(image_data)
        logger.info(f"图片 {file_name} 已下载并保存")

    else:
        logger.error(f"下载失败，HTTP状态码 ({i + 1}): {response.status_code}")

logger.info("所有图片已下载完成")
