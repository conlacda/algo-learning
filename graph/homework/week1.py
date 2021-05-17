vertice_num, edge_num = [int(i) for i in input().split(' ')]
edges = []
for _ in range(edge_num):
    edges.append([int(v) for v in input().split(' ')])

v1, v2 = [int(i) for i in input().split(' ')]

visited = [False] * (vertice_num + 1)
def explore(v):
    global visited
    if visited[v]:
        return
    else:
        visited[v] = True
        for edge in edges:
            if edge[0] == v or edge[1] == v:
                if edge[0] == v:
                    explore(edge[1])
                else:
                    explore(edge[0])

explore(v1)
if visited[v2]:
    print(1)
else:
    print(0)