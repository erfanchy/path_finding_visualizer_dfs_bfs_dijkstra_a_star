import pygame 
from queue import PriorityQueue 
from queue import Queue 
from queue import LifoQueue 

width = 1000
win = pygame.display.set_mode((width,width))
#pygame.display.set_caption("Depth First Search")
#pygame.display.set_caption("Breadth First Search")
pygame.display.set_caption("Dijkstra's Algorithm")
#pygame.display.set_caption("A*  Shortest Pathfinding Algorithm")

CLOSE = (188,143,143) 
OPEN = (216,191,216)
BACKGROUND = (255,228,196)
END = (0,0,128)
START = (128,0,0) 
BARRIER = (128,128,0) 
GRID = (0,0,0) 
PATH = (255,69,0)

class Square_Box :  
	def __init__(self,row,col,width,total_rows) : 

		self.row = row 
		self.col = col 
		self.width = width 
		self.total_rows = total_rows
		self.neighbors = [] 
		self.color_of_cube = BACKGROUND
		self.x = row * width 
		self.y = col* width

	def get_x_y_position(self) : 

		return self.row,self.col 

	def is_visited(self) : 

		return self.color_of_cube == CLOSE 

	def is_not_visited(self) : 

		return self.color_of_cube == OPEN

	def is_barrier(self) : 

		return self.color_of_cube == BARRIER

	def is_start(self): 

		return self.color_of_cube == START 

	def is_end(self) : 

		return self.color_of_cube == END 

	def clear_all(self) : 

		self.color_of_cube  = BACKGROUND

	def make_start(self) :

		self.color_of_cube = START 

	def make_end(self) : 

		self.color_of_cube = END 

	def make_barrier(self) : 

		self.color_of_cube = BARRIER

	def make_path(self) : 

		self.color_of_cube = PATH 

	def make_visited(self) :

		self.color_of_cube = CLOSE 

	def make_not_visited(self) : 

		self.color_of_cube = OPEN 


	def draw(self,win) : 

		pygame.draw.rect(win,self.color_of_cube,(self.x,self.y,self.width,self.width))

	def update_neighbors(self,grid) : 
		self.neighbors = []
		if self.col > 0 and not grid[self.row][self.col-1].is_barrier() : 
			self.neighbors.append(grid[self.row][self.col-1])
		if self.row < self.total_rows -1 and not grid[self.row+1][self.col].is_barrier() : 
			self.neighbors.append(grid[self.row + 1][self.col])
		if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier() : 
			self.neighbors.append(grid[self.row][self.col+1])
		if self.row > 0 and not grid[self.row -1][self.col].is_barrier() : 
			self.neighbors.append(grid[self.row-1][self.col])

def make_grid(rows,width) : 

	grid = [] 

	distance_between_square_boxes = width //rows 

	for i in range(rows) : 

		grid.append([])

		for j in range(rows) : 

			square_box = Square_Box(i,j,distance_between_square_boxes,rows)
			grid[i].append(square_box)
	
	return grid

def draw_grid(win,rows,width) : 

	distance_between_square_boxes = width // rows 

	for i in range(rows) : 
		pygame.draw.line(win,GRID,(0,i * distance_between_square_boxes), (width, i * distance_between_square_boxes))

		for j in range (rows) : 

			pygame.draw.line(win,GRID,(j * distance_between_square_boxes,0),(j * distance_between_square_boxes,width))


def draw(win,grid,rows,width) : 

	win.fill(BACKGROUND)

	for row in grid : 

		for square in row  : 

			square.draw(win) 

	draw_grid(win,rows,width)

	pygame.display.update() 

def clicking_position_determination(pos,rows,width) : 

	distance_between_square_boxes = width // rows 
	y,x = pos
	row = y // distance_between_square_boxes
	col = x // distance_between_square_boxes

	return row , col 

def manhattan_h_score(p1,p2) : 
	x1,y1 = p1 
	x2,y2 = p2 
	return abs(x1-x2) + abs(y1-y2)

def show_path(came_from,start,current,draw) : 
	while current in came_from : 
		current = came_from[current]
		if current == start : 
			continue
		current.make_path()
		draw() 

def depth_first_search(draw,grid,start,end) : 

	stack= LifoQueue()
	stack.put(start) 
	visited = {start}
	came_from = {} 

	while not stack.empty() : 
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 
				pygame.quit() 

		current = stack.get()
		
		if current == end : 
			show_path(came_from,start,end,draw)
			end.make_end()
			start.make_start()
			return True 

		for neighbor in current.neighbors : 

			if neighbor not in visited : 
				came_from[neighbor] = current 
				stack.put(neighbor)
				visited.add(neighbor) 
				neighbor.make_visited()

		draw()

		if current!=start : 
			current.make_not_visited() 

	return False 

def dijkstra(draw,grid,start,end) : 

	count = 0 
	visited = PriorityQueue() 
	visited.put((0,count,start))
	came_from = {} 
	distance = {square:float("inf") for row in grid for square in row}
	distance[start] = 0 
	visited_dictionary = {start}

	while not visited.empty() : 
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 
				pygame.QUIT() 

		current = visited.get()[2]
		visited_dictionary.remove(current)
		if current == end : 
			show_path(came_from,start,end,draw)
			end.make_end() 
			start.make_start() 
			return True 

		for neighbor in current.neighbors : 
			current_distance = distance[current] + 1 
			if current_distance < distance[neighbor] :
				came_from[neighbor] = current 
				distance[neighbor] = current_distance
				if neighbor not in visited_dictionary: 
					count+=1 
					visited.put((distance[current],count,neighbor))
					visited_dictionary.add(neighbor)
					neighbor.make_visited()

		draw() 
		if current!=start : 
			current.make_not_visited() 

	return False 

def breadth_first_search(draw,grid,start,end) : 
	nodes = Queue() 
	nodes.put(start)
	visited = {start}
	came_from = {} 

	while not nodes.empty() : 
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 
				pygame.quit() 

		current = nodes.get() 
		if current == end : 

			show_path(came_from,start,end,draw)
			end.make_end() 
			start.make_start() 
			return True 
		for neighbor in current.neighbors : 

			if neighbor not in visited: 
				came_from[neighbor] = current 
				nodes.put(neighbor)
				visited.add(neighbor)
				neighbor.make_visited() 

		draw() 

		if current != start : 
			current.make_not_visited() 

	return False 

import time 
def a_star(draw,grid,start,end) : 

	count = 0 
	visited = PriorityQueue() 
	visited.put((0,count,start))
	came_from = {} 
	g_score = {square:float("inf") for row in grid for square in row }
	g_score[start] = 0 
	f_score = {square:float("inf") for row in grid for square in row }
	f_score[start] =  manhattan_h_score(start.get_x_y_position(),end.get_x_y_position())

	visited_dictionary = {start} 

	while not visited.empty() :
		#time.sleep(0.3) 
		for event in pygame.event.get() : 

			if event.type == pygame.QUIT : 
				pygame.quit() 

		current = visited.get()[2]
		visited_dictionary.remove(current)

		if current == end : 
			show_path(came_from,start,end,draw)
			end.make_end()
			return True

		for neighbor in current.neighbors :
			temporary_g_score = g_score[current] + 1

			if temporary_g_score < g_score[neighbor] :

				came_from[neighbor] = current 

				g_score[neighbor] = temporary_g_score
				f_score[neighbor] = temporary_g_score + manhattan_h_score(neighbor.get_x_y_position(), end.get_x_y_position())
				if neighbor not in visited_dictionary : 
					count +=1 
					visited.put((f_score[neighbor],count,neighbor))
					visited_dictionary.add(neighbor)
					neighbor.make_visited()

		draw() 

		if current!=start : 
			current.make_not_visited() 

	return False

def main() : 

	ROWS = 50
	grid = make_grid(ROWS,width)

	start = None 
	end = None 

	run = True 

	while run : 

		draw(win,grid,ROWS,width)
		
		for event in pygame.event.get() : 

			if event.type == pygame.QUIT: 

				run = False 


			if pygame.mouse.get_pressed()[0] :
				pos = pygame.mouse.get_pos() 
				row , col = clicking_position_determination(pos,ROWS,width)
				cube = grid[row][col]

				if not start and cube!=end : 
					start = cube
					start.make_start() 

				elif not end and cube != start : 
					end = cube 
					end.make_end() 

				elif cube != end and cube != start : 

					cube.make_barrier() 

			elif pygame.mouse.get_pressed()[2] : 
				pos = pygame.mouse.get_pos()
				row,col = clicking_position_determination(pos,ROWS,width)
				cube = grid[row][col]
				cube.clear_all() 
				if cube == start : 
					start = None 
				elif cube == end : 
					end = None 

			if event.type == pygame.KEYDOWN : 

				if event.key == pygame.K_SPACE and start and end : 
					for row in grid : 
						for square in row : 
							square.update_neighbors(grid)


					dijkstra(lambda : draw(win,grid,ROWS,width), grid,start,end)

					#depth_first_search(lambda : draw(win,grid,ROWS,width), grid,start,end)

					#breadth_first_search(lambda : draw(win,grid,ROWS,width), grid,start,end)
					#a_star(lambda : draw(win,grid,ROWS,width), grid,start,end)


				if event.key == pygame.K_c : 

					start = None 
					end = None 
					grid = make_grid(ROWS,width)


	pygame.quit() 

if __name__=="__main__" : 

	main()