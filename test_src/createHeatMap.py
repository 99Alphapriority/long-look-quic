import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the performance data
#tcp_df = pd.read_csv('tcp_performance.csv')
#quic_df = pd.read_csv('quic_performance.csv')

# Calculate the difference between QUIC and HTTPS
#difference_df = quic_df - tcp_df

# Example Data - structure to match the provided image's heatmap
# Adjust this part to match your actual data structure
data = {
	'1MBx1': [31.4827, 57.4969, 57.7483],			
	'500KBx2': [31.8211, 57.5476, 57.6655],			
	'200KBx5': [31.9181, 57.4245, 57.8850],			
	'100KBx10': [32.2878, 59.1260, 58.6197],			
	'10KBx100': [10.6305, 12.8084, 12.0526],			
	'5KBx200': [20.4151, 16.4636, 16.2937]			
#	'10MB': [64.0090, 105.4950, 106.6247]			
}

# Network conditions as index
index = ['10Mbps', '50Mbps', '100Mbps']

# Create the DataFrame
df = pd.DataFrame(data, index=index)

# Create the heatmap
plt.figure(figsize=(12, 6))
heatmap = sns.heatmap(df, annot=True, cmap='coolwarm', center=0, linewidths=1, vmin=-100, vmax=100, cbar_kws={'ticks': [-100, -50, 0, 50, 100]})

# Ensure the blocks are square
plt.gca().set_aspect('equal', adjustable='box')

# Customize the colorbar
cbar = heatmap.collections[0].colorbar
cbar.set_ticks([-100, -50, 0, 50, 100])
cbar.set_ticklabels(['-100', '-50', '0', '50', '100'])

# Customize the heatmap
plt.title('Varying #Object, 0% Loss, 112 ms RTT')
plt.xlabel('Object Size')
plt.ylabel('Bandwidth')

# Show the heatmap
plt.show()

