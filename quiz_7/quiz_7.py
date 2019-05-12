# Randomly fills a grid with True and False, with width, height and density
# controlled by user input, and computes the number of all "good paths" that link
# a point of coordinates (x1, y1) to a point of coordinates (x2, y2)
# (x1 and x2 are horizontal coordinates, increasing from left to right,横向
# y1 and y2 are vertical coordinates, increasing from top to bottom,纵向
# both starting from 0), that is:
# - paths that go through nothing but True values in the grid
# - paths that never go through a given point in the grid more than once;
# - paths that never keep the same direction (North, South, East, West) over
#   a distance greater than 2.
#
# Written by *** and Eric Martin for COMP9021


from collections import namedtuple
import numpy as np 
from random import seed, randrange
import sys


Point = namedtuple('Point', 'x y')


def display_grid():
    for row in grid:
        print('   ', ' '.join(str(int(e)) for e in row))

def valid(pt):
    return 0 <= pt.x < width and 0 <= pt.y < height

def fun(y1,x1,y2,x2,solution=0,north=0,south=0,west=0,east=0):
    #标记已走过
    grid[y1][x1] = False
    #如果坐标相同,solution+1
    if y1==y2 and x1==x2:
        solution = solution + 1
    #west
    if 0<=x1-1<width and west<2 and grid[y1][x1-1]:
        west=west+1
        solution=fun(y1,x1-1,y2,x2,solution,north=0,south=0,west=west,east=0)
        #重制
        grid[y1][x1-1] = True
    #east
    if 0<=x1+1<width and east<2 and grid[y1][x1+1]:
        east=east+1
        solution=fun(y1,x1+1,y2,x2,solution,north=0,south=0,west=0,east=east)
        #重制
        grid[y1][x1+1] = True
    #north
    if 0<=y1+1<height and north<2 and grid[y1+1][x1]:
        north=north+1
        solution=fun(y1+1,x1,y2,x2,solution,north=north,south=0,west=0,east=0)
        #重制
        grid[y1+1][x1] = True
    #south
    if 0<=y1-1<height and south<2 and grid[y1-1][x1]:
        south=south+1
        solution=fun(y1-1,x1,y2,x2,solution,north=0,south=south,west=0,east=0)
        #重制
        grid[y1-1][x1] = True
    return solution

    
def nb_of_good_paths(pt_1, pt_2):
    new_grid=np.array(grid)
    if new_grid[pt_1.y][pt_1.x] ==False and new_grid[pt_2.y][pt_2.x] ==False:
        paths_nb=0
    else:
        paths_nb=fun(pt_1.y,pt_1.x,pt_2.y,pt_2.x,solution=0,north=0,south=0,west=0,east=0)
    return paths_nb


try:
    for_seed, density, height, width = (abs(int(i)) for i in
                                                  input('Enter four integers: ').split()
                                       )
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
if not density:
    density = 1
seed(for_seed)
grid = np.array([randrange(density) > 0
                              for _ in range(height * width)
                ]
               ).reshape((height, width))
print('Here is the grid that has been generated:')
display_grid()
try:
    i1, j1, i2, j2 = (int(i) for i in input('Enter four integers: ').split())
    pt_1 = Point(i1, j1)
    pt_2 = Point(i2, j2)
    if not valid(pt_1) or not valid(pt_2):
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
print('Will compute the number of good paths '
      f'from ({pt_1.x}, {pt_1.y}) to ({pt_2.x}, {pt_2.y})...'
     )
paths_nb = nb_of_good_paths(pt_1, pt_2)
if not paths_nb:
    print('There is no good path.')
elif paths_nb == 1:
    print('There is a unique good path.')
else:
    print('There are', paths_nb, 'good paths.')

