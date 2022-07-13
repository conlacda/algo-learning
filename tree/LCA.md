# LCA (lowest common ancestor)

## Giới thiệu chung
Cho 1 tree, với 2 điểm bất kỳ u, v, cha chung gần nhất của 2 điểm chính là lca. Nói cách khác trên path(u->v) điểm có chiều cao thấp nhất chính là lca

## Template
Toàn bộ code được implement theo hướng dẫn tại [CP-algorithm LCA](https://cp-algorithms.com/graph/lca.html) (có file pdf backup trong thư mục [backup](/backup/cp-algorithm))

Code [LCA template](https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/snippet/LCA.sublime-snippet)

## Các bài thực hành

<details>
  <summary>1702-G1</summary>
  
```c++
// https://codeforces.com/contest/1702/problem/G1
// Submission: https://codeforces.com/contest/1702/submission/164046789
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

// Reference: https://cp-algorithms.com/graph/lca.html - toàn bộ source code implement theo hướng dẫn
// Verification: https://www.spoj.com/status/LCA,hoanglongvn/
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
    vector<vector<ll>> graph;
    vector<bool> visited;
    vector<Euler> eulertour;
    vector<Euler> first;
    LCASegmentTree<Euler> *seg;
    LCA(vector<vector<ll>> graph){
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
    vector<ll> height(){
        vector<ll> h(this->n, 0);
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
/*
Lưu ý: LCA chạy với 1 SCC, nếu có nhiều SCC thì phải dùng DSU check trước. 
Nếu 2 node ko cùng 1 cây có thể gây ra lỗi
*/
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
		vector<ll> height(N, 0);
		auto explore = y_combinator([&] (auto explore, int u) -> void {
			if (!vis[u]){
				vis[u] = true;
				for (auto v: g[u]){
					if (!vis[v]){
						height[v] = height[u] +1;
						explore(v);
					}
				}
			}
		});
		explore(0); // 0 is root
		dbg(height);
		// Lấy ra điểm thấp nhất
		ll snode =s[0] , enode=s[0];
		for (auto v:s){
			if (height[v] > height[snode]){
				snode = v;
			}
		}
		dbg(snode);
		// Lấy ra điểm enode
		std::fill(vis.begin(), vis.end(), false);
		std::fill(height.begin(), height.end(), 0);
		explore(snode);
		for (auto v: s){
			if (height[v] > height[enode]) enode = v;
		}
		dbg(enode);
		// AC+CB = AB với mọi điểm C thuộc s
		height = lca.height();
		dbg(height);
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

https://www.spoj.com/status/LCA,hoanglongvn/  
https://www.spoj.com/status/DISQUERY,hoanglongvn/  
(Tham khảo thêm các bài thực hành ở bên dưới của trang cp-algorithm)