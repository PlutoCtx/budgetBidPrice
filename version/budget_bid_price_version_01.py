# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 23:49
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: budget_bid_price_version.py
# @Software: PyCharm
# @User: chent

from tkinter import *
from tkinter.filedialog import askopenfilename

import pandas as pd
import pulp
import xlsxwriter as xw
from pulp import *

# 创建主窗口
frameT = Tk()
# 创建两个字符串变量，用于绑定输入框的值
file_path_var = StringVar()
max_increase_var = StringVar()
max_decrease_var = StringVar()
key_list = []

def get_excel_data(path):
    """
        读取excel表中的数据，包括采购内容、原始数量、原始单价、实际数量
    :param path:    excel文件所在的位置
    :return:    DataFrame形式的列表，包括采购内容、原始数量、原始单价、实际数量
    """
    excel_data = pd.read_excel(path)
    # print("len(excel_data):" + str(len(excel_data)))

    procurementContent = excel_data.iloc[:, 0]
    originalQuantity = excel_data.iloc[:, 1]
    originalUnitPrice = excel_data.iloc[:, 2]
    actualQuantity = excel_data.iloc[:, 4]
    generate_key_list_by_length(len(excel_data))

    procurementContent_list = pandas_series_to_list(procurementContent)
    originalQuantity_list = pandas_series_to_list(originalQuantity)
    originalUnitPrice_list = pandas_series_to_list(originalUnitPrice)
    actualQuantity_list = pandas_series_to_list(actualQuantity)

    procurementContent_dict, originalQuantity_dict, originalUnitPrice_dict, actualQuantity_dict = generate_four_base_dict(key_list,
                            procurementContent_list,
                            originalQuantity_list,
                            originalUnitPrice_list,
                            actualQuantity_list)

    return procurementContent_dict, originalQuantity_dict, originalUnitPrice_dict, actualQuantity_dict

def generate_original_total_prices(originalQuantity_dict, originalUnitPrice_dict):
    """
    生成各个商品的原始总价，并得到原本的总预算数目
    :param originalQuantity_dict:   各个原始商品的数量
    :param originalUnitPrice_dict:  各个原始商品的单价
    :return: original_total_prices -> 各个商品的原始总价, original_total_price -> 原本的总预算数目
    """
    original_total_prices_dict = {}
    original_total_price = 0
    for k in key_list:
        temp = originalQuantity_dict[k] * originalUnitPrice_dict[k]
        original_total_prices_dict[k] = temp
        original_total_price += temp

    return original_total_prices_dict, original_total_price

def generate_four_base_dict(key_list,
                            procurementContent_list,
                            originalQuantity_list,
                            originalUnitPrice_list,
                            actualQuantity_list):
    """
    将原本的表格中的数据通过一个key_list实现对应，使得我们可以通过访问key_list的元素进行访问
    :param key_list:    key_list，全局的字典键值
    :param procurementContent_list:     采购内容
    :param originalQuantity_list:       原始的数量
    :param originalUnitPrice_list:      原始单价
    :param actualQuantity_list:         实际数量
    :return:
    """
    procurementContent_dict = {}
    originalQuantity_dict = {}
    originalUnitPrice_dict = {}
    actualQuantity_dict = {}

    for i in range(len(key_list)):
        procurementContent_dict[key_list[i]] = procurementContent_list[i]
        originalQuantity_dict[key_list[i]] = originalQuantity_list[i]
        originalUnitPrice_dict[key_list[i]] = originalUnitPrice_list[i]
        actualQuantity_dict[key_list[i]] = actualQuantity_list[i]


    return procurementContent_dict, originalQuantity_dict, originalUnitPrice_dict, actualQuantity_dict


def generate_key_list_by_length(length):
    """
    生成一个全局的key_list，用来生成后面各个数据的字典，防止因为没对齐导致的错误
    :param length:  待处理的excel表格中除了表头之外的数据行数
    :return: 一个key_list列表
    """
    for i in range(length):
        key_list.append('key' + str(i + 1))


def pandas_series_to_list(series):
    """
    将series转换成列表，去掉烦人的表头，方便类型的转换
    :param series:  excel_data.iloc[:, 4]类型
    :return: list
    """
    return series.tolist()


def generate_up_or_down_flag_dict(originalQuantity_dict, actualQuantity_dict):
    """
    根据原始的需求数量与当前的需求数量，生成各个商品的单价增减标签字典
    1 -> 单价上升
    0 -> 单价上升/不变/下降
    -1 -> 单价下降
    :param originalQuantity_dict:   原始的需求数量
    :param actualQuantity_dict:     当前的需求数量
    :return:
    """
    up_and_down_flag_dict = {}
    for k in key_list:
        if actualQuantity_dict[k] > originalQuantity_dict[k]:
            up_and_down_flag_dict[k] = 1
        elif actualQuantity_dict[k] == originalQuantity_dict[k]:
            up_and_down_flag_dict[k] = 0
        elif actualQuantity_dict[k] < originalQuantity_dict[k]:
            up_and_down_flag_dict[k] = -1

    return up_and_down_flag_dict


def calculate_PULP(up_and_down_flag_dict,
                   originalQuantity_dict,
                   actualQuantity_dict,
                   originalUnitPrice_dict,
                   max_increase,
                   max_decrease,
                   original_total_price
                   ):
    """
    用于解决当前的详细规划问题，计算出各个商品修改之后的价格
    :param up_and_down_flag_dict:   是否增长/不变/减小，保存有1/-1/0的数字，
                            1 代表与原始数量相比，实际数量增加，修正单价应上涨；
                            0 代表与原始数量相比，实际数量不变，修正单价可以上涨/不变/下降；
                            -1 代表与原始数量相比，实际数量减少，修正单价应下降
    :param originalQuantity_dict:   原始商品购买数量
    :param actualQuantity_dict:     实际商品购买数量
    :param originalUnitPrice_dict:  原始商品单价
    :param max_increase:            最大涨幅
    :param max_decrease:            最大降幅
    :param original_total_price:    原始预算总价
    :return:        各个商品修改之后的价格，修改后的总预算
    """
    # 定义线性规划问题
    MyProblem = LpProblem("Budget_Bid_Price", sense=LpMaximize)

    # 设置每个变量的上下限
    print("******** 设置每个变量的上下限 **********")
    for k in key_list:
        if up_and_down_flag_dict[k] == 1:
            v = pulp.LpVariable(k, lowBound=originalUnitPrice_dict[k], upBound=originalUnitPrice_dict[k] * (1 + max_increase),
                                cat='Continuous')
            MyProblem.addVariable(v)
            print(v.name, v.upBound, v.lowBound, v)
        elif up_and_down_flag_dict[k] == 0:
            v = pulp.LpVariable(k, lowBound=originalUnitPrice_dict[k] * (1 - max_decrease),
                                upBound=originalUnitPrice_dict[k] * (1 + max_increase), cat='Continuous')
            MyProblem.addVariable(v)
            print(v.name, v.upBound, v.lowBound, v)
        elif up_and_down_flag_dict[k] == -1:
            v = pulp.LpVariable(k, lowBound=originalUnitPrice_dict[k] * (1 - max_decrease),
                                upBound=originalUnitPrice_dict[k], cat='Continuous')
            MyProblem.addVariable(v)
            print(v.name, v.upBound, v.lowBound, v)
    print("********* 参数上下限设置完毕 ************")

    # 建立目标函数
    MyProblem += lpSum([actualQuantity_dict[v.name] * v for v in MyProblem.variables()]), 'TheFinalCost'

    # 约束条件
    MyProblem += lpSum([originalQuantity_dict[v.name] * v for v in MyProblem.variables()]) <= original_total_price, 'ConstrainedRequirement'

    # 计算
    currentPath = os.getcwd()
    solverPath = os.path.join(currentPath, 'cbc.exe')
    MyProblem.solve(COIN_CMD(path=solverPath))

    print("***************** Info *******************")
    print("Status:", LpStatus[MyProblem.status])
    res_updated_price = []
    updated_price_dict = {}
    for v in MyProblem.variables():
        res_updated_price.append(v.varValue)
        updated_price_dict[v.name] = v.varValue
        print(v.name, "=", v.varValue)
    print("最终总价最大值为：", pulp.value(MyProblem.objective))
    finalNumber = pulp.value(MyProblem.objective)
    MyProblem.writeLP('Budget Bid Price.lp')

    return updated_price_dict, finalNumber


def generate_final_budget_and_budget_dict(updated_price_dict, actualQuantity_dict):
    """
    生成各个商品单价修改之后的总价
    :param updated_price_dict:      修改后的商品单价
    :param actualQuantity_dict:     实际的商品购买数量
    :return:
    """
    budget_dict = {}
    final_budget = 0
    for k in key_list:
        temp = updated_price_dict[k] * actualQuantity_dict[k]
        final_budget += temp
        budget_dict[k] = temp
    return budget_dict, final_budget



def generate_excel_data(procurementContent_dict,
                        originalQuantity_dict,
                        originalUnitPrice_dict,
                        original_total_prices_dict,
                        actualQuantity_dict,
                        updated_price_dict,
                        final_budget_dict,
                        original_total_price,
                        finalNumber
                        ):
    """
    汇总各列的数据，将其合并为一张表格
    :param procurementContent_dict:     采购内容
    :param originalQuantity_dict:       原始各商品购买数量
    :param originalUnitPrice_dict:      原始各商品购买单价
    :param original_total_prices_dict:  原始各商品总价
    :param actualQuantity_dict:         实际商品购买数量
    :param updated_price_dict:          修改后商品单价
    :param final_budget_dict:           最终各商品总价
    :param original_total_price:        原始的总预算
    :param finalNumber:                 最终的总预算
    :return:
    """

    excel_data = []

    for k in key_list:
        temp = {}
        temp['procurementContent'] = procurementContent_dict[k]
        temp['originalQuantity'] = originalQuantity_dict[k]
        temp['originalUnitPrice'] = originalUnitPrice_dict[k]
        temp['originalTotalPrices'] = original_total_prices_dict[k]
        temp['actualQuantity'] = actualQuantity_dict[k]
        temp['updatedPrice'] = updated_price_dict[k]
        temp['finalBudget'] = final_budget_dict[k]
        excel_data.append(temp)

    temp = {}
    temp['procurementContent'] = None
    temp['originalQuantity'] = None
    temp['originalUnitPrice'] = '总和'
    temp['originalTotalPrices'] = original_total_price
    temp['actualQuantity'] = None
    temp['updatedPrice'] = '最终预算'
    temp['finalBudget'] = finalNumber
    excel_data.append(temp)

    return excel_data


def generate_excel_workbook(procurementContent_dict,
                        originalQuantity_dict,
                        originalUnitPrice_dict,
                        original_total_prices_dict,
                        actualQuantity_dict,
                        updated_price_dict,
                        final_budget_dict,
                        original_total_price,
                        finalNumber):

    excel_data = generate_excel_data(procurementContent_dict,
                        originalQuantity_dict,
                        originalUnitPrice_dict,
                        original_total_prices_dict,
                        actualQuantity_dict,
                        updated_price_dict,
                        final_budget_dict,
                        original_total_price,
                        finalNumber)
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
                      excel_data[j]['originalTotalPrices'],
                      excel_data[j]['actualQuantity'],
                      excel_data[j]['updatedPrice'],
                      excel_data[j]['finalBudget']
                      ]
        row = 'A' + str(i)
        print(excel_data[j]['procurementContent'], excel_data[j]['originalQuantity'], excel_data[j]['originalUnitPrice'],
                      excel_data[j]['originalTotalPrices'], excel_data[j]['actualQuantity'],
                      excel_data[j]['updatedPrice'], excel_data[j]['finalBudget'])
        sheet01.write_row(row, insertData)
        i += 1
    workbook.close()


def business_handle(path, max_increase, max_decrease):
    procurementContent_dict, originalQuantity_dict, originalUnitPrice_dict, actualQuantity_dict = get_excel_data(path)

    original_total_prices_dict, original_total_price = generate_original_total_prices(
        originalQuantity_dict=originalQuantity_dict,
        originalUnitPrice_dict=originalUnitPrice_dict)

    up_and_down_flag_dict = generate_up_or_down_flag_dict(originalQuantity_dict=originalQuantity_dict,
                                                          actualQuantity_dict=actualQuantity_dict)

    updated_price_dict, finalNumber = calculate_PULP(up_and_down_flag_dict,
                                                     originalQuantity_dict,
                                                     actualQuantity_dict,
                                                     originalUnitPrice_dict,
                                                     max_increase,
                                                     max_decrease,
                                                     original_total_price)
    final_budget_dict, final_budget = generate_final_budget_and_budget_dict(updated_price_dict, actualQuantity_dict)

    generate_excel_workbook(procurementContent_dict,
                            originalQuantity_dict,
                            originalUnitPrice_dict,
                            original_total_prices_dict,
                            actualQuantity_dict,
                            updated_price_dict,
                            final_budget_dict,
                            original_total_price,
                            finalNumber)

# 定义打开文件对话框的函数，并将选择的文件路径设置到字符串变量file_path_var中
def fileopen():
    file_sql = askopenfilename()  # 打开文件对话框，获取选择的文件路径
    if file_sql:  # 如果选择了文件路径
        file_path_var.set(file_sql)  # 将文件路径设置到字符串变量v1中
        print(f"选择了文件：{file_sql}")  # 在控制台打印被选择文件的路径


# 定义运行函数，用于打印两个输入框的值（即被选择文件的路径）
def match():
    file_path = file_path_var.get().replace('/', '//')
    max_increase_ = float(max_increase_var.get())
    max_decrease_ = float(max_decrease_var.get())
    print(file_path, max_increase_, max_decrease_)
    business_handle(file_path, max_increase_, max_decrease_)


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
