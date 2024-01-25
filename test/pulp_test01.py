# @Version: python3.10
# @Time: 2024/1/25 12:25
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: pulp_test01.py
# @Software: PyCharm
# @User: chent

import pulp
MyProbLP = pulp.LpProblem("LPProbDemo1", sense=pulp.LpMaximize)
x1 = pulp.LpVariable('x1', lowBound=0, upBound=7, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, upBound=7, cat='Continuous')
x3 = pulp.LpVariable('x3', lowBound=0, upBound=7, cat='Continuous')
MyProbLP += 2*x1 + 3*x2 - 5*x3  	# 设置目标函数
MyProbLP += (2*x1 - 5*x2 + x3 >= 10)  # 不等式约束
MyProbLP += (x1 + 3*x2 + x3 <= 12)  # 不等式约束
MyProbLP += (x1 + x2 + x3 == 7)  # 等式约束
MyProbLP.solve()
print("Status:", pulp.LpStatus[MyProbLP.status])    # 输出求解状态
for v in MyProbLP.variables():
    print(v.name, "=", v.varValue)  # 输出每个变量的最优值
print("F(x) = ", pulp.value(MyProbLP.objective))  # 输出最优解的目标函数值

# = 关注 Youcans，分享原创系列 https://blog.csdn.net/youcans =
