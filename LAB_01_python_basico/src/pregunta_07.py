def pregunta_07():
    import gzip
    import os
    file_path = os.path.join(os.path.dirname(__file__), "../data/data.csv.gz")
    def read_data():
        with gzip.open(file_path, "rt") as f:
            return [line.strip().split('\t') for line in f if line.strip()]
    
    d = {}
    for row in read_data():
        v = int(row[1])
        if v not in d: d[v] = []
        d[v].append(row[0])
    return sorted(d.items())
