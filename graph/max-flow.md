# Max flow on graph
> Sử dụng thuật toán Dinic O(E\*V*V)

Bài toán max flow có khá nhiều cách giải và độ phức tạp cũng khác nhau. Tại đây sử dụng Dinic để giải (1 phần vì các template khác lỗi, hoặc tương đối khó để sử dụng)
## 1 vài khái niệm
* Residual graph: là đồ thị để xử lý thuật toán, đồ thị này là 1 grid N*N và thay đổi trong quá trình xử lý. Toàn bộ quá trình duyệt đều sử dụng graph này (trong thuật toán Dinic, ko dùng tới graph ban đầu)
* Augment path: 1 path từ s->t mà có số dư flow > 0
* Min-cut: là 1 đường cắt các cạnh đồ thị chia nó làm 2 nửa, min-cut value chính là tổng của các cạnh bị cắt (chỉ tính cạnh đi từ Set(s) -> Set(t) không tính cạnh đi ngược hay đi ngang). 
	* Tìm min-cut: duyệt BFS() trên residual graph. Xét s, a, b, t. s - điểm đầu, t - điểm cuối, a,b - 2 điểm trong đồ thị. Điều kiện duyệt BFS(u) -> BFS(v) là u->v trên residual graph lớn hơn 0. (=0 nghĩa là nó đã có flow đi qua làm bão hòa. ví dụ ban đầu u->v=10 thì khi dùng 10 trên residual graph sẽ là 0). Khi này nếu uv=0 và trên graph ban đầu có u->v > 0 tức là đây là 1 cạnh bão hòa (saturated edge). Khi xóa bỏ cạnh này sẽ làm cho đồ thị bị cắt (gián đoạn). Xét hình dưới đây ![max-flow-sample-1](images/max-flow-sample-1.png)
	Xét việc maxflow dùng cạnh 1->3, 3->5, 1->4, 4->5. 1 tại đây ko thể tới trực tiếp 3, nhưng đi tới 2 sẽ tới 3. 3 không chạm đc 5 -> Edge(3,5) chính là 1 cạnh bão hòa. Tương tự 1->4 là 1 cạnh bão hòa. Vậy min-cut edges sẽ là 3->5 và 1->4.
## Tham khảo

* https://www.youtube.com/watch?v=oHy3ddI9X3o&ab_channel=MITOpenCourseWare
* https://www.youtube.com/watch?v=VYZGlgzr_As&ab_channel=MITOpenCourseWare
## Template
[Max flow dinic template](https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/snippet/graph-dinic-max_flow.sublime-snippet)
## Bài giải

<details>
  <summary>CSES Download speed</summary>
  
```c++
// https://cses.fi/problemset/task/1694/
#include <bits/stdc++.h>
 
using namespace std;
 
typedef long long ll;
 
#ifdef DEBUG
#include "debug.cpp"
#else
#define dbg(...)
#endif
/*
** Dinic's algorithm for maximum flow problem
** Explain video: https://www.youtube.com/watch?v=duKIzgJQ1w8&ab_channel=FitCoder
** Reference: https://github.com/fit-coder/fitcoderyoutube/blob/master/graph/dinic_algorithm.cpp
** Graph Playlist: https://youtube.com/playlist?list=PLFj4kIJmwGu3m30HfYDDufr3PZBfyngr0
*/
class Dinic_Maxflow{
private:
	ll n;
	vector<vector<ll>> graph;
	vector<vector<ll>> residualGraph;
	vector<ll> level, count_;
public:
	Dinic_Maxflow(vector<vector<ll>> graph){
		this->graph = graph;
		this->n = graph.size();
		level.resize(n, -1);
		count_.resize(n, 0);
		this->residualGraph = graph;
	}
	bool bfs(ll source, ll sink) // on residualGraph
	{
	    fill(level.begin(), level.end(), -1);
	    level[source] = 0;
	    
	    queue<ll> q;
	    q.push(source);
	 
	    while (!q.empty())
	    {
	        ll u = q.front();
	        q.pop();
	        for (ll v=0; v < n; v++)
	        {
	            if (u != v && residualGraph[u][v] > 0 && level[v] < 0)
	            {
	                // Level of current vertex is level of parent + 1
	                level[v] = level[u] + 1;
	                q.push(v);
	            }
	        }
	    }
	    // IF we can not reach to the sink we
	    // return false else true
	    return level[sink] < 0 ? false : true ;
	}
	ll sendFlow(ll u, ll sink, ll flow){ // on residualGraph
	    // Sink reached
	    if (u == sink)
	        return flow;
	 
	    if (count_[u] == (ll) residualGraph[u].size())
	        return 0;
	 
	    // Traverse all adjacent edges one-by-one.
	    for (ll v=0; v < n; v++)
	    {
	        if (residualGraph[u][v] > 0)
	        {
	            count_[u]++;
	            if (level[v] == level[u]+1)
	            {
	                // find minimum flow from u to sink
	                ll curr_flow = min(flow, residualGraph[u][v]);
	 
	                ll min_cap = sendFlow(v, sink, curr_flow);
	                if (min_cap > 0){
	                    residualGraph[u][v] -= min_cap;
	                    residualGraph[v][u] += min_cap;
	                    return min_cap;
	                }
	            }
	        }
	    }
	    return 0;
	}
 
	ll max_flow(ll source, ll sink){
	    if (source == sink)
	        return -1;
	 
	    ll max_flow = 0;
	    residualGraph = graph;
	 
	    // Augment the flow while there is path from source to sink
	    while (bfs(source, sink) == true){
	        // store how many neighbors are visited
	        fill(count_.begin(), count_.end(), 0);
	 
	        // while flow is not zero in graph from source to sink
	        while (ll flow = sendFlow(source, sink, LLONG_MAX))
	            max_flow += flow;
	    }
	    return max_flow;
	}
};
/*
Thuật toán này copy nên mình ko hiểu về cách nó hoạt động. Lưu ý graph là 1 bảng n*n nên n thường khá nhỏ <= 1000
vector<vector<ll>> graph(n, vector<ll> (n, 0));
graph[u][v] = c; // += c nếu nó cho phép u->v có nhiều đường
Dinic_Maxflow dinic(graph);
cout << dinic.max_flow(start, end);
*/
int main()
{
	ios::sync_with_stdio(0);
	cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
		freopen("out.txt", "w", stdout);
    #endif
	ll n, q; cin >> n>> q;
	vector<vector<ll>> graph(n, vector<ll> (n, 0));
	for (ll i=0;i<q;i++){
		ll u, v, c;
		cin >> u>> v>> c; u--; v--;
		graph[u][v] += c;
	}
	Dinic_Maxflow dinic(graph);
	cout << dinic.max_flow(0, n-1);
    return 0;
}
```
</details>

<details>
  <summary>CSES Police Chase</summary>
  
```c++
//https://cses.fi/problemset/task/1695/
#include <bits/stdc++.h>
 
using namespace std;
 
typedef long long ll;
 
#ifdef DEBUG
#include "debug.cpp"
#else
#define dbg(...)
#endif
/*
** Dinic's algorithm for maximum flow problem
** Explain video: https://www.youtube.com/watch?v=duKIzgJQ1w8&ab_channel=FitCoder
** Reference: https://github.com/fit-coder/fitcoderyoutube/blob/master/graph/dinic_algorithm.cpp
** Graph Playlist: https://youtube.com/playlist?list=PLFj4kIJmwGu3m30HfYDDufr3PZBfyngr0
*/
class Dinic_Maxflow{
private:
	ll n;
	vector<vector<ll>> graph;
	vector<vector<ll>> residualGraph;
	vector<ll> level, count_;
public:
	Dinic_Maxflow(vector<vector<ll>> graph){
		this->graph = graph;
		this->n = graph.size();
		level.resize(n, -1);
		count_.resize(n, 0);
	}
	bool bfs(ll source, ll sink) // on residualGraph
	{
	    fill(level.begin(), level.end(), -1);
	    level[source] = 0;
	    
	    queue<ll> q;
	    q.push(source);
	 
	    while (!q.empty())
	    {
	        ll u = q.front();
	        q.pop();
	        for (ll v=0; v < n; v++)
	        {
	            if (u != v && residualGraph[u][v] > 0 && level[v] < 0)
	            {
	                // Level of current vertex is level of parent + 1
	                level[v] = level[u] + 1;
	                q.push(v);
	            }
	        }
	    }
	    // IF we can not reach to the sink we
	    // return false else true
	    return level[sink] < 0 ? false : true ;
	}

	ll sendFlow(ll u, ll sink, ll flow){ // on residualGraph
	    // Sink reached
	    if (u == sink)
	        return flow;
	 
	    if (count_[u] == (ll) residualGraph[u].size())
	        return 0;
	 
	    // Traverse all adjacent edges one-by-one.
	    for (ll v=0; v < n; v++)
	    {
	        if (residualGraph[u][v] > 0)
	        {
	            count_[u]++;
	            if (level[v] == level[u]+1)
	            {
	                // find minimum flow from u to sink
	                ll curr_flow = min(flow, residualGraph[u][v]);
	 
	                ll min_cap = sendFlow(v, sink, curr_flow);
	                if (min_cap > 0){
	                    residualGraph[u][v] -= min_cap;
	                    residualGraph[v][u] += min_cap;
	                    return min_cap;
	                }
	            }
	        }
	    }
	    return 0;
	}

	vector<pair<ll, ll>> mincut_edges;
	ll max_flow(ll source, ll sink){
	    if (source == sink)
	        return -1;
	 
	    ll max_flow = 0;
	    residualGraph = graph;
	 
	    // Augment the flow while there is path from source to sink
	    while (bfs(source, sink) == true){
	        // store how many neighbors are visited
	        fill(count_.begin(), count_.end(), 0);
	 
	        // while flow is not zero in graph from source to sink
	        while (ll flow = sendFlow(source, sink, LLONG_MAX))
	            max_flow += flow;
	    }
	    /* Lấy ra min-cut edges - min-cut là cạnh mà khi cắt nó sẽ làm gián đoạn max-flow, là đoạn có weight nhỏ nhất trên augment path chứa nó
		* Dùng BFS() duyệt từ start. Điều kiện BFS(u) -> BFS(v) là weight(uv) tại residualGraph > 0. 
		* a->b = 3 b->c =2 c->d = 4. -> maxflow = 2 và tại residual graph a->b = 1, b->c = 0, c->d = 2. b->a=1, d->c=2. -> bc là min-cut
		* u->v nếu visited[u] = true. visited[v] = false. graph[u][v] > 0 thì nghĩa là cạnh uv ban đầu có nhưng đã sử dụng tạo ra max flow làm cho v ko tới được từ u
		* Chính vì thế uv chính là 1 mincut. Nói cách khác "Nếu đồ thị ban đầu có cạnh A->B trong đó A tới được, B không thì AB là min-cut edge"
	    * NẾU KHÔNG DÙNG MINCUT_EDGES THÌ XÓA ĐOẠN TỪ ĐÂY XUỐNG DƯỚI, MAX_FLOW VẪN ĐƯỢC TRẢ VỀ
 	    */
	    mincut_edges.resize(0);
	    vector<bool> vis(this->n, false);
	    queue<ll> Q;
	    Q.push(source); vis[source] = true;
	    while (!Q.empty()){
	    	ll p = Q.front();
	    	Q.pop();
	    	for (ll v=0; v<n;v++){
	    		if (residualGraph[p][v] > 0 && !vis[v]){
	    			Q.push(v); vis[v] = true;
	    		}
	    	}
	    }
	    for (ll i = 0;i<n;i++){
	    	for (ll j =0;j<n;j++){
	    		if (graph[i][j] > 0 && vis[i] && !vis[j]){
	    			mincut_edges.push_back({i, j});
	    		}
	    	}
	    }
	    return max_flow;
	}
};
/*
Thuật toán này copy nên mình ko hiểu về cách nó hoạt động. Lưu ý graph là 1 bảng n*n nên n thường khá nhỏ <= 1000
vector<vector<ll>> graph(n, vector<ll> (n, 0));
graph[u][v] = c; // += c nếu nó cho phép u->v có nhiều đường
Dinic_Maxflow dinic(graph);
cout << dinic.max_flow(0, n-1);
dbg(dinic.mincut_edges);
*/
int main()
{
	ios::sync_with_stdio(0);
	cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
		freopen("out.txt", "w", stdout);
    #endif
	ll n, q; cin >> n>> q;
	vector<vector<ll>> graph(n, vector<ll> (n, 0));
	for (ll i=0;i<q;i++){
		ll u, v, c=1;
		cin >> u>> v; u--; v--;
		graph[u][v] = c;
		graph[v][u] = c;
	}
	Dinic_Maxflow dinic(graph);
	dinic.max_flow(0, n-1);
	cout << dinic.mincut_edges.size()<<'\n';
	for (auto v: dinic.mincut_edges){
		cout << v.first+1<< ' '<<v.second+1<<'\n';
	}
    return 0;
}
```
</details>
