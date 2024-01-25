# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 15:44
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: demo02.py
# @Software: PyCharm
# @User: chent
import pulp
from pulp import *
key_list = ['DN', 'KT', 'XYJ', 'ZZ', 'DYJ']
# 原始数量
original_number = [10, 20, 8, 7, 35]
original_number_dict = {
    'DN': 10,
    'KT': 20,
    'XYJ': 8,
    'ZZ': 7,
    'DYJ': 35
}
# 原始单价
original_price = [15, 20, 35, 75, 52]
original_price_dict = {
    'DN': 15,
    'KT': 20,
    'XYJ': 35,
    'ZZ': 75,
    'DYJ': 52
}
# 实际数量
actual_number = [13, 18, 7, 7, 38]
actual_number_dict = {
    'DN': 13,
    'KT': 18,
    'XYJ': 7,
    'ZZ': 7,
    'DYJ': 38
}
# 原始总价
x = 3175
# 是否增长
flag_list = [1, -1, -1, 0, 1]
flag_dict = {
    'DN': 1,
    'KT': -1,
    'XYJ': -1,
    'ZZ': 0,
    'DYJ': 1
}
# 最大涨幅
max_increase = 0.2
# 最大降幅
max_decrease = 0.2

# 定义线性规划问题
MyProblem = LpProblem("Budget_Bid_Price", sense=LpMaximize)

budget_vars = LpVariable.dicts("Var", key_list, cat=LpContinuous)
# print(budget_vars)
# print(MyProblem.variables())


# 建立目标函数
MyProblem += lpSum([actual_number_dict[i] * budget_vars[i] for i in key_list]), 'TheFinalCost'

# 约束条件
MyProblem += lpSum([original_number_dict[i] * budget_vars[i] for i in key_list]) <= 3175, 'ConstrainedRequirement'


# 设置每个变量的上下限
print('***************111*******************')
for v in MyProblem.variables():
    # print(v.name)
    temp = v.name.replace('Var_', '')
    # print(temp)
    # print(type(v), type(v.lowBound), type(v.upBound))
    # print(v.name, flag_dict[v.name.replace('Var_', '')])
    # print(v, original_price_dict[v.name.replace('Var_', '')], original_price_dict[v.name.replace('Var_', '')] * (1 + max_increase))
    if flag_dict[temp] == 1:
        v = pulp.LpVariable(v.name, lowBound=original_price_dict[temp], upBound=original_price_dict[temp] * (1 + max_increase), cat='Continuous')
        # v.lowBound = original_price_dict[v]
        # v.upBound = original_price_dict[v] * (1 + max_increase)
        print(v, v.lowBound, v.upBound)
    elif flag_dict[v.name.replace('Var_', '')] == -1:
        v = pulp.LpVariable(v.name, lowBound=original_price_dict[temp] * (1 - max_decrease),
                            upBound=original_price_dict[temp], cat='Continuous')
        # v.lowBound = original_price_dict[v] * (1 - max_decrease)
        # v.upBound = original_price_dict[v]
        print(v, v.lowBound, v.upBound)
    elif flag_dict[v.name.replace('Var_', '')] == 0:
        v = pulp.LpVariable(v.name, lowBound=original_price_dict[temp] * (1 - max_decrease),
                            upBound=original_price_dict[temp] * (1 + max_increase), cat='Continuous')
        # v.lowBound = original_price_dict[v] * (1 - max_decrease)
        # v.upBound = original_price_dict[v] * (1 + max_increase)
        print(v, v.lowBound, v.upBound)



print('*****************222*****************')


MyProblem.solve()
print("***************** Info *******************")
print("Status:", LpStatus[MyProblem.status])
for v in MyProblem.variables():
    print(v.name, "=", v.varValue)
print("最终总价最大值为：", pulp.value(MyProblem.objective))
MyProblem.writeLP('Budget Bid Price.lp')












































