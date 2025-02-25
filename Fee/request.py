import requests
import os
import time
import mimetypes

base_url = ""

# 保存路径
save_dir = "./download"  # 保存目录


# 下载文件
def download_file(url):
    try:
        # 发送 GET 请求
        response = requests.get(url, stream=True)

        # 检查响应状态码
        if response.status_code == 200:
            # 获取文件的 MIME 类型
            content_type = response.headers.get("content-type")
            if not content_type:
                raise ValueError("无法获取文件的 MIME 类型")

            # 根据 MIME 类型获取文件扩展名
            extension = mimetypes.guess_extension(content_type)
            if not extension:
                raise ValueError("无法确定文件的扩展名")

            file_name = "file_"
            if extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]:
                file_name = "image_"
            elif extension in [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".mpg", ".mpeg"]:
                file_name = "video_"
            file_name = f"{file_name}{str(int(time.time()))}{extension}"

            # 构建完整的保存路径
            save_path = os.path.join(save_dir, file_name)

            # 确保保存目录存在
            os.makedirs(save_dir, exist_ok=True)

            # 打开文件并写入内容
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            # 返回文件的完整本地路径
            return os.path.abspath(save_path)
        else:
            # 处理非 200 状态码的情况
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"请求发生异常: {e}")
        return None
    except ValueError as e:
        # 处理 MIME 类型和扩展名相关的问题
        print(f"发生错误: {e}")
        return None


# def get_info():
#     try:
#         # 发送 GET 请求
#         response = requests.get(base_url + "/get/step", params={})

#         # 检查响应状态码
#         if response.status_code == 200:
#             # 返回响应内容
#             print(response.text)
#             return response.text
#         else:
#             # 处理非 200 状态码的情况
#             print(f"请求失败，状态码: {response.status_code}")
#             return None
#     except requests.exceptions.RequestException as e:
#         # 处理请求异常
#         print(f"请求发生异常: {e}")
#         return None


# get_info()

local_path = download_file(
    "https://common-1251623262.cos.ap-guangzhou.myqcloud.com/1.MOV"
)
if local_path:
    print(f"文件已下载到: {local_path}")
else:
    print("文件下载失败")
