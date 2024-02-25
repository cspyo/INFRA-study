import pandas as pd
import matplotlib.pyplot as plt

file_paths = {
    "sns": "sns_metrics.csv",
    "sqs-std": "sqs_std_metrics.csv",
    "sqs-fifo": "sqs_fifo_metrics.csv",
    "sns-sqs-std": "sns_sqs_std_metrics.csv",
    "sns-sqs-fifo": "sns_sqs_fifo_metrics.csv",
    "kinesis": "kinesis_metrics.csv"
}

dfs = {name: pd.read_csv(path) for name, path in file_paths.items()}

for metric in ["total_events", "duplicates", "unordered_events", "duration"]:
    plt.figure(figsize=(10, 6))
    plt.title(metric)
    for name, df in dfs.items():
        plt.plot(df[metric], label=name)
    plt.legend()
    plt.xlabel("Index")
    plt.ylabel(metric)
    plt.grid(True)
    plt.show()
