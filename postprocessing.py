import time
import numpy as np

def calculate_rmse(predicted_values, actual_values):    
    # Calculate the squared differences
    squared_diffs = np.square(np.array(predicted_values) - np.array(actual_values))
    
    # Calculate the mean of squared differences
    mean_squared_diff = np.mean(squared_diffs)
    
    # Take the square root to get RMSE
    rmse = np.sqrt(mean_squared_diff)
    
    return rmse

def Base(all_released_counts, sensitive_counts, budget):
    base_counts = []
    base_time = []
    base_rmse = []
    for epsilon in range(len(budget)):
        start_time = time.time()
        counts = all_released_counts[epsilon]
        if not type(counts) =='numpy.ndarray':
            counts = np.array(counts)
        counts = np.round(counts).astype(int)
        rmse = calculate_rmse(counts, sensitive_counts)
        base_rmse.append(rmse)
        end_time = time.time()
        elapsed_time = end_time - start_time
        base_time.append(elapsed_time)
        base_counts.append(counts)
    return(base_counts, base_time, base_rmse)


def Base_Pros(all_released_counts, sensitive_counts, budget):
    base_pros_counts = []
    base_pros_time = []
    base_pros_rmse = []
    for epsilon in range(len(budget)):
        start_time = time.time()

        counts = all_released_counts[epsilon]
        if not type(counts) =='numpy.ndarray':
            counts = np.array(counts)

        counts[counts<0] = 0
        counts = np.round(counts).astype(int)


        rmse = calculate_rmse(counts, sensitive_counts)
        base_pros_rmse.append(rmse)
        end_time = time.time()
        elapsed_time = end_time - start_time
        base_pros_time.append(elapsed_time)
        base_pros_counts.append(counts)

    #return(all_released_counts, all_elapsed_time, all_rmse)
    return(base_pros_counts, base_pros_time, base_pros_rmse)



def Base_Cut(all_released_counts, sensitive_counts, budget, size):
    base_cut_counts = []
    base_cut_time = []
    base_cut_rmse = []
    for epsilon in range(len(budget)):
        start_time = time.time()

        counts = all_released_counts[epsilon]
        if not type(counts) =='numpy.ndarray':
            counts = np.array(counts)
    
        counts[counts<0] = 0
        counts = np.round(counts).astype(int)
        
        #Sort array and keep indexes
        sorted_counts_idx = np.argsort(counts)[::-1]

        counter = 0
        for index in range(len(counts)):
            if counter < size:
                counter += counts[sorted_counts_idx[index]]
            else: 
                counts[sorted_counts_idx[index]] = 0

        rmse = calculate_rmse(counts, sensitive_counts)
        base_cut_rmse.append(rmse)
        end_time = time.time()
        elapsed_time = end_time - start_time
        base_cut_time.append(elapsed_time)
        base_cut_counts.append(counts)

    #return(all_released_counts, all_elapsed_time, all_rmse)
    return(base_cut_counts, base_cut_time, base_cut_rmse)



