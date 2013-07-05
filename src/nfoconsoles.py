import heimdall
from heimdall import tasks
from heimdall import resources
from heimdall import supplies, demands
from heimdall.predicates import *

import xml.etree.ElementTree as ET
       

class SearchConsoleCollector(tasks.SubjectTask):
    demand = [        
        demands.required("itemtype", "console")
    ]

    supply = []

    def require(self):
        title = self.subject[dc.title]
        basepath = self.subject['basepath']
        path = "%s/%s.nfo" %(basepath, title)
        print path

        result = resources.SimpleResource(path)
        return result

    def run(self, resource):
        
        root = ET.fromstring(resource)
        
        self.subject.emit('description', self.readTextElement(root, 'description'))
        self.subject.emit('manufacturer', self.readTextElement(root, 'genre'))
        self.subject.emit('developer', self.readTextElement(root, 'developer'))
        self.subject.emit('year', self.readTextElement(root, 'year'))
        self.subject.emit('cpu', self.readTextElement(root, 'cpu'))
        self.subject.emit('ram', self.readTextElement(root, 'ram'))
        self.subject.emit('graphics', self.readTextElement(root, 'graphics'))
        self.subject.emit('sound', self.readTextElement(root, 'sound'))
        self.subject.emit('display', self.readTextElement(root, 'display'))
        self.subject.emit('media', self.readTextElement(root, 'media'))
        self.subject.emit('maxControllers', self.readTextElement(root, 'maxControllers'))        
                    
    
    def readTextElement(self, parent, elementName):
        element = parent.find(elementName)
        if(element != None and element.text != None):
            return element.text
        else:
            return ''
        

module = [ SearchConsoleCollector ]
