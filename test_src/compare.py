import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import fill
import sys
import os

# Load data from Excel
file_path = sys.argv[1]+"times.xlsx"

sheet_1 = sys.argv[2] + " " + sys.argv[3] + " times"
sheet_2 = sys.argv[4] + " " + sys.argv[5] + " times"


# Read average times from the 'Average' sheet
df_avg = pd.read_excel(file_path, sheet_name=sheet_1, index_col=0)

# Read median times from the 'Median' sheet
df_median = pd.read_excel(file_path, sheet_name=sheet_2, index_col=0)

# Extract file sizes and speeds from the DataFrames
file_sizes = df_avg.columns.tolist()
speeds = df_avg.index.tolist()

# Convert dataframes to dictionaries for easier access
average_times = df_avg.to_dict(orient='list')
median_times = df_median.to_dict(orient='list')

# Plot the histograms for each object size
fig, axes = plt.subplots(3, 3, figsize=(10, 10))
axes = axes.flatten()

# Create subplots
fig.suptitle(f'Comparison of {sys.argv[2]} {sys.argv[3]} and {sys.argv[4]} {sys.argv[5]} Transfer Times')

bar_width = 0.35  # Width of bars
index = np.arange(len(speeds))  # Index for x locations

#function to wrap text
def wrap_text(text, width=20):
    return fill(text, width=width)

for i, size in enumerate(file_sizes):
    ax = axes[i]

    avg_times = average_times[size]
    med_times = median_times[size]

    label_1 = sys.argv[2] + " " + sys.argv[3] + " time"
    label_2 = sys.argv[4] + " " + sys.argv[5] + " time"

    # Create bars for average and median times
    bars_avg = ax.bar(index - bar_width / 2, avg_times, bar_width, label=label_1)
    bars_median = ax.bar(index + bar_width / 2, med_times, bar_width, label=label_2)

    ax.set_title(wrap_text(f'{size} Object', width=30))
    ax.set_xlabel('Bandwidth')
    ax.set_ylabel('Time (ms)')
    ax.set_xticks(index)
    ax.set_xticklabels(speeds)
    #ax.legend()

# Add a single legend outside of the subplots
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower right')

# Hide any unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

fig.tight_layout()

directory = sys.argv[1]+"histogram/"
if not os.path.exists(directory):
    # Create the directory
    os.makedirs(directory)
    print(f"Directory '{directory}' created successfully.")
else:
    print(f"Directory '{directory}' already exists.")

file_name= directory+sys.argv[2]+sys.argv[3]+"_vs_"+sys.argv[4]+sys.argv[5]+".png"
plt.savefig(file_name)
plt.close()

