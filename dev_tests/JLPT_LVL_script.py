#!/usr/bin/env python
# coding: utf-8

# # Import


import pandas as pd
import numpy as np
import MeCab
from jisho import Client

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
    print(df_script)
    df_script['trad'] = np.NaN
    df_script['reading'] = np.NaN
    client = Client()
    for i in range(0, len(df_script)):
        df_script['trad'].loc[i] = client.search(df_script['vocab'][i]).get("data")[0]['senses'][0]['english_definitions']
        df_script['reading'].loc[i] = client.search(df_script['vocab'][i]).get("data")[0]['japanese'][0]['reading']
    
    return df_script.to_html()