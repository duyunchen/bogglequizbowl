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
from SQLiteDB import query
from Player import Player

def get_player(username):
    result = query("SELECT * FROM players WHERE username=?", [username])
    if result:
        row = result[0]
        return Player(row[1], row[2])
    else:
        return None

def insert_player(username):
    query("INSERT INTO players VALUES (null, ?, 0)", [username])
    
def update_player(player):
    query("UPDATE players SET highscore=? WHERE username=?", [player.highscore, player.username])
    
def list():
    result = query("SELECT * FROM players WHERE username != 'debug' AND username != 'Guest' ORDER BY highscore DESC")
    players = []
    for row in result:
        players.append(Player(row[1], row[2]))
    return players