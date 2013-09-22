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

import requests
from flask import flash
from Config import DEBUG

AUTH_URL = "http://www.ruzzleleague.com/login/"

DEBUG_USER = "debug"
DEBUG_PASS = "debug"

def check_auth(username, password):
    data = {"userName" : username, "password" : password, "login" : 1}
    
    if DEBUG and username==DEBUG_USER and password==DEBUG_PASS:
        return True
    
    if username=="Guest" and password=="guestpassword":
        return True
    
    try:
        resp = requests.post(AUTH_URL, data=data)
        if resp.status_code is 200:
            if "Log out" in resp.text:
                return True
            return False
        else:
            flash("The authentication site is down. Please try again later.")
    except (Exception):
        flash("There was an error processing authentication! Please contact vokuheila@gmail.com.")
        return None