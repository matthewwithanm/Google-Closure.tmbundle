import sys
import os

# Add TM supoprt path.
SUPPORT_PATH = os.path.join(os.environ["TM_SUPPORT_PATH"], "lib")
if not SUPPORT_PATH in sys.path:
    sys.path.insert(0, SUPPORT_PATH)

# from dialog import menu, get_string
# from tm_helpers import current_word, env_python, sh, sh_escape

# TextMate environment vars
PROJECT_DIRECTORY = os.environ.get('TM_PROJECT_DIRECTORY', None)
FILEPATH = os.environ.get('TM_FILEPATH')
LINE_INDEX = int(os.environ.get('TM_LINE_INDEX', -1))
CURRENT_LINE = os.environ.get('TM_CURRENT_LINE', None)
LINE_NUMBER = int(os.environ.get('TM_LINE_NUMBER', -1))
SCOPE = os.environ.get('TM_SCOPE', None)
CURRENT_WORD = os.environ.get('TM_CURRENT_WORD', None)
DIALOG = os.environ.get('DIALOG', None)
PYTHONPATH = os.environ.get('PYTHONPATH', None)




