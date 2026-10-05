def pregunta_01():
    import pandas as pd
    import numpy as np
    import os
    
    base_dir = os.path.dirname(__file__)
    data_web = os.path.join(base_dir, "../data/historical_requests_web.csv.gz")
    data_let = os.path.join(base_dir, "../data/historical_requests_letter.csv.gz")
    submission_dir = os.path.join(base_dir, "../submission")
    os.makedirs(submission_dir, exist_ok=True)
    
    df_web = pd.read_csv(data_web).drop_duplicates()
    df_web['channel'] = 'web'
    
    df_let = pd.read_csv(data_let).drop_duplicates()
    df_let['channel'] = 'letter'
    
    df = pd.concat([df_web, df_let], ignore_index=True)
    
    
    
    df['in_date'] = pd.to_datetime(df['in_date']).dt.date
    df['out_date'] = pd.to_datetime(df['out_date']).dt.date
    
    mask = df['out_date'].notna()
    in_dt = df.loc[mask, 'in_date'].values.astype('datetime64[D]')
    out_dt = df.loc[mask, 'out_date'].values.astype('datetime64[D]')
    
    df.loc[mask, 'business_days'] = np.busday_count(
        in_dt + np.timedelta64(1, 'D'),
        out_dt + np.timedelta64(1, 'D')
    )
    df.loc[mask, 'calendar_days'] = (out_dt - in_dt).astype('timedelta64[D]').astype(float)
    
    df['answered'] = mask
    df['pending'] = ~mask
    df['on_time'] = mask & (df['business_days'] <= 15)
    
    channels = df.groupby('channel').agg(
        requests=('in_date', 'count'),
        answered=('answered', 'sum'),
        pending=('pending', 'sum'),
        median_business_days=('business_days', 'median'),
        on_time_rate=('on_time', 'mean')
    ).reset_index()
    
    df['year'] = pd.to_datetime(df['in_date']).dt.year
    yearly = df.groupby(['year', 'channel']).agg(
        requests=('in_date', 'count'),
        pending=('pending', 'sum'),
        on_time_rate=('on_time', 'mean')
    ).reset_index()
    
    days = df.groupby('day_name').agg(
        requests=('in_date', 'count'),
        median_calendar_days=('calendar_days', 'median'),
        median_business_days=('business_days', 'median')
    ).reset_index()
    
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days['day_name'] = pd.Categorical(days['day_name'], categories=day_order, ordered=True)
    days = days.sort_values('day_name').reset_index(drop=True)
    
    channels.to_csv(os.path.join(submission_dir, 'channel_summary.csv'), index=False)
    yearly.to_csv(os.path.join(submission_dir, 'yearly_summary.csv'), index=False)
    days.to_csv(os.path.join(submission_dir, 'entry_day_summary.csv'), index=False)
    
    return channels, yearly, days
