import settings as S
from twisted.internet import reactor

from center_client import CenterClientFactory
from uch_server import CenterUchFactory


reactor.connectTCP(S.CENTER_SERVER_HOST, S.CENTER_SERVER_PORT, CenterClientFactory())
reactor.listenTCP(S.CENTER_UCH_PORT, CenterUchFactory())
reactor.run()
