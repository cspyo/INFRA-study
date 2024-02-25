import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("./all_metrics.csv")

grouped_data = data.groupby("name")

metrics = ['total_events', 'duplicates', 'unordered_events', 'duration']

for metric in metrics:
    plt.figure(figsize=(10, 6))
    plt.title(metric)
    x_labels = []
    for name, group in grouped_data:
        plt.bar(name, group[metric].mean(), label=name)
        x_labels.append(name)
    plt.xlabel('Name')
    plt.ylabel(metric)
    plt.xticks(ticks=range(len(x_labels)), labels=x_labels, rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()
