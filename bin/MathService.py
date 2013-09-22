#!/usr/bin/env python

#  This file is part of Boggle Quiz Bowl.
# 
#     Boggle Quiz Bowl is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import random

# Returns a sample from a given distribution (as a dict of value/prob pairs)
def weighted_random_sample(distribution): 
    random_position = random.random()*sum(distribution.values())
    current_position = 0.0
    for value, p in distribution.iteritems():
        current_position += p 
        if random_position < current_position:
            return value
    return None

# Returns True or False at random.
def get_random_boolean():
    return bool(random.getrandbits(1))