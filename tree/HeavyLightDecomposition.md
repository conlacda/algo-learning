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
Nhớ điều chỉnh hàm trong segmenttree
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

**Tham số cần quan tâm**
* pos[]: trong quá trình build segment tree, cây sau khi được decomposition sẽ được ghép từng đoạn vào thành 1 mảng rồi dựng segment tree trên mảng đó. pos[] sẽ ánh xạ chỉ số node vào với index trong segment tree.  
  `pos[node] = segtree_index`.  
  `seg->set_val(pos[node], val)` khi muốn cập nhật weight của node.

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
 
<LCA-snippet>
<HLD-snippet>
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
    vector<ll> height = lca.height();
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
    
* https://cses.fi/problemset/result/3568717/    
* https://cses.fi/problemset/result/3573305/
