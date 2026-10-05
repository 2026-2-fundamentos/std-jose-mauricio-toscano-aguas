import pandas as pd

def build_cohort_analysis() -> pd.DataFrame:
    import os
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "../data/sales.csv.gz")
    submission_dir = os.path.join(base_dir, "../submission")
    os.makedirs(submission_dir, exist_ok=True)
    
    df = pd.read_csv(data_path)
    
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['order_month'] = df['OrderDate'].dt.to_period('M')
    
    df['cohort_month'] = df.groupby('CustomerID')['OrderDate'].transform('min').dt.to_period('M')
    
    df['period_index'] = (df['order_month'] - df['cohort_month']).apply(lambda x: x.n)
    
    cohort_data = df.groupby(['cohort_month', 'period_index'])['CustomerID'].nunique().reset_index()
    cohort_data.rename(columns={'CustomerID': 'active_customers'}, inplace=True)
    
    cohort_size = cohort_data[cohort_data['period_index'] == 0][['cohort_month', 'active_customers']].rename(columns={'active_customers': 'cohort_size'})
    
    cohort_data = cohort_data.merge(cohort_size, on='cohort_month')
    cohort_data['retention_rate'] = cohort_data['active_customers'] / cohort_data['cohort_size']
    
    cohort_data['cohort_month'] = cohort_data['cohort_month'].dt.strftime('%Y-%m')
    cohort_data = cohort_data.sort_values(['cohort_month', 'period_index']).reset_index(drop=True)
    
    cohort_data.to_csv(os.path.join(submission_dir, 'cohort_retention.csv'), index=False)
    
    cohort_pivot = cohort_data.pivot(index='cohort_month', columns='period_index', values='retention_rate')
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cohort_pivot, annot=True, fmt='.0%', cmap='Blues')
    plt.title('Cohort Retention Heatmap')
    plt.ylabel('Cohort Month')
    plt.xlabel('Period Index')
    plt.savefig(os.path.join(submission_dir, 'cohort_retention_heatmap.png'), bbox_inches='tight')
    plt.close()
    
    return cohort_data
