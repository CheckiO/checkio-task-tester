import json
import codecs
import os
import sys
import base64
from uuid import uuid4
import warnings

from twisted.internet.protocol import ClientFactory
from twisted.protocols import basic
from twisted.internet import reactor

import checkio_task_tester.settings as S
from checkio_task_tester.uch_server import UchControl

CON = None

#------------------------------------------------------#
#LIMIT: number of characters to remain in output string#
#ignore_arguments: keys of output data that will be    #
# ignored while truncating itself.                     #
#------------------------------------------------------#
#LIMIT = 30 
ignore_arguments = [
                    'folder', 'key', 'path',
                    'question', 'error', 'do'
                    ]

class CenterClientProtocol(basic.LineReceiver):
    delimiter = str.encode('\0')
    MAX_LENGTH = 10000000
    service = None

    def connectionMade(self):
        print('Connected.')
        global CON
        CON = self

        self.sendData({
            #'folder': S.CENTER_FOLDER,
            'key': S.TESTER_KEY,
            'do': 'connect'
        })

    def set_service(self, service):
        self.service = service

    def lineReceived(self, raw_data):
        print('CENTER GET:', raw_data)
        data = json.loads(raw_data.decode('utf8'))
        getattr(self, 'do_' + data['do'])(data)

    def do_auth_error(self, data):
        warnings.warn(data['error'])
        reactor.stop()

    def do_get_files(self, data):
        ret = {}
        for file_path in data['files'].split(','):
            folder_path = os.path.join(S.REPO_FOLDER, file_path)
            if not os.path.exists(folder_path):
                warnings.warn('File "' + folder_path + '" doesn\'t exist')
                continue
            try:
                fh = codecs.open(folder_path, "r", "utf-8")
                ret[file_path] = fh.read()
                fh.close()
            except IOError as e:
                warnings.warn('Error during oppening file "' + folder_path + '" :' + str(e))
                continue

        ret['question'] = data['question']
        ret['do'] = 'answer'
        self.sendData(ret)

    def do_get_file(self, data):
        folder_path = os.path.join(S.REPO_FOLDER, data['path'])
        if not os.path.exists(folder_path):
            warnings.warn('File "' + folder_path + '" doesn\'t exist')
            self.sendData({
                'do': 'answer',
                'error': "File doesn't exist",
                'question': data['question'],
                'path': data['path']
            })
            return

        try:
            fh = open(folder_path, "rb")
            fdata = fh.read()
            fh.close()
        except IOError as e:
            warnings.warn('Error during oppening file "' + folder_path + '" :' + str(e))
            self.sendData({
                'do': 'answer',
                'error': "Open error",
                'question': data['question'],
                'path': data['path']
            })
            return
        self.sendData({
            'do': 'answer',
            'data': base64.standard_b64encode(fdata).decode('utf8'),
            'question': data['question'],
            'path': data['path']
        })

    def do_start_process(self, data):
        self.code = data['code']
        self.runner = data['runner']
        self.connection_id = data['connection_id']
        self.task_num = data['task_num']
        reactor.spawnProcess(UchControl(),
                             S.PYTHON_3,
                             args=[S.PYTHON_3, S.UCH_FILE,
                                   str(self.connection_id),
                                   str(self.task_num),
                                   str(S.CENTER_UCH_PORT)],
                             env={
                                 'PYTHONIOENCODING': 'utf8',
                                 'PYTHONUNBUFFERED': '0',
                                 'FOLDER_USER': os.path.join(S.REPO_FOLDER, 'verification')
                             })

    def do_kill_process(self, data):
        if self.service is None:
            return

        self.service.kill_me()


    def do_to_process(self, data):
        self.service.sendData(data['data'])

    # def truncate_output(self, data):
    #     if S.SHOW_FULL_LOGS:
    #         return data
    #     output = {}
    #     keys = data.keys()
    #     for key in keys:
    #         if not key in ignore_arguments and len(data[key]) > 2*LIMIT:
    #             output.update({key: ' ...output truncated... '.join([data[key][:LIMIT], data[key][-LIMIT:]])})
    #         else:
    #             output.update({key: data[key]})
    #     return output

    def sendData(self, line):
        #output_line = self.truncate_output(line)
        print('CENTER SEND:', line)
        return self.sendLine(str.encode(json.dumps(line)))


class CenterClientFactory(ClientFactory):
    protocol = CenterClientProtocol
