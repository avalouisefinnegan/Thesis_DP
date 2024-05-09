import random
import time
import numpy as np
import pandas as pd


def calculate_rmse(predicted_values, actual_values):    
    # Calculate the squared differences
    squared_diffs = np.square(np.array(predicted_values) - np.array(actual_values))
    
    # Calculate the mean of squared differences
    mean_squared_diff = np.mean(squared_diffs)
    
    # Take the square root to get RMSE
    rmse = np.sqrt(mean_squared_diff)
    
    return rmse


def select_index(random_num, prob_q, data_universe_size, individual_index):
    cumulative_probs = [i * prob_q for i in range(data_universe_size-1)]
    cumulative_sum = sum(cumulative_probs)
    # Normalize probabilities
    normalized_probs = [cum_prob / cumulative_sum for cum_prob in cumulative_probs]
    # Find the index where p falls in the CDF
    cdf = 0
    for index, prob in enumerate(normalized_probs):
        cdf += prob
        if random_num < cdf:
            #Don't want the output index to equal the true index of the individual 
            index = index + 1 if index >= individual_index else index
            return index
        

def select_index_alternative(random_num, prob_q, data_universe_size, individual_index):
    return()



import random
def Randomised_Response(budget, size, categories, commutes, sensitive_counts):
    all_released_counts =[]
    all_elapsed_time = []
    all_rmse  =[]
    data_universe_size = len(categories)

    for epsilon in range(len(budget)):

        print("Starting Randomised Response with an epsilon value of ", epsilon)
        start_time = time.time()

        prob_p = np.exp(budget[epsilon][0]) / (np.exp(budget[epsilon][0]) + data_universe_size - 1)
        prob_q = 1 / (np.exp(budget[epsilon][0]) + data_universe_size - 1)
        
        # Generate the randomized responses
        released_counts = [0] * len(categories)
        for individual in range(size):
            true_response = commutes[individual]
            individual_index = categories.index(true_response)
            # Respond truthfully with probability p
            random_num = random.random()
            if random_num < prob_p:
                index = individual_index
            else:
                #Else Respond with one of the other values with probability  (1-p). Each value is reponded with prob q
                #prob q respond with answer 1
                #prob 2q respond with answer 2 ... prob (|X|-1)q repond with answer |X|-1  
                index = select_index(random_num, prob_q, data_universe_size, individual_index)
            released_counts[index] += 1
        end_time = time.time()

        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)

        all_released_counts.append(released_counts)

        print("Finished Randomised Response with an epsilon value of ", epsilon)

        rmse = calculate_rmse(released_counts, sensitive_counts[:-1])
        all_rmse.append(rmse)


    return(all_released_counts, all_elapsed_time, all_rmse)