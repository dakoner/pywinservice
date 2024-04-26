from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI

import logging
import logging.handlers
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import uvicorn

import boto3
from config import load_config
import yaml
import os
import sys

config = load_config()

def init_logging():
    root = logging.getLogger()
    m = logging.getLevelNamesMapping()
    log_level_str = config.get("log_level", "INFO")
    log_level = m.get(log_level_str, logging.INFO)
    root.setLevel(log_level)
    formatter = logging.Formatter('{'
            '"time":"%(asctime)s", '
            '"pid":%(process)d, '
            '"name":"%(name)s", '
            '"level":"%(levelname)s", '
            '"message":"%(message)s"'
        '}')
    
    if config["debug"] is True:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.handlers.RotatingFileHandler(
            os.path.join(os.path.dirname(sys.argv[0]), 'out.log'),
            maxBytes=10<<20,
            backupCount=1,
        )

    handler.setFormatter(
        formatter
    )
    root.addHandler(handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
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
