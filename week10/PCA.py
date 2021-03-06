import cv2
import numpy as np

def pca(mul, pan):

    #将数据转换为浮点型便于计算
    mul = np.float64(mul)
    pan = np.float64(pan)
    dst = np.zeros(mul.shape, dtype = np.uint8)

    #主成分变换，得到特征值和特征向量
    row, col, dim = mul.shape
    temp = np.zeros((row * col, dim), dtype = np.float32)
    for i in range(dim):
        temp[:, i] = (mul[:, :, i]).ravel() # 将矩阵向量化
    meanTemp, eigvect = cv2.PCACompute(temp, (np.mean(temp, axis = 0)).reshape(1, -1)) # axis=0，输出矩阵是1行，求每一列的平均（按照每一行去求平均）；转换成一行；返回排序后的特征值和特征向量

    #替换第一分量
    pca = cv2.PCAProject(temp, meanTemp, eigvect) # 旋转到主成分空间
    pca[:, 0] = pan.ravel()
    inverse = cv2.PCABackProject(pca, meanTemp, eigvect)
    temp = np.zeros(mul.shape, dtype = np.float64)
    for i in range(3):
        temp[:, :, i] = (inverse[:, i]).reshape(row, col)

    #转换到8位整型数据
    for i in range(dim):
        imax = np.max(temp[:, :, i])
        imin = np.min(temp[:, :, i])
        dst[:, :, i] = np.uint8(255.0 / (imax - imin + 0.0000001) * (temp[:, :, i] - imin))
    return dst

mul = cv2.imread('mul_input.tif', cv2.IMREAD_COLOR)
pan = cv2.imread('pan_input.tif', cv2.IMREAD_GRAYSCALE)
cv2.imshow('mul-image', mul)
cv2.imshow('pan-image', pan)

img = pca(mul, pan)
cv2.imshow('PCAFusion', img)

cv2.waitKey()
cv2.destroyAllWindows()
