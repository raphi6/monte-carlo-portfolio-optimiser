from config import *
pd.set_option('display.max_colwidth', None)

# Load our processed data
processed_df = pd.read_csv('stock_data_cleaned.csv', index_col=0, parse_dates=True)

# Some Variables
num_of_symbols = len(processed_df.columns) 
risk_free_rate = 0.01                            # Change as needed

"""
---------------------------Monte Carlo-------------------------------- 
 Instead of doing traditional optimisation by maximising Sharpe Ratio with a minimisation function of -ve Sharpe, and minimising Volatility, 
 we can do a Monte Carlo simulation to find the optimal portfolio.

"""

"""
Below we will define some large matrices to hold the results of all our simulation.

"""

# Defining number of simulations
num_of_portfolios = 10000 

# Predefining empty arrays to hold the results
# Weight Array of NumPy zeroes
all_weights = np.zeros((num_of_portfolios, num_of_symbols))

# Return Array of Numpy zeroes
ret_arr = np.zeros(num_of_portfolios)

# Volatility Array of NumPy zeroes
vol_arr = np.zeros(num_of_portfolios)

# Sharpe Array of NumPy zeroes
sharpe_arr = np.zeros(num_of_portfolios)



"""
Precompute a few statistics that can be kept outside the loop for efficiency

"""

log_return = np.log(1 + processed_df.pct_change())   # Calculate the Log Returns
log_return_mean = log_return.mean() * 252            # Annualized expected returns
log_return_cov = log_return.cov() * 252              # Annualized covariance matrix



"""
Below we start our Monte Carlo simulation

"""
# Start Simulation
for i in range(num_of_portfolios):

    # Calculate random weights
    weights = np.array(np.random.random(num_of_symbols))
    weights = weights / np.sum(weights)

    # Add weights to weights array
    all_weights[i, :] = weights

    # Calculate Expected Log Returns, Annualised
    ret_arr[i] = np.sum(log_return_mean * weights)

    # Calculate Expected Volatility, Annualised
    vol_arr[i] = np.sqrt(
        np.dot(weights.T, np.dot(log_return_cov, weights))
        )
    
    # Calculate the Sharpe Ratio
    sharpe_arr[i] = (ret_arr[i] - risk_free_rate) / vol_arr[i]


# Combining all simulation results
simulations_data = [ret_arr, vol_arr, sharpe_arr, all_weights]

# Creating a DataFrame from the simulation data
simulations_df = pd.DataFrame(data=simulations_data).T

# Naming the columns
simulations_df.columns = [
    'Returns',
    'Volatility', 
    'Sharpe Ratio', 
    'Weights'
]

# Make sure data types are correct
simulations_df = simulations_df.infer_objects()


"""
# Let's Display our Outputs

"""


# Full precision for floats
pd.options.display.float_format = '{:.10f}'.format


print('')
print('='*80)
print('Monte Carlo Simulation Results')
print('-'*80)
print(simulations_df.head())
print('-'*80)


# Reset to default formatting
pd.reset_option('display.float_format')


"""
Some Important Metrics


"""

# Max Sharpe Ratio
max_sharpe_ratios = simulations_df.loc[simulations_df['Sharpe Ratio'].idxmax()]

# Min Volatility
min_volatility = simulations_df.loc[simulations_df['Volatility'].idxmin()]

print('')
print('='*80)
print('Max Sharpe Ratio Portfolio')
print('-'*80)
print(max_sharpe_ratios)
print('='*80)
print(min_volatility)
print('-'*80)



"""
Plotting the results

"""
import matplotlib.pyplot as plt

# Plotting the efficient frontier with Sharpe Ratio color map
plt.figure(figsize=(12, 8))
scatter = plt.scatter(
    simulations_df['Volatility'], 
    simulations_df['Returns'], 
    c=simulations_df['Sharpe Ratio'], 
    cmap='viridis'
)
plt.colorbar(scatter, label='Sharpe Ratio')  # Adding color bar for Sharpe Ratios
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.title('Monte Carlo Simulation: Efficient Frontier')

# Highlighting the max Sharpe ratio portfolio
plt.scatter(
    max_sharpe_ratios['Volatility'], 
    max_sharpe_ratios['Returns'], 
    color='red', 
    marker='*', 
    s=200, 
    label='Max Sharpe Ratio'
)

# Highlighting the min volatility portfolio
plt.scatter(
    min_volatility['Volatility'], 
    min_volatility['Returns'], 
    color='blue', 
    marker='*', 
    s=200, 
    label='Min Volatility'
)

plt.legend()
plt.show()



"""
Functions for Streamlit app

"""

def monte_carlo_simulation(processed_df, num_of_portfolios=10000, risk_free_rate=0.01):
    num_of_symbols = len(processed_df.columns)
    log_return = np.log(1 + processed_df.pct_change())
    log_return_mean = log_return.mean() * 252
    log_return_cov = log_return.cov() * 252

    all_weights = np.zeros((num_of_portfolios, num_of_symbols))
    ret_arr = np.zeros(num_of_portfolios)
    vol_arr = np.zeros(num_of_portfolios)
    sharpe_arr = np.zeros(num_of_portfolios)

    for i in range(num_of_portfolios):
        weights = np.random.random(num_of_symbols)
        weights /= np.sum(weights)
        all_weights[i, :] = weights
        ret_arr[i] = np.sum(log_return_mean * weights)
        vol_arr[i] = np.sqrt(np.dot(weights.T, np.dot(log_return_cov, weights)))
        sharpe_arr[i] = (ret_arr[i] - risk_free_rate) / vol_arr[i]

    simulations_df = pd.DataFrame({'Returns': ret_arr, 'Volatility': vol_arr, 'Sharpe Ratio': sharpe_arr})
    return simulations_df
