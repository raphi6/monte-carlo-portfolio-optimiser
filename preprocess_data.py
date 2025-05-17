from config import *
# Set display options to resemble Jupyter Notebook
pd.set_option('display.width', None)             # No limit on the width of the display
pd.set_option('display.max_columns', None)       # Show all columns
pd.set_option('display.max_rows', 20)            # Limit rows to prevent overflow
pd.set_option('display.float_format', '{:.2f}'.format)  # Format float numbers

# Pre-processing Below

# Load the data    -  note header=[0, 1] and index_col=0 is used to read multi-index columns preserving the nice format
price_df: pd.DataFrame = pd.read_csv('stock_data.csv', header=[0, 1], index_col=0)


# Select only the 'Date' and 'Close' columns
price_df = price_df.loc[:, (slice(None), 'Close')]

# Flatten the multi-index columns, we don't need the Price row
price_df.columns = price_df.columns.get_level_values(0)
#print(price_df.head())


# Saving the data to a CSV file
price_df.to_csv('stock_data_cleaned.csv', index=True)




"""
Below are functions for Streamlit app.

"""

def preprocess_stock_data(input_path='data/stock_data.csv', output_path='data/stock_data_cleaned.csv'):
    price_df = pd.read_csv(input_path, header=[0, 1], index_col=0)
    price_df = price_df.loc[:, (slice(None), 'Close')]
    price_df.columns = price_df.columns.get_level_values(0)
    price_df.to_csv(output_path, index=True)
    return price_df