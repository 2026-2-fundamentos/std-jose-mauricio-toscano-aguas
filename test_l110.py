import pandas as pd

df = pd.read_csv('L110_rentabilidad_de_ventas/data/superstore_orders.csv.gz', sep=';', encoding='utf-8-sig')

df['is_loss'] = df['Profit'] < 0
df['lost_profit_val'] = df.apply(lambda row: -row['Profit'] if row['is_loss'] else 0, axis=1)

lines = len(df)
orders = df['Order ID'].nunique()
sales = df['Sales'].sum()
profit = df['Profit'].sum()
profit_margin = profit / sales
loss_lines = df['is_loss'].sum()
loss_line_rate = loss_lines / lines
lost_profit = df['lost_profit_val'].sum()

summary_1 = pd.DataFrame([{
    'lines': lines,
    'orders': orders,
    'sales': sales,
    'profit': profit,
    'profit_margin': profit_margin,
    'loss_lines': loss_lines,
    'loss_line_rate': loss_line_rate,
    'lost_profit': lost_profit
}])

def get_band(d):
    if d == 0: return '0%'
    elif 0 < d <= 0.05: return '1%-5%'
    elif 0.05 < d <= 0.10: return '6%-10%'
    else: return 'más de 10%' 

df['discount_band'] = df['Discount'].apply(get_band)
band_order = ['0%', '1%-5%', '6%-10%', 'más de 10%']

def agg_discount(g):
    lines = len(g)
    sales = g['Sales'].sum()
    profit = g['Profit'].sum()
    return pd.Series({
        'lines': lines,
        'sales': sales,
        'profit': profit,
        'profit_margin': profit / sales if sales else 0,
        'loss_line_rate': g['is_loss'].sum() / lines,
        'lost_profit': g['lost_profit_val'].sum()
    })

summary_2 = df.groupby('discount_band').apply(agg_discount, include_groups=False).reset_index()
summary_2['discount_band'] = pd.Categorical(summary_2['discount_band'], categories=band_order, ordered=True)
summary_2 = summary_2.sort_values('discount_band').reset_index(drop=True)

def agg_segment(g):
    lines = len(g)
    sales = g['Sales'].sum()
    profit = g['Profit'].sum()
    return pd.Series({
        'lines': lines,
        'sales': sales,
        'profit': profit,
        'profit_margin': profit / sales if sales else 0,
        'lost_profit': g['lost_profit_val'].sum()
    })

summary_3 = df.groupby(['Customer Segment', 'Product Category']).apply(agg_segment, include_groups=False).reset_index()
summary_3 = summary_3[summary_3['lines'] >= 100].sort_values('lost_profit', ascending=False).head(5).reset_index(drop=True)

print(summary_2['discount_band'].tolist())
