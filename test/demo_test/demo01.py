# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 13:26
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: demo01.py
# @Software: PyCharm
# @User: chent

import pulp

def calculate_maximum_quote(max_increase, max_decrease):
    original_prices = [15, 20, 35, 75, 52]
    # 建立线性规划问题 BudgetBidPrice，目标是求解最大值
    MyProblem = pulp.LpProblem(name='BudgetBidPrice', sense=pulp.LpMaximize)
    # 定义变量：电脑，设置下限单价为 15，上限单价为 15 * (1 + max_increase)
    computer_price = pulp.LpVariable('computer price', lowBound=original_prices[0], upBound=original_prices[0] * (1 + max_increase), cat='Continuous')
    # 定义变量：空调，设置下限单价为 20 * (1 - max_increase)，上限单价为 20
    air_conditioner_price = pulp.LpVariable('air conditioner price', lowBound=original_prices[1] * (1 - max_decrease), upBound=original_prices[1],
                                            cat='Continuous')
    # 定义变量：洗衣机，设置下限单价为 35 * (1 - max_increase)，上限单价为 35
    washer_price = pulp.LpVariable('washer price', lowBound=original_prices[2] * (1 - max_decrease), upBound=original_prices[2], cat='Continuous')
    # 定义变量：桌子，设置下限单价为 75 * (1 - max_increase)，上限单价为 75
    desk_price = pulp.LpVariable('desk price', lowBound=original_prices[3] * (1 - max_decrease), upBound=original_prices[3], cat='Continuous')
    # 定义变量：打印机，设置下限单价为 52，上限单价为 52 * (1 + max_increase)
    printer_price = pulp.LpVariable('printer price', lowBound=original_prices[4], upBound=original_prices[4] * (1 + max_increase), cat='Continuous')
    # 设置目标函数
    MyProblem += 13 * computer_price + 18 * air_conditioner_price + 7 * washer_price + 7 * desk_price + 38 * printer_price, "最终总价"
    # 添加约束条件
    MyProblem += (
                10 * computer_price + 20 * air_conditioner_price + 8 * washer_price + 7 * desk_price + 35 * printer_price <= 3175), "预算与原先相同"
    MyProblem.solve()
    print("***************** Info *******************")
    print("Status:", pulp.LpStatus[MyProblem.status])
    for v in MyProblem.variables():
        print(v.name, "=", v.varValue)
    print("最终总价最大值为：", pulp.value(MyProblem.objective))
    MyProblem.writeLP('Budget Bid Price.lp')

if __name__ == '__main__':
    max_increase = 0.2
    max_decrease = 0.2
    calculate_maximum_quote(max_increase, max_decrease)
