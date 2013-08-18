import settings as S
from twisted.internet import reactor

from center_client import CenterClientFactory
from uch_server import CenterUchFactory


# reactor.spawnProcess(run,
#                          S.PYTHON_3,
#                          args=[S.PYTHON_3,
#                                "uch.py",
#                                self.connection_id,
#                                self.task_num,
#                                str(settings.CHAT_SERVICE_PORT)],
#                          env={
#                             'PYTHONIOENCODING': 'utf8', 
#                             'PYTHONUNBUFFERED': '0',
#                             'FOLDER_USER': settings.CENTER_FOLDER_USER + '/' + self.folder
#                           })

reactor.connectTCP(S.CENTER_SERVER_HOST, S.CENTER_SERVER_PORT, CenterClientFactory())
reactor.listenTCP(S.CENTER_UCH_PORT, CenterUchFactory())
reactor.run()
