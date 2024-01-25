# @Version: python3.10
# @Time: 2024/1/24 22:49
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: pulp_config.py
# @Software: PyCharm
# @User: chent

import pulp

from pulp import *

list1 = [10, 20, 8, 7, 35]
max_increase1 = 0.2
max_decrease = 0.2
x = 3175
list2 = [15, 20, 35, 75, 52]
list3 = [1, -1, -1, 0, 1]
# 定义问题
prob = LpProblem("Maximize the sum of list2", LpMaximize)
# 定义变量
vars = LpVariable.dicts("Var", range(1, len(list1) + 1), 0, None, LpInteger)
# 建立目标函数
prob += lpSum(vars)
# 建立约束条件
for i in range(len(list1)):
    # 添加目标函数的约束条件
    if list3[i] == 1:
        prob += vars[i] <= max_increase1 * list2[i] / list1[i]
    elif list3[i] == 0:
        prob += vars[i] <= list2[i] / list1[i]
    else:  # list3[i] == -1
        prob += vars[i] >= list2[i] / list1[i] * (1 - max_decrease)

prob += lpSum([vars[i] * list1[i] for i in range(len(list1))]) <= x
# 求解问题
prob.solve()
# 输出结果
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Objective=", value(prob.objective))



























# 定义问题
prob = pulp.LpProblem("Maximize the sum of list2", pulp.LpMaximize)

# 定义变量
vars = pulp.LpVariable.dicts("Var", range(1, len(list1) + 1), 0, None, pulp.LpInteger)

# 建立目标函数
prob += pulp.lpSum(vars)

# 建立约束条件
for i in range(len(list1)):
    if list3[i] == 1:
        prob += vars[i] <= max_increase1 * list2[i] / list1[i]
    elif list3[i] == 0:
        prob += vars[i] <= list2[i] / list1[i]
    else:  # list3[i] == -1
        prob += vars[i] >= list2[i] / list1[i] * (1 - max_decrease)

    # 添加目标函数的约束条件
prob += pulp.lpSum([vars[i] * list1[i] for i in range(len(list1))]) <= x

# 求解问题
prob.solve()

# 输出结果
print("Status:", pulp.LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Objective=", pulp.value(prob.objective))

