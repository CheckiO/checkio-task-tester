import settings as S
from twisted.internet import reactor
import argparse

from center_client import CenterClientFactory
from uch_server import CenterUchFactory

parser = argparse.ArgumentParser(description="Checkio Task Tester")
parser.add_argument('--center', help="Center folder name for the task (CENTER_FOLDER)")
parser.add_argument('--key', help="Your tester key (TESTER_KEY)")
parser.add_argument('--folder', help="Local path for task folder (REPO_FOLDER)")
parser.add_argument('--port', help="Local port for tester (CENTER_UCH_PORT)")
parser.add_argument('--python3', help="Local path for python3 interpreter (PYTHON_3)")
parser.add_argument('--trunc_output', help="You can disable truncation of debug output. Use 'False'")
args = parser.parse_args()

settings_keys = {'center': 'CENTER_FOLDER',
                 'key': 'TESTER_KEY',
                 'folder': 'REPO_FOLDER',
                 'port': 'CENTER_UCH_PORT',
                 'python3': 'PYTHON_3',
                 'trunc_output': 'TRUNC_OUTPUT'}

for s_key in settings_keys:
    if getattr(args, s_key):
        setattr(S, settings_keys[s_key], getattr(args, s_key))


reactor.connectTCP(S.CENTER_SERVER_HOST, S.CENTER_SERVER_PORT, CenterClientFactory())
reactor.listenTCP(S.CENTER_UCH_PORT, CenterUchFactory())
reactor.run()
