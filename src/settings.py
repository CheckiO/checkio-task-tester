CENTER_SERVER_HOST = '127.0.0.1'
CENTER_SERVER_PORT = 2325

CENTER_UCH_PORT = 2323

PYTHON_3 = '/usr/local/bin/python3.3'

TESTER_KEY = 'overwrite it in settings_local.py'
CENTER_FOLDER = 'overwrite it in settings_local.py'
REPO_FOLDER = 'overwrite it in settings_local.py'

try:
    from settings_local import *
except ImportError:
    pass