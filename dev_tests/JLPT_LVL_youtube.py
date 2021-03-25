#!/usr/bin/env python
# coding: utf-8

from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import numpy as np
import MeCab

from dev_tests.JLPT_LVL_script import split_japanese

"""
Get subtitles (youtube)
https://pypi.org/project/youtube-transcript-api/#description
"""
wakati = MeCab.Tagger("-Owakati")


def get_yt_sub(youtube_id):
    st = YouTubeTranscriptApi.get_transcript(youtube_id, languages=['ja'])
    res = [sub['text'] for sub in st]
    df = pd.DataFrame({'phrases': res})
    df = df.replace('\n', ' ', regex=True)

    return df


"""
Import csv
"""

Core_Japanese_Vocabulary_N5 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N5.csv",
                                          usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])
Core_Japanese_Vocabulary_N4 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N4.csv",
                                          usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])
Core_Japanese_Vocabulary_N3 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N3.csv",
                                          usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])
Core_Japanese_Vocabulary_N2 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N2.csv",
                                          usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])
Core_Japanese_Vocabulary_N1 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N1.csv",
                                          usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])

Core_Japanese_Vocabulary_N5["count"] = 0
Core_Japanese_Vocabulary_N4["count"] = 0
Core_Japanese_Vocabulary_N3["count"] = 0
Core_Japanese_Vocabulary_N2["count"] = 0
Core_Japanese_Vocabulary_N1["count"] = 0


# Find nbr of NLPT word by level

def count_words_in_text(df_words, df_subtitles, column_words):
    global lemmas_sum
    df = df_words.copy()
    df['count'] = 0
    for i in range(0, len(df)):
        df["count"].loc[i] = len(df_subtitles[df_subtitles['phrases'].str.contains(df[column_words][i])])

    lemmas_sum = np.count_nonzero(df["count"])

    return lemmas_sum


def get_JLPT_words(df_sentence, JLPT_LVL):
    df_list = [Core_Japanese_Vocabulary_N1, Core_Japanese_Vocabulary_N2, Core_Japanese_Vocabulary_N3,
               Core_Japanese_Vocabulary_N4, Core_Japanese_Vocabulary_N5]
    df = df_sentence.merge(df_list[JLPT_LVL - 1], how='inner', left_on='vocab', right_on='Expression')

    return df



def sum_words_in_text(df_words, df_subtitles, column_words):
    global lemmas_sum
    df = df_words.copy()
    df['sum'] = 0
    for i in range(0, len(df_words)):
        df["sum"].loc[i] = df_subtitles['phrases'].str.count(df["Expression"][i]).sum()

    lemmas_sum = df["sum"].sum()

    return lemmas_sum


def JLPT_lvl_core(text, cnt_sum=0):
    global CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1
    CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1 = 0, 0, 0, 0, 0

    df_words = split_japanese(text)

    if cnt_sum == 0:
        CORE_N5 = get_JLPT_words(df_words, 5)['count_x'].sum()
        CORE_N4 = get_JLPT_words(df_words, 4)['count_x'].sum()
        CORE_N3 = get_JLPT_words(df_words, 3)['count_x'].sum()
        CORE_N2 = get_JLPT_words(df_words, 2)['count_x'].sum()
        CORE_N1 = get_JLPT_words(df_words, 1)['count_x'].sum()

    if cnt_sum == 1:
        CORE_N5 = get_JLPT_words(df_words, 5)['count_x'].count()
        CORE_N4 = get_JLPT_words(df_words, 4)['count_x'].count()
        CORE_N3 = get_JLPT_words(df_words, 3)['count_x'].count()
        CORE_N2 = get_JLPT_words(df_words, 2)['count_x'].count()
        CORE_N1 = get_JLPT_words(df_words, 1)['count_x'].count()

    CORE = CORE_N5 + CORE_N4 + CORE_N3 + CORE_N2 + CORE_N1

    return CORE_N5 / CORE, CORE_N4 / CORE, CORE_N3 / CORE, CORE_N2 / CORE, CORE_N1 / CORE