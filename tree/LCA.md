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
**Lấy cha thứ k của 1 node**: hàm này sẽ dùng HLD để lấy. LCA với spare table có thể lấy được trực tiếp nhưng mk đã ko implement.
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

<details>
  <summary>Distance in the tree</summary>

```c++
// https://acm.timus.ru/problem.aspx?space=1&num=1471
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

class LCA{
    struct Euler{
        int vertex, height, index;
    };
    template<typename T>class LCASegmentTree{private:ll n;vector<T>dat;public:T merge(T a,T b){if(a.height>b.height)return b;return a;}LCASegmentTree(vector<T>v){int _n=v.size();n=1;while(n<_n)n*=2;dat.resize(2*n-1);for(int i=0;i<_n;i++)dat[n+i-1]=v[i];for(int i=n-2;i>=0;i--)dat[i]=merge(dat[i*2+1],dat[i*2+2]);} LCASegmentTree(int _n){n=1;while(n<_n)n*=2;dat.resize(2*n-1); } void set_val(int i,T x){i+=n-1;dat[i]=x;while(i>0){i=(i-1)/2;dat[i]=merge(dat[i*2+1],dat[i*2+2]);}}T query(int l,int r){r++;T left=T{INT_MAX,INT_MAX,INT_MAX},right=T{INT_MAX,INT_MAX,INT_MAX};l+=n-1;r+=n-1;while(l<r){if((l&1)==0)left=merge(left,dat[l]);if((r&1)==0)right=merge(dat[r-1],right);l=l/2;r=(r-1)/2;}return merge(left,right);}};
public:
    int n;
    vector<vector<int>> graph;
    vector<bool> visited;
    vector<Euler> eulertour;
    vector<Euler> first;
    LCASegmentTree<Euler> *seg;
    LCA(vector<vector<int>> graph){
        this->graph = graph;
        this->n = graph.size();
        visited.resize(n);
        first.resize(n);
        this->makeEuler();
    }

    // Euler tour of tree
    void makeEuler(int root = 0){
        // Euler tour tạo ra verticies, heights, index
        std::fill(visited.begin(), visited.end(), false);
        int height =0;
        std::function<void(int)> explore = [&](int u){
            visited[u] = true;
            height++;
            eulertour.push_back(Euler{u, height, (int) eulertour.size()});
            for (auto v: this->graph[u]){
                if (!visited[v]) {
                    explore(v);
                    height--;
                    eulertour.push_back(Euler{u, height, (int) eulertour.size()});
                }
            }
        };
        explore(root);
        // Tạo ra mảng first
        std::fill(visited.begin(), visited.end(), false);
        for (auto e: eulertour){
            if (!visited[e.vertex]){
                visited[e.vertex] = true;
                first[e.vertex] = e;
            }
        }
        // Tạo 1 segment tree để query trên mảng height
        this->seg = new LCASegmentTree<Euler>(eulertour);
    }

    int lca(int u, int v){
        int uidx = first[u].index;
        int vidx = first[v].index;
        if (uidx > vidx) swap(uidx, vidx);
        Euler a = seg->query(uidx, vidx);
        return a.vertex;
    }
    /* Additional functionality*/
    // Trả về chiều cao của 1 đỉnh h[vertex] = v_height; - chiều cao bắt đầu từ 1->n (1-indexed)
    vector<ll> height(){
        vector<ll> h(this->n, 0);
        for (auto e: eulertour){
            h[e.vertex] = e.height;
        }
        return h;
    }
    // Để tính khoảng cách: distance(u, v) = height[u] + height[v] - 2*height[lca(u, v)] - ko thêm hàm để tránh làm rắc rối thêm phần khởi tạo

    int lca(int r, int u, int v){ // ar = abtrary root - LCA của u,v với r bất kỳ là root
        int ru = lca(r, u);
        int rv = lca(r, v);
        int uv = lca(u, v);
        if (ru == rv) return uv;
        if (ru == uv) return rv;
        return ru;
    }
};
/*
vector<vector<int>> graph(n); graph[u].push_back(v);
LCA lca(graph);
lca.lca(u, v);
vector<ll> h = lca.height(); // h[root] = 1;
Full doc: https://github.com/conlacda/algo-learning/blob/master/tree/LCA.md
*/
int main(){
    ios::sync_with_stdio(0); cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int n; cin >> n;
    vector<vector<pair<int,int>>> g(n);
    vector<vector<int>> g_(n);
    for (int i=0;i<n-1;i++){
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g_[u].push_back(v);
        g[v].push_back({u, w});
        g_[v].push_back(u);
    }
    /*
    duyệt DFS() để tính khoảng cách mọi điểm tới đỉnh
    */
    int root = 0;
    vector<int> distance(n, 0);
    std::function<void(int, int)> dfs = [&](int u, int parent){
        for (auto p: g[u]) {
            int v = p.first, w = p.second;
            if (v == parent) continue;
            distance[v] = distance[u] + w;
            dfs(v, u);
        }
    };
    dfs(root, -1);
    LCA lca(g_);
    int q;
    cin >> q;
    for (int i=0;i<q;i++){
        int u, v; cin >> u >> v;
        cout << distance[u] + distance[v] - 2*distance[lca.lca(u, v)] <<'\n';
    }
    // cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}
```  
</details>

https://www.spoj.com/status/DISQUERY,hoanglongvn/  
(Tham khảo thêm các bài thực hành ở bên dưới của trang cp-algorithm)