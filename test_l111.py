import pandas as pd

df = pd.read_csv('L111_demoras_ajustadas_por_horario/data/flights_by_carrier_day_hour.csv.gz')

hourly = df.groupby('scheduled_departure_hour').agg(
    operated_flights=('operated_flights', 'sum'),
    delayed_departure_15_flights=('delayed_departure_15_flights', 'sum')
).reset_index()
hourly['delay_rate'] = hourly['delayed_departure_15_flights'] / hourly['operated_flights']
hourly = hourly.sort_values('scheduled_departure_hour').reset_index(drop=True)

# Merge national rate to calculate expected
merged = df.merge(hourly[['scheduled_departure_hour', 'delay_rate']], on='scheduled_departure_hour', suffixes=('', '_nat'))
merged['expected'] = merged['operated_flights'] * merged['delay_rate']

carriers = merged.groupby('reporting_airline').agg(
    operated_flights=('operated_flights', 'sum'),
    delayed_departure_15_flights=('delayed_departure_15_flights', 'sum'),
    expected_delayed_flights=('expected', 'sum')
).reset_index()

carriers = carriers[carriers['operated_flights'] >= 100_000].copy()
carriers['delay_rate'] = carriers['delayed_departure_15_flights'] / carriers['operated_flights']
carriers['observed_to_expected_ratio'] = carriers['delayed_departure_15_flights'] / carriers['expected_delayed_flights']

carriers['crude_rank'] = carriers['delay_rate'].rank(ascending=False, method='min').astype(int)
carriers['adjusted_rank'] = carriers['observed_to_expected_ratio'].rank(ascending=False, method='min').astype(int)
carriers = carriers.sort_values('adjusted_rank').reset_index(drop=True)

carriers = carriers[['reporting_airline', 'operated_flights', 'delayed_departure_15_flights', 'delay_rate', 'expected_delayed_flights', 'observed_to_expected_ratio', 'crude_rank', 'adjusted_rank']]

print(hourly.head())
print(carriers.head())
