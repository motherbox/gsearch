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
A layer on twitter API
"""

import json
import os
import os.path as op
from requests_oauthlib import OAuth1
from requests import session

TL_URL = "http://api.twitter.com/1.1/statuse/user_timeline.json",


def get_auth(configpath):
    configpath = op.join(os.getcwd(), configpath)
    with open(configpath, "r") as fin:
        data = json.load(fin)
    return OAuth1(data['api_key'], data['api_secret'], data['access_token'],
                  data['access_token_secret'])


def _add_param(url, param_name, param_value):
    basestr = "{}={}".format(param_name, param_value)
    if url.endswith("?"):
        return url + basestr
    elif url.endswith(".json"):
        return url + "?" + basestr
    else:
        return url + "&" + basestr


def get_tweets(user_id, auth, max_id=None, tweets=[], url=TL_URL):
    parameters = {
                    "user_id": user_id,
                    "count": 200,
                    "exclude_replies": "false",
                    "include_rts": "true"
                }
    if max_id is not None:
        parameters.update({'max_id': max_id})
    for param_name, param_value in parameters.iteritems():
        url += _add_param(url, param_name, param_value)


class TwitterTimeline(object):

    def __init__(self, user_id, configpath, parameters=None):
        self.auth = self._get_auth(configpath)
        self.session = session()
        self.session.auth = self.auth
        if parameters is None:
            parameters = {
                            "user_id": user_id,
                            "count": 200,
                            "exclude_replies": "false",
                            "include_rts": "true"
                        }
        self.parameters = parameters
        self.tweets = []
        self.request_count = 0

    def _update_url(self, url=TL_URL, max_id=None):
        if max_id is not None:
            self.paramters.update(dict(max_id=max_id))
        for param_name, param_value in self.parameters.iteritems():
            url = self._add_param(url, param_name, param_value)
        return url

    def request_tweets(self):
        url = self._update_url(max_id=self.tweets[-1]['id'])
        response = self.session.get(url)
        self.request_count += 1
        self.tweets.extend(response.json())

    def _get_auth(self, configpath):
        configpath = op.join(os.getcwd(), configpath)
        with open(configpath, "r") as fin:
            data = json.load(fin)
        return OAuth1(data['api_key'], data['api_secret'], data['access_token'],
                    data['access_token_secret'])

    def _add_param(self, url, param_name, param_value):
        basestr = "{}={}".format(param_name, param_value)
        if url.endswith("?"):
            return url + basestr
        elif url.endswith(".json"):
            return url + "?" + basestr
        else:
            return url + "&" + basestr
