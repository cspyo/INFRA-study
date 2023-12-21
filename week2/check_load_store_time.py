import timeit
import shutil
import pandas as pd
import boto3

class Store_load_system:
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path

    def store_file(self):
        shutil.copy(self.src_path, self.dest_path)

    def load_file(self):
        with open(self.dest_path, 'r') as file:
            file.read()

class EBS(Store_load_system):
    def __init__(self, src_path, dest_path):
        super().__init__(src_path, dest_path)

class EFS(Store_load_system):
    def __init__(self, src_path, dest_path):
        super().__init__(src_path, dest_path)

class S3(Store_load_system):
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'hasan-assignment'
        self.file_name = './submission.csv'
        self.object_name = 'submission.csv'
    
    def store_file(self):
        if self.object_name is None:
            self.object_name = self.file_name
        self.s3_client.upload_file(self.file_name, self.bucket_name, self.object_name)

    def load_file(self):
        self.s3_client.download_file(self.bucket_name, self.object_name, self.file_name)

def make_store_load_time_results(storage):
    results = []
    for trial in range(1, 101):
        store_time = timeit.timeit(lambda: storage.store_file(), number=1)
        load_time = timeit.timeit(lambda: storage.load_file(), number=1)
        results.append([type(storage).__name__, trial, store_time, load_time])
    return results

def print_average_results(results):
    df = pd.DataFrame(results, columns=['name', 'try', 'store_time', 'load_time'])
    average_store_time = df['store_time'].mean()
    average_load_time = df['load_time'].mean()
    print(f"Average Store Time: {average_store_time}")
    print(f"Average Load Time: {average_load_time}")

def make_results_to_csv(results, storage_name):
    df = pd.DataFrame(results, columns=['name', 'try', 'store_time', 'load_time'])
    df.to_csv(f'./{storage_name}_performance.csv', index=False)


def main():
    storages = []
    src_path = '/home/ubuntu/submission.csv'

    ebs_dest_path = '/ebs-mount/submission.csv'
    storages.append(EBS(src_path, ebs_dest_path))

    efs_dest_path = '/efs-mount/submission.csv'
    storages.append(EFS(src_path, efs_dest_path))

    storages.append(S3())

    for storage in storages:
        print("Storage: ", type(storage).__name__)
        results = make_store_load_time_results(storage)
        print_average_results(results)
        make_results_to_csv(results, type(storage).__name__)

if __name__ == "__main__":
    main()