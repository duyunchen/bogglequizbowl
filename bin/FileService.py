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

from flask import g

def read_letter_freq():
    letterfreq = g.get("letterfreq", None)
    
    if letterfreq:
        return letterfreq
    else:
        letterfreq = {}
        
    with open("res/letterfreq.txt") as f:
        lines = f.readlines()
        
    for line in lines:
        letter, freq = line.split(" ")
        letterfreq[letter] = float(freq)
    
    g.letterfreq = letterfreq
    return letterfreq

def read_dictionary():
    dictionary = g.get("dictionary", None)
    
    if dictionary:
        return dictionary
    
    with open("res/dictionary.txt") as f:
        dictionary = f.read().split("\n")
        
    g.dictionary = dictionary
    return dictionary