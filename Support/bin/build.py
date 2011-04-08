#! /usr/bin/env python

# TODO: Clean up and separate templating code.
# TODO: Change columnIndicator to columnNumber and recreate string from that in template.
# TODO: Add link to line of code in HTML
# TODO: Add clear green success, red failure messages upon completion.
# TODO: Add JS_SOURCE_PATHS environment var. If not present, still use project dir, but display warning (may take a long time to compile depending on your project dir).
# TODO: Allow override of UPPERCASE settings.
# TODO: Add setting (Boolean) for exporting source map.

from compiler import parse
import os, os.path, subprocess
import sys
import re
from settings import *

from pytm import textmate, jsinterface, htmloutput


exception_pattern = re.compile('^(?P<filename>[^\:\n]+?):(?P<line_number>\d+):\s+(?P<warning_level>[A-Z]+)\s+-\s+(?P<message>[\n\w\W]*?)(\n(?P<code>.*)(\n(?P<column_indicator>.*))?)?\n\n', re.MULTILINE)


def parse_line(txt):
    return exception_pattern.search(txt)


def eval_str(str):
    """
    Evaluates a string literal. I'd use ast.literal_eval, but I don't want to
    introduce a 2.6 dependency.
    """
    try:
        return parse(str, mode='eval').node.value
    except:
        return ''
    

def build():

    # Determine what files to compile and the output file name.
    outfile = GC_OUTPUT_FILE or 'compiled.js'
    if GC_INPUT:
        files_to_compile = GC_INPUT
    else:
        files_to_compile = [eval_str(file) for file in os.environ.get('TM_SELECTED_FILES', '').split(' ')]
        if len(files_to_compile) <= 1:
            current_file = os.environ.get('TM_FILEPATH')
            if not current_file:
                if not files_to_compile:
                    textmate.exit_show_tool_tip('No file to compile.')
            else:
                files_to_compile = [current_file]
                parts = os.path.splitext(current_file)
                outfile = GC_OUTPUT_FILE or '%s-compiled%s' % (parts[0], parts[1])
    source_map = os.path.splitext(outfile)[0] + '-sourcemap'

    if not TM_PROJECT_DIRECTORY:
        textmate.exit_show_tool_tip('You need a project!')
    
    if DEBUG:
        title = 'DEBUG Build (closurebuilder.py)'
    else:
        title = 'Build (closurebuilder.py)'
    print htmloutput.header(title, ', '.join([os.path.basename(file) for file in files_to_compile]))
    print '<h2>Building...</h2>'
    
    # Create the command.
    e_sh = textmate.sh_escape
    args = [
        'python',
        e_sh(CLOSURE_BUILDER),
        '--root', e_sh(CLOSURE_LIBRARY_PATH),
        '--root', e_sh(TM_PROJECT_DIRECTORY),
        '--output_mode ', GC_OUTPUT_MODE,
        '--compiler_jar', e_sh(CLOSURE_COMPILER),
        '--output_file', e_sh(outfile),
        '--compiler_flags="--compilation_level=%s"' % GC_COMPILATION_LEVEL,
        '--compiler_flags="--warning_level=%s"' % GC_WARNING_LEVEL,]
    if DEBUG:
        args += [
            '--compiler_flags="--debug"',
            '--compiler_flags="--create_source_map=%s"' % e_sh(source_map).replace('"', '\\"')]
    for file in files_to_compile:
        args += ['--input', e_sh(file)]
    cmd = ' '.join(args)

    print '<pre>%s</pre>' % htmloutput.escape_for_html(cmd)
    print """
        <div id="error-container" style="display:none;">
            <h3>Errors</h3>
            <ul id="error-list"></ul>
        </div>
        <div id="warning-container" style="display:none;">
            <h3>Warnings</h3>
            <ul id="warning-list"></ul>
        </div>"""
    print """
        <script>
            var listMap = {};
            function addToList(warningLevel, file, ln, msg, code, columnIndicator)
            {
                var containerId = warningLevel.toLowerCase() + "-container";
                var listId = warningLevel.toLowerCase() + "-list";
                var container = document.getElementById(containerId);
                container.style.display = "block";
                var list = document.getElementById(listId);
                listMap[containerId] = listMap[containerId] || {};
                var fileList = listMap[containerId][file];
                if (!fileList)
                {
                    var li = document.createElement("li");
                    li.innerHTML = "<h3>" + file + "</h3>";
                    fileList = listMap[containerId][file] = document.createElement("ul");
                    li.appendChild(fileList);
                    list.appendChild(li);
                }
                
                var li = document.createElement("li");
                var innerHTML = "<b>" + ln + ": </b>" + msg.replace(/\\n/g, "<br />");
                if (code)
                    innerHTML += "<br /><pre><code>" + code + "\\n" + columnIndicator + "</code></pre>";
                li.innerHTML = innerHTML;
                fileList.appendChild(li);
            }
        </script>"""
    sys.stdout.flush()

    # Compile.
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    
    raw_output = ''
    buffer = ''
    while p.poll() is None:
        data = p.stderr.readline()
        raw_output += data
        buffer += data
        parsed_line = parse_line(buffer)
        if parsed_line:
            jsinterface.call('addToList',
                             parsed_line.group('warning_level'),
                             parsed_line.group('filename'),
                             parsed_line.group('line_number'),
                             parsed_line.group('message'),
                             parsed_line.group('code'),
                             parsed_line.group('column_indicator'))
            # Clear the buffer so that we don't find this one again.
            buffer = ''

    print """<br/><br/><div class="raw_out"><span class="showhide">
             <a href="javascript:hideElement('raw_out')" id='raw_out_h' style='display: none;'>&#x25BC; Hide Raw Output</a>
             <a href="javascript:showElement('raw_out')" id='raw_out_s' style=''>&#x25B6; Show Raw Output</a>
             </span></div>
             <div class="inner" id="raw_out_b" style="display: none;"><br/>
             <code>%s</code><br/>""" % raw_output    
    print htmloutput.footer()


if __name__ == '__main__':
    build()
