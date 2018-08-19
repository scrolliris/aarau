import threading

from wsgiref.simple_server import make_server

TEST_PORT = 5001
TEST_HOST = 'localhost'

BASE_URL = 'http://{}:{}'.format(TEST_HOST, TEST_PORT)


class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.srv = None

    def run(self):
        self.srv = make_server(TEST_HOST, TEST_PORT, self.app)

        try:
            self.srv.serve_forever()
        except Exception:
            import traceback
            traceback.print_exc()
            self.srv = None

    def quit(self):
        if self.srv:
            self.srv.shutdown()
