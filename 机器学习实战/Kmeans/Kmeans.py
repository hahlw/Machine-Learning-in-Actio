import numpy as np
import matplotlib.pyplot as plt
import xlrd
"""
    filename是数据源
"""
def read_file(filename):
    fr=open(filename)
    readlines=fr.readlines()
    dataMat=[]
    for lines in readlines:
        line=lines.strip().split('\t')
        #map(float，line)是把list中的数据类型转化成float
        dataMat.append(list(map(float, line)))
    return dataMat

def read_csv(filename):
    fr = open(filename)
    readlines = fr.readlines()
    dataMat = []
    for lines in readlines:
        line = lines.strip().split('\t')
        # map(float，line)是把list中的数据类型转化成float
        dataMat.append(line)
    datalist=[]
    for i in range(len(dataMat)):
        if i==0:
            continue
        line=[i]
        line.extend(dataMat[i][0].strip("'").split(",")[1:52])
        datalist.append(list(map(float, line)))
    return datalist
"""
    计算点到质点的欧氏距离
    向量和数组的计算要用到np的库，直接**2或者pow参数不能是数组或者向量
"""
def distance(vec1,vec2):
    return np.sqrt(np.sum(np.power((vec1-vec2),2)))
"""
    找到K个随机质点
    np.random.rand(k,1)是生成一个k*1的数组
"""
def randClustCore(dataMat,k):
    n=np.shape(dataMat)[1]
    randCore=np.mat(np.zeros((k,n)))
    for j in range(n):
        minJ=np.min(dataMat[:,j])
        rangeJ=float(np.max(dataMat[:,j])-minJ)
        randCore[:,j]=minJ+rangeJ*np.random.rand(k,1)#随机生成K行一列的数组或者矩阵、向量
    return randCore
"""
    py参数可以是函数：
    每一轮更新质点（选择这个簇的平均值作为质点）如果没有更新，则停止迭代。
"""
def kMeans(dataMat, k,distMeas=distance, createCent=randClustCore):
    m=np.shape(dataMat)[0]
    clustChanged=True
    clusterAssment=np.mat(np.zeros((m,2)))
    clusterCores=createCent(dataMat,k)
    while clustChanged:
        clustChanged=False
        for i in range(m):
            minDist = np.inf;minIndex = -1
            for j in range(k):
                curDist=distMeas(clusterCores[j,:],dataMat[i,:])
                if curDist<minDist:
                    minDist=curDist;minIndex=j
            if clusterAssment[i,0]!=minIndex:clustChanged=True
            clusterAssment[i, :] = minIndex, minDist**2
        print(clusterCores)
        for core in range(k):
            #np.nonzero返回一个数组中非零的索引值一般是二维的
            #np.mean(dataMat,axis=0)是按列求平均
            ptsInClust=dataMat[np.nonzero(clusterAssment[:,0].A==core)[0]]
            clusterCores[core,:]=np.mean(ptsInClust,axis=0)
    return clusterCores, clusterAssment
def showPlt(datMat, numClust,alg=kMeans):
    myCentroids, clustAssing = alg(datMat, numClust)
    fig = plt.figure()
    rect=[0.1,0.1,0.8,0.8]
    scatterMarkers=['s', 'o', '^', '8', 'p',
                    'd', 'v', 'h', '>', '<']
    axprops = dict(xticks=[], yticks=[])
    ax0=fig.add_axes(rect, label='ax0', **axprops)
    ax1=fig.add_axes(rect, label='ax1', frameon=False)
    for i in range(numClust):
        ptsInCurrCluster = datMat[np.nonzero(clustAssing[:,0].A==i)[0],:]
        markerStyle = scatterMarkers[i % len(scatterMarkers)]
        print("ptsInCurrCluster[:,0].flatten().A[0]",ptsInCurrCluster[:,0].flatten().A)
        print("ptsInCurrCluster[:,1].flatten().A[0]", ptsInCurrCluster[:,1].flatten().A[0])
        ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0], ptsInCurrCluster[:,1].flatten().A[0], marker=markerStyle, s=90)
    ax1.scatter(myCentroids[:,0].flatten().A[0], myCentroids[:,1].flatten().A[0], marker='+', s=300)
    plt.show()
def biKmeans(dataMat,k,distMeas=distance):
    m=np.shape(dataMat)[0]
    clusterAssment=np.mat(np.zeros((m,2)))
    centroid0 = np.mean(dataMat,axis=0).tolist()[0]
    centlist=[centroid0]
    for i in range (m):
        clusterAssment[i,:]=0,distMeas(dataMat[i,:],np.mat(centroid0))**2
    while len(centlist)<k:
        minSSE=np.inf
        for j in range(len(centlist)):
            splitData=dataMat[np.nonzero(clusterAssment[:,0].A==j)[0],:]
            splitCent,splitAssment=kMeans(splitData,2)
            sseSplit = sum(splitAssment[:, 1])
            sseNotSplit = sum(clusterAssment[np.nonzero(clusterAssment[:, 0].A !=j)[0], 1])
            print("sseSplit, and notSplit: ", sseSplit, sseNotSplit)
            if sseNotSplit+sseSplit<minSSE:
                minSSE=sseNotSplit+sseSplit
                bestCentToSplit = j
                bestNewCents = splitCent
                bestClustAss = splitAssment.copy()
        bestClustAss[np.nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centlist)
        bestClustAss[np.nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        print('the bestCentToSplit is: ', bestCentToSplit)
        print('the len of bestClustAss is: ', len(bestClustAss))
        centlist[bestCentToSplit] = bestNewCents[0, :].tolist()[0]
        centlist.append(bestNewCents[1, :].tolist()[0])
        clusterAssment[np.nonzero(clusterAssment[:,0].A==bestCentToSplit)[0],:]=bestClustAss
    return np.mat(centlist),clusterAssment
if __name__=="__main__":
    #dataMat=np.mat(read_file("Sales_Transactions_Dataset_Weekly.csv"))
    datMat3=np.mat(read_csv('Sales_Transactions_Dataset_Weekly.csv'))
    print(datMat3)
    """
    centList, myNewAssments =biKmeans(dataMat, 3)
    print(centList)
    showPlt(dataMat,4, alg=biKmeans)
    #print(distance(dataMat[0], dataMat[1]))
    #myCentroids, clustAssing = kMeans(dataMat,4)
    #showPlt(dataMat,4)
    """