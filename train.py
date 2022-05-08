from time import sleep
import pandas as pd
import numpy as np
from pyrsistent import freeze
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, f1_score, confusion_matrix
import pickle
import glob
import pandas as pd
from functions_kickstarter import *

import warnings
warnings.filterwarnings('ignore')


#file_directory = str(sys.argv[1]) + '/*.csv'
file_directory = str(input('please enter the folder name of your kickstarter data: ')) + '/*.csv'
RSEED = int(input('Enter the random seed integer: '))

print('Training might take a while, please be patient...')

df = pd.concat(map(pd.read_csv, glob.glob(file_directory)))
# Reset the indices
df.reset_index(drop=True, inplace=True)

df = feature_engineering(df)

print('The df shape is:', df.shape)
sleep(5)

# Set x and y
X = df.drop('state', axis = 1)
y = df['state']


# splittin into train and test
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size= 0.3, random_state=RSEED)

# Amount of volding for cross-validation
kfold = StratifiedKFold(n_splits=5)

### XGB classifier
XGB = XGBClassifier()

max_depth = [1,2,4,8,10]
min_child_weight = np.linspace(1, 10, 5, endpoint=True) 

gamma = np.linspace(0.5, 5, 5,endpoint=True)
subsample = np.linspace(0.5, 1, 5, endpoint=True)
colsample_bytree = np.linspace(0.5, 1, 5, endpoint=True)

print('XGB training......')

XGB_param_grid = {
        'min_child_weight': min_child_weight,
        'gamma': gamma,
        'subsample': subsample,
        'colsample_bytree': colsample_bytree,
        'max_depth': max_depth
        }


gsXGB = HalvingGridSearchCV(estimator = XGB, 
                    param_grid = XGB_param_grid, cv=kfold, scoring="precision", n_jobs= 4, verbose = 0)

gsXGB.fit(X_train,y_train)

XGB_best = gsXGB.best_estimator_
print(XGB_best.get_params())

# Best score
gsXGB.best_score_

print('Random Forest training......')
# RFC Parameters tunning 
RFC = RandomForestClassifier()

# Number of trees in random forest
n_estimators = [200, 400, 600, 800]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [1, 5, 20]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]

## Search grid for optimal parameters
rf_param_grid = {"max_depth": max_depth,
              "max_features": max_features,
              "min_samples_split": min_samples_split,
              "min_samples_leaf": min_samples_leaf,
              "bootstrap": bootstrap,
              "n_estimators" :n_estimators,
              "criterion": ["gini"]}
              

gsRFC = HalvingGridSearchCV(RFC,param_grid = rf_param_grid, cv=kfold, scoring="precision", n_jobs= 4, verbose = 0)

gsRFC.fit(X_train,y_train)

RFC_best = gsRFC.best_estimator_

print(('Voting classifier training......'))
# Voting Classifier (soft voting) including the three best models after grid search
votingC = VotingClassifier(estimators=[ ('XGB',XGB_best), ("RandomForest",RFC_best)], voting='soft', n_jobs=4)
# Fit train data to Voting Classifier
votingC = votingC.fit(X_train, y_train)

# Save csv file with X_test, y_test
print("Saving test data from train-test split in the models folder")

#saving the model
print("Saving model in the models folder")

filename = 'models/ensemble_model.sav'
pickle.dump(votingC, open(filename, 'wb'))