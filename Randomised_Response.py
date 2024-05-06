import random
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
        randomised_responses = []
        for individual in range(size):
            true_response = commutes[individual]
            # Respond truthfully with probability p
            if random.random() < prob_p:
                true_value = true_response
                randomised_responses.append(true_response)
            else:
                #Else Respond randomly with probability q
                false_value = random.randint(0, len(categories)-1)
                false_value = categories[false_value]
                randomised_responses.append(false_value)

        rr_response= pd.Series(randomised_responses)
        rr_counts = rr_response.value_counts()
        rr_df = pd.DataFrame({'Value': rr_counts.index, 'Count': rr_counts.values})
        #Order it so that it is the same as categories
        rr_df = randomised_reponse_df.set_index('Value').reindex(categories).fillna(0).reset_index()
        released_counts = rr_df["Count"].tolist()
        end_time = time.time()

        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)

        all_released_counts.append(released_counts)

        print("Finished Randomised Response with an epsilon value of ", epsilon)

        rmse = calculate_rmse(released_counts, sensitive_counts[:-1])
        all_rmse.append(rmse)


    return(randomised_responses, all_released_counts, all_rmse)