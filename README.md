# Kickstarter ML Project

By: Aaron Teichmann, Maximilian Hallenberger, Patrick Buyer

This repository represents a three-day effort by the authors to create and interpret a machine-learning based model
on the publicly available user data of the crowdfunding service 'kickstarter'. The model predicts if a kickstarter 
project is likely to succeed (getting funded) based on several key-parameters determined at the start of the project.
It explicitly omits parameters which are only available after the start or even the finish of the project, such as total number of backers
or pledged total amount. Besides the prediction (predict.py), this repository includes the training of the dataset (train.py) and a 
feature engineering/data cleaning (feature_engineering.py) file. Used in sequential order (feature_engineering.py --> train.py --> predict.py),
these files enable a prediction of kickstater data without any additional work by the user (see Limitations for exceptions).

The data used for this can be found at: (https://webrobots.io/kickstarter-datasets/).

---
## Requirements and Environment

Requirements:
- pyenv with Python: 3.9.8

Environment: 

For installing the virtual environment you can either use the Makefile and run `make setup` or install it manually with the following commands: 

```Bash
pyenv local 3.9.8
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

In order to train the model and store test data in the data folder and the model in models run:

```bash
#activate env
source .venv/bin/activate

python example_files/train.py  
```

In order to test that predict works on a test set you created run:

```bash
python example_files/predict.py models/linear_regression_model.sav data/X_test.csv data/y_test.csv
```

## Limitations

The .py files are only applicable on csv-files following the kickstarter datastructure, since certain column names are called in feature_engineering.py
