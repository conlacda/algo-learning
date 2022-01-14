<details>
  <summary>Range Updates and Sums</summary>

  ## Đề bài
  Cho 1 dãy a(N). Có 3 loại truy vấn.
    1. Cộng toàn bộ với x từ l->r
    2. Xét giá trị bằng x từ l->r
    3. Tổng từ l->r
  ## Code 
  ```c++
// https://cses.fi/problemset/result/2773879/
#include<bits/stdc++.h>
 
typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double
 
using namespace std;
 
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
 
struct S {
    ll a;
    int size;
};
 
struct F {
    ll a, b;
};
 
S op(S l, S r) { return S{l.a + r.a, l.size + r.size}; }
 
S e() { return S{0, 0}; }
 
S mapping(F l, S r) { return S{r.a * l.a + r.size * l.b, r.size}; }
 
F composition(F l, F r) { return F{r.a * l.a, r.b * l.a + l.b}; }
 
F id() { return F{1, 0}; }
/*main*/
// vector<Node> a(n);
// a[i] = Node{...};
// lazy_segtree<Node, merge, NodeZero, UpdateElm, mapping, composition, id> seg(a);
// seg.apply(l, r, UpdateElm{c, d});
// seg.prod(l, r) -> trả về 1 Node. Ví dụ Node{ ll sum, ll size} -> seg.prod(l, r).sum
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N, Q;
    cin >> N >> Q;
    vector<S> a(N);
    for (int i=0;i<N;i++){
        int x;
        cin >> x;
        a[i] = S{x, 1};
    }
    lazy_segtree<S, op, e, F, mapping, composition, id> seg(a);
    while (Q--){
        int t;
        cin >> t;
        int l, r;
        cin >> l >> r;
        l--;
        if (t==3){
            // Query
            cout << seg.prod(l, r).a << '\n';
        } else {
            int value;
            cin >> value;
            if (t==1){
                seg.apply(l, r, F{1, value});
                // Add value 
            } else {
                seg.apply(l, r, F{0, value});
                // t == 2 set value
            }
        }
    }
}
```
  ## Cách giải    
    Bản chất của 2 câu lệnh cập nhật là cho 2 số b,c. ai := ai*b+c. Xây dựng segment tree cho hàm này là được
</details>