# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 19:27
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: demo1_1.py
# @Software: PyCharm
# @User: chent

import pandas as pd
import xlsxwriter as xw
from pulp import *
from pypinyin import lazy_pinyin


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
    res_updated_price = []
    for v in MyProblem.variables():
        res_updated_price.append(v.varValue)
        print(v.name, "=", v.varValue)
    print("最终总价最大值为：", pulp.value(MyProblem.objective))
    finalNumber = pulp.value(MyProblem.objective)
    MyProblem.writeLP('Budget Bid Price.lp')

    return res_updated_price, finalNumber

def pandas_series_to_list(series):
    return series.tolist()


def get_key_list(series):
    temp_list = pandas_series_to_list(series)
    res_list = []
    count = 0
    for s in temp_list:
        # res_list.append(chinese_to_pinyin(s))
        res_list.append('key' + str(count))
        count += 1
        # print(chinese_to_pinyin(s))/
    return res_list

def get_original_number_dict(key_l, original_number):
    res_dict = {}
    for i in range(len(key_l)):
        res_dict[key_l[i]] = original_number[i]

    return res_dict


def get_actual_number_dict(key_l, actual_number):
    res_dict = {}
    for i in range(len(key_l)):
        res_dict[key_l[i]] = actual_number[i]

    return res_dict


def get_original_total_budget(original_unit_price, original_number):
    res_total = 0
    total = []
    original_number = pandas_series_to_list(original_number)
    for i in range(len(original_number)):
        total.append(original_number[i] * original_unit_price[i])

    res_total = sum(total)
    return total, res_total



def generate_flag_list(originalQuantity, actualQuantity):
    res_flag_list = []
    originalQuantity_list = pandas_series_to_list(originalQuantity)
    actualQuantity_list = pandas_series_to_list(actualQuantity)
    for i in range(len(actualQuantity_list)):
        if actualQuantity_list[i] > originalQuantity_list[i]:
            res_flag_list.append(1)
        elif actualQuantity_list[i] == originalQuantity_list[i]:
            res_flag_list.append(0)
        elif actualQuantity_list[i] < originalQuantity_list[i]:
            res_flag_list.append(-1)
    return res_flag_list


def get_excel_data(path):
    """
        读取excel表中的数据，包括采购内容、原始数量、原始单价、实际数量
    :param path:    excel文件所在的位置
    :return:    DataFrame形式的列表，包括采购内容、原始数量、原始单价、实际数量
    """
    excel_data = pd.read_excel(path)

    procurementContent = excel_data.iloc[:, 0]
    originalQuantity = excel_data.iloc[:, 1]
    originalUnitPrice = excel_data.iloc[:, 2]
    actualQuantity = excel_data.iloc[:, 4]
    return procurementContent, originalQuantity, originalUnitPrice, actualQuantity


def generate_data(procurementContent_list,
                            originalQuantity_list,
                            originalUnitPrice_list,
                            originalBudget_list,
                            originalTotalBudget,
                            actualQuantity_list,
                            updatedQuantity_list,
                            final_budget_list,
                            final_Budget):
    excel_data = []
    for i in range(len(procurementContent_list)):
        temp = {}
        temp['procurementContent'] = procurementContent_list[i]
        temp['originalQuantity'] = originalQuantity_list[i]
        temp['originalUnitPrice'] = originalUnitPrice_list[i]
        temp['originalBudget'] = originalBudget_list[i]
        temp['actualQuantity'] = actualQuantity_list[i]
        temp['updatedQuantity'] = updatedQuantity_list[i]
        temp['finalBudget'] = final_budget_list[i]
        excel_data.append(temp)

    temp = {}
    temp['procurementContent'] = None
    temp['originalQuantity'] = None
    temp['originalUnitPrice'] = '总和'
    temp['originalBudget'] = originalTotalBudget
    temp['actualQuantity'] = None
    temp['updatedQuantity'] = '最终预算'
    temp['finalBudget'] = final_Budget
    excel_data.append(temp)

    return excel_data


def generate_excel_workbook(procurementContent_list,
                            originalQuantity_list,
                            originalUnitPrice_list,
                            originalBudget_list,
                            originalTotalBudget,
                            actualQuantity_list,
                            updatedQuantity_list,
                            final_budget_list,
                            final_Budget):

    excel_data = generate_data(procurementContent_list,
                            originalQuantity_list,
                            originalUnitPrice_list,
                            originalBudget_list,
                            originalTotalBudget,
                            actualQuantity_list,
                            updatedQuantity_list,
                            final_budget_list,
                            final_Budget)
    workbook = xw.Workbook('example.xlsx')
    sheet01 = workbook.add_worksheet('sheet1')
    sheet01.activate()
    title = ['采购内容', '原始数量', '原始单价', '原始总价', '实际数量', '修正单价', '最终总价']
    sheet01.write_row('A1', title)
    i = 2

    for j in range(len(excel_data)):
        insertData = [excel_data[j]['procurementContent'],
                      excel_data[j]['originalQuantity'],
                      excel_data[j]['originalUnitPrice'],
                      excel_data[j]['originalBudget'],
                      excel_data[j]['actualQuantity'],
                      excel_data[j]['updatedQuantity'],
                      excel_data[j]['finalBudget']
                      ]
        row = 'A' + str(i)
        sheet01.write_row(row, insertData)
        i += 1
    workbook.close()


def generate_final_budget_list(actualQuantity_list, updated_unit_price_list):
    final_budget_list = []
    for i in range(len(actualQuantity_list)):
        final_budget_list.append(actualQuantity_list[i] * updated_unit_price_list[i])
    return final_budget_list

def business_handle(path):
    procurementContent, originalQuantity, originalUnitPrice, actualQuantity = get_excel_data(path)

    key_list = get_key_list(procurementContent)
    flag_list = generate_flag_list(originalQuantity, actualQuantity)
    original_unit_price = pandas_series_to_list(originalUnitPrice)
    actual_number_dict = get_actual_number_dict(key_list, actualQuantity)
    original_number_dict = get_original_number_dict(key_list, originalQuantity)
    max_increase = 0.2
    max_decrease = 0.2
    original_total_budget_list, original_total_budget = get_original_total_budget(original_unit_price, originalQuantity)
    updated_price, final_budget = cal_PULP(key_list=key_list,
             flag_list=flag_list,
             original_price=original_unit_price,
             actual_number_dict=actual_number_dict,
             original_number_dict=original_number_dict,
             max_increase=max_increase,
             max_decrease=max_decrease,
             original_total_budget=original_total_budget)

    procurementContent_list = pandas_series_to_list(procurementContent)
    originalQuantity_list = pandas_series_to_list(originalQuantity)
    original_unit_price_list = original_unit_price
    actualQuantity_list = pandas_series_to_list(actualQuantity)
    final_budget_list = generate_final_budget_list(actualQuantity_list=actualQuantity_list, updated_unit_price_list=updated_price)

    generate_excel_workbook(procurementContent_list=procurementContent_list,
                            originalQuantity_list=originalQuantity_list,
                            originalUnitPrice_list=original_unit_price_list,
                            originalBudget_list=original_total_budget_list,
                            originalTotalBudget=original_total_budget,
                            actualQuantity_list=actualQuantity_list,
                            updatedQuantity_list=updated_price,
                            final_budget_list=final_budget_list,
                            final_Budget=final_budget
                            )


if __name__ == '__main__':
    path = 'D:\\ProgramingCodes\\commodities\\2024y\\pythonProject\\budgetBidPrice\\demo\\data\\data.xls'

    business_handle(path)
