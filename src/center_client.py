import json
import codecs
import os
import base64
from uuid import uuid4
import warnings

from twisted.internet.protocol import ClientFactory
from twisted.protocols import basic
from twisted.internet import  reactor

import settings as S
from uch_server import UchControl

CON = None



class CenterClientProtocol(basic.LineReceiver):
    delimiter = '\0'
    MAX_LENGTH = 10000000
    service = None
    
    def connectionMade(self):
        global CON
        CON = self

        self.sendData({
            'folder': S.CENTER_FOLDER,
            'key': S.TESTER_KEY,
            'do': 'connect'
        })

    def set_service(self, service):
        self.service = service

    def lineReceived(self, raw_data):
        print 'CENTER GET:', raw_data
        data = json.loads(raw_data)
        getattr(self, 'do_'+data['do'])(data)

    def do_get_files(self, data):
        ret = {}
        for file_path in data['files'].split(','):
            folder_path = os.path.join(S.REPO_FOLDER, file_path)
            if not os.path.exists(folder_path):
                warnings.warn('File "'+ folder_path + '" doesn\'t exist')
                continue
            try:
                fh = codecs.open(folder_path, "r", "utf-8")
                ret[file_path] = fh.read()
                fh.close()
            except IOError, e:
                warnings.warn('Error during oppening file "'+ folder_path + '" :'+str(e))
                continue

        ret['question'] = data['question']
        ret['do'] = 'answer'
        self.sendData(ret)

    def do_get_file(self, data):
        folder_path = os.path.join(S.REPO_FOLDER, data['path'])
        if not os.path.exists(folder_path):
            warnings.warn('File "'+ folder_path + '" doesn\'t exist')
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
        except IOError, e:
            warnings.warn('Error during oppening file "'+ folder_path + '" :'+str(e))
            self.sendData({
                'do': 'answer',
                'error': "Open error",
                'question': data['question'],
                'path': data['path']
            })
            return

        self.sendData({
            'do': 'answer',
            'data': base64.standard_b64encode(fdata),
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
             args=[S.PYTHON_3, "uch.py",
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

    def sendData(self,line):
        print 'CENTER SEND:', line
        return self.sendLine(json.dumps(line))

class CenterClientFactory(ClientFactory):
    protocol = CenterClientProtocol
