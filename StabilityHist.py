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

def Stability_Hist(col_names, Level, budget, max_influence, size, data, histogram, categories, sensitive_counts) :

    def as_array(data):
        return [data.get(k, 0) for k in categories]

    preprocess = (
    dp.t.make_split_dataframe(separator=",", col_names=col_names) >>
    dp.t.make_select_column(key=f"{Level}_commute", TOA=str) >>
    dp.t.then_count_by(MO=dp.L1Distance[float], TV=float))

    # empty dictionary
    all_released_count_before = []
    all_released_counts = []
    all_elapsed_time = []
    all_rmse  =[]


    for epsilon in range(len(budget)):
        threshold = 2*(np.log(2/budget[1][1]))/(budget[epsilon][0]) + 1/size
        scale = max_influence/budget[epsilon][0]
        noisy_histogram = preprocess >> dp.m.then_base_laplace_threshold(scale=scale, threshold=threshold)

        print("Starting Stability Histogram with an epsilon value of ", epsilon)

        start_time = time.time()
        released_counts = noisy_histogram(data)
        end_time = time.time()

        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)

        print("Finished Stability Histogram with an epsilon value of ", epsilon)

        # postprocess to make the results easier to compare
        postprocessed_counts = {k: round(v) for k, v in released_counts.items()}

        all_released_count_before.append(postprocessed_counts)

    #all_county_released_counts are not ordered. 
    # https://docs.opendp.org/en/stable/examples/histograms.html#Private-histogram-via-make_count_by-and-make_base_laplace_threshold\n
    #Corrects order so it can be compared to the true counts    

    print("Finished Stability Histogram")
    print("Calculating RMSE")

    for i in range(len(all_released_count_before)):
        released_counts = as_array(all_released_count_before[i])
        all_released_counts.append(released_counts)
        rmse = calculate_rmse(released_counts, sensitive_counts)
        all_rmse.append(rmse)


    return(all_released_counts, all_elapsed_time, all_rmse)