#!/usr/bin/env python
from settings import *
import os

try:
    from closure_linter import checker
    from closure_linter import error_fixer
    from closure_linter.common import simplefileflags as fileflags
except:
    raise Exception('Please install the closure linter first')

style_checker = checker.JavaScriptStyleChecker(error_fixer.ErrorFixer())
style_checker.Check(os.environ['TM_FILEPATH'])
