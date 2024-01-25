# @Version: python3.10
# @Time: 2024/1/21 16:42
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: gpt.py
# @Software: PyCharm
# @User: chent

import numpy as np

def process_matrix(c, p):
    # 创建一个与c形状相同的矩阵f，所有元素初始化为0
    f = np.zeros_like(c)

    # 对矩阵c的每个元素进行遍历
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            # 获取当前元素的值
            current_value = c[i, j]

            # 根据规则对当前元素进行处理，并更新f中的对应元素
            # 这里只是一个示例，你可以根据实际需求修改处理规则
            if current_value > 0:
                f[i, j] = current_value + p  # 当前值加上一个范围在-p到p之间的值
            elif current_value < 0:
                f[i, j] = current_value - p  # 当前值减去一个范围在-p到p之间的值
            else:  # 当前值为0，保持不变
                f[i, j] = current_value

    # 返回处理后的矩阵f
    print("f:")
    print(f)
    return f


def max_sum_of_f(b, c, p):
    # 对矩阵c进行处理得到f
    f = process_matrix(c, p)

    # 计算b和f的乘积，并返回f中所有元素的和的最大值
    r1 = np.dot(b, f)  # b*f的结果记为r1，此处使用np.dot表示矩阵乘法
    return np.sum(f)  # 返回f中所有元素的和的最大值




if __name__ == '__main__':
    # 升降标记
    flag = [1, -1, -1, 0, 1]

    # 原始数量
    b = np.mat([10, 20, 8, 7, 35])
    # 原始单价
    c = np.mat([10, 20, 35, 75, 52]).T

    p = 10


    print(max_sum_of_f(b, c, p))