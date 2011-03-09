import os, os.path
import sys

BUNDLE_SUPPORT_PATH = os.environ['TM_BUNDLE_SUPPORT']
TM_SUPPORT_PATH = os.environ['TM_SUPPORT_PATH']
LIB_PATH = os.path.join(BUNDLE_SUPPORT_PATH, 'lib')
BIN_PATH = os.path.join(BUNDLE_SUPPORT_PATH, 'bin')
TM_PROJECT_DIRECTORY = os.environ.get('TM_PROJECT_DIRECTORY')

# Closure library
CLOSURE_LIBRARY_PATH = os.path.join(LIB_PATH, 'third_party/closure-library')
CLOSURE_LIBRARY_BIN_PATH = os.path.join(CLOSURE_LIBRARY_PATH, 'closure/bin')

# Closure compiler
GC_OUTPUT_FILE = os.environ.get('GC_OUTPUT_FILE')
GC_INPUT = os.environ.get('GC_INPUT')
if GC_OUTPUT_FILE:
    GC_OUTPUT_FILE = os.path.join(TM_PROJECT_DIRECTORY, GC_OUTPUT_FILE)
if GC_INPUT:
    GC_INPUT = [os.path.join(TM_PROJECT_DIRECTORY, file) for file in GC_INPUT.split(':')]
CLOSURE_BUILDER = os.path.join(CLOSURE_LIBRARY_BIN_PATH, 'build/closurebuilder.py')
CLOSURE_COMPILER = os.path.join(LIB_PATH, 'third_party/closure-compiler/compiler.jar')

# JSDoc Toolkit
JSDOC_TOOLKIT_PATH = os.path.join(LIB_PATH, 'third_party/jsdoc-toolkit')
JSRUN_JAR = os.path.join(JSDOC_TOOLKIT_PATH, 'jsrun.jar')
JSDOC_TEMPLATE_PATH = os.environ.get('JSDOC_TEMPLATE_PATH', os.path.join(JSDOC_TOOLKIT_PATH, 'templates/jsdoc'))

# Add some folders to sys.path
if TM_SUPPORT_PATH not in sys.path:
    sys.path.append(TM_SUPPORT_PATH)
if LIB_PATH not in sys.path:
    sys.path.insert(0, LIB_PATH)
if BIN_PATH not in sys.path:
    sys.path.append(BIN_PATH)
