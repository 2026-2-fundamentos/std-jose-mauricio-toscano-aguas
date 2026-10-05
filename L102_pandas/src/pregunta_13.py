def pregunta_13():
    import pandas as pd
    import os
    file_path_0 = os.path.join(os.path.dirname(__file__), "../data/tbl0.tsv")
    file_path_1 = os.path.join(os.path.dirname(__file__), "../data/tbl1.tsv")
    file_path_2 = os.path.join(os.path.dirname(__file__), "../data/tbl2.tsv")
    
    df0 = pd.read_csv(file_path_0, sep='\t')
    df2 = pd.read_csv(file_path_2, sep='\t')
    df = pd.merge(df0, df2, on='c0')
    return df.groupby('c1')['c5b'].sum()
