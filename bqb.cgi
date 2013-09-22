#!/usr/bin/env python

import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from bqb import app

CGIHandler().run(app)
