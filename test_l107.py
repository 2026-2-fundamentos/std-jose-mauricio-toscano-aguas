import os
import glob
import pandas as pd

data_dir = "L107_limpieza_de_campanas/data"
files = sorted(glob.glob(os.path.join(data_dir, "bank-marketing-campaing-*.csv.gz")))
df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

client = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
client['job'] = client['job'].str.replace('.', '').str.replace('-', '_')
client['education'] = client['education'].str.replace('.', '_')
client.loc[client['education'] == 'unknown', 'education'] = pd.NA
client['credit_default'] = (client['credit_default'] == 'yes').astype(int)
client['mortgage'] = (client['mortgage'] == 'yes').astype(int)

print(client["education"].isna().sum())

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

print(campaign['last_contact_date'].head())
