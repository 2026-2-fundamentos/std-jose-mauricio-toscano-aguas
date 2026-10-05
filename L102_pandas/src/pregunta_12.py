def pregunta_12():
    import pandas as pd
    import os
    file_path_0 = os.path.join(os.path.dirname(__file__), "../data/tbl0.tsv")
    file_path_1 = os.path.join(os.path.dirname(__file__), "../data/tbl1.tsv")
    file_path_2 = os.path.join(os.path.dirname(__file__), "../data/tbl2.tsv")
    
    df = pd.read_csv(file_path_2, sep='\t')
    df['c5'] = df['c5a'] + ':' + df['c5b'].astype(str)
    return df.groupby('c0')['c5'].apply(lambda x: ','.join(sorted(x))).reset_index()
