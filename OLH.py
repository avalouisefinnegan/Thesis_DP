import time
from pure_ldp.frequency_oracles import *
from pure_ldp.heavy_hitters import *

def OLH(budget, data, d):

    all_released_counts =[]
    all_elapsed_time = []
    for i in range(len(budget)):
        epsilon = budget[i][0]
        print("Starting OLH with an epsilon value of ", epsilon)
        start_time = time.time()

        client_olh = LHClient(epsilon=epsilon, d=d, use_olh=True)
        server_olh = LHServer(epsilon=epsilon, d=d, use_olh=True)

        for item in data:
            # Simulate client-side privatisation
            priv_data = client_olh.privatise(item)

            # Simulate server-side aggregation
            server_olh.aggregate(priv_data)

        end_time = time.time()

        elapsed_time = end_time - start_time
        all_elapsed_time.append(elapsed_time)

        #post-processing
        released_counts = []
        for i in range(d):
            count = server_olh.estimate(i)
            count = int(count)
            released_counts.append(count)
            
        all_released_counts.append(released_counts)

        print("Finished OLH with an epsilon value of ", epsilon)

    return(all_released_counts, all_elapsed_time)

