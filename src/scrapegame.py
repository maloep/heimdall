#!/usr/bin/python

from heimdall.core import Engine, Subject
from heimdall.predicates import *
from heimdall.threadpools import MainloopThreadPool

import item
import thegamesdb

import json
import time
import urlparse
import sys

import logging
logging.basicConfig()
logging.getLogger("heimdall").setLevel(logging.DEBUG)

def main(uri):
    if uri == None:
        uri = "file:///E:/Games/Testsets/RCB 3.0/SNES/Roms/Super Mario Kart.zip"

    if urlparse.urlparse(uri).scheme == "":
        uri = urlparse.urlunparse(("file", "", uri, "", "", ""))

    print "Running heimdall upon", uri

    pool = MainloopThreadPool()
    engine = Engine(pool)
    engine.registerModule(item.module)
    engine.registerModule(thegamesdb.module)

    def c(error, subject):
        if error:
            raise error

        print subject
        pool.quit()

    metadata = dict()
    metadata[dc.identifier] = uri
    metadata['itemtype'] = 'game'
    metadata['platform'] = 'Super Nintendo (SNES)'
    
    #TODO How to pass configuration to scraper?
    metadata['pathboxfront'] = 'E:\\Games\\Testsets\\Scraper Tests\\SNES\\Artwork\\boxfront'
    metadata['pathfanart'] = 'E:\\Games\\Testsets\\Scraper Tests\\SNES\\Artwork\\fanart'
    subject = Subject("", metadata)

    print "Running heimdall upon", subject

    engine.get(subject, c)

    try:
        pool.join()
    except KeyboardInterrupt:
        pool.quit()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) >= 2 else None)
