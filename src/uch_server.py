import json

from twisted.internet.protocol import ServerFactory
from twisted.protocols import basic
from twisted.internet import  reactor, protocol



class UchControl(protocol.ProcessProtocol):
    def get_con(self):
        from runner import CON
        return CON

    def outReceived(self, data):
        print 'UCH OUT:', data

    def errReceived(self, data):
        print 'UCH ERR', data

    def processEnded(self,reason):
        print 'UCH ENDED:', reason



class CenterUchProtocol(basic.LineReceiver):
    delimiter = '\0'
    MAX_LENGTH = 10000000
    pid = None
    predicted_death = False

    def kill_me():
        self.predicted_death = True

        import signal
        os.kill(self.pid, signal.SIGKILL)

    def get_con(self):
        from center_client import CON
        return CON

    def lineReceived(self, line):
        print "UCH CONNECTION GOT:", line
        data = json.loads(line)
        method = getattr(self, 'do_'+data['do'],None)
        if method is not None:
            method(data)
        else:
            con = self.get_con()
            con.sendLine('{"do":"from_process", "data":'+line+'}')

    def do_connect(self, data):
        con = self.get_con()
        con.set_service(self)
        self.pid = data['pid']

        self.sendData({
            'do': 'check',
            'code': con.code,
            'runner': con.runner
        })


    def sendData(self,line):
        print "UCH CONNECTION SEND:", line
        return self.sendLine(json.dumps(line))

    def connectionLost(self, reason):
        print 'Service Connection Lost'
        con = self.get_con()
        con.service = None

        if self.predicted_death:
            return

        con.sendData({
            'do': 'process_killed'
        })





class CenterUchFactory(ServerFactory):
    protocol  = CenterUchProtocol