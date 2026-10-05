import os
import re
import pandas as pd
file_path = "L103_ingestion_de_texto_plano/data/clusters_report.txt"
with open(file_path, "rt", encoding="utf-8") as f:
    lines = f.readlines()
data = []
current_cluster = None
for line in lines[4:]:
    if re.match(r'^\s+\d+\s+', line):
        if current_cluster:
            current_cluster['principales_palabras_clave'] = ' '.join(current_cluster['principales_palabras_clave'].split()).replace('.', '')
            data.append(current_cluster)
        parts = re.split(r'\s{2,}', line.strip(), maxsplit=3)
        cluster = int(parts[0])
        cantidad = int(parts[1])
        porcentaje = float(parts[2].replace(',', '.').replace(' %', ''))
        palabras = parts[3] if len(parts) > 3 else ""
        current_cluster = {
            'cluster': cluster,
            'cantidad_de_palabras_clave': cantidad,
            'porcentaje_de_palabras_clave': porcentaje,
            'principales_palabras_clave': palabras
        }
    elif line.strip():
        if current_cluster:
            current_cluster['principales_palabras_clave'] += ' ' + line.strip()
if current_cluster:
    current_cluster['principales_palabras_clave'] = ' '.join(current_cluster['principales_palabras_clave'].split()).replace('.', '')
    data.append(current_cluster)
print(data[0]['principales_palabras_clave'])
