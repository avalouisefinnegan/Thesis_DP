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


def Unary_Encoding_old(budget, size, categories, commutes, sensitive_counts):

    all_released_counts = []
    all_elapsed_time = []
    all_rmse = []

    for epsilon in range(len(budget)):

        print("Starting Unary Encoding with an epsilon value of ", epsilon)
        start_time = time.time()

        prob_p = 1 / 2
        prob_q = 1 / (np.exp(budget[epsilon][0]) + 1)

        released_counts = np.zeros(len(categories)) # [0] * len(categories)

        for individual in range(size):
            # Create a vector of zeros with the same size as categories
            unaryencoding = np.zeros(len(categories)) # [0] * len(categories)
            index = categories.index(commutes[individual])
            #unaryencoding[index] = 1

            if random.random() < prob_p:
                # Respond truthfully with probability p
                unaryencoding[index] == 1 

            else:   
                unaryencoding[index] = 0 

            # for i in range(len(categories)):
            #     if unaryencoding[i] == 1:
            #         if random.random() < prob_p:
            #             # Respond truthfully with probability p
            #             unaryencoding[i] == 1 
            #             #true_value = unaryencoding§
            #         else:   
            #             unaryencoding[i] = 0 
            #     if unaryencoding[i] == 0: 
            #         if random.random() < prob_q:
            #             unaryencoding[i] = 1
            #         else: 
            #             unaryencoding[i] = 0
            #else:
                #Else Respond randomly with probability q
                # Flip a random bit in the vector
                #random_index = random.randint(0, len(categories) - 1)
                #unaryencoding[random_index] = 1 if unaryencoding[random_index] == 0 else 0
            #    false_value = unaryencoding
            released_counts += unaryencoding
            # released_counts = [sum(element) for element in zip(released_counts, unaryencoding)]
        
        print("Finishing Unary Encoding with an epsilon value of ", epsilon)
        end_time = time.time()

        elapsed_time = end_time - start_time

        all_elapsed_time.append(elapsed_time)
        all_released_counts.append(released_counts)    

        rmse = calculate_rmse(list(released_counts), sensitive_counts[:-1])
        all_rmse.append(rmse)
   

    return (all_released_counts, all_elapsed_time, all_rmse)




def Unary_Encoding_Client(budget, size, categories, commutes, sensitive_counts):

    all_released_counts = []
    all_elapsed_time = []

    for epsilon in range(len(budget)):

        print("Starting Unary Encoding with an epsilon value of ", epsilon)
        start_time = time.time()

        prob_p = 1 / 2
        prob_q = 1 / (np.exp(budget[epsilon][0]) + 1)

        released_counts = np.zeros(len(categories)) #[0] * len(categories)

        for individual in range(size):
            # Create a vector of zeros with the same size as categories
            index = categories.index(commutes[individual])

            elements_before_index = []

            for i in range(index):
                random_number = random.random()
                if random_number < prob_q:
                    elements_before_index.append(1)
                else:
                    elements_before_index.append(0)

            if random.random() < prob_p:
                # Respond truthfully with probability p
                index_list = [1] 
            else:   
                index_list = [0]  

            elements_after_index = []
            for i in range(len(categories) - index - 1):
                random_number = random.random()
                if random_number < prob_q:
                    elements_after_index.append(1)
                else:
                    elements_after_index.append(0)           

            unaryencoding = np.array(elements_before_index + index_list + elements_after_index)

            released_counts += unaryencoding
            #released_counts = [sum(element) for element in zip(released_counts, unaryencoding)]
        
        print("Finishing Unary Encoding with an epsilon value of ", epsilon)
        end_time = time.time()

        elapsed_time = end_time - start_time

        all_elapsed_time.append(elapsed_time)
        all_released_counts.append(released_counts)    

    return (all_released_counts, all_elapsed_time)



def Unary_Encoding_Server(released_counts, sensitive_counts,  size, budget):
    all_released_counts = []
    all_elapsed_time = []
    all_rmse = []
    for epsilon in range(len(budget)):
        prob_p = 1 / 2
        prob_q = 1 / (np.exp(budget[epsilon][0]) + 1)
        start_time = time.time()

        released_counts_server = (released_counts[epsilon] - (prob_q*size))/(prob_p - prob_q)

        #rmse = calculate_rmse(released_counts_server, sensitive_counts[:-1])
        #all_rmse.append(rmse)
        end_time = time.time()
        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)
        all_released_counts.append(released_counts_server)

    #return(all_released_counts, all_elapsed_time, all_rmse)
    return(all_released_counts, all_elapsed_time)