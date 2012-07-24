import types
import re
from utils import Enum

match = Enum([ "NEVER", "NO", "YES" ])

class demand(object):
	def matches(self, subject):
		raise NotImplementedError("Need must implement matches")

class predicateObjectDemand(demand):
	def __init__(self, predicate, object = None):
		self.predicate = predicate
		self.object = object# if object != None else ""

# TODO This should be in task rather
#		if isinstance(self.predicate, types.ListType) or isinstance(self.predicate, types.TupleType):
#			self.predicate = self.predicate[0]
#			self.object = self.predicate[1]

		if not isinstance(self.predicate, types.StringTypes):
			raise ValueError("Predicate must be string type")

		if not (isinstance(self.object, types.StringTypes) or self.object == None):
			raise ValueError("Object must be string type or None")

	def matches(self, subject):
		obj = subject[self.predicate]
		if obj and self.object:
			return re.search(self.object, obj) != None
		else:
			return obj != None

	def __repr__(self):
		return self.__class__.__name__ + " " + self.predicate + ": " + str(self.object)

# Optional predicate, object keypair. The task will be put on hold if any task may provide the pair but will run if it is not provided
class optional(predicateObjectDemand):
	pass

# A hard dependency, the task will never run if its not provided. The task will wait until on any task which might provide or replace the key-value-pair
class required(predicateObjectDemand):
	pass

# A key-value-pair which may NOT exist on subject for this task to run, the task will be scheduled after any task which might provide or replace the key-value-pair and will
# be removed from queue if one emits the key-value-pair.
class none(predicateObjectDemand):
	def matches(self, subject):
		return not super(none, self).matches(subject)

class requiredClass(demand):
	def __init__(self, Class, allowExtended = False):
		self.Class = Class
		self.allowExtended = allowExtended

	def matches(self, subject):
		if self.Class == subject.Class: # Input and sought class are same
			return True
		elif re.match(subject.Class, self.Class): # Input class may extend towards sought class, but it has not reached there yet.
			return False
		elif re.match(self.Class, subject.Class): # Input class is extended version of sought class
			return True if self.allowExtended else match.NEVER
		else: # Input class will never reach sought class, diamond problem
			return match.NEVER

# Subject creation, a task will be scheduled after a subject which fits the given regexp and removed otherwise.
class subject(demand):
	def __init__(self, subject):
		self.subject = subject

		if not isinstance(self.subject, types.StringTypes):
			raise ValueError("Subject must be string type")

	def matches(self, subject):
		return True if re.search(self.subject, subject.uri) != None else match.NEVER
