import numpy as np
black = 1
white = 0
cross = 2
grid = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

size = len(grid)
column_hints = [[3],[4],[3,6],[1,3,5],[2,3,4],[2,6],[8],[8],[3,3],[2,6],[3,4],[4,2],[7],[2,5],[1,5]]
row_hints = [[5,5],[11],[7],[5,3],[6,3],[8,3],[1,6,3],[8,2],[3,3,1],[3,2],[3,1],[3],[4],[3],[3]]
# def set_possible():

def possible(y,x,n):
    # y: thứ tự hàng, x: cột, n giá trị grid[y][x] = n
    # n = {0,1,2} - 0 là 0 điền, 1 là tô đen, 2 là gạch chéo
    # Không thỏa mãn khi số ô đen lớn hơn tổng hint
    #                khi số ô gạch lớn hơn len(grid) - tổng hint
    #                không đúng khuôn, ko thỏa mãn hint
    global grid, column_hints, row_hints
    _black = 1 if n == black else 0
    _cross = 1 if n == cross else 0
    # grid[y] = row
    if grid[y].count(black) + _black > sum(row_hints[y]):
        return False
    if grid[y].count(cross) + _cross + sum(row_hints[y])> size:
        return False
    column = [grid[i][x] for i in range(size)]
    if column.count(black) + _black > sum(column_hints[x]):
        return False
    if column.count(cross) + _cross + sum(column_hints[x]) > size:
        return False
    # logic về thứ tự vào đây
    return True

def is_possible_result():
    global grid
    def hints_from_set(set):
        hints = []
        count = 0
        for i in range(len(set)):
            if set[i] == black:
                count += 1
            else:
                if count > 0:
                    hints.append(count)
                    count = 0
        if count > 0:
            hints.append(count)
        return hints
    for i in range(size):
        if hints_from_set(grid[i]) != row_hints[i]:
            return False
        column = [grid[j][i] for j in range(size)]
        if hints_from_set(column) != column_hints[i]:
            return False
    return True

def solve():
    global grid, count
    for y in range(size):
        for x in range(size):
            if grid[y][x] == white:
                for n in [black, cross]:
                    if possible(y,x,n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    if is_possible_result():
        print(np.matrix(grid))
    else:
        print(count)
        count +=1
count = 0
solve()