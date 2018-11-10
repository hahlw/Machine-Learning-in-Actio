from numpy import *
from numpy import linalg as la
from scipy import linalg as sla
def read_atr(filename):
    fr=open(filename)
    lines=fr.readlines()
    atrList=[]#特征属性列表
    index=0
    for line in lines:
        newline=line.strip().split(',')
        if(newline[0]=='A'):
            atrList.append(int(newline[1]))
        elif newline[0]=='C' or newline[0]=='V':
            break
        else:
            index+=1
            continue
        index+=1
    atrList.sort()
    return atrList
def read_mat(filename,atrList):
    fr = open(filename)
    lines = fr.readlines()
    curuser=0;Cdict={};curlist=[];datMat=[]
    for line in lines:
        newline=line.strip().split(',')
        if(newline[0]=='C'):
            curuser=int(newline[2])
            curlist.clear()
        elif(newline[0]=='V'):
            curlist.append(int(newline[1]))
            Cdict[curuser]=curlist.copy()
        else:
            continue
    d = sorted(Cdict.items(), key=lambda k: k[0])
    for keys in Cdict.keys():
        datMat.append(vectolist(atrList,Cdict[keys]))
    return datMat
def vectolist(atrList,vec):
    returnVec = [0] * len(atrList)  # 创建一个其中所含元素都为0的向量
    for word in vec:  # 遍历每个词条
        if word in atrList:  # 如果词条存在于词汇表中，则置1
            returnVec[atrList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary!" % word)
    return returnVec
def cosSim(inA,inB):
    num = float(inA.T*inB)
    denom = la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)
def load_svd(dataMat):
    datMat=mat(dataMat)
    U, Sigma, VT = sla.svd(datMat)
    Sig4 = mat(eye(4) * Sigma[:4])
    xformedItems = dataMat.T * U[:, :4] * Sig4.I
    print("xformedItems",xformedItems)
    return xformedItems
def svdEst(dataMat,xformedItems, user, simMeas, item):
    n = shape(dataMat)[1]
    simTotal = 0.0;ratSimTotal = 0.0
    for j in range(n):
        userRating = dataMat[user,j]
        if userRating == 0 or j==item: continue
        #这个保证了转化后的矩阵没有非零项吗？
        similarity = simMeas(xformedItems[item,:].T,\
                             xformedItems[j,:].T)
        print('the %d and %d similarity is: %f' % (item, j, similarity))
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0: return 0
    else: return ratSimTotal/simTotal
def recommend(dataMat, user, N=3, simMeas=cosSim, estMethod=svdEst):
    dataMat=mat(dataMat)
    xformedItems=load_svd(dataMat)
    unratedItems = nonzero(dataMat[user,:].A==0)[1]#找到没有访问的网站块
    if len(unratedItems) == 0: return 'you rated everything'
    itemScores = []
    for item in unratedItems:
        estimatedScore = estMethod(dataMat,xformedItems, user, simMeas, item)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]
if __name__=="__main__":
    atrList=read_atr("anonymous-msweb.data")
    datMat=read_mat("anonymous-msweb.data",atrList)
    print(datMat)
    print(recommend(datMat, 1, estMethod=svdEst))