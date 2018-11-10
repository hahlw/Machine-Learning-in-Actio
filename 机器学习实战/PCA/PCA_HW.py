import numpy as np
import matplotlib
import matplotlib.pyplot as plt
def features2vec(feature_list):
    features = [[],#-3, -2, -1, 0, 1, 2, 3.
                [],#continuous from 65 to 256.
                ['alfa-romero','audi','bmw','chevrolet','dodge', 'honda',
                 'isuzu', 'jaguar','mazda' , 'mercedes-benz', 'mercury',
                 'mitsubishi' , 'nissan', 'peugot', 'plymouth','porsche',
                 'renault' , 'saab' ,'subaru' ,'toyota' , 'volkswagen', 'volvo'],  # 15-22
                ['diesel', 'gas'],
                ['std', 'turbo' ],
                ['four', 'two' ],
                ['hardtop', 'wagon', 'sedan', 'hatchback' ,'convertible' ],  # 0-4
                ['4wd', 'fwd', 'rwd' ],  # 0-4
                ['front', 'rear'],
                [],#continuous from 86.6 120.9.
                [],#continuous from 141.1 to 208.1.
                [],#continuous from 60.3 to 72.3.
                [],#continuous from 47.8 to 59.8.
                [],# continuous from 1488 to 4066.
                ['dohc','dohcv','l','ohc' ,'ohcf' ,'ohcv','rotor'],
                ['two','three','four','five','six','eight','twelve'],
                [],
                ['1bbl','2bbl','4bbl','idi','mfi','mpfi','spdi','spfi'],
                [],#2.54 to 3.94.
                [],#2.07 to 4.17
                [],#7 to 23
                [],#48 to 288
                [],#4150 to 6600
                [],# 13 to 49
                [],# 16 to 54
                []]# 5118 to 45400
    vec_list=[]
    for i in range(len(feature_list)):
        if feature_list[i]=='?':
            vec_list.append(np.nan)
        elif len(features[i])>0:
            vec_list.append(features[i].index(feature_list[i]))
        else:
            vec_list.append(float(feature_list[i]))
    return vec_list
def read_file(filename):
    fr =open(filename)
    filelines=fr.readlines()
    dataSet=[]
    for line in filelines:
        newline=line.strip().split(',')
        dataSet.append(features2vec(newline))
    return dataSet
def process_data():
    dataMat=np.mat(read_file(r"imports-85.data"))
    n=np.shape(dataMat)[1]
    for j in range(n):
        meanVal = np.mean(dataMat[np.nonzero(~np.isnan(dataMat[:, j].A))[0], j])
        dataMat[np.nonzero(np.isnan(dataMat[:,j].A))[0],j] = meanVal  #set NaN values to mean
    return dataMat
def pca(dataMat, topNfeat):
    meanVals = dataMat.mean(0)#求每一列的均值
    meanRemoved = dataMat - meanVals #减去均值
    covMat = np.cov(meanRemoved, rowvar=0)#计算协方差矩阵
    eigVals,eigVects = np.linalg.eig(np.mat(covMat))#计算协方差的特征向量
    #将矩阵a按照axis排序，并返回排序后的下标
    eigValInd = np.argsort(eigVals)   #特征值排序，因为特征值越大影响力越大。
    eigValInd = eigValInd[:-(topNfeat+1):-1]  #找到重要的特征值
    redEigVects = eigVects[:,eigValInd]       #把特征向量从大到小排列
    lowDDataMat = meanRemoved * redEigVects#把向量映射到新的向量空间
    reconMat = (lowDDataMat * redEigVects.T) + meanVals#新的向量升维到原来的向量空间
    return eigVals
if __name__=='__main__':
    dataMat=process_data()
    eigVals = pca(dataMat, 3)
    m,n=np.shape(dataMat)
    arr=np.zeros((n,2))
    arr[0,:]=1,1
    for i in range(n):
        arr[i,:]=i+1,float(sum(eigVals[0:i+1])/sum(eigVals))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(arr[:, 0].flatten(), arr[:, 1].flatten(), marker='^', s=50)
    plt.plot(arr[:, 0].flatten(), arr[:, 1].flatten(),c='red')
    plt.show()
    print(arr)