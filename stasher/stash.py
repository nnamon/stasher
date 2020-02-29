#!/usr/bin/env python
# -*- coding: utf-8 -*-


class StashTabs():

    def __init__(self, struct, current_tab=None):
        # Get the number of tabs.
        self.num_tabs = struct['numTabs']

        # Process all the tabs in sequence.
        self.tabs = []
        for tab in struct['tabs']:
            self.tabs.append(Tab(tab))

        # Check if there is a current tab that items are drawn from.
        self.current_tab = current_tab
        self.items = None
        if current_tab and 'items' in struct:
            self.items = []
            for item in struct['items']:
                self.items.append(Item.parse(item))


class Tab():

    def __init__(self, struct):
        self.name = struct['n']
        self.index = struct['i']
        self.id = struct['id']
        self.type = struct['type']
        self.colour = (struct['colour']['r'], struct['colour']['g'], struct['colour']['b'])
        self.hidden = struct['hidden']
        self.selected = struct['selected']
        self.srcL = struct['srcL']
        self.srcC = struct['srcC']
        self.srcR = struct['srcR']


class Item():

    FRAMETYPES = {
        'Normal': 0,
        'Magic': 1,
        'Rare': 2,
        'Unique': 3,
        'Gem': 4,
        'Currency': 5,
        'DivinationCard': 6,
        'Quest': 7,
        'Prophecy': 8,
        'Relic': 9
    }

    @staticmethod
    def parse(struct):
        # Identify the generic type of the item
        return Item(struct)

    def __init__(self, struct):
        # Universal Attributes
        self.frametype = struct['frameType']
        self.x = struct['x']
        self.y = struct['y']
        self.w = struct['w']
        self.h = struct['h']
        self.icon = struct['icon']
        self.league = struct['league']
        self.id = struct['id']
        self.identified = struct['identified']
        self.name = struct['name']
        self.typeline = struct['typeLine']
        self.verified = struct['verified']


class Map(Item):

    def __init__(self, struct):
        super().__init__(self, struct)


class Gem(Item):

    def __init__(self, struct):
        super().__init__(self, struct)
