#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from distutils import dir_util

from pytest import fixture
from stasher.stash import StashTabs


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
