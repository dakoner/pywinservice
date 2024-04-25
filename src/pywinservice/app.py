from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI

import logging
import logging.handlers
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import uvicorn

import boto3
from config import Settings
import yaml
import os
import sys

logger = logging.getLogger(__name__)

settings = Settings()

def init_logging(debug=False):
    """ placeholder, dictConfig in Settings? """
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    f = logging.Formatter('{'
            '"time":"%(asctime)s", '
            '"pid":%(process)d, '
            '"name":"%(name)s", '
            '"level":"%(levelname)s", '
            '"message":"%(message)s"'
        '}')
    
    if debug:
        h = logging.StreamHandler()
        h.setFormatter(f)
        root.addHandler(h)
    else:
        lh = logging.handlers.RotatingFileHandler(
            os.path.join(os.path.dirname(sys.argv[0]), 'out.log'),
            maxBytes=10<<20,
            backupCount=1
        )
        lh.setFormatter(f)
        root.addHandler(lh)
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    yaml_config = settings.yaml_config
    yaml_config = os.path.join(os.path.dirname(sys.argv[0]), yaml_config)
    config = yaml.safe_load(open(yaml_config))
    logging.info(f"start watching directory {config['watch_path']}")
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, config["watch_path"], recursive=True)
    observer.start()
    yield
    observer.stop()
    observer.join()


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/shutdown")
def shutdown():
    server.should_exit=True
    return {"Shutting": "Down"}

@app.get("/buckets")
def read_buckets():

    s3 = boto3.client('s3')
    response = s3.list_buckets()

    return {"buckets": [bucket['Name'] for bucket in  response['Buckets']]}
