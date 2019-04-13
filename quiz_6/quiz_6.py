# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and determines the size of the largest
# isosceles triangle, consisting of nothing but 1s and whose base can be either
# vertical or horizontal, pointing either left or right or up or down.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import numpy as np
import sys




def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))



def Evaluate(a, b, c):#判断是否过界
    if 0 <= a < len(grid) and 0 <= b < len(grid) and 0 <= c < len(grid):
        return True
    else:
        return False

def get_size(new_grid): #每一个点向下得size
    size = 0
    initial = 0
    for y_index in range(len(new_grid)):
        for x_index in range(len(new_grid)):
            if new_grid[y_index][x_index] != 0:
                size = 1
                if (Evaluate(y_index+1, x_index-1, x_index+1) and new_grid[y_index + 1][x_index - 1] and new_grid[y_index + 1][x_index] and new_grid[y_index + 1][x_index + 1]):
                    size = 2
                    if (Evaluate(y_index+2, x_index-2, x_index+2) and new_grid[y_index + 2][x_index - 2] and new_grid[y_index + 2][x_index - 1] and new_grid[y_index + 2][x_index] and new_grid[y_index + 2][x_index + 1] and new_grid[y_index + 2][x_index + 2]):
                        size = 3
                        if ( Evaluate(y_index+3, x_index-3, x_index+3) and new_grid[y_index + 3][x_index - 3] and new_grid[y_index + 3][x_index - 2] and new_grid[y_index + 3][x_index - 1] and new_grid[y_index + 3][x_index] and new_grid[y_index + 3][x_index + 1] and new_grid[y_index + 3][x_index + 2] and new_grid[y_index + 3][x_index + 3]):
                            size = 4
                            if (Evaluate(y_index+4, x_index-4, x_index+4) and new_grid[y_index + 4][x_index - 4] and new_grid[y_index + 4][x_index - 3] and new_grid[y_index + 4][x_index - 2] and new_grid[y_index + 4][x_index - 1] and new_grid[y_index + 4][x_index] and new_grid[y_index + 4][x_index + 1] and new_grid[y_index + 4][x_index + 2] and new_grid[y_index + 4][x_index + 3] and new_grid[y_index + 4][x_index + 4]):
                                size = 5
            # 如果得到的size>initial返回size否则返回的值等于原来的initial
            if size > initial:
                initial = size
            else:
                initial = initial
    return initial


def size_of_largest_isosceles_triangle():
    max_size = 0
    original = 0
    original1 = 0
    original2 = 0
    original3 = 0
    new_grid = np.array(grid) #原矩阵
    original = get_size(new_grid)
    new_grid = np.rot90(new_grid) #原矩阵旋转90度
    original1 = get_size(new_grid)
    new_grid = np.rot90(new_grid) #原矩阵旋转90度
    original2 = get_size(new_grid)
    new_grid = np.rot90(new_grid) #原矩阵旋转90度
    original3 = get_size(new_grid)
    max_size = max(original, original1, original2, original3)
    return max_size

try:
    arg_for_seed, density = (abs(int(x)) for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()
print('The largest isosceles triangle has a size of',
      size_of_largest_isosceles_triangle()
     )
