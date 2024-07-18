import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# Network conditions as index
index = ['10Mbps', '50Mbps', '100Mbps']

#provide the excel file
excel_file = sys.argv[1] + "times.xlsx"

#read data from the Average times page of the provided excel sheet
df = pd.read_excel(excel_file, sheet_name='Average times', index_col=0)

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
plt.title('Varying number of objects, 0% Loss, 112 ms RTT')
plt.xlabel('Object Size')
plt.ylabel('Bandwidth')

# Show the heatmap
plt.show()

