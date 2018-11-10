import numpy as np
import matplotlib
import matplotlib.pyplot as plt
def read_file(filename):
    fr=open(filename)
    filelines=fr.readlines()
    dataSet=[]
    for line in filelines:
        newline=line.strip().split('\t')
        dataSet.append(list(map(float,newline)))
    dataMat=np.mat(dataSet)
    return dataMat
def pca(dataMat, topNfeat):
    meanVals = dataMat.mean(0)#求每一列的均值
    meanRemoved = dataMat - meanVals #减去均值
    covMat = np.cov(meanRemoved, rowvar=0)#计算协方差矩阵
    eigVals,eigVects = np.linalg.eig(np.mat(covMat))#计算协方差的特征向量
    eigValInd = np.argsort(eigVals)            #特征值排序，因为特征值越大影响力越大。
    eigValInd = eigValInd[:-(topNfeat+1):-1]  #找到像要的特征值
    redEigVects = eigVects[:,eigValInd]       #把特征向量从大到小排列
    lowDDataMat = meanRemoved * redEigVects#把向量映射到新的向量空间
    reconMat = (lowDDataMat * redEigVects.T) + meanVals#新的向量升维到原来的向量空间
    return lowDDataMat, reconMat

if __name__=="__main__":
    dataMat=read_file(r"testSet.txt")
    lowDDataMat, reconMat= pca(dataMat, 1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dataMat[:, 0].flatten().A[0], dataMat[:, 1].flatten().A[0], marker='^', s=90)
    ax.scatter(reconMat[:, 0].flatten().A[0], reconMat[:, 1].flatten().A[0], marker='o', s=50, c='red')
    plt.show()
