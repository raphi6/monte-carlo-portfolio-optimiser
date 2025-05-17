# Monte Carlo Portfolio Optimization using Streamlit

This project is a Streamlit application for portfolio optimization using Monte Carlo simulations. The app allows users to upload stock data, download data from Yahoo Finance, preprocess the data, and run Monte Carlo simulations to optimize a financial portfolio based on expected returns, volatility, and the Sharpe ratio.

**If you want to use the app directly, visit the deployed link:**
[Monte Carlo Portfolio Optimizer App](https://raphi6-monte-carlo-portfolio-optimiser-app-dxctih.streamlit.app/)

## Purpose
This app was created to help get familiar with using Streamlit and to try out portfolio optimization using Monte Carlo simulations. Future extensions can include:
- Implementing the Kelly Criterion, or Half Kelly (see inspiration from Robert Carver's amazing lectures https://gist.github.com/robcarver17/8227c5c88ad17acd6a84b9762ea79d67).
- Enhancing interactivity to visualize the best portfolios and their weights.
- Incorporating other portfolio metrics and optimisation techniques.

## Features
- **Data Upload and Download:**
  - Upload your own CSV files in the multi-index format provided by Yahoo Finance.
  - Download example data for popular stocks (AAPL, MSFT, TSLA).
  - Download custom data using the Yahoo Finance API by specifying stock symbols and date ranges.

- **Data Preprocessing:**
  - Select a file to preprocess.
  - Extracts closing prices from multi-index data and stores them in a cleaned format.

- **Monte Carlo Simulation:**
  - Configure risk-free rate and the number of portfolios to simulate.
  - Select a preprocessed file to perform the simulation.
  - Displays results including returns, volatility, and Sharpe ratio.
  - Visualizes the efficient frontier.

- **Results:**
  - View the first 5 Monte Carlo simulation results.
  - Plot of the efficient frontier, highlighting the optimal portfolio.

## Installation
Clone the repository:
```
git clone https://github.com/username/monte-carlo-portfolio-optimiser.git
cd monte-carlo-portfolio-optimiser
```

Install the required packages:
```
pip install -r requirements.txt
```

## Running the App Locally
Run the Streamlit app:
```
streamlit run app.py
```
Open the app in your browser at:
```
http://localhost:8501
```

## Deployment on Streamlit Cloud
1. Push your code to GitHub.
2. Log in to [Streamlit Cloud](https://share.streamlit.io/).
3. Deploy the app by connecting to your GitHub repository.
4. Your app will be hosted on a public URL.

## Project Structure
```
.
├── app.py                        # Main Streamlit app script
├── config.py                     # Configuration and utility functions
├── download_data.py              # Data download functionality
├── preprocess_data.py            # Data preprocessing steps
├── monte_carlo_portfolio_optimisation.py # Monte Carlo simulation
├── metrics.py                    # Portfolio metrics calculation
├── requirements.txt              # Dependencies
└── data/                         # Folder to store uploaded and processed files
```

## Usage
1. Upload your data or download from Yahoo Finance.
2. Preprocess the data to obtain cleaned CSV files.
3. Configure simulation settings and run the Monte Carlo simulation.
4. View results including portfolio metrics and the efficient frontier plot.

## Technologies Used
- **Python:** Core programming language
- **Streamlit:** Interactive web application framework
- **Pandas:** Data manipulation and analysis
- **NumPy:** Numerical computations
- **Matplotlib:** Data visualization
- **Yahoo Finance API:** Financial data retrieval


