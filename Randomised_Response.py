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

        
def select_index(random_num, prob_p, prob_q, individual_index):
    index = int((random_num - prob_p) // prob_q)
    index = index + 1 if index >= individual_index else index
    return index



import random
def Randomised_Response_Client(budget, size, categories, commutes, sensitive_counts):
    all_released_counts =[]
    all_elapsed_time = []
    data_universe_size = len(categories)

    for epsilon in range(len(budget)):

        print("Starting Randomised Response with an epsilon value of ", budget[epsilon][0])
        start_time = time.time()

        prob_p = np.exp(budget[epsilon][0]) / (np.exp(budget[epsilon][0]) + data_universe_size - 1)
        prob_q = 1 / (np.exp(budget[epsilon][0]) + data_universe_size - 1)
        
        # Generate the randomized responses
        randomised_responses = []
        for individual in range(size):
            true_response = commutes[individual]
            individual_index = categories.index(true_response)
            # Respond truthfully with probability p
            random_num = random.random()
            if random_num < prob_p:
                randomised_responses.append(true_response)
            else:
                #Else Respond with one of the other values with probability  (1-p). Each value is reponded with prob q
                #prob q respond with answer 1
                #prob 2q respond with answer 2 ... prob (|X|-1)q repond with answer |X|-1  
                #index = select_index(random_num, prob_q, data_universe_size, individual_index)
                index = select_index(random_num, prob_p, prob_q, individual_index)
                false_value = categories[index]
            randomised_responses.append(false_value)

        rr_response= pd.Series(randomised_responses)
        rr_counts = rr_response.value_counts()
        rr_df = pd.DataFrame({'Value': rr_counts.index, 'Count': rr_counts.values})
        #Order it so that it is the same as categories
        rr_df = rr_df.set_index('Value').reindex(categories).fillna(0).reset_index()
        released_counts = rr_df["Count"].tolist()


        all_released_counts.append(released_counts)
        end_time = time.time()

        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)

        print("Finished Randomised Response with an epsilon value of ", budget[epsilon][0])

    return(all_released_counts, all_elapsed_time)


def Randomised_Response_Server(released_counts, sensitive_counts,  size, budget, categories):
    all_released_counts = []
    all_elapsed_time = []
    all_rmse = []
    data_universe_size = len(categories)

    for epsilon in range(len(budget)):
        prob_p = np.exp(budget[epsilon][0]) / (np.exp(budget[epsilon][0]) + data_universe_size - 1)
        prob_q = 1 / (np.exp(budget[epsilon][0]) + data_universe_size - 1)
    
        start_time = time.time()

        released_counts_server = (released_counts[epsilon] - (prob_q*size))/(prob_p - prob_q)

        #[0 if x < 0 else x for x in released_counts_server]

        #rmse = calculate_rmse(released_counts_server, sensitive_counts[:-1])
        #all_rmse.append(rmse)
        end_time = time.time()
        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)
        all_released_counts.append(released_counts_server)

    #return(all_released_counts, all_elapsed_time, all_rmse)
    return(all_released_counts, all_elapsed_time)



def Randomised_Response_alternative(budget, size, categories, commutes, sensitive_counts):
    all_released_counts =[]
    all_elapsed_time = []
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
                #index = select_index(random_num, prob_q, data_universe_size, individual_index)
                index = select_index(random_num, prob_p, prob_q, individual_index)
            released_counts[index] += 1
        end_time = time.time()

        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)

        all_released_counts.append(released_counts)

        print("Finished Randomised Response with an epsilon value of ", epsilon)


    return(all_released_counts, all_elapsed_time)