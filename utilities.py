import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import opendp.prelude as dp
dp.enable_features("contrib")
dp.enable_features("floating-point")
from StabilityHist import *
from Laplace import *
from Randomised_Response import *
from Unary_Encoding import *

#Load in Data
#The first CSV file is the sensitive data where each individual corresponds to a row
#The second CSV file is the aggregate file where all possible elements are present, in this mobility dataset, majority of the elements have a count of 0. 
def get_variables(path, level, Level):
    agg_data_df = pd.read_csv(path + f"Dagg_commute_{level}_level_all.csv")
    data_df = pd.read_csv(path + f"Dcommute_{level}_level_all.csv")

    col_names = [f"{Level}_commute",f"{Level}_Origin",f"{Level}_Destination"]
    size = len(data_df) #Number of individuals in dataset

    categories = agg_data_df[f'{Level}_commute'].unique()
    len(categories) # MUST TAKE FROM DATA WHERE CATEGORIES CAN HAVE COUNT 0 ie.not where each individual is row
    categories = list(categories) #Number of possible categories 

    data_df.columns = col_names
    commutes = data_df[f"{Level}_commute"].tolist()

    return(size, categories, col_names, data_df, commutes)


def plot_histogram(sensitive_counts, released_counts, mechanism_name, level, epsilon, mechanism):
    """Plot a histogram that compares true data against released data"""
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    fig = plt.figure()
    ax = fig.add_axes([1,1,1,1])
    #plt.ylim([0,20000])
    
    tick_spacing = 1.
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    width = .4

    ax.bar(list([x+width for x in range(0, len(sensitive_counts))]), sensitive_counts, width=width, label='True Value', color='xkcd:dark brown')

    if mechanism == 'laplace':
        color = 'xkcd:light red'
    elif mechanism == 'stabilityhist':
        color = 'xkcd:kelly green'
    elif mechanism == 'randresponse':
        color = 'xkcd:tangerine'
    elif mechanism == 'unaryencoding':
        color = 'xkcd:azure'
    elif mechanism == 'olh':
        color = 'xkcd:sky blue'
    elif mechanism == 'hadamard':
        color = 'xkcd:pastel purple'
    else:       
        color = 'green'

    ax.bar(list([x+2*width for x in range(0, len(released_counts))]), released_counts, width=width, label='DP Value', color = color)

    ax.legend()
    plt.xticks([])  
    plt.title(f'Histogram of Counts after {mechanism_name} for {level} Level Commute')
    plt.xlabel('Commute')
    plt.ylabel(f'Count using epsilon {epsilon}')
    plt.show()



def run_client(Mechanism, Level, budget, size, categories, commutes, sensitive_counts):
    if Mechanism == "randresponse":
        released_counts_client, elapsed_time_client = Randomised_Response_Client(budget, size, categories, commutes, sensitive_counts)
    if Mechanism == "unaryencoding":
        if Level == "ED":
            raise Exception("Unary Encoding is not suitable for the electoral division level due to compuational complexity")
        else:
            released_counts_client, elapsed_time_client = Unary_Encoding_Client(budget, size, categories, commutes, sensitive_counts)
    return(released_counts_client, elapsed_time_client)

def run_server(Mechanism, Level, released_counts, sensitive_counts, size, budget, categories, g):
    if Mechanism == "randresponse":
        released_counts, elapsed_time, all_rmse = Randomised_Response_Server(released_counts, sensitive_counts, size, budget, categories)
    if Mechanism == "unaryencoding":
        if Level == "ED":
            raise Exception("Unary Encoding is not suitable for the electoral division level due to compuational complexity")
        else:
            released_counts, elapsed_time, all_rmse = Unary_Encoding_Server(released_counts, sensitive_counts, size, budget)
    return(released_counts, elapsed_time, all_rmse)


def run_central(Mechanism, col_names, Level, budget, max_influence, size, data, histogram, categories, sensitive_counts):
    if Mechanism == "laplace":
        released_counts, elapsed_time, all_rmse = Laplace_Mechamism(budget, max_influence, data, histogram, sensitive_counts)
    if Mechanism == "stabilityhist":
        released_counts, elapsed_time, all_rmse = Stability_Hist(col_names, Level, budget, max_influence, size, data, histogram, categories, sensitive_counts)

