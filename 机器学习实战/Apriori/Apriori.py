from numpy import *

def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
def CreatC1(dataSet):
    C1=[]
    for transaction in dataSet:
        for item in transaction:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
    # 可以作为key值
    #每个元素是一个frozenset,可以作为key值，set 不可以
    return list(map(frozenset,C1))
"""
    D是数据集，CK是候选项集列表，
    minSupport是最小的支持度，
"""
def scanD(D,CK,minSupport):
    ssCnt={}#声明一个空的字典用于计算各个集合的支持度
    for tid in D:
        for can in CK:
            if can.issubset(tid):#查看当先集合是不是数据集集合的一个子集，是加一否等于一
                if can not in  ssCnt:#has_key 返回关键字是否在字典中
                    ssCnt[can]=1
                else:ssCnt[can]+=1
    numItems=float(len(D))
    retlist=[]#用于返回一个当前的符合支持度的集合
    supportData={}#记录各个集合的支持度
    for key in ssCnt:
        support=ssCnt[key]/numItems#计算支持度
        if support>=minSupport:
            retlist.insert(0,key)
        supportData[key]=support
    return retlist,supportData
"""
当集合项个数大于0时候
    构建一个K个项组成的候选列表
    检查是否每个项集是频繁的
    保留频繁的并且构建K+1项的候选项列表
"""
def aprioriGen(LK,k):#构建k个元素的集合
    retlist=[]
    lenLK=len(LK)
    for i in range(lenLK):
        for j in range(i+1,lenLK):
            # 前面k-1项目相同就可以合成
            L1=list(LK[i])[:k-2];L2=list(LK[j])[:k-2]#可以考虑1个元素的时候是0直接合并
            L1.sort();L2.sort()
            if L1==L2:
                retlist.append(LK[i]|LK[j])
    return retlist
def apriori(dataSet,minSupport=0.5):
    C1 = CreatC1(dataSet)
    D = list(map(set, dataSet))
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)#返回候选集
        Lk, supK = scanD(D, Ck, minSupport)  # scan DB to get Lk
        supportData.update(supK)#加入字典更新
        L.append(Lk)#L.len +1
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf=0.7):  #supportData is a dict coming from scanD
    bigRuleList = []
    for i in range(1, len(L)):#只有含有两个元素的组才有可能含有关联，单个元素显然没有关联
        for freqSet in L[i]:
            #该函数遍历L中的每一个频繁项集并对每个频繁项集创建只包含单个元素集合的列表H1
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                # 如果频繁项集元素数目超过2,那么会考虑对它做进一步的合并
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                # 第一层时，后件数为1
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = [] #create new list to return
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
        if conf >= minConf:
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))#元组不可修改。
            prunedH.append(conseq)
    return prunedH
#合并，freqSet=频繁项集,H是待合并，supportData是各个项集的支持率，
#brl是要返回的规则list
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)): #试着合并M+1的项，保证M+1要小于频繁项集的长度。
        Hmp1 = aprioriGen(H, m+1)#create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):    #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

if __name__=="__main__":
    dataSet=loadDataSet()
    print(dataSet)
    C1=CreatC1(dataSet)
    print(C1)
    D=list(map(set,dataSet))
    L1, supportData0 = scanD(D, C1, 0.5)
    print(L1,supportData0)
    L, suppData = apriori(dataSet)
    print(L)
