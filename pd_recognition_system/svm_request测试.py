import requests

"""

curl -X POST -F file=@./test_dataset/corona/corona111.png http://127.0.0.1:9000/predict

curl -X POST -F file=@D:/pd_test_new_image/floating_image_1.png http://127.0.0.1:9000/api/v1/predict


"""

url = 'http://127.0.0.1:9000/api/v1/predict' # 替换为实际的API地址
file_path = './test_dataset/surface/surface57.png'  # 替换为实际路径
files = {'file': open(file_path, 'rb')}

response = requests.post(url, files=files)
print(response.json())


