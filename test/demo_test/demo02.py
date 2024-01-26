# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 15:44
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: demo02.py
# @Software: PyCharm
# @User: chent
from pulp import *

def cal_PULP(
        key_list,
        flag_list,
        original_price,
        actual_number_dict,
        original_number_dict,
        max_increase,
        max_decrease,
        original_total_budget):
    """
    用于解决当前的详细规划问题，计算出预期的总价
    :param key_list:    str类型列表，存储的是采购内容列的拼音
    :param flag_list:   是否增长/不变/减小，保存有1/-1/0的数字，
                        1 代表与原始数量相比，实际数量增加，修正单价应上涨；
                        0 代表与原始数量相比，实际数量不变，修正单价可以上涨/不变/下降；
                        -1 代表与原始数量相比，实际数量减少，修正单价应下降
    :param original_price:      原本货物单价
    :param actual_number_dict:  实际购买数量
    :param original_number_dict:原始购买数量
    :param max_increase:        最大涨幅（正数）
    :param max_decrease:        最大降幅（正数）
    :param original_total_budget:   原始预算总价
    :return:
    """
    # 定义线性规划问题
    MyProblem = LpProblem("Budget_Bid_Price", sense=LpMaximize)

    # 设置每个变量的上下限
    print('***************111*******************')
    for i in range(len(key_list)):
        if flag_list[i] == 1:
            v = pulp.LpVariable(key_list[i], lowBound=original_price[i], upBound=original_price[i] * (1 + max_increase),
                                cat='Continuous')
            MyProblem.addVariable(v)
            print(v.name, v.upBound, v.lowBound, v)
        elif flag_list[i] == 0:
            v = pulp.LpVariable(key_list[i], lowBound=original_price[i] * (1 - max_decrease),
                                upBound=original_price[i] * (1 + max_increase), cat='Continuous')
            MyProblem.addVariable(v)
            print(v.name, v.upBound, v.lowBound, v)
        elif flag_list[i] == -1:
            v = pulp.LpVariable(key_list[i], lowBound=original_price[i] * (1 - max_decrease),
                                upBound=original_price[i], cat='Continuous')
            MyProblem.addVariable(v)
            print(v.name, v.upBound, v.lowBound, v)
    print('*****************222*****************')

    # 建立目标函数
    MyProblem += lpSum([actual_number_dict[v.name] * v for v in MyProblem.variables()]), 'TheFinalCost'

    # 约束条件
    MyProblem += lpSum([original_number_dict[v.name] * v for v in MyProblem.variables()]) <= original_total_budget, 'ConstrainedRequirement'

    # 计算
    MyProblem.solve()
    print("***************** Info *******************")
    print("Status:", LpStatus[MyProblem.status])
    for v in MyProblem.variables():
        print(v.name, "=", v.varValue)
    print("最终总价最大值为：", pulp.value(MyProblem.objective))
    MyProblem.writeLP('Budget Bid Price.lp')


if __name__ == '__main__':
    key_list = ['DN', 'KT', 'XYJ', 'ZZ', 'DYJ']
    # 原始数量
    original_number_dict = {
        'DN': 10,
        'KT': 20,
        'XYJ': 8,
        'ZZ': 7,
        'DYJ': 35
    }
    # 原始单价
    original_price = [15, 20, 35, 75, 52]
    # 实际数量
    actual_number_dict = {
        'DN': 13,
        'KT': 18,
        'XYJ': 7,
        'ZZ': 7,
        'DYJ': 38
    }
    # 原始总价
    original_total_budget = 3175
    # 是否增长
    flag_list = [1, -1, -1, 0, 1]
    # 最大涨幅
    max_increase = 0.2
    # 最大降幅
    max_decrease = 0.2
    cal_PULP(key_list,
             flag_list,
             original_price,
             actual_number_dict,
             original_number_dict,
             max_increase,
             max_decrease,
             original_total_budget)
