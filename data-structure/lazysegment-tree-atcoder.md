# Quick note
struct S {  
    mint a; // a = tổng các element  
    int size; // độ dài của sequence  
};  
struct F {  
    mint a, b; // ax+b  
};  
S op(S l, S r) { return S{l.a + r.a, l.size + r.size}; } // hàm merge()  
S e() { return S{0, 0}; } // a*x+size + 0*x+0 = a*x+size  
S mapping(F l, S r) { return S{r.a * l.a + r.size * l.b, r.size}; }  
F composition(F l, F r) { return F{r.a * l.a, r.b * l.a + l.b}; }  
F id() { return F{1, 0}; } // x = 1*x+0   

/*  
Update: ax+b -> F{a,b}  
Mọi số đều có dạng ax+b  
-> id() = F{1,0} => x = 1*x+0  
struct S{a, size} => mọi phần tử đều có dạng a*x+size  
op() là hàm tổng => S1+S2 = (a1x+b1) + (a2x+b) => (a1+a2)*x+(b1+b2)  
    => S{a1+a2, b1+b2}  
e() => op(x,e()) = x.  ax+size + 0.x+0 = ax+size() # hàm op() - hàm merge()  
  
mapping()  
Hình dung segment tree  
```
        ----  
    (5)--    --  
   (1)--(4)  - -   
```
xét cục -- có sum = 5(bằng tổng của 2 cục bên dưới) và len=2  
-> mapping Sum này với F(b,c) -> 5\*b+2\*c = S.sum\*b+S.len\*c  
Lý giải: Mapping với F(b,c) -> 1\*b+c+4\*b+c = 5\*b + 2\*c = sum\*b+len\*c  

```
Composition() - f∘g(x) = f(g(x))  
g(x) = a1*x+b1  
f∘g(x) = f(g(x)) = (a1*x+b1)*a2+b2  
                 = (a1*a2)x + (b1*a2+b2)  
-> composition(F l, F r) = F {a1*a2, b1*a2+b2}  
                           F{r.a * l.a, r.b * l.a + l.b};  

``` 
https://atcoder.github.io/ac-library/production/document_en/lazysegtree.html  

# K - Range Affine Range Sum 
> kèm theo 1 chút giải thích


<details><summary>Show code</summary>
<p>

```c++
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 998244353;
#define ld long double

using namespace std;

/* Zero-based indexing*/
template <class S,
          S (*merge)(S, S),
          S (*e)(),
          class F,
          S (*mapping)(F, S),
          F (*composition)(F, F),
          F (*id)()>
struct lazy_segtree {
  public:
    lazy_segtree() : lazy_segtree(0) {}
    explicit lazy_segtree(int n) : lazy_segtree(std::vector<S>(n, e())) {}
    explicit lazy_segtree(const std::vector<S>& v) : _n(int(v.size())) {
        log = ceil_pow2(_n);
        size = 1 << log;
        d = std::vector<S>(2 * size, e());
        lz = std::vector<F>(size, id());
        for (int i = 0; i < _n; i++) d[size + i] = v[i];
        for (int i = size - 1; i >= 1; i--) {
            update(i);
        }
    }

    void set(int p, S x) {
        assert(0 <= p && p < _n);
        p += size;
        for (int i = log; i >= 1; i--) push(p >> i);
        d[p] = x;
        for (int i = 1; i <= log; i++) update(p >> i);
    }

    S get(int p) {
        assert(0 <= p && p < _n);
        p += size;
        for (int i = log; i >= 1; i--) push(p >> i);
        return d[p];
    }

    S prod(int l, int r) {
        assert(0 <= l && l <= r && r <= _n);
        if (l == r) return e();

        l += size;
        r += size;

        for (int i = log; i >= 1; i--) {
            if (((l >> i) << i) != l) push(l >> i);
            if (((r >> i) << i) != r) push((r - 1) >> i);
        }

        S sml = e(), smr = e();
        while (l < r) {
            if (l & 1) sml = merge(sml, d[l++]);
            if (r & 1) smr = merge(d[--r], smr);
            l >>= 1;
            r >>= 1;
        }

        return merge(sml, smr);
    }

    S all_prod() { return d[1]; }

    void apply(int p, F f) {
        assert(0 <= p && p < _n);
        p += size;
        for (int i = log; i >= 1; i--) push(p >> i);
        d[p] = mapping(f, d[p]);
        for (int i = 1; i <= log; i++) update(p >> i);
    }
    void apply(int l, int r, F f) {
        assert(0 <= l && l <= r && r <= _n);
        if (l == r) return;

        l += size;
        r += size;

        for (int i = log; i >= 1; i--) {
            if (((l >> i) << i) != l) push(l >> i);
            if (((r >> i) << i) != r) push((r - 1) >> i);
        }

        {
            int l2 = l, r2 = r;
            while (l < r) {
                if (l & 1) all_apply(l++, f);
                if (r & 1) all_apply(--r, f);
                l >>= 1;
                r >>= 1;
            }
            l = l2;
            r = r2;
        }

        for (int i = 1; i <= log; i++) {
            if (((l >> i) << i) != l) update(l >> i);
            if (((r >> i) << i) != r) update((r - 1) >> i);
        }
    }

    template <bool (*g)(S)> int max_right(int l) {
        return max_right(l, [](S x) { return g(x); });
    }
    template <class G> int max_right(int l, G g) {
        assert(0 <= l && l <= _n);
        assert(g(e()));
        if (l == _n) return _n;
        l += size;
        for (int i = log; i >= 1; i--) push(l >> i);
        S sm = e();
        do {
            while (l % 2 == 0) l >>= 1;
            if (!g(merge(sm, d[l]))) {
                while (l < size) {
                    push(l);
                    l = (2 * l);
                    if (g(merge(sm, d[l]))) {
                        sm = merge(sm, d[l]);
                        l++;
                    }
                }
                return l - size;
            }
            sm = merge(sm, d[l]);
            l++;
        } while ((l & -l) != l);
        return _n;
    }

    template <bool (*g)(S)> int min_left(int r) {
        return min_left(r, [](S x) { return g(x); });
    }
    template <class G> int min_left(int r, G g) {
        assert(0 <= r && r <= _n);
        assert(g(e()));
        if (r == 0) return 0;
        r += size;
        for (int i = log; i >= 1; i--) push((r - 1) >> i);
        S sm = e();
        do {
            r--;
            while (r > 1 && (r % 2)) r >>= 1;
            if (!g(merge(d[r], sm))) {
                while (r < size) {
                    push(r);
                    r = (2 * r + 1);
                    if (g(merge(d[r], sm))) {
                        sm = merge(d[r], sm);
                        r--;
                    }
                }
                return r + 1 - size;
            }
            sm = merge(d[r], sm);
        } while ((r & -r) != r);
        return 0;
    }

  private:
    int _n, size, log;
    std::vector<S> d;
    std::vector<F> lz;

    void update(int k) { d[k] = merge(d[2 * k], d[2 * k + 1]); }
    void all_apply(int k, F f) {
        d[k] = mapping(f, d[k]);
        if (k < size) lz[k] = composition(f, lz[k]);
    }
    void push(int k) {
        all_apply(2 * k, lz[k]);
        all_apply(2 * k + 1, lz[k]);
        lz[k] = id();
    }
    int ceil_pow2(int n) { // tìm ra kích thước cây pow(2,k) >= n
       int x = 0;
        while ((1U << x) < (unsigned int)(n)) x++;
        return x;
    }
};

/*
S chứa các thuộc tính của 1 node
*/
struct Node {
    ll a;
    ll size;
};
/*
các thuộc tính cho hàm cập nhật x = a*x+b -> có 2 thuộc tính a,b
*/
struct UpdateElm { // F() - update - element
    ll a, b; // ax+b
};
/*
Hàm merge: thể hiện việc merge 2 node từ dưới lên trên
*/
Node merge(Node l, Node r) { return Node{(l.a + r.a) % mod, (l.size + r.size)% mod}; }

/* merge(Node A + NodeZero) = Node A
Hàm này chạy ở phần rìa. 
Ví dụ: mảng a có 7 phần tử -> khởi tạo sẽ ra 7 node. Cần 1 nodeZero ở cuối để tạo ra 2^n node
-> merge(Node7, Node8 = NodeZero) = Node7
*/
Node NodeZero() { return Node{0, 0}; }

/*
Hàm thể hiện cập nhật từ lazy tree vào segment tree
mapping()
Hình dung segment tree
        ----
    (5)--    --
   (1)--(4)  - - 
xét cục -- có sum = 5(bằng tổng của 2 cục bên dưới) và len=2
-> mapping Sum này với UpdateElm(b,c) -> 5*b+2*c = S.sum*b+S.len*c
Lý giải: Mapping với UpdateElm(b,c) -> 1*b+c+4*b+c = 5*b + 2*c = sum*b+len*c
*/
Node mapping(UpdateElm l, Node r) { // update cho 1 range
    return Node{(r.a * l.a + r.size * l.b) %mod, r.size %mod}; 
}

/*
Composition của hàm cập nhật f(g(x)) trả về các thuộc tính của F
Composition() - f∘g(x) = f(g(x))
g(x) = a1*x+b1
f∘g(x) = f(g(x)) = (a1*x+b1)*a2+b2
                 = (a1*a2)x + (b1*a2+b2) 
-> composition(F l, F r) = F {a1*a2, b1*a2+b2}
                            F{r.a * l.a, r.b * l.a + l.b};
*/
UpdateElm composition(UpdateElm l, UpdateElm r) { 
    return UpdateElm{(r.a * l.a) %mod, (r.b * l.a + l.b)%mod}; 
}

/*
Định danh các tham số cho node ban đầu (dưới đáy) 
Hàm update = ax+b -> x = 1*x+0-> id= F{1,0};
*/
UpdateElm id() { return UpdateElm{1, 0}; }

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int n, q;
    scanf("%d %d", &n, &q);

    vector<Node> a(n);
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        a[i] = Node{x, 1};
    }

    lazy_segtree<Node, merge, NodeZero, UpdateElm, mapping, composition, id> seg(a);

    for (int i = 0; i < q; i++) {
        int t;
        scanf("%d", &t);
        if (t == 0) {
            int l, r;
            int c, d;
            scanf("%d %d %d %d", &l, &r, &c, &d);
            seg.apply(l, r, UpdateElm{c, d});
        } else {
            int l, r;
            scanf("%d %d", &l, &r);
            printf("%d\n", seg.prod(l, r).a);
        }
    }
}
```

</p>
</details>

## Một số kĩ thuật chính

Xét struct S (trong tài liệu atcoder gốc) và Node trong phần mình sửa đổi
```c++
struct S{
    ll value, ll index, ll size;
}
```
Các thành phần thường xuất hiện trong 1 Node
- value đại diện cho giá trị Node đó
- index - thể hiện index của Node đó
- size - kích thước của node đó
### Chi tiết các thành phần

**VALUE**: value thường là thành phần bắt buộc có trong 1 node.

**INDEX**:
Xét hàm merge() = max().
```c++
S op(S l, S r) { 
    if (l.a > r.a) return l;
    return r;
} // merge() = max() 
```
Khi `query` lấy được ra giá trị max trong 1 khoảng đồng thời lấy luôn ra được index của nó. Nếu không có `index` thì sẽ phải dùng `query` + `binary search` để tìm ra index có giá trị đó - cách này gây ra `TLE` rất tai hại.  
Code mẫu cho phần binary search sẽ như sau:
```c++
// https://codeforces.com/contest/1557/submission/127813919 - TLE
m = seg.query(l, r) # query return max of range [l,r]
while (l!=r){
            int mid = (l+r)/2;
            int x = seg.query(l, mid);
            if (x < m) mid++;
            else  r = mid;
        } // -> l là điểm đạt max.
```

Toàn bộ code sử dụng `index` sẽ như sau:
```c++
*điền vào đây template cho lazy segment tree ở atcoder*
// Hàm max() cùng với update() x = ax + b
struct S { ll a; ll index;};
struct F { ll a, b;}; // ax+b => a = 0 means set x = b. a = 1 means add b to x
S op(S l, S r) { 
    if (l.a > r.a) return l;
    return r;
} // merge() = max() 
S e() { return S{-2, -1}; } // max(S1, S{0,0}) = S1. -2 là -∞. -1 là index ko có thực
S mapping(F l, S r) { return S{r.a * l.a + l.b, r.index}; }
F composition(F l, F r) { return F{r.a * l.a, r.b * l.a + l.b}; } 
F id() { return F{1, 0};}

int main(){
    for (int i=0;i<c.size;i++) a[i] = S{0, i};
    lazy_segtree<S, op, e, F, mapping, composition, id> seg(a);
    S node = seg.query(l,r); 
    // MAX of range(l,r) is node.a (node.value) at node.index
}
```

**SIZE**:
Size sử dụng trong trường hợp lấy tổng.
Ví dụ: node A và node B đứng cạnh nhau và node `C = merge(A,B)`
Hàm `update() x = x + b`
Khi này `A+x B+x -> C+2x` nói cách khác `A+sizeA *x  B+sizeB*x -> C + (sizeA+sizeB)*x`. 
```
      ----   (1)
  - -     - - (2)
- - - - - - - - (3)
```
Trên đây là hình dung về `size` khi dựng cây. Lớp 1 sẽ có size = 4, lớp 2 -> 2, lớp 3 = 1  
Chi tiết tại đây: https://atcoder.jp/contests/practice2/submissions/25473219