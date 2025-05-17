import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import scipy.optimize as sci_plt

from pprint import pprint
from sklearn.preprocessing import StandardScaler
from tabulate import tabulate

import yfinance as yf

# Set display options to resemble Jupyter Notebook
pd.set_option('display.width', None)             # No limit on the width of the display
pd.set_option('display.max_columns', None)       # Show all columns
pd.set_option('display.max_rows', 20)            # Limit rows to prevent overflow
pd.set_option('display.float_format', '{:.2f}'.format)  # Format float numbers
