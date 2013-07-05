import heimdall
from heimdall import tasks
from heimdall import resources
from heimdall import supplies, demands
from heimdall.predicates import *

import xml.etree.ElementTree as ET
       

class SearchPersonCollector(tasks.SubjectTask):
    demand = [        
        demands.required("itemtype", "person")
    ]

    supply = []

    def require(self):
        title = self.subject[dc.title]
        basepath = self.subject['basepath']
        path = "%s/%s.nfo" %(basepath, title)
        
        result = resources.SimpleResource(path)

        return result

    def run(self, resource):
        
        try:
            root = ET.fromstring(resource)
        except:
            return
        
        self.subject.emit('description', self.readTextElement(root, 'description'))
        self.subject.emit('country', self.readTextElement(root, 'country'))
        self.subject.emit('company', self.readTextElement(root, 'company'))
                    
    
    def readTextElement(self, parent, elementName):
        element = parent.find(elementName)
        if(element != None and element.text != None):
            return element.text
        else:
            return ''
        

module = [ SearchPersonCollector ]
