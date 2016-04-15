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
    return df


def make_wc(dirpath):
    dirpath = op.join(os.getcwd(), dirpath, "Searches")
    df = json2tsv(dirpath)
    wc = WordCloud()
    wc.generate(" ".join(df['query_string']))
    wc.to_file('cloud.png')


def temporal_wc(df, tmin, tmax):
    text = df.ix[tmin:tmax]['query_string']
    wc = WordCloud()
    wc.generate(" ".join(text))
    wc.to_image().show()


def write_temporal_wc(df, freq="M", outdir="temporal_wcs", outfile_fmt="%Y-%m"):
    df = df.astype(str)
    if not op.exists(outdir):
        os.mkdir(outdir)
    df = df.resample(freq, "sum")
    df = df[df != 0]
    wc = WordCloud()
    for ts, text in df.iteritems():
        wc.generate(text)
        outpath = op.join(outdir, ts.strftime(outfile_fmt) + ".png")
        wc.to_file(outpath)


if __name__ == '__main__':
    make_wc(sys.argv[1])
