from config import *


# Our different Stock symbols
symbols = ['AAPL', 'MSFT', 'TSLA', 'AMZN', 'AMD', 'DASH']

number_of_symbols = len(symbols)

# If we don't have the data, download it from Yahoo Finance   --- Later change this to a function so we can download and change symbols for GUI 
if not pathlib.Path('stock_data.csv').exists():

    # Download the data
    data = yf.download(symbols, start='2020-03-20', end='2022-01-01', group_by='ticker')
    data.to_csv(
        'stock_data.csv',
        index=True)


    price_data_frame: pd.DataFrame = data

else:
    # Load the existing CSV file
    price_data_frame: pd.DataFrame = pd.read_csv('stock_data.csv')

print(price_data_frame.head())


"""
Below are functions for Streamlit app.

"""


# Create a function to do the above
def get_stock_data(symbols: list, start_date: str, end_date: str, save_path='data/stock_data.csv') -> pd.DataFrame:
    """
    Download stock data from Yahoo Finance and save it to a CSV file.

    - We will do this under the data/stock_data.csv folder when working with the GUI.
    """

    data = yf.download(symbols, start=start_date, end=end_date, group_by='ticker')
    data.to_csv(save_path, index=True)

    return data


