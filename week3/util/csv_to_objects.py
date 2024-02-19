import csv

def read_csv_to_objects(file_path, cls):
    objects = []
    with open(file_path, 'r', newline='\n') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # 헤더 스킵
        for row in csv_reader:
            obj = cls(*row)
            objects.append(obj)
    return objects