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


def Direct_Encoding(size, categories, commutes, epsilon):
    # Generate the randomized responses
    prob_p = 1 / 2
    prob_q = 1 / (np.exp(epsilon) + 1)

    released_counts = [0] * len(categories)

    for individual in range(size):
        # Create a vector of zeros with the same size as categories
        directencoding = [0] * len(categories)
        index = categories.index(commutes[individual])
        directencoding[index] = 1

        # Respond truthfully with probability p
        if random.random() < prob_p:
            true_value = directencoding
        else:
            #Else Respond randomly with probability q
            # Flip a random bit in the vector
            random_index = random.randint(0, len(categories) - 1)
            directencoding[random_index] = 1 if directencoding[random_index] == 0 else 0
            false_value = directencoding

        released_counts = [sum(element) for element in zip(released_counts, directencoding)]

    return released_counts