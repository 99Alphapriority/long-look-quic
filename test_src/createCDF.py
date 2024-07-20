import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import os
import sys

excel_file=sys.argv[1] + "times.xlsx"
#bw=sys.argv[2]
loss = sys.argv[2]
rtt = sys.argv[3]

bandwidth=[10,50,100]
obj_set1  = [ '5k.html', '10k.html', '100k.html', '200k.html', '500k.html', '1mb.html', '10mb.html',]  
obj_set2  = [ '1mbx1.html','500kx2.html' ,'200kx5.html' ,'100kx10.html', '10kx100.html', '5kx200.html' ]

objs = obj_set1

for bw in bandwidth:
    # Define the directory path you want to create
    directory = sys.argv[1]+"CDF/"+str(bw)+"_"+rtt+"_"+loss
    # Check if the directory already exists
    if not os.path.exists(directory):
        # Create the directory
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")

for bw in bandwidth:
    for obj in objs:
        sheet_name = str(bw) + "Mbps_" + obj
        data = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Extract TCP and QUIC data
        tcp_data = data['TCP'].dropna()
        quic_data = data['QUIC'].dropna()

        run_number = len(tcp_data)

        # Sort the data
        tcp_data_sorted = np.sort(tcp_data)
        quic_data_sorted = np.sort(quic_data)

        # Handle duplicates by adding a small offset
        tcp_data_sorted = tcp_data_sorted + np.arange(len(tcp_data_sorted)) * 1e-5
        quic_data_sorted = quic_data_sorted + np.arange(len(quic_data_sorted)) * 1e-5

        # Compute the CDF
        tcp_cdf = np.arange(1, len(tcp_data_sorted) + 1) / len(tcp_data_sorted)
        quic_cdf = np.arange(1, len(quic_data_sorted) + 1) / len(quic_data_sorted)
        # Plot the CDF with interpolation
        plt.figure(figsize=(10, 6))
        plt.plot(tcp_data_sorted, tcp_cdf, label='TCP', color='blue')
        plt.plot(quic_data_sorted, quic_cdf, label='QUIC', color='orange')

        # Add titles and labels
        plt.title(f'Cumulative Distribution Function (CDF) of {run_number} TCP and QUIC Run Times.({bw} Mbps {loss}% loss {rtt}ms RTT {obj})')
        plt.xlabel('Time (ms)')
        plt.ylabel('Cumulative Probability')
        plt.legend(loc='lower right')
        plt.grid(True)

        file_name=sys.argv[1]+"CDF/"+str(bw)+"_"+rtt+"_"+loss+"/"+obj+".png"
        plt.savefig(file_name)
        plt.close()

        # Show the plot
        #plt.show()

