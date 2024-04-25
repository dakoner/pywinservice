import asyncio
import sys
import app
import contextlib
import logging
import time
import threading
import uvicorn
import signal
logger = logging.getLogger(__name__)

class ServerThread(threading.Thread):
    def __init__(self, config):
        self.server = uvicorn.Server(config=config)
        super().__init__()
    def run(self):
        self.server.run()

if __name__ == '__main__':
    app.init_logging(debug=True)
    config = uvicorn.Config(app.app, host="0.0.0.0", port=8000, log_config={
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {},
        'loggers': {},
    })
    
    server_thread = ServerThread(config)
    server_thread.start()
    app.server = server_thread.server

    server_thread.join()