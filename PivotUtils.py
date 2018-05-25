import pandas as pd
import numpy as np
from pandas import Series


# Create lb pivot table
def create_lb_pivot(df):
    return pd.pivot_table(
        df,
        index='Coffee Type',
        values='lb',
        columns='Roast',
        aggfunc=np.sum,
        fill_value='-'
    )


def create_gm_pivot(df):
    return pd.pivot_table(
        df,
        index='Coffee Type',
        values='gm',
        columns='Roast',
        aggfunc=np.sum,
        fill_value='-'
    )


def create_green_pivot(df):
    return pd.pivot_table(
        df,
        index='Coffee Type',
        values='lb',
        aggfunc=np.sum,
        fill_value='-'
    )


def create_bag_pivot(df):
    return pd.pivot_table(
        df,
        index='Coffee Type',
        columns='Bag Size (oz)',
        values='Qty',
        aggfunc=np.sum,
        fill_value='-'
    )


def create_green_inventory(dfBeans, dfBeanTypeInfo):
    columns = ['Coffee Type', 'lb']
    dfBatch = pd.DataFrame(columns=columns)

    # loop through bean table and create batch data frame
    for bi, beanrow in dfBeans.iterrows():
        for gi, greenrow in dfBeanTypeInfo.iterrows():
            # Gets info for blends and singles from beantypeinfo
            if beanrow['Coffee Type'] == greenrow['Coffee Type']:
                # add to batch data frame
                dfBatch.loc[len(dfBatch)] = [
                    greenrow['Green Bean'],
                    greenrow['Ratio'] * beanrow['lb']
                ]
    return dfBatch


def create_batch_df(dfBeans, dfBeanTypeInfo, dfGreen):
    # Create new data frame for batches
    columns = ['Coffee Type', 'Roast', 'lb', 'gm']
    df_batch = pd.DataFrame(columns=columns)
    greens = Series(dfGreen['Default Roast'].values, index=dfGreen['Green Bean'])

    # loop through bean table and create batch data frame
    for bi, beanrow in dfBeans.iterrows():
        for gi, greenrow in dfBeanTypeInfo.iterrows():
            # Gets info for blends and singles from beantypeinfo
            if beanrow['Coffee Type'] == greenrow['Coffee Type']:
                # add to batch data frame
                df_batch.loc[len(df_batch)] = [
                    greenrow['Green Bean'],
                    get_roast(beanrow['Roast'], greens, greenrow['Green Bean']),
                    greenrow['Ratio'] * beanrow['lb'],
                    greenrow['Ratio'] * beanrow['gm']
                ]
    return df_batch


def get_roast(roast, default, green_bean):
    if not pd.isnull(roast):
        return roast

    if green_bean in default:
        return default[green_bean]

    return "Roast: NA"
