#!/usr/bin/python
import sys
sys.path.insert(0, '/usr/local/bin/python2.7')

from wsgiref.handlers import CGIHandler
from myapp import app
CGIHandler().run(app)