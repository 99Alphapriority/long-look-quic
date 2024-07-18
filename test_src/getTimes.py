import sys
import scipy.stats as stats
import numpy as np
import pandas as pd
import json
from pprint import pprint

obj_set1  = [ '5k.html', '10k.html', '100k.html', '200k.html', '500k.html', '1mb.html', '10mb.html',]  
obj_set2  = [ '1mbx1.html','500kx2.html' ,'200kx5.html' ,'100kx10.html', '10kx100.html', '5kx200.html' ]  
obj_set3  = [ '500kx2.html']  

# obj_set3 = [ '5k.jpg', '10k.jpg', '100k.jpg', '200k.jpg', '500k.jpg', '1mb.jpg', '10mb.jpg',]  

### Changing
# Q043, v1 ,v2
mainDir = sys.argv[1]
#"../replication/varying_number_of_objects/X-36-0/"
### TIMES run
total_runs = int(sys.argv[2])
# X_36_0, X_36_1, X_112_0
setting = sys.argv[3]
# Objs
objs = obj_set1
#####

cases = ["https", "quic"]

print("Setting :", setting)

tcp_df = pd.DataFrame(columns=objs)
quic_df = pd.DataFrame(columns=objs)
avg_df = pd.DataFrame(columns=objs)

run_time_array = {}

# Create an excel file
excel_file = mainDir + "times.xlsx"

bandwidth_array = [10,50,100]

for bw in bandwidth_array:
    https_obj_times = {}
    quic_obj_times = {}
    avg_obj_times = {}
    for obj in objs:
        print("Object :", obj)
        times = { "https": [], "quic": []}
        for case in cases:
            for expNo in range(1,total_runs + 1):
                file_name = mainDir + setting.replace("X", str(bw)) + "/" + obj.replace(".", "_") + "/resultsDir/"+case+"_"+str(expNo)+".har"
                try:
                    with open( file_name , 'r') as f:
                        j = json.load(f)
                        load_t = j['log']['pages'][0]['pageTimings']['onLoad']
                        dns_t = j['log']['entries'][0]['timings']['dns']
                        if -1 == dns_t:
                            plt_t = load_t
                        else:
                            plt_t = load_t - dns_t
                        times[case].append(plt_t)
                except Exception as e:
                    print("Failed ", e)
            print(file_name)

        https_group1 = np.array(times["https"])
        quic_group2 = np.array(times["quic"])

		# delete the first run as it is not 0-RTT for QUIC
        https_group1 = np.delete(https_group1, 0)
        quic_group2 = np.delete(quic_group2, 0)

        for i in range(1,total_runs):
            print(times["https"][i])

        print("\n")

        for i in range(1,total_runs):
            print(times['quic'][i])

        index = str(bw) + "Mbps_" + obj
        https_reshaped = https_group1.reshape(-1,1)
        quic_reshaped = quic_group2.reshape(-1,1)
        run_time_array[index] = np.concatenate((https_reshaped, quic_reshaped), axis=1)

        # Print the variance of both data groups
        print("TCP PLT Std: ", np.std(https_group1),"\t QUIC PLT Std :", np.std(quic_group2))
        print("TCP PLT 95th: ", np.percentile(https_group1, 95),"\t QUIC PLT 95th :", np.percentile(quic_group2, 95))


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
        
        avg_obj_times[obj] = ((https_obj_times[obj] - quic_obj_times[obj])/quic_obj_times[obj]) * 100

    # print("TCP Times :",  https_obj_times)
    # print("QUIC Times :", quic_obj_times)

    # tcp_df = tcp_df.append(https_obj_times, ignore_index = True)
    # quic_df = quic_df.append(quic_obj_times, ignore_index = True)
    tcp_df.loc[len(tcp_df)] = https_obj_times
    quic_df.loc[len(quic_df)] = quic_obj_times
    avg_df.loc[len(avg_df)] = avg_obj_times

print("QUIC Version : ", mainDir)
print("Setting :", setting)
print("Total Runs :", total_runs)
print("TCP Times")
print(tcp_df)
print()
pprint(tcp_df.to_string(header=False, index=False).split('\n'))

print()
print("QUIC Times")
print(quic_df)
print()
pprint(quic_df.to_string(header=False, index=False).split('\n'))

print()
print("Percentage Difference")
print(avg_df)
print()

# Create an excel file
excel_file = mainDir + "times.xlsx"

# Create a custom index
custom_index = ['10Mbps', '50Mbps', '100Mbps']

# Set custom index
avg_df.index = custom_index
tcp_df.index = custom_index
quic_df.index = custom_index

#Remove the .html suffix from the first row
new_columns = [col.replace('.html', '') for col in tcp_df.columns]
tcp_df.columns = new_columns
quic_df.columns = new_columns
avg_df.columns = new_columns

# Create an ExcelWriter object
with pd.ExcelWriter(excel_file) as writer:
    # Write each DataFrame to a different sheet
    tcp_df.to_excel(writer, sheet_name='TCP times', index=True)
    quic_df.to_excel(writer, sheet_name='QUIC times', index=True)
    avg_df.to_excel(writer, sheet_name='Average times', index=True)

    for bw in bandwidth_array:
        for obj in objs:
            index = str(bw) + "Mbps_" + obj
            column_names = ['TCP', 'QUIC']
            run_times_df = pd.DataFrame(run_time_array[index], columns=column_names)
            run_times_df.to_excel(writer, sheet_name=index, index=False)		
