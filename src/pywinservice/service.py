import app
from server import ServerThread

import logging
import servicemanager
import socket
import sys
import time
import win32event
import win32service
import win32serviceutil
import uvicorn

logger = logging.getLogger(__name__)

class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = 'pywinservice'
    _svc_display_name_ = 'pywinservice Service'
    _svc_description_ = 'change me'

    def __init__(self, args):
        app.init_logging()
        
        super().__init__(args)

    def SvcStop(self):
        logger.info('Stop requested')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

    def SvcDoRun(self):
        logger.info('Starting')
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        config = uvicorn.Config(app.app, host="0.0.0.0", port=8000, log_config={
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {},
            'loggers': {},
        })
        self.server = ServerThread(config)
        app.server = self.server.server
        self.server.start()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # causes segfault on windows
        # servicemanager.LogInfoMsg(f'app started')
        self.server.join()
        
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

if __name__ == '__main__':
    if len(sys.argv) != 1:
        win32serviceutil.HandleCommandLine(Service)
        sys.exit(0)

    # else running as a service
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(Service)
    servicemanager.StartServiceCtrlDispatcher()

