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

import random

## Represents a boggle board
class Board(object):
    def __init__(self, letters="", width = 4, height = 4):
        self.letters = letters
        self.width = width
        self.height = height
        self.neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        
    #Get the word corresponding to a path (list of positions).
    def get_word(self, positions):
        return ''.join([self.get_letter(i, j) for (i, j) in positions])
    
    #Get the letter at location (row, col) of the board
    def get_letter(self, row, col):
        return self.letters[self.get_index(row, col)]
    
    def get_indices(self, positions): 
        return [self.get_index(row, col) for (row, col) in positions]
    
    #Get index in array given row, col
    def get_index(self, row, col):
        return self.width*row + col
    
    def get_random_word(self, length = 3):
        return self.get_word(self.get_random_path(length))
        
    def get_random_path(self, length = 3):
        path = [(random.randint(0,3), random.randint(0,3))]
        
        for index in xrange(length - 1):
            cur = path[-1]
            neighbor = random.choice(self.neighbors);
            next = (cur[0] + neighbor[0], cur[1] + neighbor[1]);
            while next in path or not self.is_valid_position(next):
                neighbor = random.choice(self.neighbors);
                next = (cur[0] + neighbor[0], cur[1] + neighbor[1]);
            path.append(next)
        
        return path
    
    # Returns whether the board contains a certain word
    def has_word(self, word):
        if len(word) is 0:
            return False
        
        for row in xrange(self.height): 
            for column in xrange(self.width):
                success = self._has_word_helper([(row, column)], word)
                if success:
                    return True
        return False
                
    def _has_word_helper(self, path, word):
        cur = path[-1]
        letter = self.get_letter(cur[0], cur[1])
        
        if len(word) is 0:
            return True
        
        if word[0] != letter:
            return False
        
        for neighbor in self.neighbors:
            next = (cur[0] + neighbor[0], cur[1] + neighbor[1]);
            if not self.is_valid_position(next):
                continue
            success = self._has_word_helper(path + [next], word[1:])
            if success:
                return True
        return False
        
    def is_valid_position(self, position):
        row = position[0]
        col = position[1]
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return False
        return True 