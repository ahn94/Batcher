import pandas as pd
from pandas import Series
from tabulate import tabulate
import numpy as np
import os

# Read in the excel file
xls = pd.ExcelFile('../BatchSpreadsheet.xlsx')
dfBeanTypeInfo = pd.read_excel(xls, sheet_name="BeanTypeInfo")
dfGreenBeans = pd.read_excel(xls, sheet_name="GreenBeans", converters={'value': float})


# print('------ Green Beans --------')
# print(dfGreenBeans)
# print('------- dfBeantype --------')
# print(dfBeanTypeInfo)

columns = ['Blend', 'Cost']
dfTotals = pd.DataFrame(columns=columns)

# for bi, green in dfGreenBeans.iterrows():
#     for ti, beantype in dfBeanTypeInfo.iterrows():
#         if green['Green Bean'] == beantype['Green Bean']:
#             print(beantype)
#             dfTotals.loc[len(dfTotals)] = [
#                 beantype['Green Bean'],
#                 beantype['value']
#             ]
# print(dfBeanTypeInfo)


for ti, beantype in dfBeanTypeInfo.iterrows():
    beantype['test'] = 3

print(dfBeanTypeInfo)
