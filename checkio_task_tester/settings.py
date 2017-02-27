import sys
import os
import configparser

PY3 = sys.version_info[0] == 3
if PY3:
    raw_input = input
    path_to_python3 = sys.executable
else:
    path_to_python3 = '/usr/local/bin/python3'


CUR_DIR = os.path.dirname(__file__)
UCH_FILE = os.path.join(CUR_DIR, 'uch.py')

AVAILABLE_DOMAINS = {
    'py': {
        'domain': 'py.checkio.org',
        'server_port': 2325,
        'server_host': 'py-tester.checkio.org'
    },
    'js': {
        'domain': 'js.checkio.org',
        'server_port': 2345,
        'server_host': 'py-tester.checkio.org'
    }
}

DOMAIN = 'py'

config = configparser.ConfigParser()
config_filename = os.path.join(os.path.expanduser("~"), '.checkio_task_tester.ini')
if not os.path.exists(config_filename):
    config.add_section('Main')
    print('Config file {} was not found'.format(config_filename))
    print('We will need to go through a short configuration process')

    print('Which domain you want to use for testing? (first two letters are needed)')
    for dom, conf in AVAILABLE_DOMAINS.items():
        print('[{}] - {}'.format(dom, conf['domain']))
    print('by default:{}'.format(DOMAIN))

    while True:
        new_domain = raw_input('First two letters of the domain[{}]:'.format(DOMAIN)).strip()
        if not new_domain:
            break
        if new_domain not in AVAILABLE_DOMAINS:
            continue
        DOMAIN = new_domain
        break

    print('What is your TESTER_KEY?')
    print('You can find one on https://{}/mission/add/'.format(AVAILABLE_DOMAINS[DOMAIN]['domain']))
    while True:
        TESTER_KEY = raw_input('TESTER_KEY:').strip()
        if not TESTER_KEY:
            continue
        break


    config['Main']['domain'] = DOMAIN
    config['Main']['tester_key'] = TESTER_KEY

    with open(config_filename, 'w') as f:
        config.write(f)
        f.close()
        print('Config file %s was updated.')
        print('Thank you')
    

config.read(config_filename)

DOMAIN = config['Main'].get('domain', DOMAIN)
DOMAIN_CONFIG = AVAILABLE_DOMAINS[DOMAIN]

CENTER_SERVER_HOST = config['Main'].get('server_host', DOMAIN_CONFIG['server_host'])
CENTER_SERVER_PORT = config['Main'].get('server_port', DOMAIN_CONFIG['server_port'])

CENTER_UCH_PORT = config['Main'].get('local_port', 2323)

PYTHON_3 = config['Main'].get('path_to_python3', path_to_python3) 

TESTER_KEY = config['Main']['tester_key']

SHOW_FULL_LOGS = False

URL_MISSION_INFO = 'https://%s/mission/tester/' % DOMAIN_CONFIG['domain']
URL_MISSION_SOLVE = 'https://%s/mission/tester/solve/' % DOMAIN_CONFIG['domain']

INIT_REPO = 'https://github.com/CheckiO/checkio-mission-template.git'
