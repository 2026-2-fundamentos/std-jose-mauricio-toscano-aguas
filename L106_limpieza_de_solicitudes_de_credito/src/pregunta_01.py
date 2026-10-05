def pregunta_01():
    import pandas as pd
    import os
    import re
    
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "../data/solicitudes_de_credito.csv.gz")
    submission_dir = os.path.join(base_dir, "../submission")
    os.makedirs(submission_dir, exist_ok=True)
    out_path = os.path.join(submission_dir, "solicitudes_de_credito.csv")
    
    df = pd.read_csv(data_path, sep=';')
    
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    # We must ensure columns are exactly these 9 in this order
    cols_order = [
        "sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio",
        "estrato", "comuna_ciudadano", "fecha_de_beneficio",
        "monto_del_credito", "línea_credito"
    ]
    # Handle the fact that linea_credito might have encoding issues in the column name
    linea_col = [c for c in df.columns if 'credito' in c and 'monto' not in c][0]
    
    TEXT_COLUMNS = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        linea_col,
    ]
    
    cols_to_check = [c for c in df.columns if c != "comuna_ciudadano"]
    df = df.dropna(subset=cols_to_check)
    
    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.replace(r'[-_]', ' ', regex=True)
            df[col] = df[col].apply(lambda x: re.sub(r'\s+', ' ', x).strip())
            
    df['estrato'] = df['estrato'].astype(str).str.replace(r'\D', '', regex=True).astype(int)
    df['monto_del_credito'] = df['monto_del_credito'].astype(str).str.replace(r'\.00$', '', regex=True).str.replace(r'[^\d]', '', regex=True).astype(float).astype(int)
    
    def parse_dates(values):
        dates = pd.to_datetime(values, format="%d/%m/%Y", errors="coerce")
        for date_format in ["%Y-%m-%d", "%Y/%m/%d"]:
            dates = dates.fillna(
                pd.to_datetime(values, format=date_format, errors="coerce")
            )
        return dates
    
    df['fecha_de_beneficio'] = parse_dates(df['fecha_de_beneficio']).dt.strftime('%Y-%m-%d')
    df = df.drop_duplicates()
    
    # ensure column names are strictly as expected if encoding is weird
    df = df.rename(columns={linea_col: 'línea_credito'})
    
    df = df[cols_order]
    
    df.to_csv(out_path, sep=';', index=False)
