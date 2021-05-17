# Tuần 2 của khóa học graph

**Xét đồ thị có hướng**
## Directed acyclic graph (DAG)
Đồ thị không chu trình có hướng là đồ thị không khép kín (no cycles)

Thay đổi giải thuật DFS 1 chút
```
<!-- DFS -->
for all v in V: mark v unvisited
for v in V:
    if not visited(v):
        Explore(v) # hàm Explore() bên trên
    else:
        return 'Not DAG' # tại đây dùng giải thuật DFS. Thay vì bỏ qua khi xét tới 1 đỉnh đã được thăm thì đỉnh này đc xét là 1 chu trình khép kín từ u <-> v. explore(u) -> v rồi explore(v) -> u.
```

## Topological Sort
Bất kỳ 1 đồ thị ko chu trình nào cũng có thể biểu diễn ra được 1 topological sort 
Từ đồ thị dùng DFS để lấy ra các đỉnh [v1,v2,v3,...] với post(i) > post(j) khi i < j.
Remind: post() thể hiện thứ tự quay về khi duyệt DFS
post(i) > post(j) i< j. nghĩa là đỉnh i xuất hiện trước sẽ đc quay về sau.

=> Với mọi u đi được tới v thì u luôn nằm trước v

*TODO cần có code - Hint: sử dụng pre-post sau đó viết theo thứ tự post là đc. post(u) = 2 , post(v) = 5 -> v,...,u,*

*Preference:* https://iq.opengenus.org/topological-sorting-dfs/

## Strong connected components
> Thành phần liên thông mạnh (tiếng Việt)

Đang xem dở: https://www.coursera.org/learn/algorithms-on-graphs/lecture/OlOTT/strongly-connected-components