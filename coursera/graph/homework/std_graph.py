# Gom lại 1 số hàm chuẩn để tiện sử dụng sau này

from collections import defaultdict

class UndirectedGraph:
    def __init__(self, v_num):
        self.graph = defaultdict(lambda: [])
        self.v_num = v_num
    def __str__(self):
        print('---Undirected graph---')
        for u in self.graph:
            print(f'{u}->', end=" ")
            for v in self.graph[u]:
                print(v, end= " ")
            print()
        return '----------------------'
    def __repr__(self):
        return self.graph

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    def has_connected(self, u, v):
        # Kiểm tra xem có đường đi từ start tới end không
        visited = [False] * self.v_num
        def explore(start):
            if not visited[start]:
                visited[start] = True
                for v in self.graph[start]:
                    explore(v)
        explore(start)
        if visited[end]:
            return True
        return False
    def scc_num(self):
    # Count the number of strongly connected component
        ans = 0
        visited = [False] * self.v_num
        def explore(start):
            if not visited[start]:
                visited[start] = True
                for v in self.graph[start]:
                    explore(v)
        def dfs():
            nonlocal ans
            for i in range(self.v_num):
                if not visited[i]:
                    explore(i)
                    ans +=1
        dfs()
        return ans
        
class DirectedGraph:
    def __init__(self,v_num):
        self.graph = defaultdict(lambda: [])
        self.v_num = v_num
    def __str__(self):
        print('---Directed graph---')
        for u in self.graph:
            print(f'{u}->', end=" ")
            for v in self.graph[u]:
                print(v, end= " ")
            print()
        return '----------------------'
    def add_edge(self, u, v):
        self.graph[u].append(v)
    def pre_post(self):
        # Chứa cả topological sort luôn vì 2 phần giống nhau
        clock = 0
        visited = [False] * self.v_num
        pre = [-1] * self.v_num
        post = [-1] * self.v_num
        topo_sort = []
        def explore(u):
            nonlocal clock, visited, pre, post
            if not visited[u]:
                clock +=1
                pre[u] = clock
                visited[u] = True
                for v in self.graph[u]:
                    explore(v)
                clock +=1
                post[u] = clock
                topo_sort.append(u)
        def dfs():
            nonlocal visited
            for i in range(self.v_num):
                if not visited[i]:
                    explore(i)
        dfs()
        print('Pre =', pre, 'Post=',post)
        print("Topo sort=", list(reversed(topo_sort)))
        return pre, post
    def is_cyclic(self): # has cycle
        pre, post = self.pre_post()
        for u in range(v_num):
            for v in self.graph[u]:
                if post[u] < post[v]:
                    return True
        return False
    def SCCs():
        # TODO - https://atcoder.jp/contests/practice2/submissions/23351714
        pass

from math import inf
class WeightDirectedGraph:
    def __init__(self,v_num):
        self.graph = defaultdict(lambda: [])
        self.v_num = v_num
    def __str__(self):
        print('---Directed graph---')
        for u in self.graph:
            print(f'{u}->', end=" ")
            for v in self.graph[u]:
                print(v, end= " ")
            print()
        return '----------------------'
    def add_edge(self, u, v, weight):
        self.graph[u].append([v, weight])
    def weight(self, u, v):
        for x in self.graph[u]:
            if v == x[0]:
                return x[1]
        return None
    def shortest_path(self, src, target):
        queue = []
        des = [inf] * self.v_num
        spt = [False] * self.v_num # đánh dấu các đỉnh nào đã được xét rồi
        for v in self.graph[src]:
            queue.append(v[0])
            des[v[0]] = v[1]
        while len(queue) > 0:
            min_des = queue[0]
            min_idx = 0
            for i in range(len(queue)):
                if des[queue[i]] < min_des:
                    min_idx = i
                    min_des = des[queue[i]]
            min_vertex = queue[min_idx]
            for u in self.graph[min_vertex]:
                if not spt[u[0]]:
                    queue.append(u[0])
                    min_vertex_u = self.weight(min_vertex, u[0])
                    if des[min_vertex] + min_vertex_u < des[u[0]]:
                        des[u[0]] = des[min_vertex] + min_vertex_u
            spt[queue[min_idx]] = True
            del(queue[min_idx])
        print(des[target])