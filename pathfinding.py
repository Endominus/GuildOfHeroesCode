


def find_path(gamestate, actor, target):
	obstacles = []
	it = gamestate.allsprites.__iter__()
	
	try:
		while(True):
			n = it.next()
			if((not n.passable) & (n != actor) & (n != target)):
				obstacles.append(n)
	except StopIteration:
		pass
	
	blockSize = 40
	grid = [[0]*(gamestate.levelWidth/blockSize) for i in range(gamestate.levelHeight/blockSize)]
	for r in grid:
		print r

	



	

		


