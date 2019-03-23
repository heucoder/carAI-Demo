#遗传算法与神经网络
import torch
from torch import nn
import numpy as np
from copy import deepcopy
#神经网络
class Data:
    def __init__(self, x):
        self.x = x

    def forward(self):
        # Mini-batch
        return self.x

class FullyConnect:
    def __init__(self, l_x, l_y, weights = None, bias = None):
        self.l_x = l_x
        self.l_y = l_y
        self.weights = np.random.randn(l_y, l_x) * np.sqrt(2 / l_x)
        self.bias = np.random.randn(l_y, 1)

    def forward(self, x):
        self.y = np.dot(self.weights, x) + self.bias
        return self.y

class Sigmoid:
    def __init__(self):
        pass
    def sigmoid(self, x):
        # x = np.maximum(x,100)
        return 1/(1+np.exp(-x))
    def forward(self, x):
        self.x = x
        self.y = self.sigmoid(x)
        return self.y

class carAI:
    def __init__(self):
        self.linear1 = FullyConnect(7,15)
        self.linear2 = FullyConnect(15,2)

    def forward(self,x):
        x = self.linear1.forward(x)
        x = Sigmoid().forward(x)
        x = self.linear2.forward(x)
        x = Sigmoid().forward(x)
        com1 = x[0][0]
        com2 = x[1][0]
        v = 0
        dir = 0
        if com1 < 0.3:
            v = -1
        elif com1 > 0.7:
            v= 1
        else:
            v = 0
        if com2 < 0.2:
            dir = -1
        elif com2 > 0.8:
            dir = 1
        else:
            dir = 0
        return (v,dir)

    def assign_weights(self, weightsList = None, biasList = None):
        self.linear1.weights = deepcopy(weightsList[0])
        self.linear1.bias = deepcopy(biasList[0])
        self.linear2.weights = deepcopy(weightsList[1])
        self.linear2.bias = deepcopy(biasList[1])

    def get_weights(self):
        weightsList = []
        biasList = []
        weightsList.append(self.linear1.weights)
        weightsList.append(self.linear2.weights)
        biasList.append(self.linear1.bias)
        biasList.append(self.linear2.bias)
        return weightsList, biasList

    def save(self, filename):
        filename += '.npz'
        np.savez(filename, linear1_weight = self.linear1.weights, linear1_bias = self.linear1.bias,
                 linear2_weight = self.linear2.weights, linear2_bias = self.linear2.bias)

    def load(self, filename):
        para = np.load(filename)
        self.linear1.weights = deepcopy(para['linear1_weight'])
        self.linear1.bias = deepcopy(para['linear1_bias'])
        self.linear2.weights = deepcopy(para['linear2_weight'])
        self.linear2.bias = deepcopy(para['linear2_bias'])

#扰动
def fun1(weightsList, biasList, k, r = 0.1):
    carAIs = []
    for i in range(k):
        carai = carAI()
        w = deepcopy(weightsList)
        b = deepcopy(biasList)
        for i in range(len(w)):
            n,m = w[i].shape
            w[i] += r*np.random.randn(n, m)
        for i in range(len(b)):
            n,m = b[i].shape
            b[i] += r*np.random.randn(n, m)
        carai.assign_weights(w,b)
        carAIs.append(carai)
    return carAIs

#随机扰动
def fun2(weightsList,biasList,k):
    carAIs = []
    for i in range(k):
        carai = carAI()
        carAIs.append(carai)
        w = deepcopy(weightsList)
        b = deepcopy(biasList)
        for i in range(len(w)):
            t = np.random.rand(1)[0]
            if t < 0.3:
                n,m = w[i].shape
                w[i] += np.random.randn(n, m)
        for i in range(len(b)):
            t = np.random.rand(1)[0]
            if t < 0.7:
                n,m = b[i].shape
                b[i] += np.random.randn(n, m)
        carai.assign_weights(w,b)
        carAIs.append(carai)
    return carAIs

#遗传算法
#输入父母亲上次最好的那个
def gene_algo(parcarAI, n):
    carAIs = []
    carAIs.append(parcarAI)
    k1 = n//4; k2 = n - 3*k1-1
    #一半权值小幅度扰动(0.1,0.3)
    #1/4权值大幅度扰动(0.6)
    #1/4随机一个层(使用np.random.randn)
    weightsList, biasList = parcarAI.get_weights()
    #0.1
    carAIs.extend(fun1(weightsList, biasList, k1, 0.1))
    #0.2
    carAIs.extend(fun1(weightsList, biasList, k1, 0.5))
    #0.6
    carAIs.extend(fun1(weightsList, biasList, k1, 0.8))
    #随机扰动一层
    carAIs.extend(fun2(weightsList, biasList, k2))
    return carAIs

if __name__ == '__main__':
    carai_1 = carAI()

    a = np.random.randn(7,1)
    v, dir = carai_1.forward(a)
    w, b = carai_1.get_weights()
    # carAIs = gene_algo(carai_1, 10)
    # carat_2 = carAIs[0]
    # v2,dir2 = carat_2.forward(a)
    carai_2 = carAI()
    carai_2.load("test1.npz")



