import app
import contextlib
import logging
import time
import threading
import uvicorn

logger = logging.getLogger(__name__)

class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @classmethod
    def run_in_thread(cls):
        logger.info('Starting server')
        config = uvicorn.Config(app.app, log_config={
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {},
            'loggers': {},
        })

        server = cls(config=config)
        server.thread = threading.Thread(target=server.run)
        server.thread.start()
        while not server.started:
            time.sleep(.1)

        logger.info('Server started')
        return server

    def join(self):
        self.should_exit = True
        self.thread.join()

if __name__ == '__main__':
    app.init_logging()
    logger.info('main start')
    try:
        server = Server.run_in_thread()
        logger.info('main loop...')
        time.sleep(10)
        server.join()
    except:
        logger.exception('exception in main')
    logger.info('main exit')

