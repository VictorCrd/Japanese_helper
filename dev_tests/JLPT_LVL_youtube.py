#!/usr/bin/env python
# coding: utf-8

from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import numpy as np
import MeCab

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
    for i in range(0, len(df_words)):
        df_words["count"].loc[i] = len(df_subtitles[df_subtitles['phrases'].str.contains(df_words[column_words][i])])
        lemmas_sum = np.count_nonzero(df_words["count"])

    return lemmas_sum


def sum_words_in_text(df_words, df_subtitles, column_words):
    global lemmas_sum
    for i in range(0, len(df_words)):
        df_words["count"].loc[i] = len(df_subtitles[df_subtitles['phrases'].str.contains(df_words[column_words][i])])
        lemmas_sum = df_words["count"].sum()

    return lemmas_sum


def JLPT_lvl_core(df_subtitles, column_words, cnt_sum=0):
    global CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1
    Core_Japanese_Vocabulary_N5["count"], Core_Japanese_Vocabulary_N4["count"], Core_Japanese_Vocabulary_N3["count"], \
    Core_Japanese_Vocabulary_N2["count"], Core_Japanese_Vocabulary_N1["count"] = 0, 0, 0, 0, 0

    script = wakati.parse(df_subtitles).split()
    text_lenth = len(script)
    df_subtitles = [df_subtitles]
    df_subtitles = pd.DataFrame({'phrases':df_subtitles})

    if cnt_sum == 0:
        CORE_N5 = count_words_in_text(Core_Japanese_Vocabulary_N5, df_subtitles, column_words)
        CORE_N4 = count_words_in_text(Core_Japanese_Vocabulary_N4, df_subtitles, column_words)
        CORE_N3 = count_words_in_text(Core_Japanese_Vocabulary_N3, df_subtitles, column_words)
        CORE_N2 = count_words_in_text(Core_Japanese_Vocabulary_N2, df_subtitles, column_words)
        CORE_N1 = count_words_in_text(Core_Japanese_Vocabulary_N1, df_subtitles, column_words)

    if cnt_sum == 1:
        CORE_N5 = sum_words_in_text(Core_Japanese_Vocabulary_N5, df_subtitles, column_words)
        CORE_N4 = sum_words_in_text(Core_Japanese_Vocabulary_N4, df_subtitles, column_words)
        CORE_N3 = sum_words_in_text(Core_Japanese_Vocabulary_N3, df_subtitles, column_words)
        CORE_N2 = sum_words_in_text(Core_Japanese_Vocabulary_N2, df_subtitles, column_words)
        CORE_N1 = sum_words_in_text(Core_Japanese_Vocabulary_N1, df_subtitles, column_words)

    CORE = CORE_N5 + CORE_N4 + CORE_N3 + CORE_N2 + CORE_N1

    return CORE_N5/CORE, CORE_N4/CORE, CORE_N3/CORE, CORE_N2/CORE, CORE_N1/CORE