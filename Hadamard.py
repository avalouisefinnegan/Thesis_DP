import time
from pure_ldp.frequency_oracles import *
from pure_ldp.heavy_hitters import *



def Hadamard(budget, data, d):

    data_hadamard = [x+1 for x in data]


    all_released_counts =[]
    all_elapsed_time = []
    for i in range(len(budget)):
        epsilon = budget[i][0]
        print("Starting Hadamard with an epsilon value of ", epsilon)
        start_time = time.time()

        server_hr = HadamardResponseServer(epsilon, d)
        client_hr = HadamardResponseClient(epsilon, d, server_hr.get_hash_funcs())


        for item in data_hadamard:
            # Simulate client-side privatisation
            priv_data = client_hr.privatise(item)

            # Simulate server-side aggregation
            server_hr.aggregate(priv_data)


        end_time = time.time()

        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)

        #post-processing
        released_counts = []
        for i in range(d):
            count = server_hr.estimate(i+1)
            count = int(count)
            released_counts.append(count)
        all_released_counts.append(released_counts)

        print("Finished Hadamard with an epsilon value of ", epsilon)

    return(all_released_counts, all_elapsed_time)

