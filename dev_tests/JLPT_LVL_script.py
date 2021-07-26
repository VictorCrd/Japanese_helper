import pandas as pd
from dev_tests.japanese_word_management import split_japanese

"""
Import csv
"""

df_core_Japanese_Vocabulary_N5 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N5.csv",
                                             usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])
df_core_Japanese_Vocabulary_N4 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N4.csv",
                                             usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])
df_core_Japanese_Vocabulary_N3 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N3.csv",
                                             usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])
df_core_Japanese_Vocabulary_N2 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N2.csv",
                                             usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])
df_core_Japanese_Vocabulary_N1 = pd.read_csv("JLPT_Voca_csv/Core_Japanese_Vocabulary_N1.csv",
                                             usecols=['Expression', 'Meaning', 'Reading', 'Additional_meaning'])

df_core_Japanese_Vocabulary = df_core_Japanese_Vocabulary_N5.append(df_core_Japanese_Vocabulary_N4)\
    .append(df_core_Japanese_Vocabulary_N3).append(df_core_Japanese_Vocabulary_N2).append(df_core_Japanese_Vocabulary_N1)

df_lemmas = pd.read_csv("JLPT_Voca_csv/japanese_lemmas.csv")


def get_jlpt_words(df_sentence, JLPT_LVL):
    df_core_Japanese_Vocabulary_N5["count"], df_core_Japanese_Vocabulary_N4["count"], df_core_Japanese_Vocabulary_N3["count"], \
    df_core_Japanese_Vocabulary_N2["count"], df_core_Japanese_Vocabulary_N1["count"] = 0, 0, 0, 0, 0

    df_list = [df_core_Japanese_Vocabulary_N1, df_core_Japanese_Vocabulary_N2, df_core_Japanese_Vocabulary_N3,
               df_core_Japanese_Vocabulary_N4, df_core_Japanese_Vocabulary_N5]
    df = df_sentence.merge(df_list[JLPT_LVL - 1], how='inner', left_on='vocab', right_on='Expression')

    df.rename(columns={'vocab': 'Vocab', 'count_x': 'Count'}, inplace=True)

    return df


#This function create a dataframe of all the words contained in the input, retrieve their lemmas rank and then sort them in descending order
def get_lemma(df_sentence):
    df_lemmas["count"] = 0

    df = df_sentence.merge(df_lemmas[["lemma", "rank"]], how='inner', left_on='vocab', right_on='lemma')[["vocab", "rank", "count"]].sort_values('rank').reset_index(drop=True)

    df.rename(columns={'vocab': 'Vocab'}, inplace=True)

    df = df.merge(df_core_Japanese_Vocabulary[["Expression","Meaning","Reading"]], how='inner', left_on='Vocab', right_on='Expression')[["Vocab", "count", "Meaning", "Reading", "rank"]]

    return df


def sum_words_in_text(df_words, df_subtitles, column_words):
    #global lemmas_sum
    df = df_words.copy()
    df['sum'] = 0
    for i in range(0, len(df_words)):
        df["sum"].loc[i] = df_subtitles['phrases'].str.count(df["Expression"][i]).sum()

    lemmas_sum = df["sum"].sum()

    return lemmas_sum


"""
This function calculates the percentage of words in the text belonging to a jlpt level
If sum() is used, a word is taken into account multiple time in the percentage
If count() is used, a word is taken into account only one time 
"""
def jlpt_lvl_core(text, cnt_sum=0):
    #global CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1
    CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1 = 0, 0, 0, 0, 0

    df_words = split_japanese(text)

    if cnt_sum == 0:
        CORE_N5 = get_jlpt_words(df_words, 5)['Count'].sum()
        CORE_N4 = get_jlpt_words(df_words, 4)['Count'].sum()
        CORE_N3 = get_jlpt_words(df_words, 3)['Count'].sum()
        CORE_N2 = get_jlpt_words(df_words, 2)['Count'].sum()
        CORE_N1 = get_jlpt_words(df_words, 1)['Count'].sum()

    if cnt_sum == 1:
        CORE_N5 = get_jlpt_words(df_words, 5)['Count'].count()
        CORE_N4 = get_jlpt_words(df_words, 4)['Count'].count()
        CORE_N3 = get_jlpt_words(df_words, 3)['Count'].count()
        CORE_N2 = get_jlpt_words(df_words, 2)['Count'].count()
        CORE_N1 = get_jlpt_words(df_words, 1)['Count'].count()

    CORE = CORE_N5 + CORE_N4 + CORE_N3 + CORE_N2 + CORE_N1

    return CORE_N5 / CORE, CORE_N4 / CORE, CORE_N3 / CORE, CORE_N2 / CORE, CORE_N1 / CORE


"""
TOP 10 words
"""
#global top_10
def get_top_10_words(df5, df4, df3, df2, df1):
    df_known_words = pd.read_csv("known_words/known_words.csv")
    top_10 = pd.concat([df5, df4, df3, df2, df1], ignore_index=True).sort_values('Count', ascending=False).reset_index(drop=True)
    top_10 = top_10[~top_10.Vocab.isin(df_known_words.Vocab)][0:10]
    top_10 = top_10.reset_index(drop=True)

    return top_10


def get_top_10_known_words(df5, df4, df3, df2, df1):
    df_content_words = pd.concat([df5, df4, df3, df2, df1], ignore_index=True).sort_values('Count', ascending=False).reset_index(drop=True)
    df_top_10_known_words = pd.read_csv("known_words/known_words.csv")
    df_top_10_known_words = df_content_words[df_content_words['Vocab'].isin(df_top_10_known_words['Vocab'])][0:10].dropna()

    return df_top_10_known_words