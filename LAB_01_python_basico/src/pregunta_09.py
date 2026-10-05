def pregunta_09():
    import gzip
    import os
    file_path = os.path.join(os.path.dirname(__file__), "../data/data.csv.gz")
    def read_data():
        with gzip.open(file_path, "rt") as f:
            return [line.strip().split('\t') for line in f if line.strip()]
    
    from collections import Counter
    c = Counter()
    for row in read_data():
        for pair in row[4].split(','):
            c[pair.split(':')[0]] += 1
    return dict(sorted(c.items()))
