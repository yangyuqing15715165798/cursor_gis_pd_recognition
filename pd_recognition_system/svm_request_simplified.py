import requests
import os
import sys

url = 'http://127.0.0.1:9000/api/v1/predict'  # 替换为实际的API地址

def send_request(image_path):
    if not os.path.isabs(image_path):
        # 如果不是绝对路径，则假定它是相对于当前工作目录的路径
        file_path = os.path.abspath(image_path) # 获取绝对路径
    else:
        file_path = image_path

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            response.raise_for_status()  # 如果请求失败 (状态码 4xx or 5xx)，则抛出HTTPError异常
            data = response.json()
            print(data)
    except FileNotFoundError:
        print(f"错误：文件未找到，请检查路径 '{file_path}' 是否正确。")
    except requests.exceptions.ConnectionError:
        print(f"错误：无法连接到服务器 {url}。请确保API服务正在运行并且地址正确。")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err} - {response.status_code}")
        try:
            print(f"服务器响应：{response.json()}")
        except ValueError:
            print(f"服务器响应 (非JSON)：{response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("错误：请提供图像文件的路径作为命令行参数。")
        print("用法: python svm_request_simplified.py <图像路径>")
        sys.exit(1)

    image_file_path = sys.argv[1]
    send_request(image_file_path)