from config import *
import streamlit as st
import os

from download_data import get_stock_data
from preprocess_data import preprocess_stock_data
from monte_carlo_portfolio_optimisation import monte_carlo_simulation

# Utility function to list uploaded files
def list_uploaded_files(data_folder='data'):
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    return [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Streamlit App Title
st.title("Monte Carlo Simulation for Portfolio Optimization")

# Using Tabs for Better Organization
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Data", "Simulation", "Results"])

# Home Tab
with tab1:
    st.header("Welcome to the Monte Carlo Portfolio Optimizer")
    st.info(
        """
        This app allows you to perform portfolio optimization using Monte Carlo simulations.
        
        **Steps:**  
        1. Go to the **Data** tab to upload or download data.  
        2. Preprocess your data after downloading or uploading.  
        3. Configure simulation parameters in the **Simulation** tab.  
        4. View the results in the **Results** tab.  
        """
    )

# Data Tab
with tab2:
    st.header("Data Management")
    
    st.info(
        """
        
        
        **Steps:**

        1a. Download Example data.

        1b. Download Custom data.  
        
        2. Preprocess your downloaded data.  
        
        Note: 
        - Uploaded data has to be in yfinance multi-index format.  
        - Reload the page after downloading or preprocessing if file does not appear. 
        """
    )
    
    
    

    # Data Upload Section
    st.subheader("Upload Your Data")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    # Save uploaded file
    if uploaded_file:
        file_path = f"data/{uploaded_file.name}"
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # Display uploaded files
    st.subheader("Available Files:")
    uploaded_files = list_uploaded_files()
    if uploaded_files:
        st.write("Uploaded files:")
        for file in uploaded_files:
            st.write(f"- {file}")
    else:
        st.write("No uploaded files found.")

    # Download Example Data
    if st.button("Download Example Data"):
        get_stock_data(['AAPL', 'MSFT', 'TSLA'], '2020-01-01', '2023-01-01')
        st.success("Example data downloaded!")

    # Custom Data Download
    with st.expander("Download Custom Data"):
        custom_symbols = st.text_input("Enter stock symbols (comma-separated)", "AAPL, MSFT, TSLA")
        start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01")).strftime("%Y-%m-%d")
        end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01")).strftime("%Y-%m-%d")

        if st.button("Download Custom Data"):
            try:
                symbols = [symbol.strip() for symbol in custom_symbols.split(",")]
                get_stock_data(symbols, str(start_date), str(end_date), save_path=f"data/custom_data.csv")
                st.success(f"Downloaded data for: {', '.join(symbols)}")
            except Exception as e:
                st.error(f"Error downloading data: {e}")

    # Preprocess Data Section
    st.subheader("Preprocess Data")
    selected_file = st.selectbox("Select file to preprocess", uploaded_files)
    if st.button("Preprocess Selected Data"):
        try:
            input_path = f"data/{selected_file}"
            output_path = f"data/cleaned_{selected_file}"
            preprocess_stock_data(input_path=input_path, output_path=output_path)
            st.success(f"Data preprocessed and saved as cleaned_{selected_file}!")
        except Exception as e:
            st.error(f"Error during preprocessing: {e}")

# Simulation Tab
with tab3:
    st.header("Simulation Settings")
    risk_free_rate = st.number_input("Enter Risk-Free Rate", min_value=0.0, max_value=0.1, value=0.01, step=0.001)
    num_of_portfolios = st.number_input("Number of Portfolios", min_value=1000, max_value=50000, value=10000, step=1000)

    # Select preprocessed file for simulation
    preprocessed_files = [f for f in list_uploaded_files() if f.startswith('cleaned_')]
    selected_cleaned_file = st.selectbox("Select preprocessed file for simulation", preprocessed_files)

    # Run Simulation
    if st.button("Run Monte Carlo Simulation"):
        try:
            processed_df = pd.read_csv(f"data/{selected_cleaned_file}", index_col=0, parse_dates=True)
            simulations_df = monte_carlo_simulation(processed_df, num_of_portfolios=num_of_portfolios, risk_free_rate=risk_free_rate)

            # Store the simulation results for later use
            simulations_df.to_csv("data/simulation_results.csv", index=False)
            st.success("Monte Carlo simulation completed!")
        except Exception as e:
            st.error(f"Error running simulation: {e}")

# Results Tab
with tab4:
    st.header("Simulation Results")

    # Load and Display Results
    if os.path.exists("data/simulation_results.csv"):
        simulations_df = pd.read_csv("data/simulation_results.csv")
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
    else:
        st.warning("No simulation results found. Please run the simulation first.")
