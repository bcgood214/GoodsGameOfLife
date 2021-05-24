import random, inspect, math
import tkinter as tk

# some globals initialized
init_geno = ["0"] * 30
map_width = 1000
map_height = 800
map = [None] * map_width
# orgs contains all of the living individuals
# possibility for orgs: store the organisms as x, y coordinates

## blocks structure was created to map multi-pixel cells to grid

#map = [None] * map_width
#for x in range(map_width):
#		map[x] = [None] * map_height
blocks_width = map_width//4
blocks_height = map_height//4
blocks = [None] * blocks_width
for x in range(blocks_width):
	blocks[x] = [None] * (blocks_height)
				
# idea: create a structure to quickly find all organisms based on
# block coordinates

# store x coordinates as keys, y coordinates as items in a list
# store coordinates for the current and next generation in seperate dicts
curcoords = {}
nextcoords = {}

class Node:
	
	# Node should contain either a value or a function
	def __init__(self, func=None, val=None, children=[], parent=None, brain=None, body=None):
		if func is not None and val is not None:
			raise "Node passed function and value"
			
		if func is not None:
			self.func = func
			argtup = inspect.getargspec(func)
			self.arity = len(argtup[args])
			self.type = 1
		
		if val is not None:
			self.type = 0
			self.value = val
		
		self.children = children
		self.parent = parent
		
		# the "body" and "brain" are passed through a pipeline of sorts
		self.brain = brain
		self.body = body
	
	# pos is for any other block that is relevant
	def run(self, pos=None):
		if self.func is not None:
			globals[self.func](self.brain, self.body, self.children, blocks, pos)
	
	def add_child(self, child):
		#self.children.append(child)
		#self.check_for_dups(self, child, self.children)
		self.children.append()
	
	# paths that lead to a node with the same function as the terminal of the child's path
	# should be removed
#	def check_for_dups(self, node, branch):
#		if not node.children:
#			if check_for_match(node, branch):
#				for c in branch:
#					if c.func == node.func:
#						branch.remove(c)
#					break
#		else:
#			for child in node.children:
#				self.check_for_dups(child, branch)
	
	def get_child(self, func):
		for c in self.children:
			if c.func == func:
				return c
		return None
			
class Brain:
	
	
	def __init__(self, root, body):
		self.root = root
		self.body = body
		self.branches = []
		# list for prioritizing what to search for
		self.priorities = ['check_for_prey', 'check_for_mate']
		self.memories = []
		# interactions involve communication between organisms
		
		# when one individual tried to reach out, an item will be added
		# to the interactions list for the receiving organism to process
		self.interactions = []
	
	# add the basic branches connected to the root
	def build_base(self):
		for f in root:
			self.branches.append(Node(func=f, parent="root"))
	
	def mutate(self, mutrate, nodes):
		# return if an empty list is passed
		if not nodes:
			return
		mutated = False
		for node in random.shuffle(nodes):
			val = random.random()
			if val < mutrate:
				mutated = True
				# select a random element in the list possible connections,
				# excluding the first element, which is a bool
				mutfunc = random.choice(conns[node.func][1:])
				# check if the function is already in a child node and return if it is
				if check_for_match(mutfunc, node.children):
					return
				else:
					node.add_child(Node(func=mutfunc, parent=node, owner=self, body=self.body))
		if not mutated:
			# if no mutation occurred, try a the children of a randomly selected node in the list
			self.mutate(mutrate, nodes=random.choice(nodes).children)
			# if a node with no children is passed, it should just return with mutation ever happening
	
	# engage in the thinking process by calling run on all of the root nodes for the different main branches
	def think(self):
		for branch in self.branches:
			branch.run()
		
			

class Individual:
	
	# initialize the genotype, memories, and brain
	def __init__(self, geno, x, y):
		self.genotype = geno
		self.brain = Brain(conns["root"], self)
		self.x = x
		self.y = y
		self.hunger = 1.0
	
	def mutation(self):
		for g in self.genotype:
			pm = random.randint(1, len(self.genotype)) # The probability of mutation is 1/n, with n being the length of the genome
			if pm == 2:
				if g == "0":
					g = "1"
				else:
					g = "0"
	
	# checks the genotype to decide if the organism eats plants
	def eatsplants(self):
		if self.genotype[15] == "1":
			return True
		return False
	
	# checks the genotype to decide if the organism is a herbivore
	def is_herb(self):
		if self.genotype[16] == "1":
			return True
		return False
	
	# calculate the size of an organism
	def get_size(self):
		# get the segment of the genotype that determines size
		wg = self.genotype[:12]
		
		# size = 2**n, with n starting at 0 and incremented by 1 for each bit set
		exp = 0
		for bit in wg:
			if bit == "1":
				exp += 1
		self.size = 2**wg
	
	# calculate the maximum number of cells an organism can move in one step
	def get_speed(self):
		sg = self.genotype[12:15]
		exp = 0
		for bit in sg:
			if bit == "1":
				exp += 1
		self.max_moves = 2**exp
	
	def get_stamina(self):
		self.stamina = 1/(math.log(self.size)*math.log(self.max_moves))
	
	# how much the hunger value increases (i.e. how much hungrier the organism gets) each step
	def hunger_step(self):
		self.hunger -= (1-self.stamina)/10
	
	# calculate the field of view
	def get_fov(self):
		fov_geno = self.genotype[17:20]
		exp = 0
		for bit in fov_geno:
			if bit == "1":
				exp += 1
		self.fov = 2**exp
	
	# set the memory capacity
	def memlimit(self):
		mg = self.genotype[25:]
		exp = 0
		for bit in mg:
			if bit == "1":
				exp += 1
		if exp:
			self.mem_limit = 2**exp
		else:
			self.mem_limit = 0
	
	# replenish hunger value
	def feed(self):
		self.hunger = 1.0
	
	def move(self, x, y):
		# set previous position on the map to None and new position to the instance of the individual
		blocks[self.x][self.y] = None
		blocks[x][y] = self
		# update coordinates
		self.x = x
		self.y = y
		
		

# mainly for selecting the child node to run	
def choose_node(nodes, pos=None):
	# choose a child to run stochastically, with the children weighted by position in the list
	# more recent additions should be towards the end and are more likely to be chosen
	if nodes is None:
		return None
	choice = random.choices(nodes, [i*i+1 for i in range(len(nodes))], k=1)[0]
	choice.run(pos)

# idea: check if coordinates are closer to target before setting variables in loop
def get_coords(xcap, ycap, x1, y1, xmod, ymod, curmap):
	curx = x1
	cury = y1
	for x in range(xcap):
		for y in range(ycap):
			if not occupied(x1+(x*xmod), y1+(y*ymod), curmap):
				curx = x1+(x*xmod)
				cury = y1+(y*ymod)
	return [curx, cury]

# returns just an x or y coordinate instead of both
def get_coord(cap, val, other, x, mod, curmap):
	cur = val
	for v in range(cap):
		if x:
			if not occupied(val+(v*mod), other, curmap):
				cur = val+(v*mod)
		else:
			if not occupied(other, val+(v*mod), curmap):
				cur = val+(v*mod)
	
	return cur

# for shifting an organism's coordinates from the current gen to the next
# if the organism died, this function should work if only one pair of coordinates is passed
def gen_change(x1, y1, x2=None, y2=None):
	curcoords[x1].remove(y1)
	if x2 is not None and y2 is not None:
		if x2 in nextcoords:
			nextcoords.append(y2)
		else:
			nextcoords[x2] = y2

def find_closest_pos(limit, x1, y1, x2, y2, curmap):
	curx = x1
	cury = y1
	
	xdiff = x2 - x1
	ydiff = y2 - y1
	
	# the region to look at will either be the limit,
	# or the absolute value of the difference if the second
	# position is within the limit for either the x or y coordinate
	xcap = limit if limit <= abs(xdiff) else abs(xdiff)
	ycap = limit if limit <= abs(ydiff) else abs(ydiff)
	
	coords = None
	if xdiff > 0 and ydiff > 0:
		coords = get_coords(xcap, ycap, x1, y1, 1, 1, curmap)
	elif xdiff > 0 and ydiff < 0:
		coords = get_coords(xcap, ycap, x1, y1, 1, -1, curmap)
	elif xdiff < 0 and ydiff > 0:
		coords = get_coords(xcap, ycap, x1, y1, -1, 1, curmap)
	elif xdiff < 0 and ydiff < 0:
		coords = get_coords(xcap, ycap, x1, y1, -1, -1, curmap)
	elif xdiff > 0 and ydiff == 0:
		coords = []
		coords = get_coord(xcap, x1, y1, True, 1, curmap)
		coords.append(cury)
	elif xdiff < 0 and ydiff == 0:
		coords = []
		coords = get_coord(xcap, x1, y1, True, -1, curmap)
		coords.append(cury)
	elif ydiff > 0 and xdiff == 0:
		coords = []
		coords.append(curx)
		coords.append(get_coord(ycap, y1, x1, False, 1, curmap))
	elif ydiff < 0 and xdiff == 0:
		coords = []
		coords.append(curx)
		coords.append(get_coord(ycap, y1, x1, False, -1, curmap))
	
	return coords

find_child(children, func):
	for c in children:
		if c.func == func:
			return c
	
	return None
	
## beginning of definitions for primitive set

# conns stores which functions can be called by a given function/node
conns = {}
conns['root'] = ['prioritize', 'check_interactions' 'search']

# set the priorities list
def prioritize(body, brain, children, curmap, pos=None):
	# call a child, or go off default conditions if there are no children
	if choose_node(children, pos) is None:
		if body.hunger < 2.0:
			brain.priorites[0] = 'check_for_prey'
			brain.priorities[1] = 'check_for_mate'
		else:
			brain.priorities[0] = 'check_for_mate'
			brain.priorities[1] = 'check_for_prey'

conns['prioritize'] = [True]

# see if any broadcasts/interactions came in and handle them appropriately
def check_interactions(body, brain, children, curmap, pos=None):
	for bc in brain.interactions:
		if bc == 1:
			find_child(children, 'mate_selection').choose_node(children, pos)
conns['check_interactions'] = [False, 'mate_selection']

# search will call all of its children,
# as checking for different things can server different purposes
def search(body, brain, children, curmap, pos=None):
	# search the surrounding area based on the organism's field of view
	for x in range(body.x-body.fov, body.x+body.fov):
		for y in range(body.y-body.fov, body.y+body.fov):
			if occupied(x, y, curmap):
				for p in brain.priorities:
					if p.run():
						# exit the loop if something was found
						break

conns['search'] = [False, 'check_for_prey', 'check_for_mate']

# get the number of bits that are different between two binary strings
def comp_geno(ind1, ind2):
	count = 0
	for bit in range(len(ind1.genotype)):
		if ind1[bit] != ind2[bit]:
			count += 1
	return count
		

def check_for_mate(body, brain, children, curmap, pos=None):
	if pos is not None and blocks[pos[0]][pos[1]] is Individual:
		potmate = block[pos[0]][pos[1]]
		# check if the other organism is a member of the same "species"
		if comp_geno(body, potmate) < 4:
			choose_node(children, (x, y))
			return True
	
	return False

conns['check_for_mate'] = [False, 'prop_mate']

def prop_mate(body, brain, children, curmap, pos=None):
	mate = blocks[pos[0]][pos[1]]
	# 1 is the code for a sexual proposition
	mate.interactions.append(1)

conns['prop_mate'] = [True]

def check_for_prey(body, brain, children, curmap, pos=None):
	# check to see if an organism has been spotted
	if pos is not None and blocks[pos[0]][pos[1]] is Individual:
		choose_node(children, (x, y))
		return True
	
	return False

conns['check_for_prey'] = [False, 'hunt']

def hunt(body, brain, children, curmap, pos=None):
	prey = curmap[pos[0]][pos[1]]
	# check if prey is within range to attack
	if abs(prey.x-body.x) <= body.max_moves and abs(prey.y-body.y) <= body.max_moves:
		# determine victor in conflict based on size
		winner = random.choices([0, 1], weights=[prey.size, body.size], k=1)
		if winner[0]:
			# if the organism prevails, it will feed off its fallen prey and move to its last position
			#orgs[pos[0]].remove[pos[1]]
			body.feed()
			body.move(pos[0], pos[1])
		else:
			# if the organism fails, it will die
			curmap[body.x][body.y] = None
			#orgs[body.x].remove(body.y)
	else:
		# if there are no children to run, simply find the closest open cell and move there
		if children == []:
			nextpos = find_closest_pos(body.max_moves, body.x, body.y, prey.x, prey.y, curmap)
			#body.move(pos[0], pos[1])
			body.move(nextpos[0], nextpos[1])
		else:
			choose_node(children, (x, y))

conns['hunt'] = [True]

## end of definitions for primitive set

# search a brain for a specified function
def search_nodes(nodes, func):
	# return none if an empty list is passed
	if nodes == []:
		return None
	for node in nodes:
		if node.func == func:
			return node
		else:
			# search the child, returning the result if it is not None
			
			# a non-None value should only be returned if the function was found
			res = search_brain(node.children, func)
			if res is not None:
				return res
	return None

# check to see if the function passed is contained in any of the nodes
def check_for_match(func, nodes):
	for node in nodes:
		if node.func == func:
			return True
	return False

# get all children found among two brains
def get_options(p1, p2, func):
	qry1 = search_brain(p1, func)
	qry2 = search_brain(p2, func)
			
	options =  []
			
	# options is meant to consist of the children of the node(s) containing
	# the function passed
	if qry1 is not None:
		for node in qry1:
			options.append(node)
	if qry2 is not None:
		for node in qry2:
			# if the function has not already been included from the first parent,
			# add it to the list
			if not check_for_match(node.func, options):
				options.append(node)
	
	return options

# add a node, taking the brain of the child and two parents,
# along with the genetically defined size limit, as arguments.
def add_node(cb, pb1, pb2, limit):
	branches = random.shuffle(cb.branches)
	for branch in branches:
		nodes = get_ngroup(branch)
		nodes = random.shuffle(nodes)
		for node in nodes:
			# get the nodes in the parents' brains which are children of the nodes
			# for the specified function
			options = get_options(pb1.branches, pb2.branches, node.func)
			
			if len(options) > 0:
				# add a child to the node in the child's brain by randomly
				# selecting from the options
				choice = random.choices(options, k=1)[0]
				node.add_child(choice)
				# if the newly added node contains a non-terminal function,
				# build out the branch using the parents' nodes until a terminal
				# is reached
				if not conns[choice][0]:
					terminal = False
					while not terminal:
						options = get_options(pb1.branches, pb2.branches, choice)
						node = node.get_child(choice.func)
						choice = random.choices(options, k=1)[0]
						node.add_child(choice)
						if conns[choice][0] == True:
							terminal = True

# get a group of nodes in an organism's tree
def get_ngroup(node, group=[]):
	group.append(branch)
	for c in node.children:
		get_ngroup(branch, group)
	return group
		

# takes two strings and the probability of crossover
def sp_crossover(s1, s2, prob):
	if len(s1) > 2 and random.rand() > prob:
		point = random.randint(1, len(s1) - 1)
		child = s1[0:point] + s2[point:]
		return child

#def mutation(geno):
#	for g in geno:
#		pm = random.randint(1, len(geno)) # The probability of mutation is 1/n, with n being the length of the genome
#		if pm == 2:
#			if g == "0":
#				g = "1"
#			else:
#				g = "0"
	
#	return geno

# check if cell is occupied
def occupied(x, y, curmap):
	if curmap[x][y] is None:
		return False
	return True

# find an open cell
def findpos(curmap, width, height):
	x = random.randint(0, width-1)
	y = random.randint(0, height-1)
	if not occupied(x, y, curmap):
		return x, y
	else:
		return findpos(curmap, width, height)
#	for y in range(height):
#		if not occupied(x, y):
#			return x, y

# generate the initial population, including assignments to cells
def gen_initpop(size, width, height, curmap):
	#orgmap = []
	for i in range(size):
		x, y = findpos(curmap, width, height)
		curmap[x][y] = Individual(init_geno, x, y)
		#orgs[x].append(y)
		if x in curcoords:
			curcoords[x].append(y)
		else:
			curcoords[x] = [y]
	return curmap

# traverse the list of living organism, engaging in thought for each
def orgloop(curmap):
	for org in curcoords:
		for ind in curcoords[org]:
			curmap[org][ind].brain.think()
	
if __name__ == "__main__":

	def print_info(curmap):
		str = ""
		for org in curcoords:
			for ind in curcoords[org]:
				print(curmap[org][ind].genotype)
#				str += curmap[org][ind].genotype + "; "
#		print(str)
		
				
	
#	map = gen_initpop(100, map_width, map_height, map)
	blocks = gen_initpop(100, blocks_width, blocks_height, blocks)
	while True:
		for i in range(100):
			orgloop(blocks)
		print_info(blocks)
		uin = input("Press Enter any to move forward a generation, or any other key to exit: ")
		if uin != "":
			break
#	for x in range(map_width):
#			for y in range(map_height):
#				if occupied(x, y, map):
#					print("occupied")
#					can.create_rectangle(x, y, x+4, y+4, fill="red")
