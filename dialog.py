def inRange(limits, value):
	if value >= limits[0] and value <= limits[1]:
		return True
	return False
	
def inEvents(reqs, events):
	for e in reqs:
		if e not in events or not events.get(e):
			return False
	return True

class MCNode:
	#required attributes to view and required events, given as a dictionary of booleans
	req_OP = [0, 100]
	req_CO = [0, 100]
	req_EX = [0, 100]
	req_AG = [0, 100]
	req_NE = [0, 100]
	required_events = []
	
	#dialog and id of the node
	text = ""
	id = 0
	
	#next sibling and first child
	sibling = False
	child = False
	
	#picture of the character as she says the line
	pictureID = 0
	
	terminal = False
	
	def __init__(self, treeid, req_OP, req_CO, req_EX, req_AG, req_NE, events, text, picture, childAttributes, term = False):
		self.id = treeid
		self.req_OP = req_OP
		self.req_CO = req_CO
		self.req_EX = req_EX
		self.req_AG = req_AG
		self.req_NE = req_NE
		self.required_events = events
		self.text = text
		self.pictureID = picture
		self.child = NPCNode(childAttributes)
		self.terminal = term
		
	def addNode(self, id, MCSwitch, attributes):
		if id[0] == self.id:
			self.child.addNode(id, MCSwitch, attributes)
		elif not self.sibling:
			self.sibling = MCNode(id, attributes[0], attributes[1],  attributes[2], attributes[3], attributes[4], attributes[5], attributes[6], attributes[7])
		else:
			self.sibling.addNode(id, MCSwitch, attributes)
			
	def findDialog(self, id):
		if id[0] == self.id:
			return self.child.findDialog(id)
		else:
			return self.sibling.findDialog(id)
			
	def findResponse(self, id, OP, CO, EX, AG, NE, events):
		if id == self.id:
			if self.sibling:
				responseList = self.sibling.findResponse(self.sibling.id, OP, CO, EX, AG, NE, events)
			else:
				responseList = []
			if inEvents(self.required_events, events) and inRange(req_OP, OP) and inRange(req_CO, CO) and inRange(req_EX, EX) and inRange(req_AG, AG) and inRange(req_NE, NE):
				responseList.append([self.id, self.text])
		elif id[0] == self.id:
			responseList = self.child.findResponse(id, OP, CO, EX, AG, NE, events)
		else:
			responseList = self.sibling.findResponse(self.sibling.id, OP, CO, EX, AG, NE, events)
		return responseList

class NPCNode:
	id = 0
	
	eff_rel = 0
	eff_HP = 0
	text = ""
	name = ""
	pictureID = 0
	
	required_relationship = 0
	required_events = []
	
	sibling = False
	child = False
	
	terminal = False
	
	def __init__(self, treeid, text, name, picture, req_rel = 0, req_events = [], eff_rel = 0, eff_HP = 0, term = False):
		self.id = treeid
		self.text = text
		self.name = name
		self.pictureID = picture
		self.required_relationship = req_rel
		self.required_events = req_events
		self.eff_rel = eff_rel
		self.eff_HP = eff_HP
		self.terminal = term
		
	def addNode(self, id, MCSwitch, attributes):
		if id[0] == self.id:
			if self.child:
				self.child.addNode(id[2:], MCSwitch, attributes)
			else:
				if MCSwitch:
					self.child = MCNode(id[2:0], attributes[0], attributes[1],  attributes[2], attributes[3], attributes[4], attributes[5], attributes[6], attributes[7])
				else:
					self.child = NPCNode(id[2:], attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], attributes[5], attributes[6], attributes[7])
		else:
			if self.sibling:
				self.sibling.addNode(id, MCSwitch, attributes)
			else:
				self.sibling = NPCNode(id, attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], attributes[5], attributes[6], attributes[7])
				
	def findDialog(self, id):
		if id == self.id:
			return [self.id, self.name, self.text, self.eff_rel, self.eff_HP]
		elif id[0] == self.id:
			if not self.terminal:
				return self.child.findDialog(id)
			else:
				return False
		else:
			return self.sibling.findDialog(id)
			
	def findNextDialogLevel(self, id, rel, events):
		if id[0] == self.id:
			if self.terminal:
				return False
			if len(id) == 1:
				return self.child.findNextDialog(id, rel, events)
			return self.child.findNextDialogLevel(id, rel, events)
		return self.sibling.findNextDialogLevel(id, rel, events)
		
	def findNextDialog(self, id, rel, events):
		if rel >= self.required_relationship and inEvents(self.required_events, events):
			return [self.id, self.name, self.text, self.eff_rel, self.eff_HP]
		else:
			return self.sibling.findNextDialog(id, rel, events)
			
	def findResponse(self, id, OP, CO, EX, AG, NE, events):
		if id[0] == self.id:
			if not self.terminal:
				return self.child.findResponse(id[2:], OP, CO, EX, AG, NE, events)
			return False
		else:
			return self.sibling.findResponse(id, OP, CO, EX, AG, NE, events)

class DialogTree(object):
	beginNode = False
	
	def __init__(self):
		pass
		
	def addNode(self, id, MCSwitch, attributes):
		if self.beginNode:
			self.beginNode.addNode(id, MCSwitch, attributes)
		else:
			self.beginNode = NPCNode(id, attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], attributes[5], attributes[6], attributes[7])
			
	def findDialog(self, id):
		return self.beginNode.findDialog(id)
		
	def findNextDialog(self, id, rel, events):
		return self.beginNode.findNextDialogLevel(id, rel, events)
		
	def findResponse(self, id, OP, CO, EX, AG, NE, events):
		return self.beginNode.findDialog(id, OP, CO, EX, AG, NE, events)