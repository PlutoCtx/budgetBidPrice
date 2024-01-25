# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 16:37
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: demo03.py
# @Software: PyCharm
# @User: chent

from pulp import *
# 以下代码拷贝自官网文档 https://coin-or.github.io/pulp/CaseStudies/a_blending_problem.html
# Creates a list of the Ingredients
Ingredients = ["CHICKEN", "BEEF", "MUTTON", "RICE", "WHEAT", "GEL"]
# A dictionary of the costs of each of the Ingredients is created
costs = {
    "CHICKEN": 0.013,
    "BEEF": 0.008,
    "MUTTON": 0.010,
    "RICE": 0.002,
    "WHEAT": 0.005,
    "GEL": 0.001,
}
# A dictionary of the protein percent in each of the Ingredients is created
proteinPercent = {
    "CHICKEN": 0.100,
    "BEEF": 0.200,
    "MUTTON": 0.150,
    "RICE": 0.000,
    "WHEAT": 0.040,
    "GEL": 0.000,
}
# A dictionary of the fat percent in each of the Ingredients is created
fatPercent = {
    "CHICKEN": 0.080,
    "BEEF": 0.100,
    "MUTTON": 0.110,
    "RICE": 0.010,
    "WHEAT": 0.010,
    "GEL": 0.000,
}
# A dictionary of the fibre percent in each of the Ingredients is created
fibrePercent = {
    "CHICKEN": 0.001,
    "BEEF": 0.005,
    "MUTTON": 0.003,
    "RICE": 0.100,
    "WHEAT": 0.150,
    "GEL": 0.000,
}
saltPercent = {
    "CHICKEN": 0.002,
    "BEEF": 0.005,
    "MUTTON": 0.007,
    "RICE": 0.002,
    "WHEAT": 0.008,
    "GEL": 0.000,
}

# 建立线性规划问题，指定名称：CatFood， 问题的目标：求解最小值 LpMinimize
prob = pulp.LpProblem(name='CatFood', sense=LpMinimize)
# 直接用字典定义变量
ingredient_vars = LpVariable.dicts("Ingr", Ingredients, 0)
# # 查看变量字典
# ingredient_vars
# {'CHICKEN': Ingr_CHICKEN,
#  'BEEF': Ingr_BEEF,
#  'MUTTON': Ingr_MUTTON,
#  'RICE': Ingr_RICE,
#  'WHEAT': Ingr_WHEAT,
#  'GEL': Ingr_GEL}

print(ingredient_vars)
# 目标函数
prob += lpSum([costs[i]*ingredient_vars[i] for i in Ingredients]), "cost"

# 约束条件
prob += lpSum([ingredient_vars[i] for i in Ingredients]) == 100, "PercentagesSum"
prob += lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 8.0, "ProteinRequirement"
prob += lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 6.0, "FatRequirement"
prob += lpSum([fibrePercent[i] * ingredient_vars[i] for i in Ingredients]) <= 2.0, "FibreRequirement"
prob += lpSum([saltPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.4, "SaltRequirement"

# 求解并输出结果
prob.solve()
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("每100克猫粮的最小成本 = ", value(prob.objective))


# Status: Optimal
# Ingr_BEEF = 60.0
# Ingr_CHICKEN = 0.0
# Ingr_GEL = 40.0
# Ingr_MUTTON = 0.0
# Ingr_RICE = 0.0
# Ingr_WHEAT = 0.0
# 每100克猫粮的最小成本 =  0.52