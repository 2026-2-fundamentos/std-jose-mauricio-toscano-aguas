import pandas as pd
import json

df = pd.read_csv("L108_k_anonimato_de_asegurados/data/insurance.csv.gz")

original_qis = ['age', 'sex', 'bmi', 'children', 'region']

original_counts = df.groupby(original_qis, dropna=False).size()
original_k = int(original_counts.min())
original_unique_records = int((original_counts == 1).sum())

df['age_group'] = pd.cut(df['age'], bins=[0, 29, 39, 49, 100], labels=["18-29", "30-39", "40-49", "50-64"])
df['bmi_group'] = pd.cut(df['bmi'], bins=[0, 18.5, 25, 30, float('inf')], right=False, labels=["bajo peso", "normal", "sobrepeso", "obesidad"])
df['children_group'] = df['children'].apply(lambda x: '0' if x == 0 else ('1-2' if x in [1, 2] else '3+'))

schemes = {
    "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
    "without_children": ["age_group", "sex", "bmi_group", "region"]
}

report_schemes = {}

for name, qis in schemes.items():
    counts = df.groupby(qis, dropna=False).size()
    eq_classes = int(len(counts[counts > 0]))
    k_before = int(counts[counts > 0].min())
    
    # suppressed records: less than 5
    suppressed_classes = counts[(counts > 0) & (counts < 5)]
    suppressed_records = int(suppressed_classes.sum())
    
    published_classes = counts[counts >= 5]
    published_records = int(published_classes.sum())
    
    # identify published records in df
    # create a mask
    # A faster way: merge or transform
    mask = df.groupby(qis)['smoker'].transform('count') >= 5
    pub_df = df[mask]
    
    # diversity check in pub_df
    # for each class, all smokers or no smokers? i.e. nunique() == 1
    diversity = pub_df.groupby(qis)['smoker'].nunique()
    # we only care about classes that exist
    diversity = diversity[diversity > 0]
    classes_no_div = int((diversity == 1).sum())
    
    # how many records?
    records_no_div = int(pub_df.groupby(qis)['smoker'].transform('nunique').eq(1).sum())
    
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

print(json.dumps(report_schemes, indent=2))
