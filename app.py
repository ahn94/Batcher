#!/usr/bin/env python

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from Utils import beans_to_roast, beans_remove_inventory
from PivotUtils import create_lb_pivot, create_gm_pivot, create_batch_df, create_green_inventory, create_green_pivot
import argparse
import time
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate PDF report')
    parser.add_argument('batch', type=int, help='batch #')
    args = parser.parse_args()

    # Prepares jinga2 templates
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('report.html')

    # Read in the excel file
    xls = pd.ExcelFile('PandasTestFileV2.xlsx')
    dfBeans = pd.read_excel(xls, sheet_name="Beans", converters={'IS': str, 'Batch#': int})
    dfBeanTypeInfo = pd.read_excel(xls, sheet_name="BeanTypeInfo")

    """
    Batch
    """
    dfBeans = dfBeans[dfBeans['Batch#'] == args.batch]

    """
    Inventory
    """
    dfGreen = beans_remove_inventory(dfBeans)
    dfGreenBatch = create_green_inventory(dfGreen, dfBeanTypeInfo)

    """
    Roast
    """
    # Clean up Beans table and add column for green weight(lb & oz)
    dfBeans = beans_to_roast(dfBeans)
    # creates data for pivot tables
    dfBatch = create_batch_df(dfBeans, dfBeanTypeInfo)

    """
    Pivots
    """
    # Create pivots
    gm_pivot = create_gm_pivot(dfBatch)
    lb_pivot = create_lb_pivot(dfBatch)
    green_pivot = create_green_pivot(dfGreenBatch)

    """
    Styling
    """
    # Add bootstrap style to tables
    html_lb_pivot = lb_pivot.style.set_table_attributes('class="table table-striped table-bordered"').render()
    html_gm_pivot = gm_pivot.style.set_table_attributes('class="table table-striped table-bordered"').render()

    html_green_pivot = "<h3>No Inventory used</h3>"
    if len(green_pivot) > 0:
        html_green_pivot = green_pivot.style.set_table_attributes('class="table table-striped table-bordered"').render()

    """
    Template
    """
    # Template variables
    template_vars = {
        "title": "Batch Report - " + time.strftime("%b-%d-%y"),
        "batch_pivot_lb": html_lb_pivot,
        "batch_pivot_gm": html_gm_pivot,
        "green_pivot": html_green_pivot
    }

    # Render template
    html_out = template.render(template_vars)

    """
    Reports
    """
    # Create PDF version of the report
    # HTML(string=html_out).write_pdf(target=time.strftime("%b-%d-%y") + "_batch.html", stylesheets=[CSS('bootstrap.css')])

    print(os.path.join(os.pardir, time.strftime("%b-%d-%y %I:%M%p") + "_batch.html"))

    batch_dir = os.pardir + "/Batches"

    if not os.path.exists(batch_dir):
        os.makedirs(batch_dir)

    # Create HTML version of the report
    with open(os.path.join(batch_dir, time.strftime("%b-%d-%y %I:%M%p") + "_batch.html"), 'w') as f:
        f.write(html_out)
        f.close()
        pass
