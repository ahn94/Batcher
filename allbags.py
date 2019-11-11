#!/usr/bin/env python

import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
from Utils import beans_to_roast, beans_remove_inventory, df_labels, rename_labels, get_final_blend_grams
from PivotUtils import create_lb_pivot, create_gm_pivot, create_batch_df, create_green_inventory, create_green_pivot, create_bag_pivot, create_blend_df
import argparse
import time
import os
from tabulate import tabulate


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get shipping list.')
    parser.add_argument('batch', type=int, help='only coffee from specific batch number')
    # parser.add_argument('order-type', type=str, help='enter single order type. Must match text in batchspreadsheet order table.')
    args = parser.parse_args()

    # # Prepares jinga2 templates
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('allbags.html')

    # # Read in the excel file
    xls = pd.ExcelFile('../BatchSpreadsheet.xlsx')
    dfBeans = pd.read_excel(xls, sheet_name="Beans", converters={'IS': str, 'Batch#': int, 'Roast': str, 'Batch ID': int})
    dfOrders = pd.read_excel(xls, sheet_name="Orders", converters={'Order ID': int, 'Date': pd.to_datetime})

    # """
    # Batch
    # """
    dfBeans = dfBeans[dfBeans['Order ID'].notnull()]
    dfBeans = dfBeans[dfBeans['Batch#'] == args.batch]

    # print(dfOrders)

    dfBeans = pd.merge(dfOrders[['Order Type', 'Order ID']], dfBeans, how='outer', on='Order ID')

    print(dfBeans)

    beanpivot = pd.pivot_table(
        dfBeans,
        index=['Order Type', 'Name', 'Coffee Type'],
        columns='Bag Size (oz)',
        values='Qty',
        aggfunc=np.sum,
        fill_value=''
    )

    # print(beanpivot)

    # add method that returns col name if not in header dict
    print(beanpivot.columns)

    headers = {4: '4oz', 12: '12oz', 16: '1lb', 32: '2lb', 80: '5lb'}

    beanpivot.columns = [headers.get(col) for col in beanpivot.columns]

   

    # """
    # Styling
    # """
    # # Add bootstrap style to tables
    pivot = beanpivot.style.set_table_attributes('class="table table-striped table-bordered"').render()
   
    # """
    # Template
    # """
    # # Template variables
    template_vars = {
        "all_bags": pivot
    }

    # # Render template
    html_out = template.render(template_vars)

    # """
    # Create Batches Directory
    # """
    batch_dir = os.path.join(os.pardir,"Batches")

    if not os.path.exists(batch_dir):
        os.makedirs(batch_dir)

    os.chdir(batch_dir)

    # """
    # Create filename with time stamp
    # """
    NAME = ("batch-" + str(args.batch) + "-bags" + ".html")

    # Create HTML version of the report
    with open(NAME, 'w') as f:
        f.write(html_out)
        f.close()
        print('\n------------------ All bags ----------')
        print("All bags for "+ str(args.batch) +" saved as: " + NAME)
        pass