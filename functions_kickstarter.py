# Change dates to weekend(1) or weekday(0)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def change_time(dataframe, column_list):
    for column in column_list:
        dataframe[column] = [1 if x >= 6 else 0 for x in pd.to_datetime(dataframe[column], unit='s').dt.weekday]
    return dataframe


# Generic Barplots for categorical data
def bar_plot(df, column):
    """Generates barplots of categorical data

    Args:
        df (pd dataframe): Dataframe
        column (object): list of names of columns which should be plotted
    """
    # get feature
    for i in column:
        varValue = df[i].value_counts()

        plt.figure(figsize = (12,3))
        plt.bar(varValue.index, varValue, color = '#87c442', edgecolor = 'black')
        plt.xticks(varValue.index, varValue.index.values)
        plt.ylabel("Frequency")
        plt.title(i.capitalize())
        plt.xticks(rotation = 90)
        plt.show()

def scale_columns(df, column):
    """Function that scales the data with a min_max scaler

    Args:
        df (dataframe): Dataframe
        column (object): Name or list of names including the columns which should be normalized

    Returns:
        Dataframe object: Returns the dataframe including the normalized columns
    """
    scaler = MinMaxScaler()
    for i in column:
        scaler.fit(df[[i]])
        df[i] = scaler.transform(df[[i]])
    
    return df