# Heavy light decomposition

> TODO: thêm template \<class T\>.

## Giới thiệu chung

Bằng việc chia nhỏ cây thành các đoạn nhỏ. Ta có thể

* Tính khoảng cách giữa 2 node bất kỳ trên cây
* Tính k-th ancestor của 1 node bất kỳ trên cây
* Dựa vào segmentree có thể tính toán max, min, sum, .. của các node trên path(u->v). Path(u->v) tạo ra 1 array, có thể query trên đoạn đó với segmentree có trên cây

### Giải thích thuật toán
    
![image for HLD](images/hld.png)  

Trên 1 cây bất kỳ, gọi sub(v) là số node con của đỉnh v. Ví dụ node 1 có sub(1) = 4 (node 4, 5, 8, 9)  
Trong các con {u} của đỉnh v, đỉnh nào có sub(u) >= sub(v)/2 thì đó là **heavy vertex**, **uv** gọi là **heavy edge**.  
Xét điểm 0, có con là {1, 2, 3}. 
* sub(0) = 15
* sub(1) = 4
* sub(2) = 8
* sub(3) = 0.  
sub(2) >= sub(0)/2 nên `2 là heavy vertex`, `0->2 là heavy edge`.  
Tương tự như thế ta sẽ được cây như hình bên trên, cạnh dày chính là **heavy**  
Sau bước **decomposition** (lấy code theo như cp-algorithm) sẽ tới phần `builSegtree`.    
Tại đây cây đã được chia nhỏ thành các đoạn nhỏ hơn, tạm gọi là **khối**. Các khối bao gồm các đoạn thẳng - debug các biến có trong phần khởi tạo để xem lại cách tổ chức dữ liệu.  
Bởi vì khi này cây trở thành các đoạn thẳng, coi các đoạn đó là các mảng, dựng `segmenttree` lên toàn bộ các mảng đó ta có thể query trên cây.  
Thuật toán tại template dựng 1 segment tree trên toàn bộ cây để tối ưu hơn.  
**Query on path**
max(u, v) = max(u, lca(u, v)), max(lca(u, v), v)  
Max(u, lca(u, v)) sẽ dùng segtree query trên từng khối.

**Xét cây dưới đây**  
![images/example-tree.png](images/example-tree.png)  
Vấn đề: Cho cây và độ dài các cạnh, query độ dài từ đỉnh (u->v) bất kỳ.  
Cách giải: Segtree yêu cầu trọng số nằm trên các đỉnh của cây, tại đây trọng số đang nằm ở cạnh (chung của 2 đỉnh). Đẩy trọng số xuống đỉnh phía dưới.

![images/example-tree-weight-down.png](images/example-tree-weight-down.png)  
Khi này trọng số sẽ nằm trên 1 đỉnh và buildSegtree trên các node như bình thường. weight(root=0) = 0.

TODO: cần 1 ví dụ thực tế từ decomposition tới việc query. + lý giải về sự hoạt động của từng hàm đã có.

## Reference
* [HLD - cp-algorithm](https://cp-algorithms.com/graph/hld.html) (đã backup tại [backup folder](/backup/tree/))

## Template
	
[HLD template](https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/snippet/hld.sublime-snippet)

## Usage

**Khởi tạo**:  
Decomposition:
```c++
vector<vector<int>> g(N); g[u].push_back(v); g[v].push_back(u);
HeavyLightDecomposition hld(adj);
```
**Build segment tree**
```c++
vector<int> w(N); // trọng số trên các đỉnh của cây. graph sẽ chỉ chứa cạnh và w này sẽ chứa weight.
                  // với weight(u, v) = weight -> uv = depth[u] > depth[v] ? u : v; w[uv] = weight; dùng for cho mọi cạnh là được
hld.buildSegTree(w);
```
**Query**
```c++
LCA lca(g);
hld.query(u, lca(u, v)); hld.query(v, lca(u, v)); // query 2 nửa rồi hợp lại. max(u, v) = max(max(u, lca(u, v)), max(v, lca(u, v)));
                                                  //                          sum(u, v) = sum(sum(u, lca(u, v)), sum(v, lca(u, v)));
```
**Kth_ancestor**
```c++
hld.kth_ancestor(u, kth);
```

**Custom query**
TODO: hướng dẫn về việc sửa hàm, cách suy nghĩ khi gặp bài query
## Lưu ý

	
## Verifications

<details>
  <summary>QTREE</summary>

```c++
// https://www.spoj.com/status/QTREE,hoanglongvn/
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


// Reference: https://cp-algorithms.com/graph/lca.html - toàn bộ source code implement theo hướng dẫn
// Verification: https://www.spoj.com/status/LCA,hoanglongvn/
struct Euler{
    int vertex, height, index;
};
class LCA{
    // Verification: https://atcoder.jp/contests/practice2/submissions/25073318
    template<typename T>
    class LCASegmentTree {
        private:
            ll n;
            vector<T> dat;
        public:
            T merge(T a, T b){
                if (a.height > b.height) return b;
                return a;
            }
            LCASegmentTree(vector<T> v) {
                int _n = v.size();
                n = 1;
                while (n < _n)n *= 2;
                dat.resize(2 * n - 1);
                for (int i=0;i<_n;i++) dat[n + i - 1] = v[i];
                for (int i = n - 2; i >= 0; i--)dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
            }
            LCASegmentTree(int _n) {
                n = 1;
                while (n < _n)n *= 2;
                dat.resize(2 * n - 1);
            }
            void set_val(int i, T x) {
                i += n - 1;
                dat[i] = x;
                while (i > 0) {
                    i = (i - 1) / 2;
                    dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
                }
            }
            T query(int l, int r){
                r++;
                T left = T{INT_MAX, INT_MAX, INT_MAX}, right = T{INT_MAX, INT_MAX, INT_MAX};
                l += n - 1; r += n - 1;
                while (l < r) {
                    if ((l & 1) == 0)left = merge(left, dat[l]);
                    if ((r & 1) == 0)right = merge(dat[r - 1], right);
                    l = l / 2;
                    r = (r - 1) / 2;
                }
                return merge(left, right);
            }
            // Custom
            T query(int l){
                return query(l, l);
            }
            void add(int i, T x){
                set_val(i, query(i) + x);
            }
    };
    /*
    Lưu ý: dòng T left = 0, right = 0; nếu merge là hàm min() thì chuyển về LLONG_MAX. Mục đích là để ko làm ảnh hưởng tới cây khi bắt đầu vào hàm while
    Tham khảo: https://cses.fi/problemset/result/2691498/
    vector<ll> a(n);
    LCASegmentTree<ll> seg(a);
    seg.set_val(index, value);
    seg.query(start, end); //[start, end]
    seg.query(start, start); // start
    */
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
        auto explore = y_combinator([&] (auto explore, int u) -> void {
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
        });
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
    vector<int> height(){
        vector<int> h(this->n, 0);
        for (auto e: eulertour){
            h[e.vertex] = e.height;
        }
        return h;
    }
};
/*
Lưu ý: LCA chạy với 1 SCC, nếu có nhiều SCC thì phải dùng DSU check trước. 
Nếu 2 node ko cùng 1 cây có thể gây ra lỗi
*/

template<typename T>
class SegmentTree {
private:
    ll n;
    vector<T> dat;
public:
    T merge(T a, T b){
        // CHANGE HERE
        return max(a, b); // easily modify to another function like sum()
    }
    SegmentTree(vector<T> v) {
        int _n = v.size();
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
        for (int i=0;i<_n;i++) dat[n + i - 1] = v[i];
        for (int i = n - 2; i >= 0; i--)dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
    }
    SegmentTree(int _n) {
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
    }
    void set_val(int i, T x) {
        i += n - 1;
        dat[i] = x;
        while (i > 0) {
            i = (i - 1) / 2;
            dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
        }
    }
    T query(int l, int r){
        r++;
        T left = 0, right = 0;
        l += n - 1; r += n - 1;
        while (l < r) {
            if ((l & 1) == 0)left = merge(left, dat[l]);
            if ((r & 1) == 0)right = merge(dat[r - 1], right);
            l = l / 2;
            r = (r - 1) / 2;
        }
        return merge(left, right);
    }
    // Custom
    T query(int l){
        return query(l, l);
    }
    void add(int i, T x){
        set_val(i, query(i) + x);
    }
};

// Reference: https://cp-algorithms.com/graph/hld.html
// Verification: https://cses.fi/problemset/result/3568717/
//               https://cses.fi/problemset/result/3573305/
class HeavyLightDecomposition{
public:
    int n;
    vector<int> parent, depth, heavy, head, pos;
    int cur_pos;
    vector<int> pos_to_vertex; // với đỉnh u -> pos[u] + 1 là đỉnh tiếp theo được duyệt. -> pos_to_vertex[pos[u]+1] ra id của đỉnh kế tiếp u
    // dựa vào đó sẽ lấy được vị trí phía dưới trong chain (subtree) - tạm hiểu là child

    HeavyLightDecomposition(vector<vector<int>> adj) {
        this->n = adj.size();
        parent = vector<int>(n);
        depth = vector<int>(n);
        heavy = vector<int>(n, -1);
        head = vector<int>(n);
        pos = vector<int>(n);
        cur_pos = 0;
        // Recursive lambda function
        auto dfs = y_combinator([&] (auto dfs, int v) -> int {
            int size = 1;
            int max_c_size = 0;
            for (int c : adj[v]) {
                if (c != parent[v]) {
                    parent[c] = v, depth[c] = depth[v] + 1;
                    int c_size = dfs(c);
                    size += c_size;
                    if (c_size > max_c_size)
                        max_c_size = c_size, heavy[v] = c;
                }
            }
            return size;    
        });

        auto decompose = y_combinator([&] (auto decompose, int v, int h) -> void {
            head[v] = h, pos[v] = cur_pos++;
            if (heavy[v] != -1)
                decompose(heavy[v], h);
            for (int c : adj[v]) {
                if (c != parent[v] && c != heavy[v])
                    decompose(c, c);
            }
        });
        // 2 hàm này sẽ tính toán toàn bộ các vector<int> parent, depth, heavy, head, pos;
        dfs(0);
        decompose(0, 0);
        // Từ pos lấy ra đỉnh. Hiện tại mảng pos[vertex] = value => tạo ra map[value] = vertex 
        auto mappos_to_value = [&] () -> void {
            pos_to_vertex.resize(this->n);
            for (int v=0;v<pos.size();v++){
                pos_to_vertex[pos[v]] = v;
            }   
        };
        mappos_to_value();
        // dbg(parent); dbg(depth); dbg(heavy); dbg(head); dbg(pos);dbg(pos_to_vertex);
    }
    // Path từ nút con tới LCA. với 2 nút u, v bất kỳ: path(u, v) = path(u, lca(u,v)) + path(v, lca(u, v))
    vector<pair<int,int>> path(int u, int p){
        // assert(lca(u, p) == u || lca(u,p) == p)
        vector<pair<int,int>> pth; // path
        while (head[p] != head[u]){
            pth.push_back({u, head[u]});
            u = parent[head[u]]; // chạy từ u tới điểm đầu substree rồi lấy parent sẽ ra điểm cuối của subtree cha
        }
        // CHANGE HERE - để im nếu trọng số nằm trên cạnh. Trọng số đỉnh thì sử dụng đoạn code dưới
        // Loại bỏ điểm p ra khỏi path - vì weight của u->p đã chạy về u nên chỉ giữ lại u
        if (u!=p){
            int pp = pos[p]; // pp+1=> điểm tiếp theo trong chu trình 
            pth.push_back({u, pos_to_vertex[pp+1]});
        }
        // pth.push_back({u, p}); 
        return pth;
    }

    SegmentTree<int> *seg;
    void buildSegTree(vector<int> weight){ // w này nằm trên đỉnh. nếu nằm trên cạnh thì chuyển qua đỉnh phía dưới edge(u,v) chọn u với u là con v
        // pos[] lưu vị trí của các node theo thứ tự duyệt. Duyệt trong 1 khối (subtree, chain) -> duyệt từ khối này nối sang khối khác
        vector<int> wvt(n); // weight of verticies - làm phẳng tree ra dạng [[chain1][chain2][...]...]
        // khi này muốn query(u, v) thì sẽ chia ra [u..->tailu][...][headv..->v] rồi query từng khúc 1
        for (int i=0;i<n;i++) wvt[pos[i]] = weight[i]; // làm phẳng cây ra thành 1 mảng với các đoạn segment nối tiếp nhau
        this->seg = new SegmentTree<int>(wvt);
    }

    int query(int u, int p){
        // assert(lca(u,p) == u || lca(u,p) == v)
        vector<pair<int,int>> pathu = path(u, p);
        int ans = 0; // lưu ý trường hợp u=p với weight trên cạnh sẽ ko có path u->u do bị cắt đầu. Nên ans sẽ ko thay đổi vẫn = 0
        for (auto chain: pathu){
            // CHANGE HERE max() to any function
            ans = max(ans, seg->query(pos[chain.second], pos[chain.first])); // chain lưu các đỉnh. chuyển các đỉnh đó về vị trí trong seg thì = pos[u]
        }
        return ans;
    }

    void set_val(int u, int val){
        seg->set_val(pos[u], val);
    }
};
/*
vector<vector<int>> adj(N); adj[u].push_back(v); adj[v].push_back(u);
HeavyLightDecomposition hld(adj);

vector<int> w(N); // weight tại đây chính là trọng số của đỉnh đó.
// Nếu trọng số trên Edge(u,v) thì chuyển w về cho đỉnh con trong 2 đỉnh u,v (có thể so sánh depth)
hld.buildSegTree(w);

LCA lca(adj);
hld.query(u, lca.lca(u, v)); hld.query(v, lca.lca(u,v));

==========================
Nếu trọng số nằm trên cạnh cần chuyển trọng số về cho đỉnh 
// trong hàm main adj_w là vector<vector<pair<int (v), int (w)>>> adj_w;
//                adj là vector<vector<int>> loại bỏ w từ adj_w
LCA lca(adj);
vector<int> height = lca.height();
// Đẩy hết trọng số cạnh sang cho node con
vector<int> weight(N, -1);
for (int i=0;i<adj_w.size();i++){
    for (auto vw: adj_w[i]){
        int v = vw.first, w = vw.second;
        if (height[i] > height[v]) weight[i] = w;
        else weight[v] = w;
    }
}
HeavyLightDecomposition hld(adj); // khởi tạo với adj ko weight
hld.buildSegTree(weight); // build segtree có weight sau khi đã khởi tạo
*/
void solve(){
    int n;
    cin >> n;
    vector<vector<int>> adj(n);
    vector<vector<pair<int,int>>> adj_w(n);
    vector<pair<int,int>> seq;
    for (int i=0;i<n-1;i++){
        int u, v, w;
        cin >> u>>v>>w; u--; v--;
        adj[u].push_back(v); adj[v].push_back(u);
        adj_w[u].push_back({v, w}); adj_w[v].push_back({u, w});
        seq.push_back({u, v});
    }
    LCA lca(adj);
    vector<int> height = lca.height();
    HeavyLightDecomposition hld(adj);
    vector<int> weight(n, -1);
    for (int i=0;i<adj_w.size();i++){
        for (auto vw: adj_w[i]){
            int v = vw.first, w = vw.second;
            if (height[i] > height[v]) weight[i] = w;
            else weight[v] = w;
        }
    }
    hld.buildSegTree(weight);
    // Query
    while (true){
        string s; 
        cin >> s;
        if (s == "DONE") return;
        int u, v; cin >> u >> v; u--;
        if (s == "QUERY"){
            v--;
            int p = lca.lca(u, v);
            cout << max(hld.query(u, p), hld.query(v, p)) <<'\n';
        }
        else {
            // Update
            int p1 = seq[u].first;
            int p2 = seq[u].second;
            if (height[p1] > height[p2]){
                hld.set_val(p1, v);
            }
            else hld.set_val(p2, v);
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
    int N;
    cin >> N;
    while (N--) solve();
}
```

</details>
