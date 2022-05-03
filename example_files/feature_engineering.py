import pandas as pd
import numpy as np
import time
import json
import warnings
warnings.filterwarnings('ignore')



# Check for duplicate projects and store them in a table
dups = df.groupby(df.id.tolist()).size().reset_index().rename(columns={0:'count'})

# Sum the final col of that table, and subtract the number of culprits:
dups['count'].sum() - dups.shape[0]

# Drop features which will not be needed for further analysis
dropped_features = ['blurb', 'currency_symbol', 'backers_count', 'is_backing', 'permissions', 'is_starred', 'source_url',
                    'slug', 'name', 'profile', 'friends', 'spotlight', 'is_starrable', 'photo', 'pledged', 'usd_type',
                    'fx_rate', 'location', 'creator', 'currency_trailing_code','current_currency', 'created_at', 'disable_communication']
df = df.drop(dropped_features, axis=1)

# Sort dataframe by 'date_changed_at' so that we will keep the entry that was most recently updated
df.sort_values('state_changed_at')

# Remove duplicates
duplicates = df.duplicated(subset='id', keep='last')
df = df[~duplicates]

# We have some values in goal which are unrealistically high
df = df.query('goal < 1000000')

# Extract category from category column
df['category'] = df['category'].apply(lambda x: json.loads(x)['slug'])
df['category'] = df['category'].apply(lambda x: x.split('/',)[0])

# Generate new column with readable timeformat
df['launched_at_new'] = pd.to_datetime(df['launched_at'], unit='s')

#df['deadline_new'] = pd.to_datetime(df['deadline'], unit='s')
df['state_changed_at_new'] = pd.to_datetime(df['state_changed_at'], unit='s')

# Add new column 'time' that displays the time from project launch to project end
df.eval('time = state_changed_at_new - launched_at_new', inplace=True)

# Convert to days
df['time'] = df['time'].apply(lambda x: pd.Timedelta(x).days)

times_lst = ['launched_at', 'deadline', 'state_changed_at']

# Displays the goal converted to one currency (usd)
df.eval('goal = goal * static_usd_rate', inplace=True)

# Create a column that displays the month of launch
df['launched_at'] = df['launched_at'].apply(lambda x: pd.to_datetime(x, unit='s')).dt.month

# Set aside columns for later use on predicted live projects
list = ['urls','state','staff_pick']
urls_list = df[list]

# Extract urls from web dict
urls_list['urls'] = urls_list['urls'].apply(lambda x: json.loads(x)['web'])

# Only take those values where state is equal to live state
array_live = ['live']
urls_list = urls_list.loc[urls_list['state'].isin(array_live)]

# Drop state again
urls_list.drop('state', axis=1, inplace=True)

# Drop id (not needed anymore), converted pledged amount/usd_pledged (self fulfilling prophicy), country (redundant with currency), drop staff_pick bc we dont know the staff pick
# When we make predictions
drop_list = ['id','converted_pledged_amount', 'usd_pledged', 'country','launched_at_new','state_changed_at_new', 'urls', 'static_usd_rate', 'staff_pick']
df.drop(drop_list, axis = 1, inplace = True)

# One hot encode all categorical data (country, currency, categories, duration) boolean values might 
# Replace True False with strings, otherwise one-hot encoding doesnt work
one_hot_featurelist = ['currency', 'category']
one_hot = pd.get_dummies(df[one_hot_featurelist])
df.drop(one_hot_featurelist, axis = 1, inplace=True)
df = df.join(one_hot)

# Standardize numerical data according to a min-max scaler
numerical = ['goal']
df = scale_columns(df, numerical)

# Extract live values
array_live = ['live']
live_projects = df.loc[df['state'].isin(array_live)]

# Filter and concat. for target variable
array_notlive = ['successful', 'failed', 'canceled']
df = df.loc[df['state'].isin(array_notlive)]

# Add canceled to failed projects
df.replace('canceled','failed', inplace=True)

# Replace successful and failed entries with 0 and 1
df.replace(['successful','failed'],[1,0], inplace=True)