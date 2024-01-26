# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 23:49
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: ui_demo03.py
# @Software: PyCharm
# @User: chent

from tkinter import *
from tkinter.filedialog import askopenfilename

import pandas as pd
import xlsxwriter as xw
from pulp import *

# 创建主窗口
frameT = Tk()
# 创建两个字符串变量，用于绑定输入框的值
file_path_var = StringVar()
max_increase_var = StringVar()
max_decrease_var = StringVar()


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
    workbook = xw.Workbook('result.xlsx')
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

def business_handle(path, max_increase, max_decrease):
    procurementContent, originalQuantity, originalUnitPrice, actualQuantity = get_excel_data(path)

    key_list = get_key_list(procurementContent)
    flag_list = generate_flag_list(originalQuantity, actualQuantity)
    original_unit_price = pandas_series_to_list(originalUnitPrice)
    actual_number_dict = get_actual_number_dict(key_list, actualQuantity)
    original_number_dict = get_original_number_dict(key_list, originalQuantity)
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


# 定义打开文件对话框的函数，并将选择的文件路径设置到字符串变量file_path_var中
def fileopen():
    file_sql = askopenfilename()  # 打开文件对话框，获取选择的文件路径
    if file_sql:  # 如果选择了文件路径
        file_path_var.set(file_sql)  # 将文件路径设置到字符串变量v1中
        print(f"选择了总文件：{file_sql}")  # 在控制台打印被选择文件的路径


# 定义运行函数，用于打印两个输入框的值（即被选择文件的路径）
def match():
    file_path = file_path_var.get().replace('/', '//')
    max_increase_ = float(max_increase_var.get())
    max_decrease_ = float(max_decrease_var.get())

    business_handle(file_path, max_increase_, max_decrease_)

    print(file_path, type(file_path))
    print(max_increase_, type(max_increase_))
    print(max_decrease_, type(max_decrease_))

def init_frame(frameT):

    frameT.geometry('500x300+400+200')  # 设置窗口大小和位置
    frameT.title('请选择需要处理的文件')  # 设置窗口标题

    # 框架一：选择文件-文件路径显示与文件选择按钮
    frame_file_choose = Frame(frameT)
    frame_file_choose.pack(padx=10, pady=10)  # 设置外边距

    # 框架二：设置最大涨幅-最大涨幅输入框以及标签
    frame_max_increase = Frame(frameT)
    frame_max_increase.pack(padx=10, pady=10)  # 设置外边距

    # 框架三：设置最大降幅-最大降幅输入框以及标签
    frame_max_decrease = Frame(frameT)
    frame_max_decrease.pack(padx=10, pady=10)  # 设置外边距

    # 框架四:放置运行和退出按钮
    frame_run_and_exit = Frame(frameT)
    frame_run_and_exit.pack(padx=10, pady=10)  # 设置外边距

    # 创建两个标签
    label_max_increase = Label(frame_max_increase, text='请输入最大涨幅：', font=("宋体", 14))
    label_max_increase.pack(fill=X, side=LEFT)
    label_max_decrease = Label(frame_max_decrease, text='请输入最大降幅：', font=("宋体", 14))
    label_max_decrease.pack(fill=X, side=LEFT)

    # 创建第一个输入框，并绑定字符串变量file_path_var
    ent_file_path = Entry(frame_file_choose, width=50, textvariable=file_path_var)
    ent_file_path.pack(fill=X, side=LEFT)  # x方向填充，靠左

    # 创建第二个输入框，并绑定字符串变量max_increase_var
    ent_max_increase = Entry(frame_max_increase, width=25, textvariable=max_increase_var)
    ent_max_increase.pack(fill=X, side=LEFT)  # x方向填充，靠左

    # 创建第三个输入框，并绑定字符串变量max_decrease_var
    ent_max_decrease = Entry(frame_max_decrease, width=25, textvariable=max_decrease_var)
    ent_max_decrease.pack(fill=X, side=LEFT)  # x方向填充，靠左

    # 创建第一个按钮，并绑定打开文件对话框的函数fileopen
    btn_file_choose = Button(frame_file_choose, width=20, text='选择文件', font=("宋体", 14), command=fileopen)
    btn_file_choose.pack(fill=X, padx=10)

    # 创建第三个按钮，并绑定运行函数match
    ext = Button(frame_run_and_exit, width=10, text='运行', font=("宋体", 14), command=match)
    ext.pack(side=LEFT)

    # 创建第四个按钮，并绑定退出窗口的函数frameT.quit()
    etb = Button(frame_run_and_exit, width=10, text='退出', font=("宋体", 14), command=frameT.quit)
    etb.pack(side=RIGHT)

    # 进入主循环，等待用户操作和事件触发
    frameT.mainloop()


if __name__ == '__main__':

    init_frame(frameT)
