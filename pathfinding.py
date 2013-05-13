import Queue
import math

def find_path(gamestate, actor, target):
	it = gamestate.allsprites.__iter__()
	
	blockSize = 64
	
	grid = [[' ']*(gamestate.levelWidth/blockSize) for i in range(2*gamestate.levelHeight/blockSize)]
	
	try:
		while(True):
			n = it.next()
			if((not n.passable) & (n != actor) & (n != target)):
				x = n.x_pos+blockSize/2
				y = n.y_pos+blockSize/2
				x = int(x/blockSize)
				y = int(y/blockSize)
				grid[y][x]='x'
	except StopIteration:
		pass
	
	initx = int((actor.x_pos+blockSize/2)/blockSize)
	inity = int((actor.y_pos+blockSize/2)/blockSize)
	
	targetx = int((target.x_pos+blockSize/2)/blockSize)
	targety = int((target.y_pos+blockSize/2)/blockSize)

	qu = Queue.PriorityQueue()
	initp = Path()
	initp.nodes = [(initx, inity)]
	initp.length = 0
	qu.put ((abs(initx-targetx)+abs(inity-targety), initp), False)
	timeout = 500

	result = Path()
	result.nodes = [(initx, inity)]

	while timeout>0:
		timeout = timeout - 1
		position = qu.get(False)[1]
		
		if position.nodes[len(position.nodes)-1] == (targetx, targety):
			result = position
			break

		news = _neighbors(position.nodes[len(position.nodes)-1])
		for n in news:
			if (grid[n[1]][n[0]] == ' ')and (not (n in position.nodes)):
				newPath = Path.extend(position, n)
				qu.put((abs(targetx - n[0]) + abs(targety - n[1]) + newPath.length, newPath), False)
		result = newPath
	if timeout==0:
	    print "Warning: Failed to find a path"

	expanded_result = []
	while (len(result.nodes) > 0):
	    n = result.nodes.pop()
	    expanded_result.append(((n[1]*blockSize), (n[0]*blockSize)))
	#Don't go to the node we're already in
	expanded_result.pop()
	return expanded_result
	

#pos is a position tuple t = (x, y)
#returns a list of neighbors
def _neighbors(pos):
	return [
		(pos[0]-1, pos[1] -1),
		(pos[0]+1, pos[1] -1),
		(pos[0]-1, pos[1] +1),
		(pos[0]+1, pos[1] +1),
		(pos[0], pos[1] -1),
		(pos[0], pos[1] +1),
		(pos[0]-1, pos[1]),
		(pos[0]+1, pos[1]),
		]
	
class Path:
	length = 0
	#nodes is a list of tuples t = (x, y)
	nodes = 0

	def __init__(self):
		length = 0
		nodes = 0
	
#	#copy constructor
#	def __init__(self, old):
#		length = old.length
#		nodes = list(old.nodes)
	
	#copy with new node appended
	def extend(self, new_node):
		r = Path()
		r.length = self.length
		r.nodes = list(self.nodes)
		dx = abs(r.nodes[len(r.nodes)-1][0] - new_node[0])
		dy = abs(r.nodes[len(r.nodes)-1][1] - new_node[1])
		
		#using cases for this avoids taking a square root
		if dx == 0:
			r.length += dy
		elif dy == 0:
			r.length += dx
		else:
			r.length += 1.4142
			#sqrt(2)

		r.nodes.append(new_node)

		return r




