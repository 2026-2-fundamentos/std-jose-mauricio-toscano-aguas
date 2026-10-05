def pregunta_12():
    import gzip
    import os
    file_path = os.path.join(os.path.dirname(__file__), "../data/data.csv.gz")
    def read_data():
        with gzip.open(file_path, "rt") as f:
            return [line.strip().split('\t') for line in f if line.strip()]
    
    d = {}
    for row in read_data():
        v = sum(int(pair.split(':')[1]) for pair in row[4].split(','))
        d[row[0]] = d.get(row[0], 0) + v
    return dict(sorted(d.items()))
