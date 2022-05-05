# Change dates to weekend(1) or weekday(0)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import json

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

def feature_engineering(df):
    # Check for duplicate projects and store them in a table // Remove duplicates
    dups = df.groupby(df.id.tolist()).size().reset_index().rename(columns={0:'count'})
    # Sum the final col of that table, and subtract the number of culprits:
    dups['count'].sum() - dups.shape[0]

    # Sort dataframe by 'date_changed_at' so that we will keep the entry that was most recently updated
    df.sort_values('state_changed_at')
    # Remove duplicates
    duplicates = df.duplicated(subset='id', keep='last')
    df = df[~duplicates]

    # Drop features which will not be needed for further analysis, most of those features are either meaningless (ex. urls), have next to no entries (ex. friends), or are bad for predictions
    # See Target.md for a full list of explanation
    dropped_features = ['blurb', 'currency_symbol', 'backers_count', 'is_backing', 'permissions', 'is_starred', 'source_url',
                        'slug', 'name', 'profile', 'friends', 'spotlight', 'is_starrable', 'photo', 'pledged', 'usd_type',
                        'fx_rate', 'location', 'creator', 'currency_trailing_code','current_currency', 'created_at', 'disable_communication']
    df = df.drop(dropped_features, axis=1)

    # We limit our dataset to goals below 1 Million, values above are treated as outliers
    df = df.query('goal < 1000000')

    # Extract category from category column
    df['category'] = df['category'].apply(lambda x: json.loads(x)['slug'])
    df['category'] = df['category'].apply(lambda x: x.split('/',)[0])

    # Generate new column with readable timeformat
    df['launched_at'] = pd.to_datetime(df['launched_at'], unit='s')

    df['state_changed_at'] = pd.to_datetime(df['state_changed_at'], unit='s')
    # Add the deadline date as date column
    df['deadline'] = pd.to_datetime(df['deadline'], unit='s')

    # Add new column 'time' that displays the time from project launch to project end
    df.eval('duration = deadline - launched_at', inplace=True)

    # Convert to days
    df['duration'] = df['duration'].apply(lambda x: pd.Timedelta(x).days)

    # Displays the goal converted to one currency (usd)
    df.eval('goal = goal * static_usd_rate', inplace=True)

    # Create a column that displays the month of launch
    df['launched_at'] = df['launched_at'].apply(lambda x: pd.to_datetime(x, unit='s')).dt.month

    # Drop id (not needed anymore), converted pledged amount/usd_pledged (predictor not av. at the beginning of a project),
    # country (redundant with currency), drop staff_pick bc we dont know the staff pick when we make predictions
    drop_list = ['id','converted_pledged_amount', 'usd_pledged', 'country', 'urls', 'static_usd_rate', 'staff_pick', 'state_changed_at', 'deadline']
    df.drop(drop_list, axis = 1, inplace = True)

    # One hot encode all categorical data (currency, categories)
    one_hot_featurelist = ['currency', 'category', 'launched_at']
    one_hot = pd.get_dummies(df[one_hot_featurelist])
    df.drop(one_hot_featurelist, axis = 1, inplace=True)
    df = df.join(one_hot)

    # Standardize numerical data according to a min-max scaler
    numerical = ['goal']
    df = scale_columns(df, numerical)
    
    # Filter target variable
    array_notlive = ['successful', 'failed', 'canceled']

    df = df.loc[df['state'].isin(array_notlive)]
    # Add canceled to failed projects
    df.replace('canceled','failed', inplace=True)
    # Replace successful and failed entries with 0 and 1
    df.replace(['successful','failed'],[1,0], inplace=True)

    return df