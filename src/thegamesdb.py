import heimdall
from heimdall import tasks
from heimdall import resources
from heimdall import supplies, demands
from heimdall.predicates import *

import json
import os, glob
import xml.etree.ElementTree as ET
import urllib
from urllib import unquote_plus, quote_plus

tgdb_image_base = "http://thegamesdb.net/banners/"


def downloadArtwork(url, folder, title):
    searchPath = os.path.join(folder, title +".*")
    #TODO glob has some limitations (i.e. issues with [])
    files = glob.glob(searchPath)
    if(len(files) == 0):
        fileExtension = os.path.splitext(url)[1]
        newFile = os.path.join(folder, "%s%s" %(title, fileExtension))
        print "File does not exist. Start download: " +newFile
        
        try:
            urllib.urlretrieve( url, newFile)
        except Exception, (exc):
            print "Could not create file: '%s'. Error message: '%s'" %(newFile, str(exc))
    else:
        print "File already exist. Won't download artwork for " +title


class DownloadBoxfront(tasks.SubjectTask):
    demand = [
        demands.required("Filetypeboxfront")
    ]
    
    supply = []

    def run(self):
        print 'Download boxfront: ' +self.subject["Filetypeboxfront"]
        url = tgdb_image_base + self.subject["Filetypeboxfront"]
        folder = self.subject["pathboxfront"]
        title = self.subject[dc.title]
        
        downloadArtwork(url, folder, title)
        

class DownloadFanart(tasks.SubjectTask):
    demand = [
        demands.required("Filetypefanart")
    ]
    
    supply = []

    def run(self):
        print 'Download fanart: ' +self.subject["Filetypefanart"]
        
        url = tgdb_image_base + self.subject["Filetypefanart"]
        folder = self.subject["pathfanart"]
        title = self.subject[dc.title]
        
        downloadArtwork(url, folder, title)
        

class SearchGameCollector(tasks.SubjectTask):
    demand = [
        demands.required(dc.title),
        demands.required("itemtype", "game"),
        demands.required("platform")
    ]

    supply = [
        supplies.emit("Filetypeboxfront"),
        supplies.emit("Filetypefanart")
    ]

    def require(self):
        title = self.subject[dc.title]
        platform = self.subject["platform"]
        path = "http://thegamesdb.net/api/GetGame.php?name=%s&platform=%s" %(quote_plus(title), quote_plus(platform))
        print path

        return resources.SimpleResource(path)

    def run(self, resource):
        
        root = ET.fromstring(resource)

        gameRows = root.findall('Game')
        for gameRow in gameRows:
            gameTitle = self.readTextElement(gameRow, 'GameTitle')
            #TODO name quessing
            if(gameTitle == self.subject[dc.title]):
                gameid = self.readTextElement(gameRow, 'id')
                print "found match: id = %s" %gameid
                self.subject.emit('gameid', gameid)
                self.subject.emit('Description', self.readTextElement(gameRow, 'Overview'))
                self.subject.emit('Genre', self.readTextElement(gameRow, 'Genres/genre'))
                self.subject.emit('Players', self.readTextElement(gameRow, 'Players'))
                self.subject.emit('Developer', self.readTextElement(gameRow, 'Developer'))
                self.subject.emit('Publisher', self.readTextElement(gameRow, 'Publisher'))
                self.subject.emit('ReleaseYear', self.readTextElement(gameRow, 'ReleaseDate'))
                
                boxartRows = gameRow.findall('Images/boxart')
                for boxartRow in boxartRows:
                    side = boxartRow.attrib.get('side')
                    if(side == 'front'):
                        self.subject.emit('Filetypeboxfront', self.readTextElement(boxartRow, ""))
                                
                self.subject.emit('Filetypefanart', self.readTextElement(gameRow, 'Images/fanart/original'))
                break
            
    
    def readTextElement(self, parent, elementName):
        element = parent.find(elementName)
        if(element != None and element.text != None):
            return element.text
        else:
            return ''
        

module = [ SearchGameCollector, DownloadBoxfront, DownloadFanart ]
