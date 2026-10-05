def pregunta_06():
    import gzip
    import os
    file_path = os.path.join(os.path.dirname(__file__), "../data/data.csv.gz")
    def read_data():
        with gzip.open(file_path, "rt") as f:
            return [line.strip().split('\t') for line in f if line.strip()]
    
    d = {}
    for row in read_data():
        for pair in row[4].split(','):
            k, v = pair.split(':')
            v = int(v)
            if k not in d: d[k] = []
            d[k].append(v)
    return [(k, min(v), max(v)) for k, v in sorted(d.items())]
