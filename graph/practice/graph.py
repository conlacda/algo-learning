# # Đồ thị vô hướng có trọng số
from collections import defaultdict

class Graph:
    
    def __init__(self):
        self.verticies = []
        self.graph = defaultdict(lambda: []) # giá trị mặc định
        # self.graph = {
        #     u: [[v1,w1],[v2,w2],[v3, w3],...], # đồ thị có hướng, có trọng số
        #     u1: [...]
        # }
    
    def add_vertex(self, u):
        if u not in self.verticies:
            self.verticies.append(u)

    def add_edge(self, u, v, w):
        # Thêm đỉnh
        self.add_vertex(u)
        self.add_vertex(v)
        # Thêm cạnh với
        self.graph[u].append([v,w])
        self.graph[v].append([u,w]) # nếu có hướng thì ko có dòng này
    
    def dfs():
        pass
    
    def kruskal():
        # Thuật toán kruskal để tìm MST (minimum spanning tree)
        """
        Ý tưởng thuật toán # TODO
        """
        pass
    
    def prim():
        # Thuật toán tại tuần 5
        pass

#     def printg(): # in ra graph
#         pass

if __name__ == "__main__":
    g =  Graph()
    g.add_edge(1,2,3)
    g.add_edge(1,4,5)
    print(g.graph)