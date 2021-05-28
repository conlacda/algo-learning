# # Đồ thị vô hướng có trọng số
from collections import defaultdict

class Graph:
    
    def __init__(self):
        self.verticies = []
        # self.graph = defaultdict(lambda: []) # giá trị mặc định
        # self.graph = {
        #     u: [[v1,w1],[v2,w2],[v3, w3],...], # đồ thị có hướng, có trọng số
        #     u1: [...]
        # }
        self.graph = []
    
    def add_vertex(self, u):
        if u not in self.verticies:
            self.verticies.append(u)

    def add_edge(self, u, v, w):
        # Thêm đỉnh
        self.add_vertex(u)
        self.add_vertex(v)
        # Thêm cạnh với
        # self.graph[u].append([v,w])
        # self.graph[v].append([u,w]) # nếu có hướng thì ko có dòng này
        self.graph.append([u,v,w])
    
    def has_cycle(self, V, E, new_vertex):
        """ Kiểm tra xem có cycle không
        @param: V - các đỉnh của đồ thị (minimum spanning tree)
               E - các cạnh của đồ thị
               new_edge - cạnh mới thêm vào đồ thị
        @return: True|False
        @idea: dùng hàm dfs() duyệt đồ thị sau đó đánh dấu parent vào đó.
        """
        pass
        # TODO
        
    def kruskal(self):
        # Thuật toán kruskal để tìm MST (minimum spanning tree)
        """
        Sắp xếp các cạnh theo thứ tự từ nhỏ tới lớn
        Duyệt lần lượt qua các cạnh đã được sắp xếp
        Cạnh nào ko tạo ra chu trình sẽ được thêm vào MST (minimum spanning tree)
        """
        mst_edges = [] # chứa danh sách cạnh có trong mst
        mst_verticies = []
        # Sắp xếp các cạnh
        self.graph.sort(key= lambda x:x[2])
        # Duyệt cạnh -> thêm đỉnh
        print(self.graph)
        for edge in self.graph:
            if edge[0] not in mst_verticies or edge[1] not in mst_verticies:
                if edge[0] not in mst_verticies:
                    mst_verticies.append(edge[0])
                if edge[1] not in mst_verticies:
                    mst_verticies.append(edge[1])
                mst_edges.append(edge)
        print(mst_edges)
        
    def prim(self):
        # Thuật toán tại tuần 5
        pass

#     def printg(): # in ra graph
#         pass

if __name__ == "__main__":
    g =  Graph()
    g.add_edge(1,2,2)
    g.add_edge(1,3,1)
    g.add_edge(2,3,3)
    g.add_edge(1,4,4)
    g.add_edge(3,4,5)
    g.add_edge(4,5,8)
    g.add_edge(4,6,6)
    g.add_edge(3,6,9)
    g.add_edge(5,6,1)
    print(g.graph)
    g.kruskal()