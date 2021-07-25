#!/usr/bin/env python
# coding: utf-8

from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import MeCab

"""
Get subtitles (youtube)
https://pypi.org/project/youtube-transcript-api/#description
"""
wakati = MeCab.Tagger("-Owakati")


def get_yt_sub(youtube_id):
    st = YouTubeTranscriptApi.get_transcript(youtube_id, languages=['ja'])
    res = [sub['text'] for sub in st]
    start = [sub['start'] for sub in st]
    duration = [sub['duration'] for sub in st]
    df = pd.DataFrame({'phrases':res, 'duration':duration, 'start':start})
    df = df.replace('\n', ' ', regex=True)
    df = df.loc[~df['phrases'].str.contains('[音楽]')]

    return df