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

import sqlite3

DB_NAME = "bqb.db"

def query(q, params = None):
    conn = sqlite3.connect(DB_NAME)
    if params:
        results = conn.cursor().execute(q, params)
    else:
        results = conn.cursor().execute(q)
    
    data = results.fetchall()
    
    conn.commit()
    conn.close()
    return data 
    
def init_db():
    query("CREATE TABLE IF NOT EXISTS players (id integer primary key autoincrement, username text UNIQUE NOT NULL, highscore integer)")