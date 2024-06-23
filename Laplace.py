import time
import numpy as np
import opendp.prelude as dp
dp.enable_features("contrib")
dp.enable_features("floating-point")


def calculate_rmse(predicted_values, actual_values):    
    # Calculate the squared differences
    squared_diffs = np.square(np.array(predicted_values) - np.array(actual_values))
    
    # Calculate the mean of squared differences
    mean_squared_diff = np.mean(squared_diffs)
    
    # Take the square root to get RMSE
    rmse = np.sqrt(mean_squared_diff)
    
    return rmse

def Laplace_Mechamism(budget, max_influence, data, histogram, sensitive_counts):
    # empty lists
    all_released_counts = []
    all_elapsed_time = []
    all_rmse  =[]


    for epsilon in range(len(budget)):
        #d_in is the sensistivity 
        #d_out is the privacy budget ie.epsilon
        # noisy_histogram = dp.binary_search_chain(
        #     lambda s: histogram >> dp.m.then_laplace(scale=s),
        #     d_in=max_influence, d_out=epsilon)

        noisy_histogram = histogram >> dp.m.then_base_discrete_laplace(scale = max_influence/budget[epsilon][0])

        print("Starting Laplace with an epsilon value of ", epsilon)


        start_time = time.time()
        released_counts = noisy_histogram(data)
        end_time = time.time()

        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)

        print("Finished Laplace with an epsilon value of ", epsilon)

        # Post-processing to ensure non-negative counts
        released_counts = [max(count, 0) for count in released_counts]
        released_counts = released_counts[:-1]
        all_released_counts.append(released_counts)

        rmse = calculate_rmse(released_counts, sensitive_counts)
        all_rmse.append(rmse)
    
    print("Finished Laplace")

    return(all_released_counts, all_elapsed_time, all_rmse)