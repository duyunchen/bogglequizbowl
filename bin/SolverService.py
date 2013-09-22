#!/usr/bin/env python

#  This file is part of Boggle Quiz Bowl.
# 
#     Boggle Quiz Bowl is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Boggle Quiz Bowl is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Boggle Quiz Bowl.  If not, see <http://www.gnu.org/licenses/>.

from Solution import Solution
import FileService
import MathService
import flask, sys

_end = '_end_'

#Checks if a word is a prefix in the trie
def prefix_in_trie(trie, word):
    current_dict = trie
    for letter in word:
        if letter in current_dict:
            current_dict = current_dict[letter]
        else:
            return False
    return True

#Checks if a word is in the trie
def in_trie(trie, word):
    current_dict = trie
    for letter in word:
        if letter in current_dict:
            current_dict = current_dict[letter]
        else:
            return False
    else:
        if _end in current_dict:
            return True
        else:
            return False

#Make a trie data structure out of words
def make_trie(words):
    root = {}
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict = current_dict.setdefault(_end, _end)
    return root
 
neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
 
def explore(board, positions, trie, words):
    # process current word
    word = board.get_word(positions)
    # check if the word is in the words
    if len(word) >= 2 and in_trie(trie, word) and word not in words:
        words.append(Solution(word, board.get_indices(positions)))
    # stop if this path is condemned, i.e. no more word possible
    if not prefix_in_trie(trie, word):
        return
    # go through all neighbors of the last position
    pos = positions[-1]
    for neighbor in neighbors:
        npos = (pos[0] + neighbor[0], pos[1] + neighbor[1])
        # check if the neighbor is admissible
        if npos[0] >= 0 and npos[0] < board.height and npos[1] >= 0 and npos[1] < board.width:
            # avoid self-intersections
            if npos not in positions:
                # we create a copy of the list positions instead of
                # updating the same list!
                npositions = positions + [npos] 
                # explore the new path 
                explore(board, npositions, trie, words)
                
def find_words(board):
    """Return all possible words in a board."""
    
    trie = flask.g.get("trie", None)
    if trie is None:
        trie = make_trie(FileService.read_dictionary())
        flask.g.trie = trie
    
    words = [] 
    for row in xrange(board.height): 
        for column in xrange(board.width):
            explore(board, [(row, column)], trie, words)
            
    return words