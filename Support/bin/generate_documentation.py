#! /usr/bin/env python

# TODO: Make project setting for --directory
# TODO: Make project setting for --template
# TODO: Add link to documentation index upon completion.
# TODO: Format warnings nicely (like I do in build.py)
# TODO: Add clear green success, red failure messages upon completion.

from settings import *
import subprocess
import textmate
import webpreview2


def generate_documentation():
    input = TM_PROJECT_DIRECTORY
    print webpreview2.html_header('Generating Documentation...', '')

    # Create the command.
    e_sh = textmate.sh_escape
    args = [
        'java',
    	'-jar', e_sh(JSRUN_JAR),
    	e_sh(os.path.join(JSDOC_TOOLKIT_PATH, 'app/run.js')),
    	'-a',
    	'--directory=' + e_sh(os.path.join(TM_PROJECT_DIRECTORY, 'docs')),
    	'--template=' + e_sh(JSDOC_TEMPLATE_PATH),
        '--exclude="[\.\-]compiled\.js$"', # Exclude compiled files.
    	'--recurse=10',
    	e_sh(input)]
    cmd = ' '.join(args)
    
    # Run the command.
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    
    print '<pre>'
    while p.poll() is None:
        sys.stdout.write(webpreview2.escape_for_html(p.stdout.readline()))
        sys.stdout.flush()
    print '</pre>'    
    print webpreview2.html_footer()


if __name__ == '__main__':
    generate_documentation()
