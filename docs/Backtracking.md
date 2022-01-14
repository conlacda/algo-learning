# Backtracking
Backtracking thường có 2 yêu cầu:
* Tìm ra số khả năng có thể xảy ra
* In ra 1 khả năng thỏa mãn

## Form chung

```c++
bool possible(int x){
    return True/False;
}
void solve(int x){
    if (x>N){
        return false;
    } else{
        int nx;// next position of x
        nx = x+1;
        if (grid[x] != 0 && possible(x)){
            grid[x] = 1;
            if (solve(nx)) return true;
            grid[x] = 0;
        }
        if (grid[x] != 0 && possible(x)){
            grid[x] = 2;
            if (solve(nx)) return true;
            grid[x] = 0;
        }
        //...
        return false;
    }
}
```
Khi muốn backtracking đếm số lượng khả năng xảy ra, thay đổi 1 chút
```c++
int c=0;
// Thay vì if (solve(nx)) return true; thì 
if (solve(nx)) c++;
// Đồng thời tại đoạn c++ này có thể viết hàm in ra kết quả tìm thấy
}
```

## Code thực tế
<details>
  <summary>Soduko - tìm 1 khả năng xảy ra</summary>
  
  ```c++
  #include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Copy from nealwu's template - http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0200r0.html
template<class Fun> class y_combinator_result {
    Fun fun_;
public:
    template<class T> explicit y_combinator_result(T &&fun): fun_(std::forward<T>(fun)) {}
    template<class ...Args> decltype(auto) operator()(Args &&...args) { return fun_(std::ref(*this), std::forward<Args>(args)...); }
};
template<class Fun> decltype(auto) y_combinator(Fun &&fun) { return y_combinator_result<std::decay_t<Fun>>(std::forward<Fun>(fun)); }


template<typename A, typename B> ostream& operator<<(ostream &os, const pair<A, B> &p) { return os << '(' << p.first << ", " << p.second << ')'; }
template<typename T_container, typename T = typename enable_if<!is_same<T_container, string>::value, typename T_container::value_type>::type> ostream& operator<<(ostream &os, const T_container &v) { os << '{'; string sep; for (const T &x : v) os << sep << x, sep = ", "; return os << '}'; }

void dbg_out() { cerr << endl; }
template<typename Head, typename... Tail> void dbg_out(Head H, Tail... T) { cerr << ' ' << H; dbg_out(T...); }
#ifdef DEBUG
#define dbg(...) cerr << "(" << #__VA_ARGS__ << "):", dbg_out(__VA_ARGS__)
#else
#define dbg(...)
#endif

int N = 9;
vector<vector<int>> grid = {
     {3, 0, 6, 5, 0, 8, 4, 0, 0}, 
     {5, 2, 0, 0, 0, 0, 0, 0, 0}, 
     {0, 8, 7, 0, 0, 0, 0, 3, 1}, 
     {0, 0, 3, 0, 1, 0, 0, 8, 0}, 
     {9, 0, 0, 8, 6, 3, 0, 0, 5}, 
     {0, 5, 0, 0, 9, 0, 6, 0, 0}, 
     {1, 3, 0, 0, 0, 0, 2, 5, 0}, 
     {0, 0, 0, 0, 0, 0, 0, 7, 4}, 
     {0, 0, 5, 2, 0, 6, 3, 0, 0}
};

bool possible(int x, int y, int value){
    // check ngang
    for (int i=0;i<9;i++){
        if (grid[x][i] == value) return false;
    }
    // check doc
    for (int i=0;i<9;i++){
        if (grid[i][y] == value) return false;
    }
    // check o vuong
    int min_x = x/3*3;
    int max_x = min_x+2;
    int min_y = y/3*3;
    int max_y = min_y+2;
    for (int i=min_x;i<=max_x;i++){
        for (int j=min_y;j<=max_y;j++){
            if (grid[i][j] == value) return false;
        }
    }
    return true;
}

bool solve(int x, int y){
    dbg(x, y);
    if (y >= N){
        return true;
    } else{
        int nx, ny;
        if (x<N-1) {
            nx = x+1; ny =y;
        } else{
            nx = 0; ny = y+1;
        }
        if (grid[x][y] != 0){
            if (solve(nx, ny)) return true;
        } else{
            if (grid[x][y] == 0 && possible(x, y, 1)){
                grid[x][y] = 1;
                if (solve(nx, ny)) return true;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 2)){
                grid[x][y] = 2;
                if (solve(nx, ny)) return true;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 3)){
                grid[x][y] = 3;
                if (solve(nx, ny)) return true;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 4)){
                grid[x][y] = 4;
                if (solve(nx, ny)) return true;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 5)){
                grid[x][y] = 5;
                if (solve(nx, ny)) return true;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 6)){
                grid[x][y] = 6;
                if (solve(nx, ny)) return true;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 7)){
                grid[x][y] = 7;
                if (solve(nx, ny)) return true;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 8)){
                grid[x][y] = 8;
                if (solve(nx, ny)) return true;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 9)){
                grid[x][y] = 9;
                if (solve(nx, ny)) return true;
                grid[x][y] = 0;
            }
        }
        return false;
    }
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
        dbg(solve(0,0));
    // if (solve(0,0)){
        for (auto v: grid){
            dbg(v);
        }
    // }
}
  ```
</details>

<details>
  <summary>Soduko - đếm số khả năng xảy ra (tìm ra tất cả khả năng</summary>
  
  ```javascript
    #include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Copy from nealwu's template - http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0200r0.html
template<class Fun> class y_combinator_result {
    Fun fun_;
public:
    template<class T> explicit y_combinator_result(T &&fun): fun_(std::forward<T>(fun)) {}
    template<class ...Args> decltype(auto) operator()(Args &&...args) { return fun_(std::ref(*this), std::forward<Args>(args)...); }
};
template<class Fun> decltype(auto) y_combinator(Fun &&fun) { return y_combinator_result<std::decay_t<Fun>>(std::forward<Fun>(fun)); }


template<typename A, typename B> ostream& operator<<(ostream &os, const pair<A, B> &p) { return os << '(' << p.first << ", " << p.second << ')'; }
template<typename T_container, typename T = typename enable_if<!is_same<T_container, string>::value, typename T_container::value_type>::type> ostream& operator<<(ostream &os, const T_container &v) { os << '{'; string sep; for (const T &x : v) os << sep << x, sep = ", "; return os << '}'; }

void dbg_out() { cerr << endl; }
template<typename Head, typename... Tail> void dbg_out(Head H, Tail... T) { cerr << ' ' << H; dbg_out(T...); }
#ifdef DEBUG
#define dbg(...) cerr << "(" << #__VA_ARGS__ << "):", dbg_out(__VA_ARGS__)
#else
#define dbg(...)
#endif

int N = 9;
vector<vector<int>> grid = {
     {3, 0, 6, 5, 0, 8, 4, 0, 0}, 
     {5, 2, 0, 0, 0, 0, 0, 0, 0}, 
     {0, 8, 7, 0, 0, 0, 0, 3, 1}, 
     {0, 0, 3, 0, 1, 0, 0, 8, 0}, 
     {9, 0, 0, 8, 6, 3, 0, 0, 5}, 
     {0, 5, 0, 0, 9, 0, 6, 0, 0}, 
     {1, 0, 0, 0, 0, 0, 2, 5, 0}, 
     {0, 0, 0, 0, 0, 0, 0, 7, 4}, 
     {0, 0, 0, 0, 0, 0, 0, 0, 0}
};

bool possible(int x, int y, int value){
    // check ngang
    for (int i=0;i<9;i++){
        if (grid[x][i] == value) return false;
    }
    // check doc
    for (int i=0;i<9;i++){
        if (grid[i][y] == value) return false;
    }
    // check o vuong
    int min_x = x/3*3;
    int max_x = min_x+2;
    int min_y = y/3*3;
    int max_y = min_y+2;
    for (int i=min_x;i<=max_x;i++){
        for (int j=min_y;j<=max_y;j++){
            if (grid[i][j] == value) return false;
        }
    }
    return true;
}
int c=0;
bool solve(int x, int y){
    dbg(x, y);
    if (y >= N){
        return true;
    } else{
        int nx, ny;
        if (x<N-1) {
            nx = x+1; ny =y;
        } else{
            nx = 0; ny = y+1;
        }
        if (grid[x][y] != 0){
            if (solve(nx, ny)) return true;
        } else{
            if (grid[x][y] == 0 && possible(x, y, 1)){
                grid[x][y] = 1;
                if (solve(nx, ny)) c++;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 2)){
                grid[x][y] = 2;
                if (solve(nx, ny)) c++;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 3)){
                grid[x][y] = 3;
                if (solve(nx, ny)) c++;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 4)){
                grid[x][y] = 4;
                if (solve(nx, ny)) c++;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 5)){
                grid[x][y] = 5;
                if (solve(nx, ny)) c++;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 6)){
                grid[x][y] = 6;
                if (solve(nx, ny)) c++;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 7)){
                grid[x][y] = 7;
                if (solve(nx, ny)) c++;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 8)){
                grid[x][y] = 8;
                if (solve(nx, ny)) c++;
                grid[x][y] = 0;
            } 
            if (grid[x][y] == 0 && possible(x, y, 9)){
                grid[x][y] = 9;
                if (solve(nx, ny)) c++;
                grid[x][y] = 0;
            }
        }
        return false;
    }
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
        dbg(solve(0,0));
        cout << c<<'\n';
}
  ```
</details>

Submit [này](https://codeforces.com/contest/1624/submission/142405191) cũng sử dụng backtracking - lưu ý là backtracking có độ phức tạp lớn nên cần hạn chế sử dụng chỉ khi thực sự cần thiết. (Dynamic programming có thể nghĩ tới thay thế cho nó)