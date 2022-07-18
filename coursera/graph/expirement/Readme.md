# Đồ thị có hướng

## Circle problem

### SCC (DFS)
Mỗi Scc sẽ là 1 circle của đồ thị  
Cách này yêu cầu implement SCC

### Tìm 1 điểm trong circle (mỗi circle chỉ ra 1 điểm thuộc circle đó) (DFS)

Dùng thuật toán DFS, sửa đổi pre post 1 chút ta sẽ được

```c++
void explore(int u){
    if (!visited[u]){
        pre[u] = true; // ||pre[u] = clock++;
        visited[u] = true;
        for (int i=0;i<g[u].size();i++){
            if (!visited[g[u][i]]) explore(g[u][i]);
            else {
                if (pre[u] && !post[u]) cout << "Circle here" << u<< "->" <<g[u][i];
            }
        }
        post[u] = true;
    }
}
```
Điểm mấu chốt: với 1 vòng pre-post thì pre là đi (đang xử lý), post là quay về(xử lý hoàn toàn). Khi 1 điểm pre mà chưa post thì tại điểm đó sẽ tạo ra circle. a->..->c  c->a => circle a...c  
a->b b->c. Khi này a pre&&!post. Nếu c->a thì sẽ tạo circle  
a->b c->a. Khi này ko tạo circle vì a->b mà b ko thể chạm tới c => a post&&pre -> mọi điểm tới a lúc này sẽ chỉ có 1 chiều tới a vì mọi điểm a tới được đều đã được duyệt