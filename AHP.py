# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:50:43 2020

@author: 养猪人
"""


import numpy as np
from sklearn import preprocessing

'''
层级分析法
原理参考地址：https://www.cnblogs.com/yhll/p/9967726.html
方法结构：
      目标层          A
      准则层          B
      方案层          C
      
第一步：构成准则层矩阵   准则层矩阵就是指准则层B中N个因素对于目标A的的相对重要性
       重要性排序由1至9 准则层矩阵是对角矩阵，即Bi对Bj的重要性与Bj对Bi的重要性互为倒数
第二步：矩阵分解  将准则层矩阵直接求解特征值Val与特征向量Vec
        排序得到最大的特征值ValMax,并将对应的特征向量归一化，归一化后的特征向量是对应的权值
第三步：按照 （VALMAX-ROW）/（ROW-1）对照表格进行一致性检验，若通过则继续计算，若不通过需要重新建立矩阵

        后续方案层求解权重的方式重复步骤1-3，需要重复准则层因素个数N次
        
第四步：矩阵乘法  np.dot(Weight_B,Weight_C)
                即用准则层权值乘方案层权值矩阵，得到的结果是最终各个方案的成绩
                成绩对应最高则优
'''

class AHP():
    
    def __init__(self,Layer=3,B=3,C=8):
        '''
        Score :比较矩阵
        Layer :层数
        B     ：准则层个数
        C     ：方案层个数
        
        '''
        self.Layer = Layer
        self.B = B
        self.C = C
        
    def decompose(self,Data):
        
        # scaler = preprocessing.StandardScaler().fit(Data)#标准化
        # DataScale = scaler.transform(Data
        DataScale = Data#网上的过程似乎只需要对特征向量标准化
        
        # 特征值，特征向量矩阵（特征向量是列向量）
        val,vec = np.linalg.eig(DataScale)
        # 注意：这里复数只取了实数部分
        val = val.real.astype(float)
        vec = vec.real.astype(float)
        order = val.argsort()
        val = np.flip(val[order],0)
        vec = np.flip(vec[:,order],1)    #按列排列
        
        return val,vec
        
    def check(self,Data,Val):
        Row = Data.shape[0]
        RI = [0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1.49,1.51]
        CI = np.divide((Val-Row),(Row-1))
        CR = np.divide(CI,RI[Row-1])
        
        if CR > 0.1:
            raise Exception("Failed the consistency test.Please modify the matrix.")
        else:
            print('Consistency check passed')
            
        return CR
            
    def fit(self,Data_B,Data_C):
        
        B = self.B
        C = self.C
        
        CR_C = []
        Weight_C=[]
        Val_C = []
        #首先计算准则层
        Val_B,Vec_B = AHP.decompose(self,Data_B)
        Val_BMAX = Val_B[0]
        Weight_B = Vec_B[:,0]
        Weight_B = Weight_B.T
        Weight_B = np.divide(Weight_B,sum(Weight_B))
        CR_B = AHP.check(self,Data_B, Val_BMAX)
        
        self.CR_B = CR_B
        self.Weight_B = Weight_B
        self.Val_BMAX = Val_BMAX
        #计算方案层
        for i in range(B):
            if i == 0:
                Matrix_Current = Data_C[0:C,:]
                EndPoint = C
            else:
                StartPoint = EndPoint
                EndPoint = StartPoint+C
                Matrix_Current = Data_C[StartPoint:EndPoint,:]
                
            Val,Vec_C = AHP.decompose(self,Matrix_Current)
            Val_CMAX = Val[0]
            Val_C.append(Val_CMAX)
            Weight = Vec_C[:,0]
            Weight = Weight.T
            Weight = np.divide(Weight,sum(Weight))
            if i ==0:
                Weight_C = Weight
            else:
                Weight_C = np.vstack((Weight_C,Weight))
            CR = AHP.check(self,Matrix_Current, Val_CMAX)
            CR_C.append(CR)
                
        self.CR_C = CR_C
        self.Weight_C = Weight_C
        self.Val_C = Val_C
                
        
        Score = np.dot(Weight_B,Weight_C)
        
        return Score,self.Val_BMAX,self.Weight_B,self.CR_B,self.Val_C,self.Weight_C,self.CR_C,
                
    
if __name__ == '__main__':
    
    '''
    需要输入的参数：
    B            ：准则层个数   需要与外部对应的准则层矩阵.txt配合  
                   注意这个矩阵是对角矩阵   如果是N个准则  则是一个NXN的矩阵
    C            ：方案层个数   需要与外部对应的方案层矩阵.txt配合
                   每一个对应一个准则  都有一个方案层矩阵 如果是M个方案  则是一个MXM矩阵
                   在方案层矩阵.txt文件里面竖向存放了N个方案层矩阵
    
    
    因为你之前的论文有8个二级因素  所以默认的是准则层有8个 方案层三个     
    在运行时如果报错
    Failed the consistency test.Please modify the matrix.    
    那么代表没有通过一致性检验  需要重新构造矩阵 



    输出数据如下：
    Score       ：最终输出的三个方案的成绩
    Val_BMAX    ：准则层矩阵的最大特征值
    Weight_B    ：准则层矩阵的权向量（即对应最大特征值的归一化特征向量）
    CRB         ：准则层的一致化检验值，如果在右边变量管理器看不到，就在右下方控制台输入CRB回车就行
    Val_CMAX    ：方案层矩阵的最大特征值
    Weight_C    ：方案层矩阵的权向量（即对应最大特征值的归一化特征向量）
    CRC         ：方案层的一致化检验值，如果在右边变量管理器看不到，就在右下方控制台输入CRC回车就行
    
    这个矩阵的输入因为是分数 最好是你确定好 我帮你输
    '''
    Data_B = np.loadtxt('准则层矩阵.txt')
    Data_C = np.loadtxt('方案层矩阵.txt')
    
    AHP_Method = AHP(B=8,C=3)
    Score,Val_BMAX,Weight_B,CRB,Val_CMAX,Weight_C,CRC = AHP_Method.fit(Data_B,Data_C)
        
                
        
                
    