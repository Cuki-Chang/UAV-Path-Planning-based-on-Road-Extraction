import pygame
import math
from queue import PriorityQueue

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")
pygame.font.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
LIGHTGREY = (205 , 205 , 205)

class Spot:#keeps track of location of nodes, keeps track of its neighbours, and keeps track of its colours, wall, end node, start node, etc.
	def __init__(self, row, col, width, total_rows): # keep track of how many rows
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
		self.weight = 0

	def get_pos(self):#RED = we already looked at it, Black = wall, avoid, WHITE = not looked at
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def is_weight(self):
		return self.color == LIGHTGREY

	def reset(self):
		self.color = WHITE
		self.weight = 0

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_weight(self):
		self.color = LIGHTGREY

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def increase_weight(self):
		self.weight += 1

	def check_barrier(self):
		if self.color == BLACK:
			return True
		else:
			return False

	def check_weight(self):
		if self.color == LIGHTGREY:
			return True
		else:
			return False

	# TODO def draw_weight(self, surface):
		

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
                                self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):#def __lt__ , lt means less than, how we handle comparing 2 spots together
		return False #Defines the behaviour of the less-than operator <


def h(p1, p2): # heuristic function : function that ranks alternative paths in a search function
	x1, y1 = p1	# gives p1 = (1,2)
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start)) #puts the start node and its information into open set :(F_value,No. which entered to know who entered first in case of ties, node name)
	came_from = {} # keep track of which node did this node come from, 
	g_score = {spot: float("inf") for row in grid for spot in row} #table which stores all the g_score as inf
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row} #set all f_score of spot to infinity
	f_score[start] = h(start.get_pos(), end.get_pos()) # the manhattan distance from start to end node

	open_set_hash = {start} #priority queue has no functionality to tell us what elements exist in the queue, this helps us do so

	while not open_set.empty(): # algorithm runs until open_set is empty
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] # gets 2nd index in the priority queue, the open_set stores (f_score, count, node) so we want the node
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()

			return True

		for neighbor in current.neighbors:# start algorithm, first run through is go through start nodes neighbours
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score + current.weight
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start: #close out those nodes that has already been considered
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			
			spot.draw(win)

			if spot.weight >0 : # earlier as separate function didn't work as didn't pygame.display.update
				font = pygame.font.SysFont('comicsans', 20, bold=True)
				text = str(spot.weight)

				label = font.render(text, 1, (0,0,0)) #(text, antialias, color)
				win.blit(label, (spot.x, spot.y))


	draw_grid(win, rows, width)
	pygame.display.update()

'''
def draw_weight(win, grid, rows, width):

	for row in grid:
		for spot in row:
			if spot.weight >0 :
				font = pygame.font.SysFont('comicsans', 40, bold=True)
				text = str(spot.weight)

				label = font.render(text, 1, (0,0,0)) #(text, antialias, color)
				win.blit(label, (spot.x, spot.y))

'''

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		#draw_weight(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					
					if spot.check_barrier():
						spot.increase_weight()
						spot.make_weight()
					elif not spot.check_barrier() and not spot.check_weight():
						spot.make_barrier()

					else: 
						spot.increase_weight()



				

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)# x = lambda: print("Hello"), x() will result in "Hello"

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)
