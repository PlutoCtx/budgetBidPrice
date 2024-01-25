# @Version: python3.10
# @Time: 2024/1/25 11:38
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: lowest_cost.py
# @Software: PyCharm
# @User: chent
import pulp
# 导入 PulP
from pulp import *

# 建立线性规划问题，指定名称：CatFood， 问题的目标：求解最小值 LpMinimize
prob = pulp.LpProblem(name='CatFood', sense=LpMinimize)
# 定义变量: 鸡肉占比，设置下限值为 0 ， 不能是负数
x1 = LpVariable("鸡肉占比", lowBound=0)
# 定义变量: 牛肉占比，设置下限值为 0 ， 不能是负数
x2= LpVariable("牛肉占比", lowBound=0)
# 将目标函数用 += 方式附加到 prob 变量
prob += 0.013*x1 + 0.008*x2, "最小成本"
# 将约束条件用 += 方式附加到 prob 变量，注意区别是约束条件有判断操作符
prob += x1 + x2 == 100, "占比总和"
prob += (0.100 * x1 + 0.200 * x2 >= 8.0), "蛋白质含量"
prob += (0.080 * x1 + 0.100 * x2 >= 6.0), "脂肪含量"
prob += (0.001 * x1 + 0.005 * x2 <= 2.0), "纤维含量"
prob += (0.002 * x1 + 0.005 * x2 <= 0.4), "盐含量"
prob.solve()
# 输出求解状态
print("Status:", LpStatus[prob.status])
# 输出每个变量最优值
for v in prob.variables():
    print(v.name, "=", v.varValue)
print(pulp.value(prob.objective))
# 将问题输出为 lp 文件
prob.writeLP('catfood.lp')

