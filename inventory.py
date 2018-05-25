import pandas as pd
from Utils import beans_remove_inventory
from PivotUtils import create_green_inventory, create_green_pivot
from tabulate import tabulate

# Read in the excel file
xls = pd.ExcelFile('../BatchSpreadsheet.xlsx')
dfBeans = pd.read_excel(xls, sheet_name="Beans", converters={'IS': str, 'Batch#': int})
dfBeanTypeInfo = pd.read_excel(xls, sheet_name="BeanTypeInfo", index_col=0)

"""
Inventory
"""

dfGreen = beans_remove_inventory(dfBeans)
dfGreenBatch = create_green_inventory(dfGreen, dfBeanTypeInfo)
green_pivot = create_green_pivot(dfGreenBatch)

if len(green_pivot) == 0:
    print('No beans in BatchSpreadsheet')
    exit()

"""
Format Output
"""
headers = ['Green Bean', 'lb']
green_pivot = green_pivot.sort_values(by=['lb'], ascending=False)
print(tabulate(green_pivot, headers, tablefmt='fancy_grid'))
