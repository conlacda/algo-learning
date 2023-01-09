# LCA (lowest common ancestor)

## Giới thiệu chung
Trên 1 tree, LCA chính là cha chung gần nhất của u,v.  
Nói cách khác trên path(u->v) điểm có chiều cao nhỏ nhất là LCA (cũng là điểm gần root nhất khi đi từ u->v)

## Reference
Toàn bộ code được implement theo hướng dẫn tại [CP-algorithm LCA](https://cp-algorithms.com/graph/lca.html)  
Phần hướng dẫn đã được backup trong folder [backup](/backup/cp-algorithm)
## Template
[LCA template](https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/snippet/LCA.sublime-snippet)

## Usage
```c++
vector<vector<int>> graph(n);
graph[u].push_back(v);
graph[v].push_back(u);
```
### Khởi tạo
```c++
LCA lca(graph);
```
### Các hàm 
```c++
lca.lca(u, v); // tìm ra lca của u, v
lca.lca(root, u, v); // tìm ra lca của u, v với root tự chọn
// https://stackoverflow.com/questions/25371865/find-multiple-lcas-in-unrooted-tree?rq=1
// Verification: https://www.codechef.com/viewsolution/58731653
```
**Lấy chiều cao cây**
```c++
vector<ll> height = lca.height();
// Tính khoảng cách của 2 node
distance(u, v) = height[u] + height[v] - 2*height[lca.lca(u, v)]
```

## Lưu ý:
LCA **chỉ chạy trên tree** nên nếu có 1 bài chạy trên graph thì cần dùng **DSU** kiểm tra trước.
## Verification
> Tiện thể cũng là các bài thực hành

<details>
  <summary>LCA -SPOJ.com</summary>

```c++
// https://www.spoj.com/status/LCA,hoanglongvn/
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;

using namespace std;

#ifdef DEBUG
#include "debug.cpp"
#else
#define dbg(...)
#endif

<LCA-snippet>
void solve(){
    int n;
    cin >>n;
    vector<vector<ll>> g(n);
    for (int i=0;i<n;i++){
        int m; cin >>m;
        for (int j=0;j<m;j++){
            int v; cin >>v; v--;
            g[i].push_back(v);
            g[v].push_back(i);
        }
    }
 
    int q;
    cin >>q;
    LCA lca(g);
    for (int i=0;i<q;i++){
        int u, v; cin >> u>>v; u--;v--;
        cout<< lca.lca(u, v) +1<< '\n';
    }
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N;
    cin >> N;
    for (int i=0;i<N;i++){
        cout << "Case " << i+1<< ":\n";
        solve();
    }
}   
```
</details>

<details>
  <summary>1702-G1-G2</summary>
  
```c++
// https://codeforces.com/contest/1702/problem/G1
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

#ifdef DEBUG
#include "debug.cpp"
#else
#define dbg(...)
#endif

<LCA-snippet>
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    // cout << setprecision(2);
    int N;
    cin >> N;
    /*
    Lấy ra điểm thấp nhất -> chính là 1 đỉnh -> A
    Lấy ra đỉnh có khoảng cách xa nhất với nó -> B
    Với mọi điểm C thì AC+BC = AB
    */
    vector<vector<ll>> g(N);
    for (int i=0;i<N-1;i++) {
        ll u, v; cin >> u>> v; u--; v--;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    LCA lca(g);
    vector<ll> height = lca.height();
    ll q;
    cin >> q;
    for (int _=0;_<q;_++){
        ll size; cin >> size;
        vector<ll> s(size);
        for (int i=0;i<size;i++){
            ll e; cin >> e; e--;
            s[i] = e;
        }
        dbg(s);
        // Recursive (1)
        vector<bool> vis(N, false);
        // Lấy ra điểm thấp nhất
        ll snode =s[0] , enode=s[0];
        for (auto v:s){
            if (height[v] > height[snode]){
                snode = v;
            }
        }
        dbg(snode);
        // Lấy ra điểm enode
        ll enode_to_snode = 0;
        for (auto v: s){
            // Tính khoảng cách điểm này tới điểm enode
            ll dis = height[v] + height[snode] - 2*height[lca.lca(v, snode)];
            if (dis > enode_to_snode){
                enode_to_snode = dis;
                enode = v;
            }
        }
        dbg(enode);
        // AC+CB = AB với mọi điểm
        bool ans = true;
        for (auto v: s){
            ll ac = height[snode] + height[v] - 2*height[lca.lca(snode, v)];
            ll cb = height[enode] + height[v] - 2*height[lca.lca(enode, v)];
            ll ab = height[snode] + height[enode] - 2*height[lca.lca(snode, enode)];
            if (ac + cb != ab) {
                ans = false;
                break;
            }
        }
        if (ans) cout << "YES\n"; else cout << "NO\n";
    }
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}
```
</details>

https://www.spoj.com/status/DISQUERY,hoanglongvn/  
(Tham khảo thêm các bài thực hành ở bên dưới của trang cp-algorithm)