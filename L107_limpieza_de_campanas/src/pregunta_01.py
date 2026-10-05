import pandas as pd
import os
import glob

def clean_campaign_data():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "../data")
    submission_dir = os.path.join(base_dir, "../submission")
    os.makedirs(submission_dir, exist_ok=True)
    
    files = sorted(glob.glob(os.path.join(data_dir, "bank-marketing-campaing-*.csv.gz")))
    df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
    
    client = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
    client['job'] = client['job'].str.replace('.', '', regex=False).str.replace('-', '_', regex=False)
    client['education'] = client['education'].str.replace('.', '_', regex=False)
    client.loc[client['education'] == 'unknown', 'education'] = pd.NA
    client['credit_default'] = (client['credit_default'] == 'yes').astype(int)
    client['mortgage'] = (client['mortgage'] == 'yes').astype(int)
    client.to_csv(os.path.join(submission_dir, 'client.csv'), index=False)
    
    campaign = df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'month', 'day']].copy()
    campaign['previous_outcome'] = (campaign['previous_outcome'] == 'success').astype(int)
    campaign['campaign_outcome'] = (campaign['campaign_outcome'] == 'yes').astype(int)
    month_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
        'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    campaign['month'] = campaign['month'].map(lambda x: month_map.get(str(x).lower()[:3], x))
    campaign['day'] = campaign['day'].astype(str).str.zfill(2)
    campaign['last_contact_date'] = '2022-' + campaign['month'].astype(str) + '-' + campaign['day']
    campaign = campaign.drop(columns=['month', 'day'])
    campaign.to_csv(os.path.join(submission_dir, 'campaign.csv'), index=False)
    
    economics = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
    economics.to_csv(os.path.join(submission_dir, 'economics.csv'), index=False)
    
    return client, campaign, economics
