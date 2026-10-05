def pregunta_01():
    import pandas as pd
    import json
    import os
    
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "../data/insurance.csv.gz")
    submission_dir = os.path.join(base_dir, "../submission")
    os.makedirs(submission_dir, exist_ok=True)
    report_path = os.path.join(submission_dir, "privacy_report.json")
    out_csv = os.path.join(submission_dir, "insurance_published.csv")
    
    df = pd.read_csv(data_path)
    
    original_qis = ['age', 'sex', 'bmi', 'children', 'region']
    original_counts = df.groupby(original_qis, dropna=False, observed=True).size()
    original_k = int(original_counts[original_counts > 0].min())
    original_unique_records = int((original_counts == 1).sum())
    
    df['age_group'] = pd.cut(df['age'], bins=[0, 29, 39, 49, 100], labels=["18-29", "30-39", "40-49", "50-64"])
    df['bmi_group'] = pd.cut(df['bmi'], bins=[0, 18.5, 25, 30, float('inf')], right=False, labels=["bajo peso", "normal", "sobrepeso", "obesidad"])
    df['children_group'] = df['children'].apply(lambda x: '0' if x == 0 else ('1-2' if x in [1, 2] else '3+'))
    
    schemes_def = {
        "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
        "without_children": ["age_group", "sex", "bmi_group", "region"]
    }
    
    report_schemes = {}
    pub_dfs = {}
    
    for name, qis in schemes_def.items():
        counts = df.groupby(qis, dropna=False, observed=True).size()
        eq_classes = int(len(counts[counts > 0]))
        k_before = int(counts[counts > 0].min())
        
        suppressed_classes = counts[(counts > 0) & (counts < 5)]
        suppressed_records = int(suppressed_classes.sum())
        
        published_classes = counts[counts >= 5]
        published_records = int(published_classes.sum())
        
        mask = df.groupby(qis, observed=True)['smoker'].transform('count') >= 5
        pub_df = df[mask].copy()
        pub_dfs[name] = pub_df
        
        diversity = pub_df.groupby(qis, observed=True)['smoker'].nunique()
        diversity = diversity[diversity > 0]
        classes_no_div = int((diversity == 1).sum())
        
        records_no_div = int(pub_df.groupby(qis, observed=True)['smoker'].transform('nunique').eq(1).sum())
        
        report_schemes[name] = {
            "quasi_identifiers": qis,
            "equivalence_classes": eq_classes,
            "k_before_suppression": k_before,
            "suppressed_records": suppressed_records,
            "published_records": published_records,
            "published_classes": int(len(published_classes)),
            "classes_without_smoker_diversity": classes_no_div,
            "records_without_smoker_diversity": records_no_div,
        }
        
    selected_scheme = "without_children"
    
    mean_charges_original = float(df['charges'].mean())
    mean_charges_published = float(pub_dfs[selected_scheme]['charges'].mean())
    
    smoker_rate_original = float((df['smoker'] == 'yes').mean())
    smoker_rate_published = float((pub_dfs[selected_scheme]['smoker'] == 'yes').mean())
    
    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": report_schemes,
        "selected_scheme": selected_scheme,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published
    }
    
    with open(report_path, "wt", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    out_df = pub_dfs[selected_scheme][schemes_def[selected_scheme] + ['smoker', 'charges']]
    out_df.to_csv(out_csv, index=False)
    
    return report
