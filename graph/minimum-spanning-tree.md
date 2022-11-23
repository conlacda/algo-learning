# Minimum spanning tree - MST

## Khái niệm
Cho 1 đồ thị G(N), và các cạnh Edges. Tìm tập hợp N-1 cạnh sao cho nó bao phủ hết N đỉnh và có tổng trọng số nhỏ nhất

## Thuật toán
* Sắp xếp các cạnh theo danh sách từ weight nhỏ tới lớn
* Duyệt qua các cạnh và dùng DSU để kiểm tra xem 2 đỉnh u,v có được nối với nhau chưa. Nếu chưa nối thì merge(u,v) và MST.push(Edge{u, v, w})
* Kiểm tra xem MST có đủ N-1 phần tử không. Nếu không thì nghĩa là đồ thị ko phải strong connected và ko có MST.

## Template
* [MST kruskal cũ](https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/old/snippet/mst-kruskal-graph.sublime-snippet) - dùng với class Graph mà mình thấy hơi lộn xộn nên đã tách ra riêng
* [MST kruskal mới](https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/snippet/mst-kruskal-graph.sublime-snippet) - được tách ra đứng độc lập
## Verification
* [Katis - Minimum Spanning Tree.](https://github.com/conlacda/algo-practice/blob/master/katis/KTH%20CSC%20Popup%202005/Minimum%20Spanning%20Tree.cpp)
* [Cses - Road Reparation](https://github.com/conlacda/algo-practice/blob/master/cses/Graph%20Algorithms/Road%20Reparation.cpp)