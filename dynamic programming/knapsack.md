# Bài toán knapsack
> https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/
> https://www.javatpoint.com/0-1-knapsack-problem
> https://cses.fi/problemset/result/4691378/

<!-- # TODO 
Viết về tư tưởng của thuật toán (quay 1 video ngắn cũng được) -->
## Nội dung
Cho 1 cái túi chứa được trọng lượng `cap`. Có n vật có trọng lượng `weight ={w1, w2, w3,..., wn}` và giá trị lần lượt của các vật là `point = {p1, p2, p3,.., pn}`. Hỏi rằng túi có thể đựng được tối đã bao nhiêu point (mỗi đồ chỉ đựng duy nhất 1 lần)

## Cách giải
Xem video hướng dẫn của mình tại [đây](https://github.com/conlacda/algo-video/blob/main/dynamic%20programming/knapsack.mp4). Video xem dễ hiểu mà cũng nhanh hơn viết đỡ phải nghĩ.

## So sánh với bitmask
Bitmask cũng cho n phần tử (n nhỏ) và yêu cầu dựng tất cả các sự kết hợp (tổ hợp) để tính toán. Và thường sẽ cho i từ 0->2^n và i trong binary có 1 tại vị trí nào thì vị trí đó được chọn.  
Bitmask thường yêu cầu toàn bộ sự kết hợp để tính toán (max, sum, ...) tức là bruteforce tất cả các trường hợp.  
Thế nhưng trong bài knapsack này cũng là sự kết hợp của các phần tử mỗi phần tử chỉ xuất hiện 1 nhưng n tại đây là rất lớn (1000 -> 2^1000) là ko được và mình cũng ko cần xét toàn bộ các trường hợp mà chỉ tối ưu từ bộ nhỏ (1->k) rồi (1->k+1) = f(1->k)

## Chuyển đổi qua lại giữa recursion

## Backup
2 slide đã được back up tại [dynamic programming folder](/backup/dynamic-programming/)

## Bài giải mẫu

<details>
  <summary>Knapsack</summary>

```c++
//https://cses.fi/problemset/task/1746
#include<bits/stdc++.h>
 
typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double
 
using namespace std;

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    // https://www.javatpoint.com/0-1-knapsack-problem
    int n, W;
    cin >> n>> W;
    vector<int> w(n), val(n);
    for (int i=0;i<n;i++) cin >> w[i];
    for (int i=0;i<n;i++) cin >> val[i];
    dbg(w, val);
    vector<vector<int>> table(n+1, vector<int>(W+1));
    for (int i=0;i<=n;i++){
        for (int j=0;j<=W;j++){
            // Lấy cái này hoặc ko lấy cái này
            if (i==0 || j==0) table[i][j] = 0;
            else
            if (w[i-1] > j){
                table[i][j] = table[i-1][j]; // nếu vật phẩm thứ i (1-indexing) to quá lớn hơn sức chứa j thì nó ko lấy vật phẩm này và giá trị bằng sức chứa j xét với các vật phẩm bên trên.
            } else {
                table.at(i).at(j) = max(table[i-1][j], table.at(i-1).at(j-w[i-1]) + val.at(i-1));
            }
        }
    }
    cout << table[n][W];
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
    return 0;
}
```
</details>

<details>
  <summary>Cses - Array description</summary>

```c++
//https://cses.fi/problemset/task/1746/
#include<bits/stdc++.h>
 
typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double
 
using namespace std;
 
// Copy from nealwu's template - http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0200r0.html
template<class Fun> class y_combinator_result { Fun fun_; public:template<class T> explicit y_combinator_result(T &&fun): fun_(std::forward<T>(fun)) {} template<class ...Args> decltype(auto) operator()(Args &&...args) { return fun_(std::ref(*this), std::forward<Args>(args)...); }}; template<class Fun> decltype(auto) y_combinator(Fun &&fun) { return y_combinator_result<std::decay_t<Fun>>(std::forward<Fun>(fun)); }
 
#ifdef DEBUG
#include "debug.cpp"
#else
#define dbg(...)
#endif
 
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    ll n, bound; cin >> n>> bound;
    vector<ll> a(n);
    for (auto &v: a) cin >> v;
    vector<vector<ll>> table(n, vector<ll>(bound+1, 0));
    for (int j=1;j<=bound;j++){
        if (a[0] == 0) {
            table[0][j] = 1;
        } else {
            table[0][j] = 0;
            if (a[0] == j) table[0][j] = 1;
        }
    }
    for (ll i=1;i<n;i++){
        for (ll j=1;j<=bound;j++){
            if (a[i] != 0){
                if (j+1 == a[i]){
                    table[i][a[i]] += table[i-1][j];
                    table[i][a[i]] = table[i][a[i]] % mod;
                } else if (j == a[i]){
                    table[i][j] += table[i-1][j];
                    table[i][j] = table[i][j] % mod;
                } else if (j-1== a[i]){
                    table[i][a[i]] += table[i-1][j];
                    table[i][a[i]] = table[i][a[i]] % mod;
                }
            } else {
                table[i][j] += table[i-1][j];
                table[i][j] = table[i][j] % mod;
                if (j>1) {
                    table[i][j] += table[i-1][j-1];
                    table[i][j] = table[i][j] % mod;
                }
                if (j<bound) {
                    table[i][j] += table[i-1][j+1];
                    table[i][j] = table[i][j] % mod;
                }
            }
        }
    }
    ll ans = 0;
    for (auto v: table[table.size()-1]){
        ans += 1LL*v;
        ans = ans %mod;
    }
    cout << ans;
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}
/*Nguyên nhân lỗi: tràn số int -> chuyển qua dùng ll
Thuật toán cơ bản có bảng giống knapsack
Dùng 1 table
ij 0 1 2 3 4 (bound)
0
1
2
3
4
5
(n)
Table[i][j] thể hiện rằng đang xét tới a[i] và với giá trị j thì có bao nhiêu cách.
Ví dụ 2 0 2 -> table[1][2] -> i = 1 -> xét a[0], j = 2 -> có 1 cách tới là a[0] = 2 -> 2
               từ 2->0 thì table[1][1,2,3] = 1
               table[2][0, 1, 3] = 0 vì a[2] có giá trị nên chỉ đặt giá trị vào được table[2][2]
               table[2][2] = table[1][1] + table[1][2] + table[1][3]
=> Tổng quát table[i][j] = table[i-1][j-1] + table[i-1][j] + table[i-1][j+1] với trường hợp a[i] = 0 hoặc a[i] != 0 nhưng j = a[j] (nghĩa là tại j này có thể đặt các giá trị vào được)
*/
```
</details>