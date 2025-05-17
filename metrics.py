from config import *

# Load our processed data
processed_df = pd.read_csv('stock_data_cleaned.csv', index_col=0, parse_dates=True)
#print(processed_df)


"""

 In this section, we will try -a single- Monte Carlo simulation for Portfolio Optimization

- This will happen in each loop of the simulation.

"""

"""
Below calculating Log Returns and Portfolio Weights

"""

# Calculate the Log Returns
log_return = np.log(1 + processed_df.pct_change())

# Generate some Random Portfolio Weights
number_of_symbols = len(processed_df.columns)
random_weights = np.array(np.random.random(number_of_symbols))

# Normalize the weights to sum to 1
rebalance_weights = random_weights / np.sum(random_weights)
    #print(f"rebalance_weights: {rebalance_weights}")


"""
Expected Returns, Volatility and Sharpe Ratio

"""

# Calculate Expected Returns, Annualised
exp_ret = np.sum((log_return.mean() * rebalance_weights) * 252)

# Calculate Expected Volatility, Annualised
exp_vol = np.sqrt(
    np.dot(rebalance_weights.T, np.dot(log_return.cov() * 252, rebalance_weights))
)

# Calculate the Sharpe Ratio
risk_free_rate = 0.01                                                                       # Change as needed
sharpe_ratio = (exp_ret - risk_free_rate) / exp_vol


# Optional : Putting Weights, Portfolio Return, Volatility and Sharpe Ratio in a DataFrame

weights_df = pd.DataFrame( data={
    'random_weights': random_weights,
    'rebalance_weights': rebalance_weights,
})

metrics_df = pd.DataFrame( data={
    'Expected Portfolio Returns': exp_ret,
    'Expected Portfolio Volatility': exp_vol,
    'Portfolio Sharpe Ratio': sharpe_ratio
}, index=[0])


"""
A nice way to print below


"""


def print_weights_metrics(weights_df: pd.DataFrame, metrics_df: pd.DataFrame):
    """
    Print the weights and metrics of the portfolio.
    """
    print("Weights:")
    print(tabulate(weights_df, headers='keys', tablefmt='psql'))
    print("\nMetrics:")
    print(tabulate(metrics_df, headers='keys', tablefmt='psql'))

print_weights_metrics(weights_df, metrics_df)



"""
Functions for Streamlit app


"""

def calculate_portfolio_metrics(weights, log_return):
    exp_ret = np.sum((log_return.mean() * weights) * 252)
    exp_vol = np.sqrt(np.dot(weights.T, np.dot(log_return.cov() * 252, weights)))
    sharpe_ratio = (exp_ret - risk_free_rate) / exp_vol  # risk-free rate as 0.01
    return exp_ret, exp_vol, sharpe_ratio