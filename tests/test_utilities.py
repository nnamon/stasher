#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from distutils import dir_util

from pytest import fixture
from stasher.stash import Gear, StashTabs
from stasher.utilities import Utilities


"""This module provides the tests for the utilities.
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


def test_unidentified(datadir):
    '''Tests that the find identified algorithm works.
    '''
    chaos_path = datadir.join('chaos_recipe_tab.json')
    chaos_data = json.load(open(chaos_path, 'r'))
    stash_tabs = StashTabs(chaos_data, 3)

    # Check that the items exist.
    assert stash_tabs.items is not None
    utils = Utilities()
    unidentified = utils.find_all_unidentified(stash_tabs)
    assert len(unidentified) == 127
    first_unidentified = unidentified[0]
    assert isinstance(first_unidentified, Gear)
    assert first_unidentified.typeline == 'Supreme Spiked Shield'


def test_chaos_recipe(datadir):
    '''Tests that the chaos recipe utility works.
    '''
    chaos_path = datadir.join('chaos_recipe_tab.json')
    chaos_data = json.load(open(chaos_path, 'r'))
    stash_tabs = StashTabs(chaos_data, 3)

    # Check that the items exist.
    assert stash_tabs.items is not None

    # Verify that at least one set of chaos recipe items exist.
    shield_one = stash_tabs.items[1]  # actually not required since the weapon used is a two hand.
    assert isinstance(shield_one, Gear)
    assert shield_one.identified is False
    assert shield_one.gearslot == 'WieldedOne'

    bodyarmour_one = stash_tabs.items[2]
    assert isinstance(bodyarmour_one, Gear)
    assert bodyarmour_one.identified is False
    assert bodyarmour_one.gearslot == 'Body'

    gloves_one = stash_tabs.items[3]
    assert isinstance(gloves_one, Gear)
    assert gloves_one.identified is False
    assert gloves_one.gearslot == 'Hands'

    helmet_one = stash_tabs.items[12]
    assert isinstance(helmet_one, Gear)
    assert helmet_one.identified is False
    assert helmet_one.gearslot == 'Head'

    boots_one = stash_tabs.items[13]
    assert isinstance(boots_one, Gear)
    assert boots_one.identified is False
    assert boots_one.gearslot == 'Feet'

    ring1_one = stash_tabs.items[20]
    assert isinstance(ring1_one, Gear)
    assert ring1_one.identified is False
    assert ring1_one.gearslot == 'Rings'

    weapon_one = stash_tabs.items[25]
    assert isinstance(weapon_one, Gear)
    assert weapon_one.identified is False
    assert weapon_one.gearslot == 'WieldedTwo'

    ring2_one = stash_tabs.items[36]
    assert isinstance(ring2_one, Gear)
    assert ring2_one.identified is False
    assert ring2_one.gearslot == 'Rings'

    amulet_one = stash_tabs.items[40]
    assert isinstance(amulet_one, Gear)
    assert amulet_one.identified is False
    assert amulet_one.gearslot == 'Amulet'

    belt_one = stash_tabs.items[71]
    assert isinstance(belt_one, Gear)
    assert belt_one.identified is False
    assert belt_one.gearslot == 'Waist'

    # Try to retrieve sets.
    utils = Utilities()
    sets = utils.get_chaos_sets(stash_tabs)
    assert sets is not None
    for i in sets:
        # Check that the sets contain either 9 or 10 items.
        assert len(i) == 9 or len(i) == 10
        # Check that the sets are all unidentified.
        for j in i:
            assert j.identified is False

    # Now that we know the sets are okay, test that we can batch them and get the packing orders.
    batches = utils.batch_chaos_sets(sets)
    assert len(batches) > 2  # The minimum number of batched is 3.


def test_pack_inventory_success(datadir):
    '''Tests that the inventory packing algorithm works on a suitable item packing.
    '''
    # Use the chaos recipe tab as an example.
    chaos_path = datadir.join('chaos_recipe_tab.json')
    chaos_data = json.load(open(chaos_path, 'r'))
    stash_tabs = StashTabs(chaos_data, 3)

    # Check that the items exist.
    assert stash_tabs.items is not None

    # Pick a few select items.
    shield_one = stash_tabs.items[1]
    bodyarmour_one = stash_tabs.items[2]
    gloves_one = stash_tabs.items[3]
    helmet_one = stash_tabs.items[12]
    boots_one = stash_tabs.items[13]
    ring1_one = stash_tabs.items[20]
    weapon_one = stash_tabs.items[25]
    ring2_one = stash_tabs.items[36]
    amulet_one = stash_tabs.items[40]
    belt_one = stash_tabs.items[71]

    # Pack the items.
    utils = Utilities()
    itemlist = [shield_one, bodyarmour_one, gloves_one, helmet_one, boots_one, ring1_one,
                weapon_one, ring2_one, amulet_one, belt_one]
    packed = utils.pack_inventory(itemlist)
    assert packed is not None
    assert len(packed) == len(itemlist)


def test_pack_inventory_failure(datadir):
    '''Tests that the inventory packing algorithm does not work when there are too many items.
    '''
    # Use the chaos recipe tab as an example.
    chaos_path = datadir.join('chaos_recipe_tab.json')
    chaos_data = json.load(open(chaos_path, 'r'))
    stash_tabs = StashTabs(chaos_data, 3)

    # Check that the items exist.
    assert stash_tabs.items is not None

    # Pick a few select items.
    shield_one = stash_tabs.items[1]
    bodyarmour_one = stash_tabs.items[2]
    gloves_one = stash_tabs.items[3]
    helmet_one = stash_tabs.items[12]
    boots_one = stash_tabs.items[13]
    ring1_one = stash_tabs.items[20]
    weapon_one = stash_tabs.items[25]
    ring2_one = stash_tabs.items[36]
    amulet_one = stash_tabs.items[40]
    belt_one = stash_tabs.items[71]

    # Pack the items.
    utils = Utilities()
    itemlist = [shield_one, bodyarmour_one, gloves_one, helmet_one, boots_one, ring1_one,
                weapon_one, ring2_one, amulet_one, belt_one]
    itemlist = itemlist * 3  # Triple it
    packed = utils.pack_inventory(itemlist)
    assert packed is None
