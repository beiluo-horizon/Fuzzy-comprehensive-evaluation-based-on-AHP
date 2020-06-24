# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:52:25 2020

@author: 你老公写的
"""

import numpy as np
import AHP

'''
模糊综合评价法的解释
（1）指标
该模型有方案集 U = [u1,u2...um] 即提出的可能物流中心位置，m个
评价指标集合   V = [v1,v2...v4] 即合理，较合理，不太合理，差
因素指标集     D = [d1,d2...d4] 即包含四个一级指标
                  其中 d1 = [d11,d12]   d2 =[d21,d22,d23,d24]....  即一级指标下的二级指标
(2) 权重集
一级指标有4个  A = [a1,a2...a4] 是一级指标对应的权重
                  二级指标的权重为 Ai = [ai1,ai2...]
(3) 模糊评价集
邀请了m个专家  对所有的二级指标按照评价指标集合V评价
设对于因素集合 dij(二级指标)  分别属于 v1,v2,v3,v4的评价个数为  m1 m2 m3 m4
则对于该dij因素都模糊评价集为：

R = [m1/m... m4/m] = [rij1,rij2,rij3,rij4]     对于每一个二级因素 会产生一个 个数为len(V)的向量
则对于一级指标di 会形成一个模糊评价矩阵：

     | ri11 ri12...ri14|
Ri = |  .     .     .  |
     | rij1 rij2...rij4|
     
对于一级指标di  一级评判向量Bi,Bi是一个对于V都隶属度组成的向量:
    Bi = np.dot(AiRi) = [bi1,bi2,bi3...bi4]

由此得到二级评价矩阵

    | b11 b12 b13 b14|
R = | .    .   .   . |
    | b41 b42 b43 b44|

二次评价向量 B ：
    B = np.dot(AR)
'''


class fuzzy():
    
    def __init__(self,Score,U=4,V=4,num_D=4,list_D=[2,4,2,2]):
        '''
        Score :打分矩阵
        U     ：考虑都选址个数
        V     ：评价指标个数
        num_D : 一级指标个数
        list_D: 一级指标分别的二级指标个数

        
        '''
        self.Score = Score
        self.U = U
        self.V = V
        self.num_D = num_D
        self.list_D = list_D

    def Get_weight(self):
        '''
        获取权重
        '''
        Score = self.Score
        V = self.V
        num_D = self.num_D
        list_D = self.list_D
        Fir_sum = 0
        Fireach_score = [0]*num_D
        weight = []
        
        for i in range(num_D):         #一级
            for j in range(V):
                if i < num_D:
                    Fir_sum += (V-j)*Score[i,j]
                    Fireach_score[i] += (V-j)*Score[i,j]     
        Fir_weight = np.divide(Fireach_score,Fir_sum)
        weight.append(Fir_weight)
        
        up_limit = num_D
        for model in range(len(list_D)):  #二级
            Sec_sum = 0
            Seceach_score = [0]*list_D[model]
            low_limit = up_limit
            up_limit = low_limit + list_D[model]
            for i in range(Score.shape[0]):
                for j in range(V):
                    if i >=low_limit and i<up_limit :
                        Sec_sum += (V-j)*Score[i,j]
                        Seceach_score[i-low_limit] += (V-j)*Score[i,j]
            Sec_weight = np.divide(Seceach_score,Sec_sum)
            weight.append(Sec_weight)
        
        self.Weight = weight
        return weight
    
    def GetWeight_AHP(self,Matrix_B,Matrix_C):
        
        self.Matrix_B= Matrix_B
        self.Matrix_C= Matrix_C
        V = self.V
        num_D = self.num_D
        list_D = self.list_D
        U = self.U
        weight = []
        CR_list = []
        AHP_Method = AHP.AHP()
        #计算一级指标权重
        Fir_Val,Fir_Vec = AHP_Method.decompose(Matrix_B)
        Fir_ValMAX = Fir_Val[0]
        Fir_weight = Fir_Vec[:,0]
        Fir_weight = Fir_weight.T
        Fir_weight = np.divide(Fir_weight,sum(Fir_weight))
        CR_First = AHP_Method.check(Matrix_B, Fir_ValMAX)
        CR_list.append(CR_First)
        weight.append(Fir_weight)
        #计算二级指标权重
        for model in range(len(list_D)):  #二级
            
            # if model == 0:
            #     Matrix_Current = Matrix_C[0:U,:]
            #     EndPoint = U
            # else:
            #     StartPoint = EndPoint
            #     EndPoint = StartPoint+U
            #     Matrix_Current = Matrix_C[StartPoint:EndPoint,:]
            Matrix_Current = Matrix_C[model]
                
            Sec_Val,Sec_Vec = AHP_Method.decompose(Matrix_Current)
            Sec_ValMAX = Sec_Val[0]
            Sec_weight = Sec_Vec[:,0]
            Sec_weight = Sec_weight.T
            Sec_weight = np.divide(Sec_weight,sum(Sec_weight))
            CR_Sec = AHP_Method.check(Matrix_Current, Sec_ValMAX)
            CR_list.append(CR_Sec)
            weight.append(Sec_weight)
            
        self.CR=CR_list
        self.Weight = weight
        return weight
        
    
    def Get_R(self):
        
        '''
        评价矩阵
        '''
        Score = self.Score
        V = self.V
        num_D = self.num_D
        list_D = self.list_D
        R_list = []
        
        for i in range(num_D):         #一级
            sum_i = 0
            for j in range(V):
                if i < num_D:
                    sum_i += Score[i,j]
            score_i = np.divide(Score[i,:],sum_i)
            if i ==0:
                R = score_i
            elif i < num_D:
                R = np.vstack((R,score_i))
        R_list.append(R)
        up_limit = num_D
        for model in range(len(list_D)):  #二级
            low_limit = up_limit
            up_limit = low_limit + list_D[model]
            for i in range(Score.shape[0]):
                sum_i = 0
                for j in range(V):
                    if i >= low_limit and i< up_limit :
                        sum_i += Score[i,j]
                score_i = np.divide(Score[i,:],sum_i)
                if i == low_limit:
                    R = score_i
                if i > low_limit and i< up_limit :
                    R = np.vstack((R,score_i))
            R_list.append(R)
        
        self.R = R_list
        return R_list        
    
    def Get_B(self):
        '''
        评价向量
        '''
        B_list = []
        weight = self.Weight
        R = self.R
        
        for i in range(len(weight)):
            B = np.dot(weight[i],R[i])
            B_list.append(B)
        
        R_Sec = B_list[1]
        for m in range(len(B_list)-2):
            R_Sec = np.vstack((R_Sec,B_list[m+2]))
        
        B_Sec = np.dot(weight[0].T,R_Sec)
        
        self.B_list = B_list
        self.R_Sec = R_Sec
        self.B_Sec = B_Sec
        return B_list,R_Sec,B_Sec
    
    
        
    
        
if __name__ == '__main__':
    '''
    输入：
    test 是投票数据矩阵    在代码文件夹里面有个test.txt文件  可以直接改投票数据
    U    是指明有几个待比较的地点  没啥用
    V    投标标准个数  默认4
    num_D一级指标个数  默认3
    list_D 二级指标个数  默认 2 3 3
    num_D 和list_D必须和test一致
    输出：
    weight  根据投票结果得到的每个指标的权重  编号0是一级其余为二级
    R_list  一级评价矩阵， 编号0是一级其余是二级
    B_list  一级评价向量   编号0是一级其余是二级
    R_Sec   二级评价矩阵
    B_Sec   二级评价向量   最后的B_Sec就是模糊评价结果  0 1 2 3 分别是很合理 一般合理  不合理  很差
    '''
#    Score = np.loadtxt('Score.txt')
    test = np.loadtxt('test4.txt')          #在这里改数据输入
    Address_=['二级指标矩阵1.txt',
              '二级指标矩阵2.txt',
              '二级指标矩阵3.txt',]
    
    Data_C = []
    Data_B = np.loadtxt('一级指标矩阵.txt')
    Data = np.loadtxt('二级指标矩阵1.txt')
    Data_C.append(Data)
    Data = np.loadtxt('二级指标矩阵2.txt')
    Data_C.append(Data)
    Data = np.loadtxt('二级指标矩阵3.txt')
    Data_C.append(Data)

    
    
    Fuzzy = fuzzy(test,U=4,V=4,num_D=3,list_D=[2,3,3])   #在这里改输入
    #weight = Fuzzy.Get_weight()
    weight = Fuzzy.GetWeight_AHP(Data_B,Data_C)
    R_list = Fuzzy.Get_R()
    B_list,R_Sec,B_Sec = Fuzzy.Get_B()