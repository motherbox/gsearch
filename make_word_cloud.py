#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Cube26 product code
#
# (C) Copyright 2015 Cube26 Software Pvt Ltd
# All right reserved.
#
# This file is confidential and NOT open source.  Do not distribute.
#

"""
Make a word cloud from Google search history.
"""

import os.path as op
import os
from wordcloud import WordCloud
import pandas as pd
import json
import sys


def json2tsv(dirpath):
    dirpath = op.join(os.getcwd(), dirpath, "Searches")
    quarterly_files = os.listdir(dirpath)
    q_events = []
    for filename in quarterly_files:
        filepath = op.join(dirpath, filename)
        with open(filepath, "r") as fin:
            data = json.load(fin)
        q_events.extend([x['query'] for x in data['event']])
    queries = []
    for event in q_events:
        for ix in event['id']:
            queries.append((ix['timestamp_usec'], event['query_text']))
    df = pd.DataFrame(queries, columns="timestamp query_string".split())
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit="us")
    df.to_csv("gsearch.tsv", sep="\t", index=False, encoding='utf8')


def make_wc(dirpath):
    dirpath = op.join(os.getcwd(), dirpath, "Searches")
    quarterly_files = os.listdir(dirpath)
    words = []
    for filename in quarterly_files:
        filepath = op.join(dirpath, filename)
        with open(filepath, "r") as fin:
            data = json.load(fin)
        for query_event in data['event']:
            _words = query_event['query']['query_text'].split()
            words.extend(_words)
    wc = WordCloud()
    wc.generate(" ".join(words))
    wc.to_file('cloud.png')

if __name__ == '__main__':
    json2tsv(sys.argv[1])
