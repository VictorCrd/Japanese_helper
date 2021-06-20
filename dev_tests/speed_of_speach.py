def get_speed_of_speach(df):
    df['raw_real_duration'] = df['start'].shift(-1) - df['start']
    df = df.apply(lambda df: find_duration(df, 'duration', 'raw_real_duration', 'real_duration'), axis=1)
    df['nbr_characters'] = df.apply(lambda df: len(df['phrases']), axis=1)
    df['ratio_duration_characters'] = df.apply(lambda df: df['real_duration'] / df['nbr_characters'], axis=1)

    return round(df['ratio_duration_characters'].mean(), 2)


def find_duration(df, var1, var2, var3):
    if df[var1] > df[var2]:
        df[var3] = df[var2]
    else:
        df[var3] = df[var1]
    return df
