import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("./one_vs_ten.csv")

metrics = ['total_events', 'duplicates', 'unordered_events', 'duration']

for metric in metrics:
    plt.figure(figsize=(8, 6))
    bar_width = 0.35
    index = np.arange(len(data))

    plt.bar(index, data[metric], bar_width, label='one')
    plt.bar(index + bar_width, data[metric], bar_width, label='ten')

    plt.xlabel('Metric')
    plt.ylabel(metric)
    plt.title(f'Comparison of {metric} between one and ten')
    plt.xticks(index + bar_width / 2, data['name'])
    plt.legend()
    plt.tight_layout()
    plt.show()

