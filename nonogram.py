grid = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]
column = [[4],[1,3],[4],[1,2],[3]]
row = [[1],[1,2],[3,1],[5],[5]]

def possible(y,x,n):
    # y: thứ tự hàng, x: cột, n giá trị grid[y][x] = n
    # n = {0,1,2} - 0 là 0 điền, 1 là tô đen, 2 là gạch chéo
    # Không thỏa mãn khi số ô đen lớn hơn tổng hint
    #                khi số ô gạch lớn hơn len(grid) - tổng hint
    #                không đúng khuôn, ko thỏa mãn hint
    global grid, column, row
