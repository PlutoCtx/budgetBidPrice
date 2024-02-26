# @Version: python3.10
# @Time: 2024/1/21 15:32
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: matrix_test.py
# @Software: PyCharm
# @User: chent

import numpy as np
import pandas as pd
pd.set_option('display.unicode.ambiguous_as_wide', True)  # 处理数据的列标题与数据无法对齐的情况
# pd.set_option('display.unicode.east_asian_width', True)   # 无法对齐主要是因为列标题是中文


def get_excel_data(path):
    """
        读取excel表中的数据，包括采购内容、原始数量、原始单价、实际数量
    :param path:    excel文件所在的位置
    :return:    DataFrame形式的列表，包括采购内容、原始数量、原始单价、实际数量
    """
    excel_data = pd.read_excel(path)
    procurementContent = excel_data[['采购内容']]
    originalQuantity = excel_data[['原始数量']]
    originalUnitPrice = excel_data[['原始单价']]
    actualQuantity = excel_data[['实际数量']]

    return procurementContent, originalQuantity, originalUnitPrice, actualQuantity


def change_data_frame_to_int(dataFrame_list):
    """
        转换DataFrame的数据类型
    :param dataFrame_list:  DataFrame类型的列表
    :return:   原始数据形式的列表，按道理是数字
    """
    res = []
    for i in range(len(dataFrame_list)):
        res.append(dataFrame_list[i:i + 1].values[0][0])
    return res


def get_original_total_price(quality_value_list, unit_price_value_list):
    """
    计算各个采购商品的原始总价
    :param quality_value_list:      各个采购商品的原始数量
    :param unit_price_value_list:   各个采购商品的原始单价
    :return:    res_list--各个采购商品的原始总价
                total_sum--各个采购商品的总价格
    """
    res_list = []
    for i in range(len(quality_value_list)):
        # print(quality_value_list[i], unit_price_value_list[i], quality_value_list[i] * unit_price_value_list[i])
        res_list.append(quality_value_list[i] * unit_price_value_list[i])
    total_sum = sum(res_list)

    return res_list, total_sum


def get_revised_unit_price(original_quantity, actual_quantity):
    """
    标记是否修正单价应该上涨还是下跌
    在实际数量增加的情况下，标记为1，代表上涨；
    不变 -> 0，待定
    减少 -> -1，下降
    :param original_quantity:   原始数量
    :param actual_quantity:     实际数量
    :return:
    """
    revised_unit_price_flag = []
    for i in range(len(original_quantity)):
        if original_quantity < actual_quantity:
            revised_unit_price_flag.append(1)
        elif original_quantity == actual_quantity:
            revised_unit_price_flag.append(0)
        elif original_quantity > actual_quantity:
            revised_unit_price_flag.append(-1)

    return revised_unit_price_flag




if __name__ == '__main__':
    # excel文件路径
    path = "D:\ProgramingCodes\commodities\\2024y\pythonProject\\budgetBidPrice\\test\data\\test.xlsx"
    # 分别对应 采购内容、原始数量、原始单价、实际数量
    procurementContent, originalQuantity, originalUnitPrice, actualQuantity = get_excel_data(path)

    # 把以上内容转为数字类型的列表，方便计算（原先的会显示表头）
    # 原始数量
    originalQuantity_value = change_data_frame_to_int(originalQuantity)
    # 原始单价
    originalUnitPrice_value = change_data_frame_to_int(originalUnitPrice)
    # 实际数量
    actualQuantity_value = change_data_frame_to_int(actualQuantity)

    # 各个采购内容的原始总价，以及所有采购内容的总价
    originalTotalPrice, totalOriginalPrice = get_original_total_price(originalQuantity_value, originalUnitPrice_value)

    print('*********************************')
    print(originalQuantity_value)
    print(originalUnitPrice_value)
    print(originalTotalPrice)
    print(totalOriginalPrice)
