# Thuật toán backtracking
Backtracking là thuật toán thử điền lần lượt tất cả các giá trị có khả năng vào, sau đó tiếp tục điền cho tới khi hết bảng (bài toán được giải quết) hoặc đến khi không có giá trị nào thỏa mãn ô hiện tại, ô trước đó sẽ được thay thế bằng giá trị khác.

## Dạng bài
Backtracking có 2 dạng bài.  
* Tìm ra mọi kết quả, đếm số kết quả có thể  
* Tìm ra 1 kết quả (bài toán chỉ có 1 kết quả)  
**=>** Điểm khác nhau giữa 2 dạng bài này là 1 bài có return true, false, 1 bài ko có.  

*Lưu ý:* khi có return true, false thì sẽ if(true) được.
## Code mẫu

**Code mẫu 1**
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

**Code mẫu 2**
```C++
void is_possible(row, col){
    if (..) return false;
    if (..) return false;
    return true;
}
void solve(col){ // có nhiều kết quả
    if (col> boundary){
        # found. print here, count here
    } else {
        // in boundary N
        for (int i=0;i<N;i++){
            board[i][col] = fill_value;
            if (is_possible()){
                solve(col+1);
            }
            board[i][col] = blank;
        }
    }
}
void solve1(){ // có 1 kết quả
    if (column > boundary) {
        // Found
        // return if only have 1 answer
    }
    next_x, next_y = f(x), g(y);
    assign new value to board(x,y)
    if (is_possible(x,y) && solve1(next_x, next_y)) {
        return true;
    }
    assign another value to board(x,y)
    if (is_possible(x,y) && solve1(next_x, next_y)) {
        return true;
    }
}
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

## N-Queen problem

```C++
// https://cses.fi/problemset/task/1624
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

vector<string> board;
int N;
int c=0;
bool is_possible(int row, int col){
    for (int i=0;i<N; i++){
        if (board[row][i] == 'Q') return false;
        if (board[i][col] == 'Q') return false;
        if ( row-i >=0 && col-i >=0 &&board[row-i][col-i] == 'Q') return false;
        if (row+i<N && col-i>=0 && board[row+i][col-i] == 'Q') return false;
    }
    return true;
}
void solve(int col){
    if (col >=N){
        // for (int i = 0;i< N;i++){
        //     cout << board[i] << '\n';
        // }
        // cout << "---------\n";
        c++;
    } else{
        for (int i=0;i<N;i++){
            if (board[i][col] != '*' && is_possible(i, col)){
                board[i][col] = 'Q';
                solve(col+1);
                board[i][col] = '.';
            }
        }
    }
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    string s;
    cin >> s;
    board.push_back(s);
    N = s.size();
    for (int i=0;i<N-1;i++){
        cin >> s;
        board.push_back(s);
    }
    // for (int i = 0;i< N;i++){
    //     cout << board[i] << ' ';
    //     cout << '\n';
    // }
    solve(0);
    cout << c;
}
```

Nonogram-solver
```C++
/*
Giải tự động nonogram
Input
5 -> số N*N
2 1 1 -> 2 là chỉ ra dòng này bao nhiêu số. hàng 1 = {1,1}
1 3 -> hàng 2 = {3}
1 2 
1 3
1 3 -> 5 dòng đầu là row
1 2 -> 5 dòng sau này là column
1 1
2 2 2
1 3
1 3
Output: 
1 0 1 0 0 
1 1 1 0 0 
0 0 0 1 1 
0 0 1 1 1 
0 0 1 1 1 
----------
Sử dụng thuật toán backtracking để giải
*/
#include<bits/stdc++.h>

typedef long long ll;

using namespace std;

vector<vector<bool>> board;
vector<vector<int>> rows, cols;
int N;
void print(){
    for(int i =0;i<N;i++){
        for (int j=0;j<N;j++){
            if (board[i][j]) {
                cout << 1 << ' ';
            } else cout << 0 << ' ';
        }
        cout << '\n';
    }
    cout << "----------\n";
}

bool is_possible(vector<bool> rl, vector<int> row, int idx){
    // rl = {0,0,1,1,1}  row = {1,1};
    vector<int> hint;
    int cnt=0;
    for (int i=0; i<N; i++){
        if (rl[i]) {
            cnt ++;
        } else {
            if (cnt>0) hint.push_back(cnt);
            cnt = 0;
        }
    }
    if (cnt>0) hint.push_back(cnt);
    if (idx+1>=N && hint!=row) return false; 
    if (hint.size() > row.size()) return false;
    else {
        for (int i=0;i< hint.size();i++){
            if (hint[i] > row[i]) return false;
        }
    }
    return true;
}
vector<bool> get_column(int idx){
    vector<bool> result;
    for (int i=0;i<N;i++){
        result.push_back(board[i][idx]);
    }
    return result;
}
bool solve(int x, int y){
    // cout << x << ' '<<  y << '\n';
    // print();
    if (x>=N) {
        print();
        return true;
    }
    int next_x, next_y;
    if (y+1<N) {
        next_y = y+1; next_x = x;
    } else {next_y = 0; next_x= x+1;}
    board[x][y] = true;
    if (is_possible(board[x], rows[x], y) && is_possible(get_column(y), cols[y], x) && solve(next_x, next_y)){
        return true;
    }
    //  else {
    //     for (auto v: board[x])  cout << v << ' ';cout << '~';
    //     for (auto v: rows[x]) cout << v << ' '; cout << '|'; cout<< "index="<< y;cout << "->";
    //     cout << is_possible(board[x], rows[x], y) <<'\n';
    // }
    board[x][y] = false;
    if (is_possible(board[x], rows[x], y) && is_possible(get_column(y), cols[y], x) && solve(next_x, next_y)){
        // cout << "FOUND";
        return true;
    }
    return false;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    // #ifdef DEBUG
    freopen("inp.txt", "r", stdin);
    freopen("out.txt", "w", stdout);
    // #endif
    cin >> N;
    for (int i=0;i<N;i++){
        int x,k;
        vector<int> row;
        cin >> x;
        for (int j=0;j<x;j++){
            cin >> k;
            row.push_back(k);
        }
        rows.push_back(row); 
    }
    for (int i=0;i<N;i++){
        int x,k;
        vector<int> col;
        cin >> x;
        for (int j=0;j<x;j++){
            cin >> k;
            col.push_back(k);
        }
        cols.push_back(col); 
    }
    // Initial board
    for (int i=0;i<N;i++){
        vector<bool> x;
        for (int j=0;j<N;j++){
            x.push_back(false);
        }
        board.push_back(x);
    }
    solve(0,0);// 0 0 0 0 
    // cout << is_possible({true, true, false, true, false}, {2,2}, 3);
}
```