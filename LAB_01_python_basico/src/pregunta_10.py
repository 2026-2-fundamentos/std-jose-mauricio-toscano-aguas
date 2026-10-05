def pregunta_10():
    import gzip
    import os
    file_path = os.path.join(os.path.dirname(__file__), "../data/data.csv.gz")
    def read_data():
        with gzip.open(file_path, "rt") as f:
            return [line.strip().split('\t') for line in f if line.strip()]
    
    return [(row[0], len(row[3].split(',')), len(row[4].split(','))) for row in read_data()]
