#!/usr/bin/env python
# coding: utf-8

# # Import


import pandas as pd
import numpy as np
import MeCab
from jisho import Client

global top_10
top_10 = pd.DataFrame()

wakati = MeCab.Tagger("-Owakati")

list_drop = ['、', '。', 'の', 'て', 'に', 'と', 'は', 'ます', 'が', 'です', 'で', 'も', 'か', 'を', 'し', 'な', 'へ', 'み', '」', '「', 'た', 'ん', 'ね', 'よ', 'だ']
known_vocab_drop = ['私', 'さん']
list_drop_vocab = list_drop + known_vocab_drop

def split_japanese(sentence):
    script = wakati.parse(sentence).split()
    df_script = pd.DataFrame({'vocab': script})
    df_script['count'] = 1
    df_script = df_script.groupby('vocab').sum().sort_values('count', ascending=False)
    for i in range(0, len(list_drop_vocab)):
        if list_drop_vocab[i] in df_script.index:
            df_script = df_script.drop(index=list_drop_vocab[i])

    # df_script = df_script.groupby('vocab').sum().sort_values('count', ascending = False).drop(index = list_drop)[0:10]
    df_script = df_script.reset_index()

    return df_script

"""
This function alow to request Jisho to get a traduction
"""
def get_traduction_10_jp_words(sentence):
    script = wakati.parse(sentence).split()
    df_script = pd.DataFrame({'vocab':script})
    df_script['count'] = 1
    df_script = df_script.groupby('vocab').sum().sort_values('count', ascending = False)
    for i in range(0, len(list_drop_vocab)):
        if list_drop_vocab[i] in df_script.index:
            df_script = df_script.drop(index = list_drop_vocab[i])
        
    #df_script = df_script.groupby('vocab').sum().sort_values('count', ascending = False).drop(index = list_drop)[0:10]
    df_script = df_script.reset_index()[0:10]

    df_script['trad'] = np.NaN
    df_script['reading'] = np.NaN
    client = Client()
    for i in range(0, len(df_script)):
        df_script['trad'].loc[i] = client.search(df_script['vocab'][i]).get("data")[0]['senses'][0]['english_definitions']
        df_script['reading'].loc[i] = client.search(df_script['vocab'][i]).get("data")[0]['japanese'][0]['reading']
    
    return df_script.to_html()


def get_top_10_words(df1, df2, df3, df4, df5):
    top_10 = pd.concat([df5, df4, df3, df2, df1], ignore_index=True).sort_values('Count', ascending=False).reset_index(drop=True)[0:10]

    return top_10