import pandas as pd
import re

df = pd.read_csv("L106_limpieza_de_solicitudes_de_credito/data/solicitudes_de_credito.csv.gz", sep=';')

if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

TEXT_COLUMNS = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "línea_credito",
]
linea_col = [c for c in df.columns if 'credito' in c and 'monto' not in c][0]
TEXT_COLUMNS[-1] = linea_col

cols_to_check = [c for c in df.columns if c != "comuna_ciudadano"]
df = df.dropna(subset=cols_to_check)

for col in TEXT_COLUMNS:
    if col in df.columns:
        df[col] = df[col].astype(str).str.lower().str.replace(r'[-_]', ' ', regex=True)
        df[col] = df[col].apply(lambda x: re.sub(r'\s+', ' ', x).strip())

df['estrato'] = df['estrato'].astype(str).str.replace(r'\D', '', regex=True).astype(int)

df['monto_del_credito'] = df['monto_del_credito'].astype(str).str.replace(r'\.00$', '', regex=True).str.replace(r'[^\d]', '', regex=True).astype(float).astype(int)

# parse dates
def parse_dates(values):
    dates = pd.to_datetime(values, format="%d/%m/%Y", errors="coerce")
    for date_format in ["%Y-%m-%d", "%Y/%m/%d"]:
        dates = dates.fillna(
            pd.to_datetime(values, format=date_format, errors="coerce")
        )
    return dates

df['fecha_de_beneficio'] = parse_dates(df['fecha_de_beneficio']).dt.strftime('%Y-%m-%d')
df = df.drop_duplicates()
print(df.head())
print(len(df))
