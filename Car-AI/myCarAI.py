#coding: utf-8

# 遗传算法与神经网络
import numpy as np
from copy import deepcopy

# 神经网络
# 数据层
class Data:
    def __init__(self, x):
        self.x = x
    def forward(self):
        # Mini-batch
        return self.x

# 全连接层
class FullyConnect:
    def __init__(self, l_x, l_y, weights = None, bias = None):
        self.l_x = l_x
        self.l_y = l_y
        self.weights = np.random.randn(l_y, l_x) * np.sqrt(2 / l_x)
        self.bias = np.random.randn(l_y, 1)
    def forward(self, x):
        self.y = np.dot(self.weights, x) + self.bias
        return self.y

# Sigmoid
class Sigmoid:
    def __init__(self):
        pass
    
    def sigmoid(self, x):
        return 1/(1+np.exp(-np.maximum(x,-100)))

    def forward(self, x):
        self.x = x
        self.y = self.sigmoid(x)
        return self.y

# 控制小车的AI
class carAI:
    def __init__(self,node_list = [7,15,2]):
        self.fullyconnect_list = []
        for i in range(len(node_list) - 1):
            linear = FullyConnect(node_list[i], node_list[i+1])
            self.fullyconnect_list.append(linear)

    # 调整速度与方向
    def _adjust(self, t, v1, v2):
        if t < v1:
            return -1
        elif t > v2:
            return 1
    # 速度
    def _car_v_adjust(self, v_flag, v_thre1 = 0.3, v_thre2 = 0.7):
        car_v = self._adjust(v_flag, v_thre1, v_thre2)
        return car_v
    # 方向
    def _car_dir_adjust(self, dir_flag, dir_thre1 = 0.2, dir_thre2 = 0.8):
        car_dir = self._adjust(dir_flag, dir_thre1, dir_thre2)
        return car_dir
    
    def forward(self,x):
        for linear in self.fullyconnect_list:
            x = linear.forward(x)
            x = Sigmoid().forward(x)
        
        # 方向
        dir_flag = x[0][0]
        # 速度
        v_flag = x[1][0]
        car_v = self._car_v_adjust(v_flag)
        car_dir = self._car_dir_adjust(dir_flag)

        return (car_v, car_dir)
    
    # 重新赋予权值,与get_weights配对使用
    def assign_weights(self, weightsList = None, biasList = None):
        for i in range(len(self.fullyconnect_list)):
            linear = self.fullyconnect_list[i]
            linear.weights = deepcopy(weightsList[i])
            linear.bias = deepcopy(biasList[i])

    # 获得权值
    def get_weights(self):
        weightsList = []
        biasList = []

        for i in range(len(self.fullyconnect_list)):
            linear = self.fullyconnect_list[i]
            weightsList.append(linear.weights)
            biasList.append(linear.bias)

        return weightsList, biasList

    def save(self, filename):
        np.savez(filename, fullyconnect_list = np.array(self.fullyconnect_list))

    def load(self, filename):
        para = np.load(filename)
        self.fullyconnect_list = list(deepcopy(para['fullyconnect_list']))

class GeneOptimize:
    def __init__(self):
        pass
    # 扰动
    @classmethod
    def _distur_param(self, weightsList, biasList, k, r = 0.1):
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

    # 替换
    @classmethod
    def _replace_one_layer_param(self, weightsList,biasList,k):
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

    # 遗传算法
    # 输入上次最好的那个
    @classmethod
    def gene_algo(self, parcarAI, n):
        carAIs = []
        carAIs.append(parcarAI)
        k1 = n//4; k2 = n - 3*k1-1
        # 一半权值小幅度扰动(0.1,0.3)
        # 1/4权值大幅度扰动(0.6)
        # 1/4随机一个层(使用np.random.randn)
        weightsList, biasList = parcarAI.get_weights()
        # 0.1
        carAIs.extend(self._distur_param(weightsList, biasList, k1, 0.1))
        # 0.2
        carAIs.extend(self._distur_param(weightsList, biasList, k1, 0.5))
        # 0.6
        carAIs.extend(self._distur_param(weightsList, biasList, k1, 0.8))
        # 随机扰动一层
        carAIs.extend(self._replace_one_layer_param(weightsList, biasList, k2))
        # print("-------", parcarAI.get_weights() == carAIs[0].get_weights())
        return carAIs

if __name__ == '__main__':
    carai = carAI()
    car_ai3 = carAI()

    a = np.random.randn(7,1)
    v, dir = carai.forward(a)
    w, b = carai.get_weights()
    car_ai3.assign_weights(w,b)
    for (l1, l2) in zip(carai.fullyconnect_list, car_ai3.fullyconnect_list):
        print(l1.weights == l2.weights)
    carAIs = GeneOptimize.gene_algo(carai, 10)
    for c in carAIs:
        print(c == carai)



