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


def Unaary_Encoding(budget, size, categories, commutes, sensitive_counts):

    all_released_counts = []
    all_elapsed_time = []
    all_rmse = []

    for epsilon in range(len(budget)):

        print("Starting Unary Encoding with an epsilon value of ", epsilon)
        start_time = time.time()

        # Generate the randomized responses
        prob_p = 1 / 2
        prob_q = 1 / (np.exp(budget[epsilon][0]) + 1)

        released_counts = [0] * len(categories)

        for individual in range(size):
            # Create a vector of zeros with the same size as categories
            unaryencoding = [0] * len(categories)
            index = categories.index(commutes[individual])
            unaryencoding[index] = 1

            for i in range(len(categories)):
                if unaryencoding[i] == 1:
                    if random.random() < prob_p:
                        # Respond truthfully with probability p
                        unaryencoding[i] == 1 
                        #true_value = unaryencoding
                    else:   
                        unaryencoding[i] = 0 
                if unaryencoding[i] == 0: 
                    if random.random() < prob_q:
                        unaryencoding[i] = 1
                    else: 
                        unaryencoding[i] = 0
            #else:
                #Else Respond randomly with probability q
                # Flip a random bit in the vector
                #random_index = random.randint(0, len(categories) - 1)
                #unaryencoding[random_index] = 1 if unaryencoding[random_index] == 0 else 0
            #    false_value = unaryencoding

            released_counts = [sum(element) for element in zip(released_counts, unaryencoding)]
        
        print("Finishing Unary Encoding with an epsilon value of ", epsilon)
        end_time = time.time()

        elapsed_time = end_time - start_time

        all_elapsed_time.append(elapsed_time)
        all_released_counts.append(released_counts)    

        rmse = calculate_rmse(released_counts, sensitive_counts[:-1])
        all_rmse.append(rmse)
   

    return (all_released_counts, all_elapsed_time, all_rmse)