
import scipy.stats as stats
import numpy as np
import pandas as pd
import json

obj_set1  = [ '5k.html', '10k.html', '100k.html', '200k.html', '500k.html', '1mb.html', '10mb.html',]  
obj_set2  = [ '1mbx1.html','500kx2.html' ,'200kx5.html' ,'100kx10.html', '10kx100.html', '5kx200.html' ]  



obj_names = obj_set1 + obj_set2

graph1 = [ '10_36_0', '50_36_0', '100_36_0' ]
graph2 = ['10_112_0', '50_112_0', '100_112_0']
graph3 = ['10_36_1', '50_36_1', '100_36_1' ]

settings = graph1 + graph2 + graph3

setting = "100_36_0"
cases = ["https", "quic"]
total_runs = 10

print("Setting :", setting)
https_obj_times = {}
quic_obj_times = {}

for obj in obj_set2:
    print("Object :", obj)
    times = { "https": [], "quic": []}
    for case in cases:
        for expNo in range(1,total_runs + 1):
            file_name = "../data/results/" + setting + "/" + obj.replace(".", "_") + "/resultsDir/"+case+"_"+str(expNo)+".har"
            try:
                with open( file_name , 'r') as f:
                    j = json.load(f)
                    # print('\t\t', j['log']['entries'][0]['time'])
                    load_t = j['log']['pages'][0]['pageTimings']['onLoad']
                    dns_t = j['log']['entries'][0]['timings']['dns']
                    plt_t = load_t - dns_t
                    times[case].append(plt_t)
            except Exception as e:
                print("Failed ", e)
    
    # print(times["https"])
    # print(times["quic"])

    https_group1 = np.array(times["https"])
    quic_group2 = np.array(times["quic"])

    # Print the variance of both data groups
    # print(np.var(https_group1), np.var(quic_group2))

    # Calculate Stats and P-value of both data groups
    welch_test = stats.ttest_ind(https_group1, quic_group2, equal_var=False)
    # print(welch_test.pvalue)

    if welch_test.pvalue < 0.01:
        print("Performance Difference Statistically Significant")
    else:
        print("!!!!Performance Difference Statistically INSignificant!!!!")

    https_avg_time = np.average(https_group1)
    print("HTTPS: ", https_avg_time)
    https_obj_times[obj] = https_avg_time

    quic_avg_time = np.average(quic_group2)
    print("QUIC: ", quic_avg_time)
    quic_obj_times[obj] = quic_avg_time
    print("")

print("Setting :", setting)
# print("TCP Times :",  https_obj_times)
# print("QUIC Times :", quic_obj_times)

print("TCP Times")
tcp_df = pd.DataFrame(https_obj_times, index=[0])
print(tcp_df)
print()
print("QUIC Times")
quic_df = pd.DataFrame(quic_obj_times, index=[0])
print(quic_df)