import pandas as pd
import numpy as np
import time
import json
import warnings
warnings.filterwarnings('ignore')
import glob

    # Import the .csv files and concat them into one dataframe
    original_dataframe = pd.concat(map(pd.read_csv, glob.glob('data/data-2/*.csv')))

    # Reset the indices
    original_dataframe.reset_index(drop=True, inplace=True)

    # Set a working dataframe, so that we don't have to wait 10s it to import again if we want to start fresh
    df = original_dataframe
