#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from distutils import dir_util

from pytest import fixture
from stasher.stash import Gear, Map, StackableCurrency, StashTabs


"""This module provides the tests for the parser.
"""


@fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def test_stash_tab_39(datadir):
    """Tests that stash tab 39 (PremiumStash) can be properly parsed.
    """
    stash_tab_39_path = datadir.join('stash_tab_39.json')
    stash_tab_39_data = json.load(open(stash_tab_39_path, 'r'))
    stash_tabs = StashTabs(stash_tab_39_data, 39)

    # Check that the items exist.
    assert stash_tabs.items is not None

    # Test different items for parsing.
    # Testing Stackable Currency
    trans_orb = stash_tabs.items[0]
    assert isinstance(trans_orb, StackableCurrency)
    assert trans_orb.stacksize == 1
    assert trans_orb.maxstacksize == 40
    assert trans_orb.x == 1
    assert trans_orb.y == 9
    assert trans_orb.w == 1
    assert trans_orb.h == 1

    # Testing Maps
    shore_map = stash_tabs.items[1]
    assert isinstance(shore_map, Map)
    # TODO: Implement and test map parameters

    # Testing Prophecies
    # lightning_falls_prophecy = stash_tabs.items[3]
    # TODO: Implement this

    # Testing Scarabs
    # polished_elder_scarab = stash_tabs.items[4]
    # TODO: Implement this

    # Testing Rare Gear (Belts)
    viper_lock_belt = stash_tabs.items[9]
    assert isinstance(viper_lock_belt, Gear)
    assert viper_lock_belt.upperclass == 'Belts'
    assert viper_lock_belt.lowerclass == 'Belts'
    assert viper_lock_belt.gearslot == 'Waist'
    assert viper_lock_belt.ilvl == 81
    assert viper_lock_belt.identified is True
    assert viper_lock_belt.get_rarity() == 'Rare'
    assert viper_lock_belt.x == 4
    assert viper_lock_belt.y == 0
    assert viper_lock_belt.w == 2
    assert viper_lock_belt.h == 1

    # Testing Oils
    clear_oil = stash_tabs.items[10]
    assert isinstance(clear_oil, StackableCurrency)
    assert clear_oil.stacksize == 1
    assert clear_oil.maxstacksize == 10

    # Testing Flasks
    # hallowed_flask = stash_tabs.items[13]
    # TODO: implement this

    # Testing Normal Gear (Knife)
    slaughter_knife = stash_tabs.items[14]
    assert isinstance(slaughter_knife, Gear)
    assert slaughter_knife.upperclass == 'Weapons'
    assert slaughter_knife.lowerclass == 'OneHandWeapons'
    assert slaughter_knife.gearslot == 'WieldedOne'
    assert slaughter_knife.ilvl == 62
    assert slaughter_knife.identified is True
    assert slaughter_knife.get_rarity() == 'Normal'
    assert slaughter_knife.x == 3
    assert slaughter_knife.y == 0
    assert slaughter_knife.w == 1
    assert slaughter_knife.h == 3

    # Testing Jewels
    # eye_jewel = stash_tabs.items[16]
    # TODO: implement this


def test_stash_tab_40(datadir):
    """Tests that test quad stash tab 40 (QuadStash) can be properly parsed.
    """
    stash_tab_40_path = datadir.join('stash_tab_40.json')
    stash_tab_40_data = json.load(open(stash_tab_40_path, 'r'))
    stash_tabs = StashTabs(stash_tab_40_data, 40)

    # Check that the items exist.
    assert stash_tabs.items is not None

    # Testing Rare Gear (Stygian Vise)
    stygian_vise = stash_tabs.items[0]
    assert isinstance(stygian_vise, Gear)
    assert stygian_vise.upperclass == 'Belts'
    assert stygian_vise.lowerclass == 'Belts'
    assert stygian_vise.gearslot == 'Waist'
    assert stygian_vise.ilvl == 73
    assert stygian_vise.identified is True
    assert stygian_vise.get_rarity() == 'Rare'
    assert stygian_vise.x == 12
    assert stygian_vise.y == 0
    assert stygian_vise.w == 2
    assert stygian_vise.h == 1
    # TODO: Test the socketed item.


def test_mass_stash_tab(datadir):
    """Tests that all stash tab examples can be properly parsed as an overview.
    """
    example_files = ['stash_tab_40.json',
                     'stash_tab_5.json',
                     'stash_tab_4.json',
                     'dump_tab1.json',
                     'stash_tab_2.json',
                     'stash_tab_1.json',
                     'stash_tab_13.json',
                     'stash_tab_12.json',
                     'chaos_recipe_tab.json',
                     'dump_tab2.json',
                     'stash_tab_0.json',
                     'stash_tab_39.json',
                     'stash_tab_7.json',
                     'stash_tab_6.json']
    for example in example_files:
        stash_tab_path = datadir.join(example)
        stash_tab_data = json.load(open(stash_tab_path, 'r'))
        stash_tabs = StashTabs(stash_tab_data, 1)  # Dummy index.

        # Check that the items exist.
        assert stash_tabs.items is not None

        # Run all functions.
        for item in stash_tabs.items:
            rarity = item.get_rarity()
            assert rarity in [None, 'Normal', 'Magic', 'Rare', 'Unique']


def test_stash_tab_list_parsing(datadir):
    """Tests that the list of stash tabs can be parsed.
    """
    stash_tab_list_path = datadir.join('stash_tab_list.json')
    stash_tab_list_data = json.load(open(stash_tab_list_path, 'r'))
    stash_tabs = StashTabs(stash_tab_list_data)

    # Check the general stash tab responses.
    assert type(stash_tabs) == StashTabs
    assert stash_tabs.num_tabs == 41
    assert len(stash_tabs.tabs) == stash_tabs.num_tabs
    assert stash_tabs.items is None

    # Check tab index 0
    tab0 = stash_tabs.tabs[0]
    assert tab0.name == 'Cu'
    assert tab0.index == 0
    assert tab0.type == 'CurrencyStash'
    assert tab0.colour == (255, 213, 0)

    # Check tab index 4
    tab4 = stash_tabs.tabs[4]
    assert tab4.name == 'Ca'
    assert tab4.index == 4
    assert tab4.type == 'DivinationCardStash'
    assert tab4.colour == (221, 221, 221)

    # Check tab index 5
    tab5 = stash_tabs.tabs[5]
    assert tab5.name == 'Ma'
    assert tab5.index == 5
    assert tab5.type == 'MapStash'
    assert tab5.colour == (50, 50, 50)

    # Check tab index 6
    tab6 = stash_tabs.tabs[6]
    assert tab6.name == 'Un'
    assert tab6.index == 6
    assert tab6.type == 'UniqueStash'
    assert tab6.colour == (191, 94, 0)

    # Check tab index 7
    tab7 = stash_tabs.tabs[7]
    assert tab7.name == 'Es'
    assert tab7.index == 7
    assert tab7.type == 'EssenceStash'
    assert tab7.colour == (191, 0, 0)

    # Check tab index 12
    tab12 = stash_tabs.tabs[12]
    assert tab12.name == 'Fragments'
    assert tab12.index == 12
    assert tab12.type == 'FragmentStash'
    assert tab12.colour == (255, 128, 128)

    # Check tab index 13
    tab13 = stash_tabs.tabs[13]
    assert tab13.name == 'Delve'
    assert tab13.index == 13
    assert tab13.type == 'DelveStash'
    assert tab13.colour == (99, 128, 0)

    # Check tab index 39.
    tab39 = stash_tabs.tabs[39]
    assert tab39.name == 'Test Standard'
    assert tab39.index == 39
    assert tab39.type == 'PremiumStash'
    assert tab39.colour == (255, 213, 0)

    # Check tab index 40.
    tab40 = stash_tabs.tabs[40]
    assert tab40.name == 'Test Quad'
    assert tab40.index == 40
    assert tab40.type == 'QuadStash'
    assert tab40.colour == (221, 221, 221)
