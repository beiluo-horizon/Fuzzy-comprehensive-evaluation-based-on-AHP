# Fuzzy-comprehensive-evaluation-based-on-AHP
Fuzzy comprehensive evaluation method based on Analytic hierarchy process
    test 是投票数据矩阵    在代码文件夹里面有个test4.txt文件  可以直接改投票数据，需要和各个指标个数匹配
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
    
    在函数中使用Get_weight则直接使用专家投票得到权重
    在函数中使用GetWeight_AHP则使用层次分析法得到权重
    
    层次分析法需要的参数：
       需要输入的参数：
    B            ：准则层个数   需要与外部对应的 准则层矩阵.txt配合  
                   注意这个矩阵是对角矩阵   如果是N个准则  则是一个NXN的矩阵
    C            ：方案层个数   需要与外部对应的 方案层矩阵.txt配合
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
    
    
    上传的时候隔了太久，输入可能有问题，但是代码原理应该没错。
