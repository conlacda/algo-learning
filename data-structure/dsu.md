# Disjoint set union

## Template

```c++
// Full example:
// https://github.com/conlacda/algo-practice/blob/master/atcoder/beginner-acl/disjoint-union-set.md
class DSU {
 public:
  vector<int> parent, _rank;
  DSU(int N) {
    this->parent.resize(N);
    this->_rank.resize(N);
    for (int i = 0; i < N; i++) {
      this->make_set(i);
    }
  }

  void make_set(int v) {
    this->parent[v] = v;
    this->_rank[v] = 0;
  }

  int find_set(int v) {
    if (v == parent[v]) {
      return v;
    }
    return parent[v] = find_set(parent[v]);
  }

  void merge_set(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
      if (_rank[a] < _rank[b]) {
        swap(a, b);
      }
      parent[b] = a;
      if (_rank[a] == _rank[b]) {
        _rank[a]++;
      }
    }
  }
};
/*
DSU dsu(N);
dsu.merge_set(u,v);
dsu.find_set(u) == dsu.find_set(v); // check if u,v in the same SCC
*/
```

## Reference
* https://cp-algorithms.com/data_structures/disjoint_set_union.html#toc-tgt-0

## Practicing

Trong nhiều bài ta sẽ sử dụng giá trị của phần tử trong vector để tạo set.

Ví dụ:
Cho các đỉnh 1,2,3,6,7,... đỉnh 1->3 hỏi đỉnh 2->6 không.

Nhưng khi giá trị các đỉnh được mở rộng tới 1.000.000 (lưu ý mảng trong c++ tối đa tới 100.000) nên việc lưu giá trị đỉnh không được. Hoặc khi các đỉnh là 1 string a b c.  
Lúc này thay vì sử dụng giá trị, ta sẽ sử dụng index để lưu trữ các đỉnh. Đỉnh root sẽ lưu trữ giá trị cho toàn bộ set.  
Ví dụ: vấn đề Unbelievable Array tại data-structure/dsu-practice.md và vấn đề Lexicographically minimal string  
**Summary**: dsu sẽ sử dụng trực tiếp giá trị đỉnh. Nếu không dsu có thể sử dụng index của đỉnh. Khi đó sẽ xuất hiện thêm 1 mảng a[] lưu trữ giá trị cho root của set đó  

```
      1                  1
    2     + 3    ->    2  3
  4  6       5       4  6  5 
Ta có root1 = 1, root2 = 3. -> root_merge = find_set(1) -> 1
root = 1 -> a[1] = f_compare(a[1], a[3])
Khi merge 2 set. Ta lấy ra giá trị 2 root có sẵn (ví nó có chứa thông tin chung của set).
Sau đó khi merge 2 set. thông tin đó sẽ lấy từ 2 giá trị a[] từ đỉnh cũ và gán vào root mới.

Ví dụ mảng a[] là mảng min[]. khi này min[1] = 1, min[3] = 3. khi merge 2 set có root mới là 1. min[1] = giá trị nhỏ nhất(1,3) = 1. -> thông tin về set được truyền lại vào set mới. 
```

**Lấy thông tin từ set**: muốn lấy giá trị của set. Đơn giản find_set(i) để tìm root sau đó return a[root]   
tiếp tục ví dụ trên. Tìm root của set chứa 3. return a[find_set(3)]

## Dsu với trọng số các cạnh

```c++
// Full example: https://github.com/conlacda/algo-practice/blob/master/atcoder/beginner-acl/disjoint-union-set.md
class DSU_has_weight {
 public:
  vector<int> parent, _rank;
  vector<int> weight;
  DSU_has_weight(int N) {
    this->parent.resize(N);
    this->_rank.resize(N);
    this->weight.resize(N);
    for (int i = 0; i < N; i++) {
      this->make_set(i);
    }
  }

  void make_set(int v) {
    this->parent[v] = v;
    this->_rank[v] = 0;
    this->weight[v] = 0;
  }

  int find_set(int v) {
    if (v == parent[v]) {
      return v;
    }
    int root = find_set(parent[v]);
    weight[v] += weight[parent[v]];
    parent[v] = root;
    return root;
  }

  void merge_set(int a, int b, int d) {
    assert(find_set(a) != find_set(b)); // dsu này không chấp nhận việc merge 2 phần tử đã có rồi. nếu không sẽ làm hỏng trọng số khi có đường tròn vd 1 là root, 2->1=1 3->1=2 thì 2->3 tính được bằng distance(). Nếu có 2->3=x thêm vào sẽ lỗi.
    int newd = -distance(a, find_set(a)) + d + distance(b, find_set(b));
    int ra = find_set(a); a = ra;
    int rb = find_set(b); b = rb;
    if (ra != rb) {
      if (_rank[ra] < _rank[rb]) {
        swap(ra, rb);
      }
      parent[rb] = ra;
      if (_rank[ra] == _rank[rb]) {
        _rank[ra]++;
      }
    }
    int r = find_set(ra);
    if (r==a){
        weight[a] = 0;
        weight[b] = -newd;
    } else {
        weight[a] = newd;
        weight[b] = 0;
    }
  }

  // tính khoảng cách của 2 node. (a->b = 0 - b->a)
  int distance(int a, int b){
    int pa = find_set(a);
    int pb = find_set(b);
    if (pa != pb) return -INT_MAX;
    else return weight[a] - weight[b];
  }
};
/*
DSU_has_weight dsu(N); // dsu này chiều 1->2 khác 2->1
if (dsu.find_set(u) != dsu.find_set(v)) {
    dsu.merge_set(u,v, w); 
}
dsu.distance(u, v); // tính khoảng cách 2 điểm
dsu.find_set(u) == dsu.find_set(v); // check if u,v in the same SCC
*/
```