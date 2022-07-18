vertice_num, edge_num = [int(i) for i in input().split(' ')]
edges = []
for _ in range(edge_num):
    edges.append([int(v) for v in input().split(' ')])


pre = [0] * (vertice_num+1)
post = [0] * (vertice_num+1)
visited = [False] * (vertice_num + 1)
clock = 0
def explore(v):
    global pre, post, visited, clock
    if not visited[v]:
        clock += 1
        pre[v] = clock
        visited[v] = True
        for edge in edges:
            if edge[0] == v or edge[1] == v: # dòng này thể hiện đồ thị vô hướng hay có hướng
                                        # nếu có hướng chỉ xét edge[0] = v.
                if edge[0] == v:
                    explore(edge[1])
                else:
                    explore(edge[0])
        clock +=1
        post[v] = clock
explore(2)
print(visited)
# Pre post thể hiện thứ tự duyệt qua các đỉnh của đồ thị
print(f"pre = {pre}")
print(f"post = {post}")
"""
# INP
5 5 # 5 đỉnh, 5 cạnh
1 2 # 5 dòng tiếp theo là danh sách các cạnh
2 3
4 5
2 4
2 5
# OUT
[False, True, True, True, True, True]
pre = [0, 1, 2, 3, 5, 6]
post = [0, 10, 9, 4, 8, 7]
-> index 0 là margin vì đỉnh đánh số từ 1
từ pre post -> thứ tự duyệt theo thứ tự 1->10 là 1->2->3->3->4->5->5->4->2->1
"""
"""* Với đồ thị có hướng không chu trình, từ post sắp xếp theo giá trị sẽ được 1 topological sort (week2)"""