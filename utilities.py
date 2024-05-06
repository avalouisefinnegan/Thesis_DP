import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import opendp.prelude as dp
dp.enable_features("contrib")
dp.enable_features("floating-point")
from StabilityHist import *
from Laplace import *

#Load in Data
#The first CSV file is the sensitive data where each individual corresponds to a row
#The second CSV file is the aggregate file where all possible elements are present, in this mobility dataset, majority of the elements have a count of 0. 
def get_variables(path, level, Level):
    agg_data_df = pd.read_csv(path + f"agg_commute_{level}_level_all.csv")
    data_df = pd.read_csv(path + f"commute_{level}_level_all.csv")

    col_names = [f"{Level}_commute",f"{Level}_Origin",f"{Level}_Destination"]
    size = len(data_df) #Number of individuals in dataset

    categories = agg_data_df[f'{Level}_commute'].unique()
    len(categories) # MUST TAKE FROM DATA WHERE CATEGORIES CAN HAVE COUNT 0 ie.not where each individual is row
    categories = list(categories) #Number of possible categories 
    return(size, categories, col_names)


def calculate_rmse(predicted_values, actual_values):    
    # Calculate the squared differences
    squared_diffs = np.square(np.array(predicted_values) - np.array(actual_values))
    
    # Calculate the mean of squared differences
    mean_squared_diff = np.mean(squared_diffs)
    
    # Take the square root to get RMSE
    rmse = np.sqrt(mean_squared_diff)
    
    return rmse

def plot_histogram(sensitive_counts, released_counts):
    """Plot a histogram that compares true data against released data"""
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    fig = plt.figure()
    ax = fig.add_axes([1,1,1,1])
    #plt.ylim([0,20000])
    
    tick_spacing = 1.
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    width = .4

    ax.bar(list([x+width for x in range(0, len(sensitive_counts))]), sensitive_counts, width=width, label='True Value')
    ax.bar(list([x+2*width for x in range(0, len(released_counts))]), released_counts, width=width, label='DP Value')

    ax.legend()
    plt.xticks([])  
    plt.title(f'Histogram of Counts after {Mechanism_name} for {Level} Level Commute')
    plt.xlabel('Commute')
    plt.ylabel('Count')
    plt.show()

def run_dp(Mechanism, col_names, Level, budget, max_influence, size, data, histogram, categories, sensitive_counts):
    if Mechanism == "laplace":
        released_counts, elapsed_time, all_rmse = Laplace_Mechamism(budget, max_influence, data, histogram, sensitive_counts)
    if Mechanism == "stabilityhist":
        released_counts, elapsed_time, all_rmse = Stability_Hist(col_names, Level, budget, max_influence, size, data, histogram, categories, sensitive_counts)

    return(released_counts, elapsed_time, all_rmse)

