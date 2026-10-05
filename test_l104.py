import os
import pandas as pd
data_dir = "L104_ingestion_de_texto_en_directorios/data"
for split in ["train", "test"]:
    split_dir = os.path.join(data_dir, split)
    data = []
    for target in ["negative", "neutral", "positive"]:
        target_dir = os.path.join(split_dir, target)
        if not os.path.exists(target_dir):
            continue
        filenames = sorted(os.listdir(target_dir))
        for filename in filenames:
            if filename.endswith(".txt"):
                filepath = os.path.join(target_dir, filename)
                with open(filepath, "rt", encoding="utf-8") as f:
                    phrase = f.read().strip()
                    data.append({"phrase": phrase, "target": target})
    df = pd.DataFrame(data)
    print(split, len(df), df["phrase"].str.len().sum())
