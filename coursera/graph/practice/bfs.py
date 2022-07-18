# Thuật toán BFS để duyệt đồ thị
"""
6 7
1 2
2 3
1 3
2 4
4 5
5 6
2 6
"""
import math

vertex_num, edge_num = [int(i) for i in input().split(' ')]
edges = []
for _ in range(edge_num):
    edges.append([int (v) for v in input().split(' ')])

dist = [math.inf] * (vertex_num +1)
prev = [None] * (vertex_num +1)
def bfs(v):
    global dist, prev
    queue = [v] 
    dist[v] = 0 # đánh dấu khoảng cách tại chính điểm đó là 0
    while len(queue) > 0:
        u = queue[0]
        del (queue[0])
        for edge in edges:
            if edge[0] == u or edge[1] == u: # đồ thị vô hướng
                m = 0 if edge[0] == u else 1
                if dist[edge[1-m]] == math.inf: # nếu chưa được duyệt tới
                    queue.append(edge[1-m])
                    dist[edge[1-m]] = dist[edge[m]] + 1
                    prev[edge[1-m]] = u

bfs(1)
print(dist)
print(prev)
"""
Dist thể hiện khoảng cách gần nhất tới điểm bắt đầu
Prev thể hiện node đó đã được duyệt tới từ node nào
prev = [None, None, 1, 1, 2, 4, 2] -> node 1 = None - bắt đầu
                                   -> node 4 = 2 là trước đó được duyệt từ node 2
"""