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

import flask
import json

def jsonify(obj):
    obj = prepare(obj)
    jsondict = json.loads(json.dumps(prepare(obj), default=lambda o: o.__dict__ if o else None))
    return flask.jsonify(jsondict)
    
def prepare(obj):
    if obj is None:
        return {}
    elif type(obj) == dict:
        return obj
    elif type(obj) == list:
        return {"results" : [prepare(item) for item in obj]}
    else:
        return obj.__dict__