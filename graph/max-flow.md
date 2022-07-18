# Max flow on graph
> Sử dụng thuật toán Dinic

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