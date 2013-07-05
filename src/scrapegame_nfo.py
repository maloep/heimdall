#!/usr/bin/python

from heimdall.core import Engine, Subject
from heimdall.predicates import *
from heimdall.threadpools import MainloopThreadPool

import item
import nfogames
import nfoconsoles
import nfocompanies
import nfopersons

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
    
    metadata = dict()
    metadata[dc.identifier] = uri
    metadata['itemtype'] = 'game'
    metadata['console'] = 'SNES'
    metadata['basepath'] = 'file:///E:/Games/Testsets/RCB 3.0/nfo/games'
    
    modules = [item.module, nfogames.module]
        
    gameSubject = getSubject(uri, metadata, modules)
    
    metadata = dict()
    metadata[dc.identifier] = uri
    metadata['itemtype'] = 'console'
    metadata[dc.title] = gameSubject['console']
    metadata['basepath'] = 'file:///E:/Games/Testsets/RCB 3.0/nfo/consoles'
    
    modules = [nfoconsoles.module]
    consoleSubject = getSubject(uri, metadata, modules)
    
    
    if(gameSubject['developer']):
        metadata = dict()
        metadata[dc.identifier] = uri
        metadata['itemtype'] = 'company'
        metadata[dc.title] = gameSubject['developer']
        metadata['basepath'] = 'file:///E:/Games/Testsets/RCB 3.0/nfo/companies'
    
    modules = [nfocompanies.module]
    subject = getSubject(uri, metadata, modules)
    
    
    if(gameSubject['producer']):
        metadata = dict()
        metadata[dc.identifier] = uri
        metadata['itemtype'] = 'person'
        metadata[dc.title] = gameSubject['producer']
        metadata['basepath'] = 'file:///E:/Games/Testsets/RCB 3.0/nfo/persons'
    
    modules = [nfopersons.module]
    subject = getSubject(uri, metadata, modules)
    


def getSubject(uri, metadata, modules):
    
    pool = MainloopThreadPool()
    engine = Engine(pool)
    for module in modules:
        engine.registerModule(module)    

    def c(error, subject):
        if error:
            raise error

        print subject
        pool.quit()
    
    subject = Subject("", metadata)

    print "Running heimdall upon", subject

    engine.get(subject, c)

    try:
        pool.join()
    except KeyboardInterrupt:
        pool.quit()

    return subject


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) >= 2 else None)
