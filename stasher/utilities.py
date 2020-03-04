#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import itertools
from functools import cmp_to_key
from operator import itemgetter

from stasher.stash import Gear


# https://stackoverflow.com/questions/1143671/python-sorting-list-of-dictionaries-by-multiple-keys
def multikeysort(items, columns):
    def cmp(a, b):
        return (a > b) - (a < b)

    comparers = [
        ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1))
        for col in columns
    ]

    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))


class Utilities():
    '''Common utilities that might be useful.
    '''

    def find_all_unidentified(self, stashtabs):
        unidentified_items = []
        for i in stashtabs.items:
            if i.identified is False:
                unidentified_items.append(i)
        return unidentified_items

    def batch_chaos_sets(self, chaos_sets):
        '''Packs chaos sets into batches for vendoring.
        '''
        # The maximum number of sets that can fit into the inventory is 2.
        batches = []
        accounted_for = []

        # Iterate through every pair to see what we can get.
        pairs = itertools.combinations(chaos_sets, 2)
        for p1, p2 in pairs:
            # First check that both sets have not been accounted for.
            if p1 in accounted_for or p2 in accounted_for:
                continue

            # Construct the pseudo item set.
            itemset = p1 + p2

            # Check if the set is possible to pack into one inventory.
            result = self.pack_inventory(itemset)

            # If it is, add it to batches and add the sets to accounted for
            if result is not None:
                batches.append(result)
                accounted_for.append(p1)
                accounted_for.append(p2)

        # Finally, do single batches of the remaining.
        for i in chaos_sets:
            if i not in accounted_for:
                result = self.pack_inventory(i)
                # We should not fail here!
                accounted_for.append(i)
                batches.append(result)

        return batches

    def get_chaos_sets(self, stashtabs):
        '''Build a list of all sets of chaos recipe viable combinations.
        '''
        unidentified = self.find_all_unidentified(stashtabs)
        remaining = copy.deepcopy(unidentified)
        sets = []

        # Define the build_set function. This is non-functional, modifies list in place.
        def build_set(items):
            combination = {}
            for i in Gear.GEAR_SLOTS:
                combination[i] = None

            # Try to build the non-weapons first. Handle rings separately too.
            non_weapons = []
            for i in Gear.GEAR_SLOTS:
                if 'Wielded' not in i and 'Rings' not in i:
                    non_weapons.append(i)
            combination['Rings'] = []

            # We operate in reverse so that we can remove items easily.
            for item in reversed(items):
                # Check if it is a piece of gear, that is a non-weapon, and we are lacking it.
                if (isinstance(item, Gear) and item.gearslot in non_weapons
                        and combination[item.gearslot] is None):
                    combination[item.gearslot] = item
                    items.remove(item)
                # Check if it is a ring.
                if (isinstance(item, Gear) and item.gearslot == 'Rings' and
                        len(combination['Rings']) < 2):
                    combination['Rings'].append(item)
                    items.remove(item)

            # Check that all non weapon slots are filled. If not, then chaos recipe is fail.
            for i in non_weapons:
                if combination[i] is None:
                    return None
            # Check that rings are filled.
            if len(combination['Rings']) < 2:
                return None

            # Prepare the results
            result = []
            for i in non_weapons:
                result.append(combination[i])
            for i in combination['Rings']:
                result.append(i)

            # Otherwise, attempt to find two one-handed items (except quivers).
            one_handed_items = []
            for item in items:
                if (isinstance(item, Gear) and item.gearslot == 'WieldedOne' and item.lowerclass !=
                        'Quivers'):
                    one_handed_items.append(item)
                if len(one_handed_items) >= 2:
                    # We only need two.
                    break
            if len(one_handed_items) == 2:
                # We succeeded in completing the set. Remove them from the remaining list and return
                for i in one_handed_items:
                    items.remove(i)
                    result.append(i)
                return result

            # Otherwise, attempt to find one two-handed item.
            # We operate in reverse so that we can remove items easily.
            for item in reversed(items):
                # Check if it is a piece of gear and that is a two-handed-weapon
                if (isinstance(item, Gear) and item.gearslot == 'WieldedTwo'):
                    # We succeeded, remove item from list and return results.
                    items.remove(item)
                    result.append(item)
                    return result

            # We completely failed to make a set with not enough weapons, return None
            return None

        # Keep iterating through what's remaining to see if we can fulfil the criteria.
        while True:
            attempt = build_set(remaining)
            if attempt is None:
                # Cannot find any more sets, break
                break
            sets.append(attempt)

        return sets

    def pack_inventory(self, items):
        '''Given a list of Items, figure out if it is possible to pack them into the inventory.

        If it is possible, return the sequence of control clicks to get them into the inventory and
        the coordinate sequence to get them out.

        # Otherwise, return None
        '''

        # Inventory size is 12x5
        xcount = 12
        ycount = 5

        # Create the inventory matrix
        inventory_matrix = [[False] * ycount for i in range(xcount)]

        # Extract the important features from the item. (index, height, width)
        item_features = []
        for item in items:
            w = item.w
            h = item.h
            sq = w * h
            item_features.append({'item': item, 'w': w, 'h': h, 'sq': sq})

        # Sort the features from largest to smallest with sort order total_size, h, w
        features_sorted = multikeysort(item_features, ['-sq', '-h', '-w'])

        # Define all the helper fitting functions.
        def find_free_spot(matrix, startx, starty):
            for x in range(startx, xcount):
                for y in range(starty, ycount):
                    if matrix[x][y] is False:
                        return (x, y)
            # Unable to find a suitable spot, return None
            return None

        def is_spot_suitable(matrix, x, y, w, h):
            # Check that the entire area is free.
            for cw in range(w):
                for ch in range(h):
                    # Check out of bounds
                    if x + cw >= xcount or y + ch >= ycount:
                        return False
                    if matrix[x + cw][y + ch] is True:
                        return False
            return True

        def mark_spot(matrix, x, y, w, h):
            for cw in range(w):
                for ch in range(h):
                    matrix[x + cw][y + ch] = True

        def print_matrix(matrix):
            print(' '.join('-' * xcount))
            for y in range(ycount):
                for x in range(xcount):
                    print('1' if matrix[x][y] else '0', end=' ')  # NOQA
                print('')
            print(' '.join('-' * xcount))

        def fit(matrix, item):
            found_spot = None
            # Scan the inventory_matrix for a free spot from top to bottom, left to right
            current_x = 0
            current_y = 0
            while found_spot is None:
                # Try to get an empty spot.
                free_spot = find_free_spot(matrix, current_x, current_y)
                if free_spot is None:
                    # There are no suitable spots left, return our failure as None
                    return None
                # Check if free spot is suitable to fit our item.
                current_x, current_y = free_spot
                if is_spot_suitable(matrix, current_x, current_y, item['w'], item['h']):
                    # We have found our spot, mark it as taken and return the result.
                    mark_spot(matrix, current_x, current_y, item['w'], item['h'])
                    # ix and iy refers to the position in the inventory.
                    return {'item': item['item'], 'w': item['w'], 'h': item['h'], 'ix': current_x,
                            'iy': current_y, 'x': item['item'].x, 'y': item['item'].y}
                else:
                    # Otherwise, increment the counters.
                    current_y += 1
                    if current_y >= ycount:
                        current_y = 0
                        current_x += 1

        # Attempt to fit the items into the inventory_matrix
        unordered_sequence = []
        for item in features_sorted:
            result = fit(inventory_matrix, item)
            if result is None:
                return None
            unordered_sequence.append(result)

        # Order the sequence for control clicks.
        ordered_sequence = multikeysort(unordered_sequence, ['iy', 'ix'])
        return ordered_sequence
