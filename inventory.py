import pandas as pd
from Utils import beans_remove_inventory
from PivotUtils import create_green_inventory, create_green_pivot
from tabulate import tabulate
import numpy as np
from jinja2 import Environment, FileSystemLoader
import os



# Read in the excel file
xls = pd.ExcelFile('../BatchSpreadsheet.xlsx')
dfBeans = pd.read_excel(xls, sheet_name="Beans", converters={'IS': str, 'Batch#': int, 'Roast': str})
dfBeanTypeInfo = pd.read_excel(xls, sheet_name="BeanTypeInfo")
dfInventory = pd.read_excel(xls, sheet_name="Inventory", converters={'Green Bean': str, 'lb': float})
dfInventory = dfInventory[['Green Bean', 'lb']]


# Prepares jinga2 templates
env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('inv-report.html')

"""
Inventory
"""
# removes blank and instock bean rows
# adds converts from oz to total green lbs for each row
dfGreen = beans_remove_inventory(dfBeans)
dfGreenBatch = create_green_inventory(dfGreen, dfBeanTypeInfo)

# rename Coffee Type to Green Bean for clarity
dfGreenBatch.rename({'Coffee Type': 'Green Bean'}, axis='columns', inplace=True)

# required so when summed with inventory table it will subtract the used beans
dfGreenBatch['lb'] = dfGreenBatch['lb'].apply(lambda w: -w)

# combine the inventory and green bean(with negative numbers for removal and positive for adding)
dfTotals = pd.concat([dfGreenBatch, dfInventory])

# sum each one by group "Green Bean"
dfTotals = dfTotals.groupby('Green Bean').sum()

# sort largest inventory to smallest
dfTotals = dfTotals.sort_values(by=['lb'], ascending=False)


if len(dfTotals) == 0:
    print('No beans in BatchSpreadsheet')
    exit()

"""
Format Output
"""
headers = ['Green Bean', 'lb']
print(tabulate(dfTotals, headers, tablefmt='fancy_grid'))

html_inventory = dfTotals.style.set_table_attributes('class="table table-striped table-bordered"').render()


template_vars = {
    "inventory_table": html_inventory
}

html_out = template.render(template_vars)


"""
Create Batches Directory
"""
batch_dir = os.path.join(os.pardir,"Batches")

if not os.path.exists(batch_dir):
    os.makedirs(batch_dir)

os.chdir(batch_dir)

"""
Create filename with time stamp
"""
# Create HTML version of the report
with open("inventory.html", 'w') as f:
    f.write(html_out)
    f.close()
    pass
