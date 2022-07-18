# Đồ thị có trọng số (weighted graph)

## Shortest path (đường đi ngắn nhất)

![Hình ảnh cho việc tìm đường đi ngắn nhất từ s->v](images/w4-relax-path.png)

Sử dụng công thức trên ta có cách tiếp cận đầu tiên cho việc tìm đường đi ngắn nhất cho 2 điểm bất kỳ trong đồ thị (ko có nhiều ý nghĩa1)

![](images/w4-naive-shortest-path.png)

**Thuật toán Dijkstra**
> Dijkstra là thuật toán tìm đường đi ngắn nhất với trọng số cạnh không âm


![Pseudo-code of dijkstra algorithm](images/w4-dijkstra-pseudo-code.png)

**B1**: Khởi tạo mọi khoảng cách dist[inf, inf, ..]
    sptSet = [False,...] đánh dấu mọi đỉnh chưa được xét
    Khoảng cách dist[source] = 0 # dist(source->source) = 0

**B2**: For i in range(len(V))

Tại đây vòng for tương ứng với **while H is not empty**. Nhưng với mỗi vòng lặp sẽ thực hiện việc xử lý 1 vertex (node) nên vòng lặp sẽ tương đương với range(len(V))

**B3**: Lấy ra node đang có khoảng cách nhỏ nhất chưa được xử lý
* Lưu ý: xét thời điểm ban đầu. S (source) bắt đầu được xử lý thì mọi neighbour của nó sẽ dược tính khoảng cách -> khi lấy ra node có khoảng cách nhỏ nhất node đó mới chuẩn bị được xử lý
-> node đó thỏa mãn là min(dist) và sptSet[node] = False

![](images/w4-dijkstra-explanation.png)
Xét tại đây
sptSet (visited) sẽ bao gồm S và khi đó V, U đã dược tính khoảng cách sẵn. Node có dist nhỏ nhất mà chưa visited là U (V,U - node chưa thăm = Graph - Visited). min_distance_node = U.
Lấy ra các hàng xóm chưa thăm của U ta có V, K (S là hàng xóm nhưng thăm rồi).
For vertex in (V,K):
    SV + VU > SU -> ignore
    SU(5) + UK(3) < SK (inf) => SK = SU + UK
-> In ra khoảng cách của điểm cần tìm là xong.
Chú thích:
* sptSet: shortest path tree set

> Thêm giá trị prev vào là sẽ in ra được đường đi ngắn nhất

## Currency Exchange

**Bài toán:**
Có các loại tiền (USD, VND, YEN, ....) và tỉ giá của chúng. Từ 100 USD có thể đổi ra được tối đa bao nhiêu VND.

-> Nếu xét mỗi loại tiền là 1 node thì trọng số giữa 2 node sẽ là tỉ giá. Cần tìm 1 đường đi từ source->target sao cho tích hệ số là lớn nhất

Xét **log(ab) = log(a) + log(b)**

-> cần tính log(e1) + log(e2) + ... với e là cạnh đi qua. Thay đổi phần duyệt đồ thị tính tổng các trọng số thì giờ tính tổng các log của trọng số. Tổng log(e1) + log(e2) + .. lớn nhất tương đương với âm của chúng nhỏ nhất -> tìm đường đi ngắn nhất với hệ số là -log(e) với e là tỉ lệ chuyển đổi.

*Nhận xét*: -log(e) sẽ sinh ra 1 số cạnh âm, Dijkstra không thể giải quyết được vấn đề cạnh âm vì càng đi qua cạnh âm thì khoảng cách càng nhỏ và tiến tới **-inf**

**Nếu**: tìm được 1 chu trình mà a->b->c->a mà a trước < a sau (1 a trước đc n a sau n>1) thì ta sẽ có 1 quy trình đổi tiền luôn có lợi và tiền tự tăng

## Bellman-Ford Algorithm
> Hoạt động với đồ thị có trọng số cạnh âm (chậm hơn Dijkstra)

Thuật toán dùng hàm relax() trên
if (S->U + U->V <  S-> V){
    S->V = S->U + U->V
    prev[V] = U
}
với 2 vòng lặp for
for i in V:
    for e in E:
        relax() # chạy theo kiểu duyệt mọi (vertex, edge) vì relax có đầu vào là cạnh S->V và đỉnh U

### Tìm negative cycle

**Xác định nagatice cycle**
Sau khi lặp |V|*|E| lần relax().
Xảy ra negative cycle khi 2 đỉnh U,V cạnh nhau có dist[U] + U->V < dist[V]. Điều này nghĩa là dist[V] có thể được thay thế bằng dist[U] + U->V trong khi đồ thị đã được tính toán khoảng cách nhỏ nhất 1 lần rồi. -> tính được U,V nằm trong negative cycle

**Tìm nagative cycle**

Sử dụng mảng prev. Xét node S (s = for v in all verticies)
p = S
While exist(prev[p]):
    p = prev[p]
    print(p) # p này sẽ nằm trong nagative cycle mà S là 1 node trong đó

## Đang xem dở (Đang tạm bỏ qua)
https://www.coursera.org/learn/algorithms-on-graphs/lecture/MrQ2H/infinite-arbitrage