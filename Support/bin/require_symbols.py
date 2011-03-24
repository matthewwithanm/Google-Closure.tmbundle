#! /usr/bin/env python

import os
import re
from settings import *


def require_dropped_symbols():
    """
    Requires the symbols provided by the dropped file.
    """

    TM_DROPPED_FILE = os.environ['TM_DROPPED_FILE']
    file = open(TM_DROPPED_FILE, 'r')
    js = file.read()
    pattern = re.compile('goog.provide\s*\(\s*[\'"](?P<symbol>[\w\.]+)[\'"]\s*\)')
    for match in pattern.finditer(js):
        print 'goog.require(\'%s\');' % match.group('symbol')
    

if __name__ == '__main__':
    require_dropped_symbols()
