#!/usr/bin/python3.7

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/Documents/deepbuzz-pi/')
from deepbuzz-pi import app as application
application.secret_key = 'anything you wish'
