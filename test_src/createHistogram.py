import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os

excel_file=sys.argv[1] + "times.xlsx"
#bw=sys.argv[2]
loss = sys.argv[2]
rtt = sys.argv[3]

# Number of bins for the histogram
bins = int(sys.argv[4])

bandwidth=[10,50,100]
obj_set1  = [ '5k.html', '10k.html', '100k.html', '200k.html', '500k.html', '1mb.html', '10mb.html',]  
obj_set2  = [ '1mbx1.html','500kx2.html' ,'200kx5.html' ,'100kx10.html', '10kx100.html', '5kx200.html' ]

objs = obj_set1

for bw in bandwidth:
    # Define the directory path you want to create
    directory = sys.argv[1]+"histogram/"+str(bw)+"_"+rtt+"_"+loss
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

        # Create the histogram
        plt.figure(figsize=(12, 8))
        plt.hist(tcp_data, bins, histtype='barstacked', density=False, cumulative=False, alpha=0.5, label='TCP', color='blue')
        #plt.hist(tcp_data, bins, histtype='stepfilled', density=False, cumulative=True, alpha=0.2, label='TCP', color='blue', edgecolor='black')
        plt.hist(quic_data, bins, histtype='barstacked', density=False, cumulative=False, alpha=0.5, label='QUIC', color='orange')
        #plt.hist(quic_data, bins, histtype='stepfilled', density=False, cumulative=True, alpha=0.2, label='QUIC', color='orange', edgecolor='black')

        #for side to side analysis
        '''
        # Compute the histograms
        tcp_hist, bin_edges = np.histogram(tcp_data, bins=bins)
        quic_hist, _ = np.histogram(quic_data, bins=bin_edges)

        # Bar width
        bar_width = (bin_edges[1] - bin_edges[0]) / 3

        # Plot histograms side by side
        plt.figure(figsize=(10, 6))
        plt.bar(bin_edges[:-1] - bar_width/2, tcp_hist, width=bar_width, alpha=0.7, label='TCP', color='blue', edgecolor='black')
        plt.bar(bin_edges[:-1] + bar_width/2, quic_hist, width=bar_width, alpha=0.7, label='QUIC', color='orange', edgecolor='black')
        '''

        # Add titles and labels
        plt.title('Comparison of {} runs: TCP vs RFCv1 ({} Mbps {}% loss {}ms RTT {}) Bin size:{}'.format(run_number, bw, loss, rtt, obj, bins))
        plt.xlabel('Time (ms)')
        plt.ylabel('Frequency')
        plt.legend(loc='upper right')
        plt.grid(True)

        file_name=sys.argv[1]+"histogram/"+str(bw)+"_"+rtt+"_"+loss+"/"+obj+".png"
        plt.savefig(file_name)
        plt.close()

# Show the plot
#plt.show()
plt.close()
