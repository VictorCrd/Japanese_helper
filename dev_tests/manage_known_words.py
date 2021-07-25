import pandas as pd

df_known_words = pd.read_csv("known_words/known_words.csv")


def add_known_word(df, i):
    i = int(i)
    entry = df[i:i+1][['Vocab', 'Count', 'Meaning', 'Reading']].copy()
    #entry = df.iloc[i][['Vocab', 'Count', 'Meaning', 'Reading']]
    entry.to_csv('known_words/known_words.csv', mode='a', index=False, header=False)