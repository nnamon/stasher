#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from .stash import StashTabs

HOST = 'https://pathofexile.com/'
REALM = 'pc'
LEAGUE = 'Metamorph'
STASH_ITEMS_PATH = 'character-window/get-stash-items'


class Account():

    def __init__(self, account_name, poe_sessionid, host=HOST, realm=REALM, league=LEAGUE):
        self.account_name = account_name
        self.poe_sessionid = poe_sessionid
        self.host = host
        self.realm = realm
        self.league = league

    def make_request(self, query):
        cookies = {'POESESSID': self.poe_sessionid}
        path = '{}/{}'.format(self.host, STASH_ITEMS_PATH)
        struct = requests.get(path, params=query, cookies=cookies).json()
        return struct

    def get_tabs_list(self):
        parameters = {'accountName': self.account_name, 'realm': self.realm, 'league': self.league,
                      'tabs': '1'}
        struct = self.make_request(parameters)
        return StashTabs(struct)

    def get_tab(self, index):
        parameters = {'accountName': self.account_name, 'realm': self.realm, 'league': self.league,
                      'tabs': '1', 'tabIndex': str(index)}
        struct = self.make_request(parameters)
        return StashTabs(struct, index)
