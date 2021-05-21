import random, inspect, math
import tkinter as tk

# some globals initialized
init_geno = ["0"] * 60
map_width = 1000
map_height = 800
map = [None] * map_width

## blocks structure was created to map multi-pixel cells to grid

#map = [None] * map_width
#for x in range(map_width):
#		map[x] = [None] * map_height
blocks_width = map_width//4
blocks_height = map_height//4
blocks = [None] * blocks_width
for x in range(blocks_width):
	blocks[x] = [None] * (blocks_height)
				

class Node:
	
	# Node should contain either a value or a function
	def __init__(self, func=None, val=None, children=[], parent=None, owner=None, body=None):
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
		self.owner = owner
		self.body = body
	
	# pos is for any other block that is relevant
	def run(self, pos=None):
		if self.func is not None:
			globals[self.func](self.owner, self.body, self.children, blocks, pos)
	
	def add_child(self, child):
		self.children.append(child)
	
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
	
	# add the basic branches connected to the root
	def build_base(self):
		for f in root:
			self.branches.append(Node(func=f, parent="root"))
	
	def mutate(self, mutrate, nodes=self.branches):
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
		
			

class Individual:
	
	# initialize the genotype, memories, and brain
	def __init__(self, geno, x, y):
		self.genotype = geno
		self.memories = []
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
		
	
	
## beginning of definitions for primitive set

# conns stores which functions can be called by a given function/node
conns = {}
conns['root'] = ['search']

def search(body, brain, children, curmap, pos=None):
	# search the surrounding area based on the organism's field of view
	for x in range(body.x-body.fov, body.x+body.fov):
		for y in range(body.y-body.fov, body.y+body.fov):
			if occupied(x, y, curmap):
				for c in children:
					c.run((x, y))
conns['search'] = [False, 'check_for_prey']

def check_for_prey(body, brain, children, curmap, pos=None):
	# check to see if an organism has been spotted
	if pos is not None and blocks[pos[0]][pos[1]] is Individual:
		for c in children:
			c.run(pos)
conns['check_for_prey'] = [False, 'hunt']

def hunt(body, brain, children, curmap, pos=None):
	prey = curmap[pos[0]][pos[1]]
	# check if prey is within range to attack
	if abs(prey.x-body.x) <= body.max_moves and abs(prey.y-body.y) <= body.max_moves:
		# determine victor in conflict based on size
		winner = random.choices([0, 1], weights=[prey.size, body.size], k=1)
		if winner[0]:
			# if the organism prevails, it will feed off its fallen prey and move to its last position
			body.feed()
			body.move(pos[0], pos[1])
		else:
			# if the organism fails, it will die
			curmap[body.x][body.y] = None
	else:
		# if there are no children to run, simply find the closes open cell and move there
		if children == []:
			nextpos = find_closest_pos(body.x, body.y, prey.x, prey.y, curmap)
			body.move(pos[0], pos[1])
		else:
			for c in children:
				c.run()
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
	for node is nodes:
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
	return curmap
	
if __name__ == "__main__":

	def paint_cells(curmap, canvas, width, height):
		for x in range(width):
			for y in range(height):
				if occupied(x, y, curmap):
					canvas.create_rectangle(x*4, y*4, (x+1)*4, (y+1)*4, fill="red")
	
#	map = gen_initpop(100, map_width, map_height, map)
	blocks = gen_initpop(100, blocks_width, blocks_height, blocks)
	root = tk.Tk()
	can = tk.Canvas(root, bg="white", height=800, width=1000)
	can.pack()
	paint_cells(blocks, can, blocks_width, blocks_height)
#	for x in range(map_width):
#			for y in range(map_height):
#				if occupied(x, y, map):
#					print("occupied")
#					can.create_rectangle(x, y, x+4, y+4, fill="red")
	root.mainloop()
