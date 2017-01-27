import sys
import os

from twisted.internet import reactor
import argparse


from checkio_task_tester.center_client import CenterClientFactory
from checkio_task_tester.uch_server import CenterUchFactory
import checkio_task_tester.settings as S
import checkio_task_tester.tools as T

parser = argparse.ArgumentParser(description="Checkio Task Tester")
parser.add_argument('folder', help="Local path for task folder (REPO_FOLDER)")
parser.add_argument('--init', action='store_true', help="Create a new repository")
parser.add_argument('--repo', help="Link mission to remote repository")
parser.add_argument('-v', '--verbose', action='store_true', help="Disable truncation of debug output")
args = parser.parse_args()

settings_keys = {'folder': 'REPO_FOLDER',
                 'verbose': 'SHOW_FULL_LOGS'}


def main():
    for s_key in settings_keys:
        if getattr(args, s_key):
            setattr(S, settings_keys[s_key], getattr(args, s_key))

    if args.init:
        if os.path.exists(S.REPO_FOLDER):
            print('Folder {} exists'.format(S.REPO_FOLDER))
            sys.exit()

        print('Creating a new missin folder {}...'.format(S.REPO_FOLDER))
        T.init()
        print('Done.')
            
    elif args.repo:
        if not os.path.exists(S.REPO_FOLDER):
            print('Folder {} does not exist'.format(S.REPO_FOLDER))
            sys.exit()
        if os.path.exists(os.path.join(S.REPO_FOLDER,'.git')):
            print('Folder {} is a git repository already'.format(S.REPO_FOLDER))
            sys.exit()
        T.link_repo(args.repo)
    else:
        print('Connecting to {}:{} ...'.format(S.CENTER_SERVER_HOST, S.CENTER_SERVER_PORT))
        reactor.connectTCP(S.CENTER_SERVER_HOST, S.CENTER_SERVER_PORT, CenterClientFactory())
        reactor.listenTCP(S.CENTER_UCH_PORT, CenterUchFactory())
        reactor.run()
