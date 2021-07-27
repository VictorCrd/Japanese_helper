import numpy as np
from jisho import Client
import pandas as pd
from janome.tokenizer import Tokenizer

"""try:
    # wakati = MeCab.Tagger('-d "{}"'.format(unidic.DICDIR))
    wakati = MeCab.Tagger('/unidic/unidic - lite - 1.0.8/unidic_lite/dicdir/mydic')
    print("ça fonctionne")
except:
    wakati = MeCab.Tagger('-r/dev/null -d /unidic/unidic - lite - 1.0.8/unidic_lite/dicdir/mydic')"""

list_drop = ['、', '。', 'の', 'て', 'に', 'と', 'は', 'ます', 'が', 'です', 'で', 'も', 'か', 'を', 'し', 'な', 'へ', 'み', '」', '「', 'た',
             'ん', 'ね', 'よ', 'だ']

list_drop_vocab = list_drop


def split_japanese(sentence):
    wakati = Tokenizer()
    #script = wakati.parse(sentence).split()
    script = [x.surface for x in wakati.tokenize(sentence)]
    df_script = pd.DataFrame({'vocab': script})
    df_script['count'] = 1
    df_script = df_script.groupby('vocab').sum().sort_values('count', ascending=False)
    for i in range(0, len(list_drop_vocab)):
        if list_drop_vocab[i] in df_script.index:
            df_script = df_script.drop(index=list_drop_vocab[i])

    # df_script = df_script.groupby('vocab').sum().sort_values('count', ascending = False).drop(index = list_drop)[0:10]
    df_script = df_script.reset_index()
    del wakati

    return df_script


"""
This function alow to request Jisho to get a traduction
Not used, too long to process and actual list of words have a traduction 
"""
def get_traduction_10_jp_words(sentence):
    wakati = Tokenizer()
    script = wakati.parse(sentence).split()
    df_script = pd.DataFrame({'vocab': script})
    df_script['count'] = 1
    df_script = df_script.groupby('vocab').sum().sort_values('count', ascending=False)
    for i in range(0, len(list_drop_vocab)):
        if list_drop_vocab[i] in df_script.index:
            df_script = df_script.drop(index=list_drop_vocab[i])

    # df_script = df_script.groupby('vocab').sum().sort_values('count', ascending = False).drop(index = list_drop)[0:10]
    df_script = df_script.reset_index()[0:10]

    df_script['trad'] = np.NaN
    df_script['reading'] = np.NaN
    client = Client()
    for i in range(0, len(df_script)):
        df_script['trad'].loc[i] = client.search(df_script['vocab'][i]).get("data")[0]['senses'][0][
            'english_definitions']
        df_script['reading'].loc[i] = client.search(df_script['vocab'][i]).get("data")[0]['japanese'][0]['reading']

    del wakati

    return df_script.to_html()