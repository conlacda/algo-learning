# Centroid decompose

## Tư tưởng centroid:
+ Dựng mọi node thành centroid và các centroid đó đứng cạnh nhau trong parent[] (centroid tree)
+ Thao tác update: lần lượt đi từ node đó tới các centroid cấp cao hơn và cập nhật lại bảng giá trị (ans) cho các centroid cha đó
+ Thao tác query: lần lượt đi từ node đó tới các centroid cấp cao hơn và so sánh xem node nào gần hơn
Ví du: node A -> node B -> node C. Tìm node gần với A nhất thỏa mãn điều kiện. min(ans[A], ans[B] + dis(A,B), ans[C] + dis(A,C))
nếu node thỏa mãn X nằm giữa A và C -> sẽ tìm được 1 centroid B sao cho A->B->X->C. Khi đó result = min(ans[A], ans[B]+dis(A,B))
-> không bao giờ có trường hợp A->X->C mà kết quả lại bằng ans[C] + dis(A,C)
Verification: https://codeforces.com/contest/342/submission/152517523

## Template
https://github.com/conlacda/noteforprofessionals/blob/ea39d251df/language/C%2B%2B/snippet/centroid-decomposition.sublime-snippet

##

<details>
  <summary>E. Xenia and Tree</summary>
  
  ```c++
// https://codeforces.com/contest/342/problem/E
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
#define debug(...)
#endif

class LCA{
    struct Euler{
        int vertex, height, index;
    };
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
    vector<set<int>> graph;
    vector<bool> visited;
    vector<Euler> eulertour;
    vector<Euler> first;
    LCASegmentTree<Euler> *seg;
    LCA(vector<set<int>> graph, int root=0){
        this->graph = graph;
        this->n = graph.size();
        visited.resize(n);
        first.resize(n);
        this->makeEuler(root);
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
    /* Additional functionality*/
    // Trả về chiều cao của 1 đỉnh h[vertex] = v_height; - chiều cao bắt đầu từ 1->n (1-indexed)
    vector<int> height(){
        vector<int> h(this->n, 0);
        for (auto e: eulertour){
            h[e.vertex] = e.height;
        }
        return h;
    }

    // https://stackoverflow.com/questions/25371865/find-multiple-lcas-in-unrooted-tree?rq=1
    // Verification: https://www.codechef.com/viewsolution/58731653
    int lca_ar(int r, int u, int v){ // ar = abtrary root - LCA của u,v với r bất kỳ là root
        int ru = lca(r, u);
        int rv = lca(r, v);
        int uv = lca(u, v);
        if (ru == rv) return uv;
        if (ru == uv) return rv;
        return ru;
    }
};

// Reference: https://robert1003.github.io/2020/01/16/centroid-decomposition.html#whats-a-centroid
// Xem phần code nguyên bản: https://codeforces.com/contest/342/submission/152517523 - cho phần code như hiện tại: https://codeforces.com/contest/342/submission/152554214
class CentroidDecomposition{
private:
    int N;
    vector<set<int>> original_gr;
public:
    vector<int> parent; // thể hiện centroid tree
    vector<int> childNum;
    CentroidDecomposition(vector<set<int>> original_gr){
        // Assign values
        N = original_gr.size();
        this->original_gr = original_gr;
        parent.assign(N, -1);
        childNum.assign(N, 0);
        // initial calls
        cal_childNum(0, -1);
        decompose(0, -1); // return parent[]
        // additional part
        ans.resize(N, INT_MAX);
        this->lca = new LCA(original_gr);
        this->depth = this->lca->height();
    }
    int cal_childNum(int root, int parent){
        childNum[root] = 0;
        for (auto v: original_gr[root]){
            if (v != parent) 
                childNum[root] += cal_childNum(v, root) +1;
        }
        return childNum[root];
    }
    int get_centroid(int root, int parent, int n){
        for (auto v: original_gr[root]){
            if (v != parent)
                if (childNum[v] +1 > n/2) return get_centroid(v, root, n); 
        }
        return root;
    }
    void decompose(int u, int c){
        int size_subTree = cal_childNum(u, c) + 1;
        int sub_centroid = get_centroid(u, u, size_subTree);
        parent[sub_centroid] = c;
 
        set<int> tmp = original_gr[sub_centroid];
        for (auto v: tmp){
            original_gr[sub_centroid].erase(v);
            original_gr[v].erase(sub_centroid);            
            decompose(v, sub_centroid);
        }
    }
    // Additional part
    vector<int> ans;
    LCA *lca;
    vector<int> depth;
    void update(int u){
        // CHANGE HERE
        // Update từ node u tới mọi centroid (đi lên trong centroid tree)
        ans[u] = 0;
        int p = u;
        // Leo lên vị trí trên bằng mảng parent[] - centroid tree
        while (parent[p] != -1){
            p = parent[p];
            int u_to_p = depth[u] + depth[p] - 2* depth[this->lca->lca(u, p)];
            ans[p] = min(ans[p], u_to_p);
        }
    }
    int query(int u){
        // CHANGE HERE
        // Query từ node u tới mọi centroid (đi lên trong centroid tree)
        int result = ans[u];
        int p = u;
        while (parent[p] != -1){
            p = parent[p]; // leo lên trong cây centroid
            int u_to_p = depth[u] + depth[p] - 2* depth[this->lca->lca(u, p)]; // khoảng cách u->p trong cây ban đầu
            if (ans[p] != INT_MAX)
                result = min(result, ans[p] + u_to_p);            
        }
        return result;
    }
};

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N, q;
    cin >> N >> q;
    // Read graph
    vector<set<int>> sgr(N);
    for (int i=0;i<N-1;i++){
        int u, v; cin >> u>> v; u--; v--;
        sgr[u].insert(v);
        sgr[v].insert(u);
    }
    CentroidDecomposition ctd(sgr); // ctd.parent
    // Query
    ctd.update(0);
    for (int i=0;i<q;i++){
        int t, u; cin >> t >> u; u--;
        if (t == 1){
            // Update
            ctd.update(u);
        } else{
            // Query
            cout << ctd.query(u) <<'\n';
        }
    }
}
  ```
</details>

<details>
  <summary>QTREE5 - Query on a tree V</summary>
  
  ```c++
  https://www.spoj.com/problems/QTREE5/
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
#define debug(...)
#endif

class LCA{
    struct Euler{
        int vertex, height, index;
    };
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
public:
    int n;
    vector<set<int>> graph;
    vector<bool> visited;
    vector<Euler> eulertour;
    vector<Euler> first;
    LCASegmentTree<Euler> *seg;
    LCA(vector<set<int>> graph){
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
    /* Additional functionality*/
    // Trả về chiều cao của 1 đỉnh h[vertex] = v_height; - chiều cao bắt đầu từ 1->n (1-indexed)
    vector<int> height(){
        vector<int> h(this->n, 0);
        for (auto e: eulertour){
            h[e.vertex] = e.height;
        }
        return h;
    }

    // https://stackoverflow.com/questions/25371865/find-multiple-lcas-in-unrooted-tree?rq=1
    // Verification: https://www.codechef.com/viewsolution/58731653
    int lca_ar(int r, int u, int v){ // ar = abtrary root - LCA của u,v với r bất kỳ là root
        int ru = lca(r, u);
        int rv = lca(r, v);
        int uv = lca(u, v);
        if (ru == rv) return uv;
        if (ru == uv) return rv;
        return ru;
    }
};

class CentroidDecomposition{
private:
    int N;
    vector<set<int>> original_gr;
public:
    vector<int> parent; // thể hiện centroid tree
    vector<int> childNum;
    vector<int> color;
    CentroidDecomposition(vector<set<int>> original_gr){
        // Assign values
        N = original_gr.size();
        this->original_gr = original_gr;
        parent.assign(N, -1);
        childNum.assign(N, 0);
        // initial calls
        cal_childNum(0, -1);
        decompose(0, -1); // return parent[]
        // additional part
        ans.resize(N);
        this->lca = new LCA(original_gr);
        this->depth = this->lca->height();
        this->color.resize(N, 1);
    }
    int cal_childNum(int root, int parent){
        childNum[root] = 0;
        for (auto v: original_gr[root]){
            if (v != parent) 
                childNum[root] += cal_childNum(v, root) +1;
        }
        return childNum[root];
    }
    int get_centroid(int root, int parent, int n){
        for (auto v: original_gr[root]){
            if (v != parent)
                if (childNum[v] +1 > n/2) return get_centroid(v, root, n); 
        }
        return root;
    }
    void decompose(int u, int c){
        int size_subTree = cal_childNum(u, c) + 1;
        int sub_centroid = get_centroid(u, u, size_subTree);
        parent[sub_centroid] = c;
 
        set<int> tmp = original_gr[sub_centroid];
        for (auto v: tmp){
            original_gr[sub_centroid].erase(v);
            original_gr[v].erase(sub_centroid);            
            decompose(v, sub_centroid);
        }
    }
    // Additional part
    vector<multiset<int>> ans;
    LCA *lca;
    vector<int> depth;
    void update(int u){
        if (color[u] == 0){ // white -> black
            // ans[u].erase(0);
            ans[u].erase(ans[u].lower_bound(0));
            int p = u;
            // leo dần lên để xóa đi giá trị tương ứng với node này
            while (parent[p] != -1){
                p = parent[p];
                int u_to_p = depth[u] + depth[p] - 2*depth[this->lca->lca(u, p)];
                ans[p].erase(ans[p].lower_bound(u_to_p));
            }
        } else {// black -> white
            // leo dần lên để thêm vào
            ans[u].insert(0);
            int p = u;
            while (parent[p] != -1){
                p = parent[p];
                int u_to_p = depth[u] + depth[p] - 2*depth[this->lca->lca(u, p)];
                ans[p].insert(u_to_p);
            }
        }
        color[u] = 1 - color[u];
    }
    int query(int u){        
        // Query từ node u tới mọi centroid (đi lên trong centroid tree)
        int result;
        if (!ans[u].empty()) result = *ans[u].begin();
        else result = INT_MAX;
        int p = u;
        while (parent[p] != -1){
            p = parent[p]; // leo lên trong cây centroid
            int u_to_p = depth[u] + depth[p] - 2* depth[this->lca->lca(u, p)]; // khoảng cách u->p trong cây ban đầu
            if (!ans[p].empty())
                result = min(result, *ans[p].begin() + u_to_p);            
        }
        if (result == INT_MAX) return -1;
        return result;
    }
};

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N;
    cin >> N;
    vector<set<int>> adj(N);
    for (int i=0;i<N-1;i++){
        int u, v; cin >> u>> v; u--;v--;
        adj[u].insert(v);
        adj[v].insert(u);
    }
    CentroidDecomposition cdc(adj);

    int q;
    cin >> q;
    for (int i=0;i<q;i++){
        int t, u; cin>>t>>u; u--;
        // query, update
        if (t==0) cdc.update(u);
        else {
            cout << cdc.query(u)<<'\n';
        }
    }
}
  ```
</details>