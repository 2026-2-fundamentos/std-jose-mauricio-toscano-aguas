def pregunta_01():
    import gzip
    import os
    file_path = os.path.join(os.path.dirname(__file__), "../data/data.csv.gz")
    def read_data():
        with gzip.open(file_path, "rt") as f:
            return [line.strip().split('\t') for line in f if line.strip()]
    
    return sum(int(row[1]) for row in read_data())
