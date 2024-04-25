import app
from server import Server

import logging
import servicemanager
import socket
import sys
import time
import win32event
import win32service
import win32serviceutil

logger = logging.getLogger(__name__)

class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = 'pywinservice'
    _svc_display_name_ = 'pywinservice Service'
    _svc_description_ = 'change me'

    def __init__(self, args):
        app.init_logging()

        super().__init__(args)

        self.should_exit = False

    def SvcStop(self):
        logger.info('Stop requested')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

        self.should_exit = True

    def SvcDoRun(self):
        logger.info('Starting')
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)

        try:
            self.should_exit = False
            server = Server.run_in_thread()
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            servicemanager.LogInfoMsg(f'{self._svc_name_} started')

            while True:
                #logger.info('Service is alive')
                #servicemanager.LogInfoMsg('Service is alive')
                time.sleep(1)
                if self.should_exit:
                    server.join()
                    break
        except:
            logger.exception('Service failed')
            servicemanager.LogErrorMsg('Check the app log')

        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

if __name__ == '__main__':
    if len(sys.argv) != 1:
        win32serviceutil.HandleCommandLine(Service)
        sys.exit(0)

    # else running as a service
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(Service)
    servicemanager.StartServiceCtrlDispatcher()

