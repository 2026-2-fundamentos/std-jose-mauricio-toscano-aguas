import pandas as pd
import json
import re

df = pd.read_csv("L105_validacion_de_datos/data/ventas.csv.gz", keep_default_na=False)

def clean_col(c):
    # BOM usually appears at the start of the first column
    c = c.replace('\ufeff', '').replace('\xef\xbb\xbf', '')
    c = c.strip().lower()
    c = re.sub(r'\s+', '_', c)
    return c

original_cols = df.columns.tolist()
cleaned_cols = [clean_col(c) for c in df.columns]
df.columns = cleaned_cols

required_cols = [
    'supplier_id', 'supplier', 'country', 'city', 'purchase_date', 
    'amount', 'discount', 'weight', 'units', 'unit_price', 'contact_email'
]

missing_required_columns = sorted([c for c in required_cols if c not in cleaned_cols])
unexpected_columns = sorted([c for c in cleaned_cols if c not in required_cols])

duplicate_row_count = int(df.duplicated().sum())

if 'supplier_id' in df.columns:
    duplicate_supplier_id_row_count = int(df.duplicated(subset=['supplier_id'], keep=False).sum())
else:
    duplicate_supplier_id_row_count = 0

missing_value_count_by_column = {}
for c in df.columns:
    # missing means empty string or "N/A"
    missing = df[c].astype(str).str.strip().isin(['', 'N/A']).sum()
    missing_value_count_by_column[c] = int(missing)

if 'contact_email' in df.columns:
    # invalid email: user@domain.extension
    # regex for invalid: not matching r'^[^@]+@[^@]+\.[^@]+$'
    def is_invalid(e):
        e = str(e).strip()
        if e in ['', 'N/A']: return False
        return not bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', e))
    invalid_email_count = sum(is_invalid(e) for e in df['contact_email'])
else:
    invalid_email_count = 0

if 'units' in df.columns:
    def is_invalid_unit(u):
        u = str(u).strip()
        if u in ['', 'N/A']: return False
        try:
            val = float(u)
            return val <= 0 or not val.is_integer()
        except:
            return True
    invalid_unit_count = sum(is_invalid_unit(u) for u in df['units'])
else:
    invalid_unit_count = 0

if 'country' in df.columns:
    # "country_values": lista ordenada de los valores distintos de `country`, escritos exactamente como aparecen en el archivo.
    country_values = sorted(df['country'].unique().tolist())
else:
    country_values = []

report = {
    "row_count": len(df),
    "column_count": len(df.columns),
    "missing_required_columns": missing_required_columns,
    "unexpected_columns": unexpected_columns,
    "duplicate_row_count": duplicate_row_count,
    "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
    "missing_value_count_by_column": missing_value_count_by_column,
    "invalid_email_count": invalid_email_count,
    "invalid_unit_count": invalid_unit_count,
    "country_values": country_values
}

print(json.dumps(report, indent=2))
