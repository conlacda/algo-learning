# Thuật toán backtracking
Backtracking là thuật toán thử điền lần lượt tất cả các giá trị có khả năng vào, sau đó tiếp tục điền cho tới khi hết bảng (bài toán được giải quết) hoặc đến khi không có giá trị nào thỏa mãn ô hiện tại, ô trước đó sẽ được thay thế bằng giá trị khác.

## Code mẫu
```python
var something
def possible(...):
    if (...):
        return False
    return True
def solve():
    for y in range(size): # các vòng for để chạy qua tất cả các gtri
        for x in range(size):
            if chưa được điền:
                for n in [các giá trị có thể xảy ra]:
                    if possible(...):
                        điền giá trị
                        solve() # đệ quy
                        trả về giá trị trống
                return
    print(grid) # đât là dòng lưu lại giá trị đã giải, sau đó nó sẽ quay ngược lại vì sau hàm solve() luôn là backtrack
```

## Bài toán mẫu

### Bài toán giải sodoku
Cho một bảng sudoku, tự động điền các giá trị vào để giải bài toán

***Code mẫu***
```python
grid = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]
size = len(grid)
def possible(y,x,n):
    global grid
    for i in range(0,9):
        if grid[y][i] == n:
            return False
    for i in range(0,9):
        if grid[i][x] == n:
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j] == n:
                return False
    return True

def solve():
    global grid
    for y in range(size):
        for x in range(size):
            if grid[y][x] == 0:
                for n in range(1,10):
                    if possible(y,x,n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    print(grid)
    
solve()
```