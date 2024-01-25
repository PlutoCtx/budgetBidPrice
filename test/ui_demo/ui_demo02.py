# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 17:19
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: ui_demo02.py
# @Software: PyCharm
# @User: chent

import openpyxl

wb = openpyxl.load_workbook("D:\可售项目\接单项目\\2024-01-19 400 预算投标价格\【01】提供材料\数据案例.xls")

app = openpyxl.App(visible=True)

wb = app.books.open("D:\可售项目\接单项目\\2024-01-19 400 预算投标价格\【01】提供材料\数据案例.xls")

wb._app.visible = True
