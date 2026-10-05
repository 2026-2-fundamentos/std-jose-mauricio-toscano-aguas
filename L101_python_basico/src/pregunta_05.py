def pregunta_05():
    import gzip
    import os
    file_path = os.path.join(os.path.dirname(__file__), "../data/data.csv.gz")
    def read_data():
        with gzip.open(file_path, "rt") as f:
            return [line.strip().split('\t') for line in f if line.strip()]
    
    d = {}
    for row in read_data():
        v = int(row[1])
        if row[0] not in d: d[row[0]] = []
        d[row[0]].append(v)
    return [(k, max(v), min(v)) for k, v in sorted(d.items())]
