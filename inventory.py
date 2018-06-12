import pandas as pd
from Utils import beans_remove_inventory
from PivotUtils import create_green_inventory, create_green_pivot
from tabulate import tabulate
import numpy as np

# Read in the excel file
xls = pd.ExcelFile('../BatchSpreadsheet.xlsx')
dfBeans = pd.read_excel(xls, sheet_name="Beans", converters={'IS': str, 'Batch#': int, 'Roast': str})
dfBeanTypeInfo = pd.read_excel(xls, sheet_name="BeanTypeInfo")
dfInventory = pd.read_excel(xls, sheet_name="Inventory", converters={'Green Bean': str, 'lb': float})
dfInventory = dfInventory[['Green Bean', 'lb']]

"""
Inventory
"""
dfGreen = beans_remove_inventory(dfBeans)
dfGreenBatch = create_green_inventory(dfGreen, dfBeanTypeInfo)

dfGreenBatch.rename({'Coffee Type': 'Green Bean'}, axis='columns', inplace=True)


dfGreenBatch['lb'] = dfGreenBatch['lb'].apply(lambda w: -w)

dfTotals = pd.concat([dfGreenBatch, dfInventory])

dfTotals = dfTotals.groupby('Green Bean').sum()

dfTotals = dfTotals.sort_values(by=['lb'], ascending=False)


if len(dfTotals) == 0:
    print('No beans in BatchSpreadsheet')
    exit()

"""
Format Output
"""
headers = ['Green Bean', 'lb']
print(tabulate(dfTotals, headers, tablefmt='fancy_grid'))
