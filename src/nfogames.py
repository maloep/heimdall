import heimdall
from heimdall import tasks
from heimdall import resources
from heimdall import supplies, demands
from heimdall.predicates import *

import xml.etree.ElementTree as ET

       

class SearchGameCollector(tasks.SubjectTask):
    demand = [
        demands.required(dc.title),
        demands.required("itemtype", "game")        
    ]

    supply = []

    def require(self):
        title = self.subject[dc.title]
        console = self.subject['console']
        basepath = self.subject['basepath']        
        
        path = "%s/%s/%s.nfo" %(basepath, console, title)
        print path

        result = resources.SimpleResource(path)
        return result

    def run(self, resource):
        
        root = ET.fromstring(resource)
        
        self.subject.emit('description', self.readTextElement(root, 'plot'))
        self.subject.emit('genre', self.readTextElement(root, 'genre'))
        self.subject.emit('maxplayers', self.readTextElement(root, 'maxPlayer'))
        self.subject.emit('developer', self.readTextElement(root, 'developer'))
        self.subject.emit('publisher', self.readTextElement(root, 'publisher'))
        self.subject.emit('year', self.readTextElement(root, 'year'))
        self.subject.emit('region', self.readTextElement(root, 'region'))
        self.subject.emit('media', self.readTextElement(root, 'media'))
        self.subject.emit('perspective', self.readTextElement(root, 'perspective'))
        self.subject.emit('controller', self.readTextElement(root, 'controller'))
        self.subject.emit('version', self.readTextElement(root, 'version'))
        self.subject.emit('mobyRank', self.readTextElement(root, 'mobyRank'))
        self.subject.emit('mobyScore', self.readTextElement(root, 'mobyScore'))
        self.subject.emit('mobyScoreVotes', self.readTextElement(root, 'mobyScoreVotes'))
        self.subject.emit('thegamesdbScore', self.readTextElement(root, 'thegamesdbScore'))
        self.subject.emit('thegamesdbVotes', self.readTextElement(root, 'thegamesdbVotes'))
        self.subject.emit('language', self.readTextElement(root, 'language'))
        self.subject.emit('executiveProducer', self.readTextElement(root, 'executiveProducer'))
        self.subject.emit('producer', self.readTextElement(root, 'producer'))
        self.subject.emit('director', self.readTextElement(root, 'director'))
        self.subject.emit('programmer', self.readTextElement(root, 'programmer'))
        self.subject.emit('graphicDesigner', self.readTextElement(root, 'graphicDesigner'))        
        self.subject.emit('soundComposer', self.readTextElement(root, 'soundComposer'))
        self.subject.emit('illustrator', self.readTextElement(root, 'illustrator'))
        self.subject.emit('manualEditor', self.readTextElement(root, 'manualEditor'))
        self.subject.emit('translator', self.readTextElement(root, 'translator'))
        
        self.subject.emit('romCollection', self.readTextElement(root, 'romCollection'))
        self.subject.emit('completed', self.readTextElement(root, 'completed'))
        self.subject.emit('broken', self.readTextElement(root, 'broken'))
        self.subject.emit('dateAdded', self.readTextElement(root, 'dateAdded'))
        self.subject.emit('dateModified', self.readTextElement(root, 'dateModified'))
        self.subject.emit('lastPlayed', self.readTextElement(root, 'lastPlayed'))
        self.subject.emit('isFavorite', self.readTextElement(root, 'isFavorite'))
        self.subject.emit('launchCount', self.readTextElement(root, 'launchCount'))
        
                    
    
    def readTextElement(self, parent, elementName):
        element = parent.find(elementName)
        if(element != None and element.text != None):
            return element.text
        else:
            return ''
        

module = [ SearchGameCollector ]
