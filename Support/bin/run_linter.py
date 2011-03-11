#!/usr/bin/env python
from settings import *
import os, sys
import textmate
import webpreview2

from cStringIO import StringIO

try:
    from closure_linter import checker
    from closure_linter import errors
    from closure_linter.common import errorprinter
except:
    raise Exception("Please install the closure linter first")
    
try:
    os.environ['TM_FILEPATH']
except:
    raise Exception("Please save file before running linter.")

    
def run_linter():
    print webpreview2.html_header('Running Google Closure Linter...', '')

    old_stdout = sys.stdout    
    error_handler = errorprinter.ErrorPrinter(errors.NEW_ERRORS)
    error_handler.SetFormat(1)
    runner = checker.GJsLintRunner()
    
    # Hijack the stdout to capture the command output
    sys.stdout = mystdout = StringIO()

    # Run the linter
    result = runner.Run([os.environ['TM_FILEPATH'],], error_handler)

    # Set the old stdout back
    sys.stdout = old_stdout

    # Reset the StringIO
    mystdout.seek(0)

    # Print the File Name
    first_line = mystdout.readline()
    print "<h3>%s</h3>" % first_line[first_line.find(':') + 2:-7]
    
    print '<pre>'
    for line in mystdout.readlines():
        sys.stdout.write(webpreview2.escape_for_html(line))
        sys.stdout.flush()
    print '</pre>'
    result.PrintSummary()
    print webpreview2.html_footer()

if __name__ == '__main__':
    run_linter()



