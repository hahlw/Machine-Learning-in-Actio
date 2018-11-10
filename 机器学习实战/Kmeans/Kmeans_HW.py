import numpy as np
"""
    读取文件，去掉第一行，
"""
def read_csv(filename):
    fr = open(filename)
    readlines = fr.readlines()
    dataMat = []
    for lines in readlines:
        line = lines.strip().split('\t')
        dataMat.append(line)
    datalist=[]
    for i in range(len(dataMat)):
        if i==0:
            continue
        line=[i]
        line.extend(dataMat[i][0].strip("'").split(",")[1:53])
        # map(float，line)是把list中的数据类型转化成float
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
    print(n)
    randCore=np.mat(np.zeros((k,n-1)))#因为数据第一列是药品号，所以去之后的列。
    for j in range(1,n):
        minJ=np.min(dataMat[:,j])
        rangeJ=float(np.max(dataMat[:,j])-minJ)
        randCore[:,j-1]=minJ+rangeJ*np.random.rand(k,1)
    return randCore
"""
    py参数可以是函数：
    每一轮更新质点（选择这个簇的平均值作为质点）如果没有更新，则停止迭代。
"""
def kMeans(dataMat, k,distMeas=distance, createCent=randClustCore):
    m=np.shape(dataMat)[0]
    clustChanged=True
    clusterAssment=np.mat(np.zeros((m,3)))
    clusterCores=createCent(dataMat,k)
    while clustChanged:
        clustChanged=False
        for i in range(m):
            minDist = np.inf;minIndex = -1
            for j in range(k):
                curDist=distMeas(clusterCores[j,:],dataMat[i,1:])
                if curDist<minDist:
                    minDist=curDist;minIndex=j
            if clusterAssment[i,0]!=minIndex:clustChanged=True
            clusterAssment[i, :] = minIndex, minDist**2,dataMat[i,0]
        print(clusterCores)
        for core in range(k):
            ptsInClust=dataMat[np.nonzero(clusterAssment[:,0].A==core)[0]]
            clusterCores[core,:]=np.mean(ptsInClust[:,1:],axis=0)
    return clusterCores, clusterAssment
def biKmeans(dataMat,k,distMeas=distance):
    m=np.shape(dataMat)[0]
    clusterAssment=np.mat(np.zeros((m,3)))
    centroid0 = np.mean(dataMat[:,1:],axis=0).tolist()[0]
    centlist=[centroid0]
    for i in range (m):
        clusterAssment[i,:]=0,distMeas(dataMat[i,1:],np.mat(centroid0))**2,dataMat[i,0]
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
    datMat3=np.mat(read_csv('Sales_Transactions_Dataset_Weekly.csv'))
    m=np.shape(datMat3)[0]
    centList, myNewAssments = biKmeans(datMat3, int(m/5))
    print(centList, myNewAssments)
