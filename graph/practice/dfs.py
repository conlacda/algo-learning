# Thuật toán DFS
"""
Pseudo code
# Explore()
Explore(v)
for all v in V: mark v unvisited
for (v, u) in E:
    if not visited(u):
        explore(u)
# DFS
for all v in V: mark v unvisited
for v in V:
    if not visited(v):
        Explore(v)
"""
vertice_num, edge_num = [int(i) for i in input().split(' ')]
edges = []
for _ in range(edge_num):
    edges.append([int (v) for v in input().split(' ')])

visited = [False] * (vertice_num +1)
CCs_num = 0 # số connected component có trong đồ thị

def explore(v):
    global visited
    if not visited[v]:
        visited[v] = True
        for edge in edges:
            if edge[0] == v or edge[1] == v:
                if edge[0] == v:
                    explore(edge[1])
                else:
                    explore(edge[0])

def dfs():
    global CCs_num
    for v in range(1, vertice_num +1):
        if not visited[v]:
            explore(v)
            CCs_num +=1

dfs()
print(CCs_num)