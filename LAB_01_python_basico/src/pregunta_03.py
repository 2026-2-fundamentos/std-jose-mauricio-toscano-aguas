def pregunta_03():
    import gzip
    import os
    file_path = os.path.join(os.path.dirname(__file__), "../data/data.csv.gz")
    def read_data():
        with gzip.open(file_path, "rt") as f:
            return [line.strip().split('\t') for line in f if line.strip()]
    
    c = {}
    for row in read_data():
        c[row[0]] = c.get(row[0], 0) + int(row[1])
    return sorted(c.items())
