import sys
import time
import win32evtlog
import win32evtlogutil
print("Python {:s} on {:s}".format(sys.version, sys.platform))
DUMMY_EVT_APP_NAME = "Dummy Application"
DUMMY_EVT_ID = 7040  # Got this from another event
DUMMY_EVT_CATEG = 9876
DUMMY_EVT_STRS = ["Dummy event string {:d}".format(item) for item in range(5)]
DUMMY_EVT_DATA = b"Dummy event data"
print('rent time: 2018-07-18 20:03:08')
win32evtlogutil.ReportEvent(
    DUMMY_EVT_APP_NAME, DUMMY_EVT_ID, eventCategory=DUMMY_EVT_CATEG,
    eventType=win32evtlog.EVENTLOG_WARNING_TYPE, strings=DUMMY_EVT_STRS,
    data=DUMMY_EVT_DATA)
