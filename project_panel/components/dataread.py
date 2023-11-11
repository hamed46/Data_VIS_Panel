import pandas as pd


def read_csv(path):
    df = pd.read_csv(path)
    df.drop(['Unnamed: 0', 'track_id'], axis=1, inplace=True)
    df.drop_duplicates(subset=['track_name'], keep='first', inplace=True)
    return df
