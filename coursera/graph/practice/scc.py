"""Tính số strongly connected component
In ra các node thuộc 1 scc trong graph
6 7
2 1
1 4
4 3
3 1
4 5
5 6
6 5
"""

vertex_num, edge_num = [int(i) for i in input().split(' ')]
edges = []
for _ in range(edge_num):
    edges.append([int (v) for v in input().split(' ')])

visited = [False] * (vertex_num +1)
pre = [0] * (vertex_num +1)
post = [0] * (vertex_num +1)
clock = 0
SCCs = []
def explore(v, reverse=False, scc=False):
    global visited, clock, SCCs
    if not visited[v]:
        if scc:
            SCCs[-1].append(v)
            print(SCCs)
        visited[v] = True
        clock +=1
        pre[v] = clock
        for edge in edges:
            if reverse:
                if edge[1] == v:
                    explore(edge[0], scc=scc)
            else:
                if edge[0] == v: # chỉ xét đồ thị có hướng
                    explore(edge[1], scc=scc)
        clock +=1
        post[v] = clock

def dfs(reverse=False):
    for v in range(1, vertex_num +1):
        if not visited[v]:
            explore(v, reverse=reverse)
dfs(reverse=True) # duyệt đồ thị GR
print(f"pre = {pre}")
print(f"post = {post}")
# Tìm source của reverse graph
visited = [False] * (vertex_num +1)
max_post = max(post)
min_post = min(post)
index = max_post

# while index > min_post:
while index >= min_post:
    try:
        vertex = post.index(index)
        SCCs.append([])
        explore(vertex, scc=True)
        index -=1
    except:
        index -=1

print(SCCs)