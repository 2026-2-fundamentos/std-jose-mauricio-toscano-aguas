import os
import glob

queries = {
    1: "SELECT SUM(c12) FROM tbl1;",
    2: "SELECT COUNT(*) FROM tbl1;",
    3: "SELECT * FROM tbl1 ORDER BY c14 ASC LIMIT 5;",
    4: "SELECT K0, c16 FROM tbl1 WHERE SUBSTR(c16, 1, 1) = K0;",
    5: "SELECT * FROM tbl0 WHERE c02 IN (100, 600);",
    6: "SELECT * FROM tbl1 WHERE K0 = 'A' ORDER BY c14 ASC;",
    7: "SELECT * FROM tbl1 WHERE K0 NOT IN ('A', 'B') AND c13 NOT IN (200, 900) ORDER BY c14 ASC;",
    8: "SELECT CAST(strftime('%Y', c23) AS INTEGER) AS YEAR, AVG(c21) FROM tbl2 GROUP BY YEAR;",
    9: "SELECT * FROM tbl2 ORDER BY c21 ASC LIMIT 1;",
    10: "SELECT * FROM tbl0 WHERE c02 >= 300;",
    11: "SELECT CAST(strftime('%Y', c14) AS INTEGER) AS YEAR, COUNT(*) FROM tbl1 WHERE strftime('%Y', c14) = '2018' GROUP BY YEAR;",
    12: "SELECT K0, MAX(c12), MIN(c12) FROM tbl1 GROUP BY K0;",
    13: "SELECT K0, AVG(c12) FROM tbl1 WHERE c13 > 400 GROUP BY K0;",
    14: "SELECT tbl1.K0, AVG(tbl2.c21) FROM tbl1 JOIN tbl2 ON tbl1.K1 = tbl2.K1 WHERE tbl1.c13 > 400 GROUP BY tbl1.K0;"
}

base_dir = "L109_sql_con_sqlite3/src"

for i, query in queries.items():
    path = os.path.join(base_dir, f"pregunta_{i:02d}.sql")
    with open(path, "rt", encoding="utf-8") as f:
        content = f.read()
    
    # find "--  Escriba su consulta debajo de esta lA-nea." or similar
    sep = "--  Escriba su consulta debajo de esta lA-nea."
    if sep not in content:
        sep = "--  Escriba su consulta debajo de esta l"
        
    parts = content.split("--  Escriba su consulta debajo de esta")
    if len(parts) > 1:
        prefix = parts[0] + "--  Escriba su consulta debajo de esta" + parts[1].split("\n")[0] + "\n\n"
        with open(path, "wt", encoding="utf-8") as f:
            f.write(prefix + query + "\n")
