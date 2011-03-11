"""
Many of these methods are ported or adopted from the TextMate support bundle's
(Ruby) TextMate module.
"""
import sys
import pytm
from tm_helpers import sh_escape

def exit_discard():
    sys.exit(200)


def exit_replace_text(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(201)


def exit_replace_document(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(202)


def exit_insert_text(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(203)


def exit_insert_snippet(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(204)


def exit_show_html(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(205)


def exit_show_tool_tip(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(206)


def exit_create_new_document(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(207)


def go_to(options = {}):
    if 'file' in options:
        default_line = 1
    else:
        default_line = LINE_NUMBER
    
    defaults = {
        'file': FILEPATH,
        'line': default_line,
        'column': 1
    }
    defaults.update(options)
    options = defaults
    
    command = "txmt://open?"
    if 'file' in options:
        command = "%surl=file://%s&" % (command, options['file'])
    command = "%sline=%s&column=%s" % (command, options['line'], options['column'])
    command = 'open %s' % sh_escape(command)

    import subprocess
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    process.wait()

