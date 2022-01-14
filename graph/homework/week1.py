"""
Input:
4 2
1 2
3 2
1 4
Output:
2 - số scc
0-1 thể hiện có đường đi từ 1->4 ko (last statement)
"""
from collections import defaultdict

class UndirectedGraphs:
    def __init__(self, v_num, e_num):
        self.graph = defaultdict(lambda: [])
        self.v_num = v_num
        self.e_num = e_num
    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def has_connected(self, start, end):
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
                
if __name__ == "__main__":
    v_num,e_num = [int(i) for i in input().split()]
    g = UndirectedGraphs(v_num, e_num)
    for _ in range(e_num):
        u,v = [int(i)-1 for i in input().split()]
        g.add_edge(u,v)
    print(g.scc_num())
    start, end = [int(i) -1 for i in input().split()]
    if g.has_connected(start, end):
        print(1)
    else:
        print(0)