import numpy as np
a=np.mat([[1, 2, 3],
        [4, 5, 6]])
cent=np.mean(a,axis=0).tolist()[0]
cents=[]
cents.append(cent)
print(cents)