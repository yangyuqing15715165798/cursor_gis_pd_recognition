from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import joblib
import cv2
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
import uvicorn

app = FastAPI(
    title="局放图像识别API",
    description="这是一个使用SVM模型进行局放图像分类的API服务",
    version="1.0.0",
)

# 加载模型和预处理器
clf = joblib.load('./svm_pd_model/svm_model.pkl')
scaler = joblib.load('./svm_pd_model/svm_scaler.pkl')
pca = joblib.load('./svm_pd_model/svm_pca.pkl')

# 定义类别

categories = ['corona', 'particle', 'floating', 'surface','void'] 

# 读取新图像并转换为灰度图
def load_new_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is not None:
        img = cv2.resize(img, (64, 64))  # 调整图像大小
        img = img.flatten()  # 将图像展平成向量
        return img
    else:
        return None

@app.post("/api/v1/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # 将文件保存到临时路径
        img_path = 'temp_image.jpg'
        with open(img_path, "wb") as buffer:
            buffer.write(await file.read())

        # 加载并处理图像
        new_image = load_new_image(img_path)
        if new_image is None:
            raise HTTPException(status_code=400, detail="Failed to process image")

        # 标准化和降维
        new_image = scaler.transform([new_image])
        new_image = pca.transform(new_image)

        # 预测
        new_pred = clf.predict(new_image)
        predicted_category = categories[new_pred[0]]

        # 获取预测概率
        pred_prob = clf.predict_proba(new_image)
        predicted_probability = pred_prob[0][new_pred[0]] * 100

        return JSONResponse(content={
            'predicted_category': predicted_category,
            'predicted_probability': f"{predicted_probability:.2f}%"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9000)
