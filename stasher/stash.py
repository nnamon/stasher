#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json


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
        # Identify the type of the item
        if struct['frameType'] == Item.FRAMETYPES['Currency']:
            # Only checking for stackable currency at the moment.
            # TODO: Scarabs and such
            return StackableCurrency(struct)
        elif struct['frameType'] == Item.FRAMETYPES['Gem']:
            return Gem(struct)
        elif Map.is_map(struct):
            return Map(struct)
        elif Gear.is_gear(struct):
            return Gear(struct)

        # Otherwise default back to just the generic item type.
        return Item(struct)

    @staticmethod
    def struct_has_property(struct, prop):
        if 'properties' not in struct:
            return False
        for i in struct['properties']:
            if prop == i['name']:
                return True
        return False

    @staticmethod
    def parse_icon_link(uri):
        stripped = uri[:uri.index('?')] if '?' in uri else uri
        tokens = stripped.split('/')
        if '/gen/' in uri:
            # Need to extract base64 and then json
            encoded = tokens[5] + '==='
            decoded = json.loads(base64.b64decode(encoded))
            classpath = decoded[2]['f']
            return classpath.split('/')[2:] + tokens[-1:]
        else:
            return tokens[6:]

    def get_rarity(self):
        if self.frametype == self.FRAMETYPES['Normal']:
            return 'Normal'
        elif self.frametype == self.FRAMETYPES['Magic']:
            return 'Magic'
        elif self.frametype == self.FRAMETYPES['Rare']:
            return 'Rare'
        elif self.frametype == self.FRAMETYPES['Unique']:
            return 'Unique'
        else:
            return None

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
        self.ilvl = struct['ilvl']
        self.parsed_icon_classes = self.parse_icon_link(self.icon)

        # Detect if corrupted.
        self.corrupted = False
        if 'corrupted' in struct:
            self.corrupted = struct['corrupted']

        self.struct = struct  # Save the struct just in case we want to debug.


class Map(Item):

    @staticmethod
    def is_map(struct):
        return Map.struct_has_property(struct, 'Map Tier')

    def __init__(self, struct):
        super().__init__(struct)


class Currency(Item):

    def __init__(self, struct):
        super().__init__(struct)

        # Currencies have type lines.
        self.typeline = struct['typeLine']


class StackableCurrency(Currency):

    def __init__(self, struct):
        super().__init__(struct)

        # Stackable currencies have stack sizes.
        self.stacksize = struct['stackSize']
        self.maxstacksize = struct['maxStackSize']

        # TODO: explicitMods, descrText


class Gem(Item):

    def __init__(self, struct):
        super().__init__(struct)


class Gear(Item):

    GEAR_CLASSES = ['Armours', 'Weapons', 'Amulets', 'Rings', 'Belts', 'Quivers']
    GEAR_SUBCLASSES = {
        'Armours': ['Gloves', 'Shields', 'BodyArmours', 'Boots', 'Helmets'],
        'Weapons': ['OneHandWeapons', 'TwoHandWeapons'],
        'Rings': None,
        'Belts': None,
        'Amulets': None,
        'Quivers': None,
    }
    GEAR_SLOTS = {
        'Head': ['Helmets'],
        'Body': ['BodyArmours'],
        'Hands': ['Gloves'],
        'Feet': ['Boots'],
        'Rings': ['Rings'],
        'Amulet': ['Amulets'],
        'Waist': ['Belts'],
        'WieldedOne': ['OneHandWeapons', 'Shields', 'Quivers'],
        'WieldedTwo': ['TwoHandWeapons']
    }

    @staticmethod
    def is_gear(struct):
        # Easy work around for now is to just parse the icon for classes.
        icon_tokens = Gear.parse_icon_link(struct['icon'])
        class_type = icon_tokens[0]
        return class_type in Gear.GEAR_CLASSES

    def __init__(self, struct):
        super().__init__(struct)

        # Gear has type lines
        self.typeline = struct['typeLine']

        # Categorise the gear.
        icon_tokens = self.parsed_icon_classes
        self.upperclass = icon_tokens[0]
        if self.GEAR_SUBCLASSES[self.upperclass] is None:
            self.lowerclass = self.upperclass
        else:
            self.lowerclass = icon_tokens[1]
        gear_slot_map = {}
        for slot in self.GEAR_SLOTS:
            for classtype in self.GEAR_SLOTS[slot]:
                gear_slot_map[classtype] = slot
        self.gearslot = gear_slot_map[self.lowerclass]

        # TODO: All the other possible attributes...
        # TODO: Handle socketed items (e.g. test tab 40, index 0)
        # TODO: Handle influenced items (e.g. test tab 40, index 1)

    def __repr__(self):
        return '<{} ({}/{}:{})>'.format(self. typeline, self.upperclass, self.lowerclass,
                                        self.gearslot)
