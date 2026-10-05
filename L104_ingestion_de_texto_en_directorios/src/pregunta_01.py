def pregunta_01():
    import os
    import pandas as pd
    
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "../data")
    submission_dir = os.path.join(base_dir, "../submission")
    os.makedirs(submission_dir, exist_ok=True)
    
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
        df.to_csv(os.path.join(submission_dir, f"{split}_dataset.csv"), index=False)
