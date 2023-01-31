import pygame
import random
import pyautogui
import math
import os

pyautogui.FAILSAFE = False
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"

pygame.init()

width,height = 1200,600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Maze Generator")

size = 40

start = [0,0]
end = [width//size-1,height//size-1]
currentfind = [-1,-1]
created = False
solved = False
captured = False

class Cell():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True,True,True,True]

        self.pos = [self.x,self.y]
        self.open = False
        self.closed = False
        self.pointto = [-1,-1]
        self.fromstart = 0
        self.fromend = 0
        self.total = 0
        self.parent = [-1,-1]
        
    def draw(self,win):
        if self.visited:
            pygame.draw.rect(win,(255,255,255),(self.x*size,self.y*size,size,size))
        if created and not solved:
            if self.closed:
                pygame.draw.rect(win,(0,255,0),(self.x*size,self.y*size,size,size))
            elif self.open:
                pygame.draw.rect(win,(255,0,0),(self.x*size,self.y*size,size,size))
        if self.walls[0]:
            pygame.draw.line(win,(0,0,0),(self.x*size,self.y*size),(self.x*size+size,self.y*size))
        if self.walls[1]:
            pygame.draw.line(win,(0,0,0),(self.x*size+size-1,self.y*size),(self.x*size+size-1,self.y*size+size))
        if self.walls[2]:
            pygame.draw.line(win,(0,0,0),(self.x*size,self.y*size+size-1),(self.x*size+size,self.y*size+size-1))
        if self.walls[3]:
            pygame.draw.line(win,(0,0,0),(self.x*size,self.y*size),(self.x*size,self.y*size+size))

    def visit(self,cells):
        self.visited = True
        neighbours = []
        if self.y != 0:
            if not cells[self.y-1][self.x].visited:
                neighbours.append(cells[self.y-1][self.x])
        if self.y != len(cells)-1:
            if not cells[self.y+1][self.x].visited:
                neighbours.append(cells[self.y+1][self.x])
        if self.x != 0:
            if not cells[self.y][self.x-1].visited:
                neighbours.append(cells[self.y][self.x-1])
        if self.x != len(cells[0])-1:
            if not cells[self.y][self.x+1].visited:
                neighbours.append(cells[self.y][self.x+1])

        if len(neighbours) > 0:
            cell = random.choice(neighbours)
            return cell.x, cell.y
        else:
            return None

    def find(self,cells):
        self.closed = True
        if not self.walls[0] and self.y != 0:
            if not cells[self.y-1][self.x].closed:
                cells[self.y-1][self.x].open = True
                cells[self.y-1][self.x].parent = [self.x,self.y]
                cells[self.y-1][self.x].calculate()
        if not self.walls[1] and self.x != width//size - 1:
            if not cells[self.y][self.x+1].closed:
                cells[self.y][self.x+1].open = True
                cells[self.y][self.x+1].parent = [self.x,self.y]
                cells[self.y][self.x+1].calculate()
        if not self.walls[2] and self.y != height//size - 1:
            if not cells[self.y+1][self.x].closed:
                cells[self.y+1][self.x].open = True
                cells[self.y+1][self.x].parent = [self.x,self.y]
                cells[self.y+1][self.x].calculate()
        if not self.walls[3] and self.x != 0:
            if not cells[self.y][self.x-1].closed:
                cells[self.y][self.x-1].open = True
                cells[self.y][self.x-1].parent = [self.x,self.y]
                cells[self.y][self.x-1].calculate()

    def calculate(self):
        self.fromstart = math.sqrt(self.x**2 + self.y**2)
        self.fromend = math.sqrt((self.x-end[0])**2 + (self.y-end[1])**2)
        self.total = self.fromstart + self.fromend + self.fromend

cells = []
for y in range(height//size):
    cells.append([])
    for x in range(width//size):
        cells[y].append(Cell(x,y))

count = 1
current = [random.randint(0,width//size-1),random.randint(0,height//size-1)]
stack = []
stack.append(current)
run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    

    new = cells[current[1]][current[0]].visit(cells)
    if new:

        x = new[0] - current[0]

        if x == 1:
            cells[current[1]][current[0]].walls[1] = False
            cells[new[1]][new[0]].walls[3] = False
        elif x == -1:
            cells[current[1]][current[0]].walls[3] = False
            cells[new[1]][new[0]].walls[1] = False

        y = new[1] - current[1]

        if y == 1:
            cells[current[1]][current[0]].walls[2] = False
            cells[new[1]][new[0]].walls[0] = False
        elif y == -1:
            cells[current[1]][current[0]].walls[0] = False
            cells[new[1]][new[0]].walls[2] = False

        current = new
        stack.append(current)
    else:
        if len(stack) > 0:
            current = stack.pop()

    if len(stack) == 0 and not created:
        img = pyautogui.screenshot(region=(0,30, width, height))
        img.save(os.getcwd() + "\\mazes\\maze " + str(count) + ".png")
        created = True
        cells[start[1]][start[0]].open = True
        cells[start[1]][start[0]].closed = True
        currentfind = start

    if created and not solved:
        cells[currentfind[1]][currentfind[0]].find(cells)

        bestindex = [-1,-1]
        record = 1000000000000000
        for y in range(len(cells)):
            for x in range(len(cells[0])):
                if cells[y][x].open and not cells[y][x].closed:
                    if cells[y][x].total < record:
                        bestindex = [x,y]
        

        if bestindex != [-1,-1]:
            currentfind = bestindex

        if cells[end[1]][end[0]].closed:
            solved = True


    if created and solved and captured:
        img = pyautogui.screenshot(region=(0,30, width, height))
        img.save(os.getcwd() + "\\mazes\\maze " + str(count) + " solution.png")
        created = False
        captured = False
        solved = False
        count += 1
        cells = []
        for y in range(height//size):
            cells.append([])
            for x in range(width//size):
                cells[y].append(Cell(x,y))

        current = [random.randint(0,width//size-1),random.randint(0,height//size-1)]
        stack = []
        stack.append(current)

    win.fill((0,0,0))

    for row in cells:
        for cell in row:
            cell.draw(win)

    if created:
        pygame.draw.rect(win,(255,0,0),(size/4,size/4,size/2,size/2))
        pygame.draw.rect(win,(255,0,0),((width/size-1)*size + size/4,(height/size-1)*size + size/4,size/2,size/2))
    
    if created and solved and not captured:
        points = []
        points.append([cells[end[1]][end[0]].x,cells[end[1]][end[0]].y])
        parent = cells[end[1]][end[0]].parent
        points.append([cells[parent[1]][parent[0]].x,cells[parent[1]][parent[0]].y])
        while True:
            parent = cells[parent[1]][parent[0]].parent
            points.append(parent)

            if parent == [-1,-1]:
                break
        
        for i in range(len(points) - 2):    
            pygame.draw.line(win,(255,0,0),(points[i][0]*size+size/2,points[i][1]*size+size/2),(points[i+1][0]*size+size/2,points[i+1][1]*size+size/2),int(size/4))
            pygame.draw.circle(win,(255,0,0),(points[i][0]*size+size/2,points[i][1]*size+size/2),size/4)

        captured = True

    pygame.display.set_caption("Maze Generator - Creating Maze " + str(count))

    pygame.display.update()

    if count > 30:
        exit()

pygame.quit()
exit()