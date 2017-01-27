import json
import os

from twisted.internet.protocol import ServerFactory
from twisted.protocols import basic
from twisted.internet import reactor, protocol


class UchControl(protocol.ProcessProtocol):
    def get_con(self):
        from checkio_task_tester.runner import CON

        return CON

    def outReceived(self, data):
        print(data.decode('utf8'))

    def errReceived(self, data):
        print(data.decode('utf8'))

    def processEnded(self, reason):
        pass


class CenterUchProtocol(basic.LineReceiver):
    delimiter = b'\0'
    MAX_LENGTH = 10000000
    pid = None
    predicted_death = False

    def kill_me(self):
        self.predicted_death = True

        import signal

        os.kill(self.pid, signal.SIGTERM)

    def get_con(self):
        from  checkio_task_tester.center_client import CON

        return CON

    def lineReceived(self, line):
        #print "UCH CONNECTION GOT:", line
        data = json.loads(line.decode('utf8'))
        method = getattr(self, 'do_' + data['do'], None)
        if method is not None:
            method(data)
        else:
            con = self.get_con()
            con.sendLine(b'{"do":"from_process", "data":' + line + b'}')

    def do_connect(self, data):
        con = self.get_con()
        con.set_service(self)
        self.pid = data['pid']

        self.sendData({
            'do': 'check',
            'code': con.code,
            'runner': con.runner
        })


    def sendData(self, line):
        #print "UCH CONNECTION SEND:", line
        return self.sendLine(str.encode(json.dumps(line)))

    def connectionLost(self, reason):
        #print 'Service Connection Lost'
        con = self.get_con()
        con.service = None

        if self.predicted_death:
            return

        con.sendData({
            'do': 'process_killed'
        })


class CenterUchFactory(ServerFactory):
    protocol = CenterUchProtocol
