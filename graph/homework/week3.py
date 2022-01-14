from std_graph import WeightDirectedGraph, UndirectedGraph
# Task 1
"""
graph = WeightDirectedGraph(5)
graph.add_edge(4,1,1)
graph.add_edge(0,2,1)
graph.add_edge(2,3,1)
graph.add_edge(0,3,1)
print(graph)
graph.shortest_path(2,4)
"""
# Task 2
graph = UndirectedGraph(5)
graph.add_edge(4,1)
graph.add_edge(3,1)
graph.add_edge(2,3)
graph.add_edge(0,3)
print(graph)
def check(graph):
    color = [None] * graph.v_num
    start = 0
    queue = [start] # 0 is assigned as starting vertex
    color[start] = 'white'
    while len(queue) > 0:
        for v in graph.graph[queue[0]]:
            if color[v] is None:
                queue.append(v)
                color[v] = 'white' if color[queue[0]] =='black' else 'black' 
            else:
                if color[v] == color[queue[0]]:
                    print(v, queue[0], 'has conflict')
                    return False
        queue.pop(0)
    return True

print(check(graph))