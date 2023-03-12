# Segment tree


## Template

```c++
// Verification: https://atcoder.jp/contests/practice2/submissions/25073318
template<typename T>
class SegmentTree {
private:
    ll n;
    vector<T> dat;
public:
    T merge(T a, T b){
        return max(a,b); // easily modify to another function like sum()
    }
    SegmentTree(vector<T> v) {
        int _n = v.size();
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
        for (int i=0;i<_n;i++) dat[n + i - 1] = v[i];
        for (int i = n - 2; i >= 0; i--)dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
    }
    SegmentTree(int _n) {
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
    }
    void set_val(int i, T x) {
        i += n - 1;
        dat[i] = x;
        while (i > 0) {
            i = (i - 1) / 2;
            dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
        }
    }
    T query(int l, int r){
        r++;
        T left = 0, right = 0;
        l += n - 1; r += n - 1;
        while (l < r) {
            if ((l & 1) == 0)left = merge(left, dat[l]);
            if ((r & 1) == 0)right = merge(dat[r - 1], right);
            l = l / 2;
            r = (r - 1) / 2;
        }
        return merge(left, right);
    }
};
/*
vector<ll> a(n);
SegmentTree<ll> seg(a);
seg.set_val(index, value);
seg.query(start, end); //[start, end]
seg.quert(start, start); // start
*/
```

## Reference
* https://cp-algorithms.com/data_structures/segment_tree.html#toc-tgt-0

## Describe

Segment-tree trên đây được implement theo dạng 1 mảng 2*N phần tử (efficent segment tree) - dạng thông thường sẽ dùng 1 mảng 4*N hoặc dùng dạng object -> leftChild + rightChild khi di chuyển qua các lớp của cây.

Segment tree gồm các thao tác chính:
* Cập nhật giá trị 1 phần tử trong mảng (O(logN))
* Truy vấn giá trị của 1 range[x:y] với hàm merge(x,y) được định nghĩa trước (O(logN))
* Với thao tác truy vấn x==y thì sẽ truy vấn giá trị phần tử tại x
* Tìm kiếm nhị phân với hàm query.  
    Ví dụ hàm merge là max(a,b) thì với query ta sẽ tìm được max(range[x:y]) rồi tìm được giá trị yêu cầu (ví dụ 1 bên dưới)

**Các biến thể**  
* Lazy segment tree - tương đương range update (bao gồm cả range query và point query)
* Segment tree beats
* Thay thế fenwicktree - point update range query.

## Practicing

<details>
  <summary>Segment tree max (binary search)</summary>

```c++
// Confirmed: https://atcoder.jp/contests/practice2/submissions/25073318
#include<bits/stdc++.h>
using namespace std;

typedef long long ll;


template<typename T>
class SegmentTree {
private:
    ll n;
    vector<T> dat;
public:
    T merge(T a, T b){
        return max(a,b);
    }
    SegmentTree(vector<T> v) {
        int _n = v.size();
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
        for (int i=0;i<_n;i++) dat[n + i - 1] = v[i];
        for (int i = n - 2; i >= 0; i--)dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
    }
    SegmentTree(int _n) {
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
    }
    void set_val(int i, T x) {
        i += n - 1;
        dat[i] = x;
        while (i > 0) {
            i = (i - 1) / 2;
            dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
        }
    }
    T query(int l, int r){
        r++;
        T left = 0, right = 0;
        l += n - 1; r += n - 1;
        while (l < r) {
            if ((l & 1) == 0)left = merge(left, dat[l]);
            if ((r & 1) == 0)right = merge(dat[r - 1], right);
            l = l / 2;
            r = (r - 1) / 2;
        }
        return merge(left, right);
    }
};
/*
vector<ll> a(n);
SegmentTree<ll> seg(a);
seg.set_val(index, value);
seg.query(start, end); //[start, end]
seg.quert(start, start); // start
*/
int main() {
    ios::sync_with_stdio(false);
    std::cin.tie(0);
    std::cout.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    ll n, q;
    cin >> n >> q;
    vector<ll> a(n);
    for (auto& e : a)cin >> e;
    SegmentTree<ll> seg(a);
    while (q--) {
        ll t, x, y;
        cin >> t >> x >> y;
        x--;
        if (t == 1) seg.set_val(x, y);
        else if (t == 2)cout << seg.query(x, y-1) << "\n";
        else {
            ll l = x, r = n-1;
            while (r!=l){
                ll m = (l+r)/2;
                if (seg.query(l, m) >= y) r = m;
                else l = m+1;
            }
            if (seg.query(r,r) >= y) cout << r+1 << '\n';
            else cout << n+1<<'\n';
        }
    }
    return 0;
}
```
</details>

<details>
  <summary>Segment tree to solve Fenwicktree problem</summary>
  
```c++
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Verification: https://atcoder.jp/contests/practice2/submissions/25073647
template<typename T>
class SegmentTree {
private:
    ll n;
    vector<T> dat;
public:
    T merge(T a, T b){
        return a+b; // easily modify to another function like sum()
    }
    SegmentTree(vector<T> v) {
        int _n = v.size();
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
        for (int i=0;i<_n;i++) dat[n + i - 1] = v[i];
        for (int i = n - 2; i >= 0; i--)dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
    }
    SegmentTree(int _n) {
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
    }
    void set_val(int i, T x) {
        i += n - 1;
        dat[i] = x;
        while (i > 0) {
            i = (i - 1) / 2;
            dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
        }
    }
    T query(int l, int r){
        r++;
        T left = 0, right = 0;
        l += n - 1; r += n - 1;
        while (l < r) {
            if ((l & 1) == 0)left = merge(left, dat[l]);
            if ((r & 1) == 0)right = merge(dat[r - 1], right);
            l = l / 2;
            r = (r - 1) / 2;
        }
        return merge(left, right);
    }
};
/*
vector<ll> a(n);
SegmentTree<ll> seg(a);
seg.set_val(index, value);
seg.query(start, end); //[start, end]
seg.quert(start, start); // start
*/
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N,Q;
    cin >> N>>Q;
    vector<ll> a(N);
    for (int i=0;i<N;i++){
        cin >> a[i];
    }
    SegmentTree<ll> seg(a);
    while (Q--){
        int t, x,y;
        cin >> t >> x>>y;
        if (t ==0){
            // Gán
            a[x] = a[x] + y;
            seg.set_val(x, a[x]);
        } else if (t==1){
            // Truy vấn
            cout << seg.query(x,y-1) << '\n';
        }
    }
}
```
</details>

<details>
  <summary>Static Range Minimum Queries</summary>
  
```c++
#include<bits/stdc++.h>
 
typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double
 
using namespace std;
 
// Verification: https://cses.fi/problemset/result/2691498/
template<typename T>
class SegmentTree {
private:
    ll n;
    vector<T> dat;
public:
    T merge(T a, T b){
        return min(a,b); // easily modify to another function like sum()
    }
    SegmentTree(vector<T> v) {
        int _n = v.size();
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1, LLONG_MAX);
        for (int i=0;i<_n;i++) dat[n + i - 1] = v[i];
        for (int i = n - 2; i >= 0; i--)dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
    }
    SegmentTree(int _n) {
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
    }
    void set_val(int i, T x) {
        i += n - 1;
        dat[i] = x;
        while (i > 0) {
            i = (i - 1) / 2;
            dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
        }
    }
    T query(int l, int r){
        r++;
        T left = LLONG_MAX, right = LLONG_MAX;
        l += n - 1; r += n - 1;
        while (l < r) {
            if ((l & 1) == 0)left = merge(left, dat[l]);
            if ((r & 1) == 0)right = merge(dat[r - 1], right);
            l = l / 2;
            r = (r - 1) / 2;
        }
        return merge(left, right);
    }
};
/*
vector<ll> a(n);
SegmentTree<ll> seg(a);
seg.set_val(index, value);
seg.query(start, end); //[start, end]
seg.quert(start, start); // start
*/
 
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N, Q;
    cin >> N >> Q;
    vector<ll> a(N);
    for (int i=0;i<N;i++){
        cin >> a[i];
    }
    SegmentTree<ll> seg(a);
    while (Q--){
        int x,y;
        cin >> x >> y;
        cout << seg.query(x-1,y-1) << '\n';
    }
}
```
</details>

<details>
  <summary>Dynamic Range Sum Queries</summary>

```c++
#include<bits/stdc++.h>
 
typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double
 
using namespace std;
 
// Verification: https://cses.fi/problemset/result/2691630/
template<typename T>
class SegmentTree {
private:
    ll n;
    vector<T> dat;
public:
    T merge(T a, T b){
        return a + b;
    }
    SegmentTree(vector<T> v) {
        int _n = v.size();
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
        for (int i=0;i<_n;i++) dat[n + i - 1] = v[i];
        for (int i = n - 2; i >= 0; i--)dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
    }
    SegmentTree(int _n) {
        n = 1;
        while (n < _n)n *= 2;
        dat.resize(2 * n - 1);
    }
    void set_val(int i, T x) {
        i += n - 1;
        dat[i] = x;
        while (i > 0) {
            i = (i - 1) / 2;
            dat[i] = merge(dat[i * 2 + 1], dat[i * 2 + 2]);
        }
    }
    T query(int l, int r){
        r++;
        T left = 0, right = 0;
        l += n - 1; r += n - 1;
        while (l < r) {
            if ((l & 1) == 0)left = merge(left, dat[l]);
            if ((r & 1) == 0)right = merge(dat[r - 1], right);
            l = l / 2;
            r = (r - 1) / 2;
        }
        return merge(left, right);
    }
};
 
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N,Q;
    cin >> N >> Q;
    vector<ll> a(N);
    for (int i=0;i<N;i++) cin >> a[i];
    SegmentTree<ll> seg(a);
    while (Q--){
        int t, x, y;
        cin >> t >> x >> y;
        if (t==1){
            seg.set_val(x-1, y);
        } else if (t==2){
            cout << seg.query(x-1,y-1) << '\n';
        }
    }
}
```
<details>

<!-- <details>
  <summary>Title</summary>

```c++
```
<details> -->