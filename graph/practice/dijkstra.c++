//https://cses.fi/problemset/result/2532354/
// Bài toán áp dụng priority_queue vào thuật toán dijkstra để làm giảm độ phức tạp thuật toán
/*
Giải thuật Dijkstra:
* Khởi tạo node S có dist=0, mọi node khác có dist=inf
* Thêm các node xung quanh S vào Queue với độ dài là w từ S->node và đánh dấu visited
* Khi S còn phần tử thì lấy ra phần tử có độ dài nhỏ nhất trong Queue.
* if (S->node + node->neighbour < S->neighbour){
     S->neighbour = S->node + node->neighbour;
     if (!visited[neighbour]) {
         Queue.push_back(neighbour);
         visited[neighbour] = true;
     }
}
* In ra dist

* Phân tích: tại thao tác tìm kiếm node nhỏ nhất trong Queue. Nếu node A có 100.000 neighbour thì mỗi vòng lặp lấy ra 1 phần tử nhỏ nhất sẽ tốn 100.000 thao tác => O(N^2) trong thao tác tìm kiếm gây ra TLE.

* Thay thế Queue từ vector thông thường thành 1 priority_queue.
priority_queue là 1 cấu trúc tự động sắp xếp với hàm được định nghĩa. Insert 1 node mới sẽ tốn O(logN) thao tác. Lấy node nhỏ nhất sẽ tốn O(1)
-> tổng thời gian log(N)*N. 100000*log100000=500000 <<10*9
*/
#include<bits/stdc++.h>
 
typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double
 
using namespace std;

struct Node {
    int id; ll dist;
    friend bool operator<(const Node &a, const Node &b){
        return a.dist > b.dist;
    }
};

class WeightedDirectedGraph{
public:
    int V;
    vector<vector<pair<int,int>>> G;
    vector<bool> visited;
    WeightedDirectedGraph(int V){
        for (int i=0;i<=V;i++){
            G.push_back({});
            this->visited.push_back(false);
        }
        this->V = V;
    }
    void addEdge(int a, int b, ll w){
        G[a].push_back(make_pair(b,w));
    }
    void show(){
        cout << G.size() -1 << " verticies\n";
        for (int i=0;i<=V;i++){
            for (auto v: G[i]){
                cout << i << "->";
                cout << v.first << " = " << v.second << '\n';
            }
        }
    }
    void dijkstra(int start){
        priority_queue<Node> Q;
        vector<ll> dist(V+1, LLONG_MAX);
        dist[start] = 0; visited[start] = true;
        
        for (int i=0;i<G[start].size();i++){
            if (dist[G[start][i].first] > G[start][i].second)
                dist[G[start][i].first] = G[start][i].second;
            visited[G[start][i].first] = true;
            Q.push({G[start][i].first, dist[G[start][i].first]});
        }

        while (!Q.empty()){
            ll d = Q.top().dist;
            int u = Q.top().id;
            Q.pop();
            if (d>dist[u]) continue;
            /*if (d>dist[u]) continue;
            Thao tác này giả sử trong Q có {x,d1} {x,d2}. Nếu d1>dist[x] thì bỏ qua
            và sau 1 số thao tác d2=dist[x] x sẽ được xử lý
            */
            for (int i=0;i<G[u].size();i++){
                if (d+ G[u][i].second <dist[G[u][i].first]){
                    dist[G[u][i].first] = d + G[u][i].second;
                    Q.push({G[u][i].first, dist[G[u][i].first]});
                    /*1->2 2->1 2->3 xét u=2. Thao tác thêm tại đây sẽ thêm 3 vào Q. 1 sẽ bỏ qua vì 1->2 nên dist[1] < dist[2] => dist[2] + 2->1 > dist[1]*/
                }
            }
        }
        for (int i =1;i<dist.size();i++) cout << dist[i] << ' ';
    }
};

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int n,m;
    cin >> n>>m;
    WeightedDirectedGraph g(n);
    while (m--){
        int a,b,w;
        cin >> a>>b>>w;
        g.addEdge(a,b,w);
    }
    int start = 1;
    // g.show();
    g.dijkstra(start);
}