def pregunta_01():
    import pandas as pd
    import os
    import re
    file_path = os.path.join(os.path.dirname(__file__), "../data/clusters_report.txt")
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
            current_cluster = {
                'cluster': int(parts[0]),
                'cantidad_de_palabras_clave': int(parts[1]),
                'porcentaje_de_palabras_clave': float(parts[2].replace(',', '.').replace(' %', '')),
                'principales_palabras_clave': parts[3] if len(parts) > 3 else ""
            }
        elif line.strip():
            if current_cluster:
                current_cluster['principales_palabras_clave'] += ' ' + line.strip()
    if current_cluster:
        current_cluster['principales_palabras_clave'] = ' '.join(current_cluster['principales_palabras_clave'].split()).replace('.', '')
        data.append(current_cluster)
    return pd.DataFrame(data)
