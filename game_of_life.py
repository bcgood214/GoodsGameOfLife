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
	
	def run(self):
		if self.func is not None:
			globals[self.func](self.owner, self.body, self.children)
	
	def add_child(self, child):
		self.children.append(child)
			
class Brain:
	
	
	def __init__(self, root, body):
		self.root = root
		self.body = body
		self.branches = []
	
	# add the basic branches connected to the root
	def build_base(self):
		for f in root:
			self.branches.append(Node(func=f, parent="root"))
			

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
conns['root'] = []

def search(body, brain, children, curmap):
	# search the surrounding area based on the organism's field of view
	for x in range(body.x-body.fov, body.x+body.fov):
		for y in range(body.y-body.fov, body.y+body.fov):
			if occupied(x, y, curmap):
				for c in children:
					c.run()

## end of definitions for primitive set

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
