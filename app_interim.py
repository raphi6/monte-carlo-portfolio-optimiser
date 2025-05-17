from config import *
import streamlit as st
import os

from download_data import get_stock_data
from preprocess_data import preprocess_stock_data
from monte_carlo_portfolio_optimisation import monte_carlo_simulation


st.title("Monte Carlo Simulation for Portfolio Optimization")

# Sidebar: Step-by-Step Instructions
st.sidebar.title("Instructions")
st.sidebar.info(
    """
    Enter your risk-free rate and number of simulations in the sidebar.
    
    You can upload your own data, download example data, or enter your symbols in 1b.

    Click in the following order:

    **Step 1:** "Download Example Data". 
    **Step 1b:** "Download Custom Data".  
    **Step 2:** "Preprocess Data".  
    **Step 3:** "Run Monte Carlo Simulation".  
    """
)

risk_free_rate = st.sidebar.number_input("Enter Risk-Free Rate", min_value=-0.5, max_value=0.4, value=0.01, step=0.01)
num_of_portfolios = st.sidebar.number_input("Number of Simulations", min_value=1000, max_value=100000, value=10000, step=1000)

# Data Upload Section
st.sidebar.header("Upload Your Data (Optional)")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Fetching or loading data
if uploaded_file:
    with open('data/stock_data.csv', 'wb') as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")

# Download Example Data
if st.sidebar.button("1. Download Example Data"):
    get_stock_data(['AAPL', 'MSFT', 'TSLA'], '2020-01-01', '2023-01-01')
    st.success("Example data downloaded!")

# DOwnload Custom Data
with st.sidebar.expander("1b. Download Custom Data"):
    custom_symbols = st.text_input("Enter stock symbols (comma-separated)", "AAPL,MSFT,TSLA,AMZN,AMD,DASH")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01")).strftime("%Y-%m-%d")
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01")).strftime("%Y-%m-%d")


    if st.button("Download Custom Data"):

        try:
            symbols = [symbol.strip() for symbol in custom_symbols.split(",")]
            get_stock_data(symbols, str(start_date), str(end_date))
            st.success(f"Downloaded data for: {', '.join(symbols)}")
        except Exception as e:
            st.error(f"Error downloading data: {e}")

# Preprocess Data
if st.sidebar.button("2. Preprocess Data"):
    try:
        preprocess_stock_data()
        st.success("Data preprocessed!")
    except Exception as e:
        st.error(f"Error during preprocessing: {e}")

# Monte Carlo Simulation

if st.sidebar.button("3. Run Monte Carlo Simulation"):
    try:




        processed_df = pd.read_csv('data/stock_data_cleaned.csv', index_col=0, parse_dates=True)
        simulations_df = monte_carlo_simulation(processed_df)

        # Display Results
        st.write("First 5 Monte Carlo Simulation Results")
        st.dataframe(simulations_df.head())

        # Plotting the Efficient Frontier
        st.write("Efficient Frontier")
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(simulations_df['Volatility'], simulations_df['Returns'], c=simulations_df['Sharpe Ratio'], cmap='viridis')
        plt.colorbar(scatter, label='Sharpe Ratio')
        plt.xlabel('Volatility')
        plt.ylabel('Returns')
        plt.title('Monte Carlo Simulation: Efficient Frontier')
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Error running simulation: {e}")