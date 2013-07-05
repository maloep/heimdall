import heimdall
from heimdall import tasks
from heimdall import resources
from heimdall import supplies, demands
from heimdall.predicates import *

import xml.etree.ElementTree as ET
       

class SearchCompanyCollector(tasks.SubjectTask):
    demand = [        
        demands.required("itemtype", "company")
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
        self.subject.emit('country', self.readTextElement(root, 'country'))
        self.subject.emit('city', self.readTextElement(root, 'city'))
                    
    
    def readTextElement(self, parent, elementName):
        element = parent.find(elementName)
        if(element != None and element.text != None):
            return element.text
        else:
            return ''
        

module = [ SearchCompanyCollector ]
