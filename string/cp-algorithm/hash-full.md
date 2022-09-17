# String hash
> Tài liệu gốc tham khảo tại [Cp-algorithm Hashstring](https://cp-algorithms.com/string/string-hashing.html#improve-no-collision-probability)

## Overview
Hash 1 string/vector/set mục đích để việc so sánh từ O(N) chuyển về O(1) khi này có thể dùng sort() và so sánh các cặp đôi một.

### Vấn đề
Khi dùng hash từ không gian mẫu lớn về không gian mẫu nhỏ (thông thường là 1 số nguyên tố 1e9+7). Khi này nếu có 1 triệu phần tử thì tỉ lệ collision ~ 1. (Tương tự bài toán sinh nhật có 27 người tỉ lệ cặp có trùng ngày sinh đã là 50%)
### Giải quyết
* Thêm mask vào sau khi hash. Ví dụ string thì thêm s.size(), s[0], s[s.size()-1] thêm vào hash_value để làm giảm collision. Cách này nhiều lúc vẫn collsion và khi cộng vào làm hash_value có độ dài tăng lên đáng kể (lưu ý ll chỉ có 18 chữ số, mất 9 vào giá trị hash gốc) -> Tổng quan: không bao quát được toàn bộ.

* Dùng `hash xuôi` và `hash ngược` làm 1 cặp để so sánh. Khi này tỉ lệ mà 2 giá trị khác nhau có hash xuôi collision là 1/1e6. Tỉ lệ hash ngược là 1/1e6. Tỉ lệ collision chung là 1/1e12 cực kì nhỏ và đáng tin cậy. Cách này dùng trong template (xem bài Double profile codeforce sẽ thấy có tận 50 submit chỉ để tìm ra cách này)

## Template

[Hash string template](https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/snippet/hash-string.sublime-snippet)

### Giải thích code có trong template

Các tham số cần lưu ý:
* `min_char`: đây là giá trị nhỏ nhất trong Iterable s, thường là 'a', '0', 'A' cho string hoặc 0 với vector<int>. Tham khảo ascii table tại [đây](https://www.rapidtables.com/code/text/ascii-table.html). '0' < 'A' < 'a'
* `factor`: mặc định = 31. Vì 31 là prime và lớn hơn 26 là kích thước của bảng alphabet. `factor nên là số nguyên tố lớn hơn max_char - min_char`.  
    Giải thích: `string s = ab; hash = a+b*factor`. Nếu `factor < max_char - min_char` thì `a+b*factor = c+d*factor`. Ví dụ `factor = 10 < 26. a+10b = c+10d => a=b=1,c=11,d=0` -> ab, cd collsion ngay tại 2 chữ số chứ chưa cần tới collision trong không gian 10^6 phần tử. 

Các hàm sử dụng và mục đích
* `Hash hash; hash.build();` để khởi tạo.  
    `hash.build(s.size()+5);` được sử dụng để tiết kiệm thời gian tính toán hơn  
* `hash.once(s); hash.ronce(s)` hash xuôi, hash ngược cho s - hàm này dạng rolling.
* `hash.load(s); hash.substr(start, length)` sau khi dùng load(s) (O(n)) thì việc lấy giá trị hash của 1 range bất kỳ mất O(1)  
    `hash.rload(s); hash.rsubstr(start, length)` tương tự như load(s), substr(start, length) nhưng theo chiều ngược lại.  
    Ví dụ: `string s = "abcd";` thì `substr(0, 3) = once("abc");` `substr(2, 3) = once("cda");`, `rsubstr(0, 3) = once("adc") = substr(2, 3)`
    Nếu muốn `substr(l, r)` dạng thông thường, ko có dạng rolling từ cuối ngược lên đầu thì thêm `assert` ở hàm `substr` là được.
* Khi muốn so sánh 2 substr/vector/set,... thì cần so sánh 2 hash xuôi và ngược cùng 1 lúc  
    Ví dụ:
    ```c++
    Iterable a, b;
    ha = hash.once(a); hb = hash.once(b); // so sánh kiểu này collision cực lớn khi có 10^6 cặp (a,b) so sánh với nhau cho dù có tăng mod, thay đổi factor tới đâu. 10^6 cặp trong không gian mẫu 10^12 thì tỉ lệ đã là 1 cặp (a,b) collision
    ha = a[0] + a[-1] + a.size() + hash.once(a);
    hb = b[0] + b[-1] + b.size() + hash.once(b);
    /*Với kiểu thêm 1 số tham số vào đầu để mở rộng không gian mẫu sẽ giải quyết đc với 1 số bài. Đôi khi phải kết hợp với việc thay đổi factor, mod -> không tin cậy, không bao quát được toàn bộ các trường hợp. 
    */
    struct HashObject {
        ll hvalue, rhvalue;
        friend bool operator<(HashObject x, HashObject y){
            if (x.hvalue == y.hvalue) return x.rhvalue < y.rhvalue;
            return x.hvalue < y.hvalue;
        }
    }
    HashObject h1, h2;
    ha = {hash.once(a), hash.ronce(a)};
    hb = {hash.once(b), hash.ronce(b)};
    map<HashObject, bool> m;
    vector<HashObject> v;
    set<HashObject> _set;
    // Với vector<> thì tốn bộ nhớ do push_back() liên tục vào mà ko loại bỏ đi các phần tử trùng nhau đi được luôn
    // set.insert() mất O(logN) cho 1 insert -> độ phức tạp lớn
    // map.insert() mất O(logN) cho việc dùng self-balanced tree
    // => Cần dùng unordered_map để việc thêm vào chỉ mất O(1)
    unordered_map<HashObject, bool> um; // như này không cho phép nên mình sẽ phải tự thêm 1 hash function cho HashObject
    using IntPair = std::pair<ll, ll>; // tương đương với HashObject
    struct IntPairHash {
        static_assert(sizeof(int) * 2 == sizeof(size_t));
        size_t operator()(IntPair p) const noexcept {
            return size_t(p.first) << 32 | p.second; // <<32 chỉ chạy với 64 bit.
        }
    };
    std::unordered_map<IntPair, bool, IntPairHash> hashed;
    hashed[{hash.once(a), hash.ronce(a)}] = true;
    hashed[{hash.once(b), hash.ronce(b)}] = true;
    hashed.size();
    // https://codeforces.com/contest/271/submission/172361578
    ```

## Verified

<details>
    <summary>Codeforces - D. Good Substrings</summary>

```c++
// https://codeforces.com/contest/271/problem/D
// Submission: https://codeforces.com/contest/271/submission/172361578
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Copy from nealwu's template - http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0200r0.html
template<class Fun> class y_combinator_result { Fun fun_; public:template<class T> explicit y_combinator_result(T &&fun): fun_(std::forward<T>(fun)) {} template<class ...Args> decltype(auto) operator()(Args &&...args) { return fun_(std::ref(*this), std::forward<Args>(args)...); }}; template<class Fun> decltype(auto) y_combinator(Fun &&fun) { return y_combinator_result<std::decay_t<Fun>>(std::forward<Fun>(fun)); }

#ifdef DEBUG
#include "debug.cpp"
#else
#define dbg(...)
#endif

template<class Iterable>
class Hash{
private:
    vector<ll> pc;
    ll factor = 31; // factor > num_of_character and is a prime.
    ll length;
    vector<ll> inv;
    string s, rs;
public:
    vector<ll> prefix_hash, rprefix_hash;
    char min_char = 'a'; // xem bảng ascii để lấy ra min_char. Ví dụ string có hoa thường, số -> min_char = '0'
    // a*x ≡ 1 mod m -> find x - xem thêm tại math-compilation snippet
    ll mod_inv(ll a) { ll x, y;auto extended_gcd = [&] (ll a, ll b) -> ll { x = 1; y =0; ll x1 = 0, y1 = 1, a1 = a, b1 = b; while (b1) {ll q = a1 / b1;tie(x, x1) = make_tuple(x1, x - q * x1);tie(y, y1) = make_tuple(y1, y - q * y1);tie(a1, b1) = make_tuple(b1, a1 - q * b1);}return a1;};ll g = extended_gcd(a, mod);if (g != 1) return -1;else x = (x%mod +mod) %mod;return x;}
    Hash(){}
    void build(ll length = 200005){
        // Pre compute 
        ll p = 1;
        for (ll i=0;i<length;i++){
            pc.push_back(p);
            p = (p* factor) % mod;
        }
        for (auto v: pc) inv.push_back(mod_inv(v));
    }
    ll once(Iterable s){
        ll hash_value = 0;
        for (int i=0;i<(int)s.size();i++){
            int v = s[i] - min_char + 1;
            hash_value = (hash_value + 1LL*v*pc[i]) % mod;
        }
        return hash_value; 
    }
    ll ronce(Iterable s){
        reverse(s.begin(), s.end()); // phần này viết giống dạng once nhanh hơn được 1 chút
        return once(s);
    }
    // Precompute O(N) dạng prefix sum để sau tính hash từ l->r với O(1). 
    void load(Iterable s, bool reverse = false){
        vector<ll> *ph;
        string *str;
        if (!reverse) {
            str = &(this->s);
            ph = &prefix_hash;
        } else {
            str = &(this->rs);
            ph = &rprefix_hash;
        }
        *str = s;
        ph->resize(0);
        ph->push_back(0);
        ll hash_value = 0;
        ll start = (!reverse) ? 0 : (int)s.size() -1;
        ll end = (!reverse) ? (int)s.size() : -1;
        ll increment = (!reverse) ? 1 : -1;
        for (int i=start;i!=end;i+=increment){
            int v = str->at(i) - min_char + 1;
            if (!reverse) hash_value = (hash_value + 1LL*v*pc[i]) %mod;
            else hash_value = (hash_value + 1LL*v*pc[s.size()-1-i]) %mod;
            ph->push_back(hash_value);
        }
    }

    // hash dạng rolling substr- tức là nếu start+length>s.size() thì sẽ vòng lại lấy từ đầu đi tiếp
    ll substr(ll start, ll length){
        assert(length <= s.size());
        ll ans = 0;
        if (start + length <= s.size()) {
            ans = (prefix_hash[start + length] - prefix_hash[start] + mod) % mod;
            return (ans * inv[start]) % mod;
        }
        ll start2ssize = (prefix_hash[s.size()] - prefix_hash[start] + mod) % mod;
        start2ssize = (start2ssize * inv[start]) % mod;
        ll zero2end = prefix_hash[length + start - s.size()];
        ans = (start2ssize + zero2end * pc[s.size() -start]) % mod;
        return ans;
    }
    // Đoạn này có thể tách xừ ra thành 2 object Hash. reverse_hash(start, length) = hash(s.size()-1-start, length)
    // Nếu tách ra thì đoạn reverse và đoạn load sẽ gọn hơn và sau dễ chỉnh sửa hơn
    ll rsubstr(ll start, ll length){
        assert(length <= rs.size());
        ll ans = 0;
        start = (ll) rs.size() - 1 - start;
        if (start + length <= rs.size()) {
            ans = (rprefix_hash[start + length] - rprefix_hash[start] + mod) % mod;
            return (ans * inv[start]) % mod;
        }
        ll start2ssize = (rprefix_hash[rs.size()] - rprefix_hash[start] + mod) % mod;
        start2ssize = (start2ssize * inv[start]) % mod;
        ll zero2end = rprefix_hash[length + start - rs.size()];
        ans = (start2ssize + zero2end * pc[rs.size() -start]) % mod;
        return ans;
    }
    ll compare_2substrs(ll start1, ll len1, ll start2, ll len2){
        return -1;
    }
};

using IntPair = std::pair<ll, ll>;
struct IntPairHash {
    static_assert(sizeof(int) * 2 == sizeof(size_t));

    size_t operator()(IntPair p) const noexcept {
        return size_t(p.first) << 32 | p.second;
    }
};
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    string s; cin >> s;
    string ap; cin >> ap;
    int k; cin >> k;
    std::unordered_map<IntPair, bool, IntPairHash> hashed;
    int i=0, j =0;
    int bad = 0;
    Hash<string> hash;
    hash.build(s.size()+5);
    hash.load(s); hash.load(s, true);
    // Dùng 2 pointer để đếm số bad chars
    while (i<s.size()){
        if (ap[s[i] - hash.min_char] == '0') bad++;
        while (bad > k){
            if (ap[s[j] - hash.min_char] == '0') bad--;
            j++;
        }
        for (int z=j;z<=i;z++){
            hashed[{hash.substr(z, i-z+1), hash.rsubstr(i, i-z+1)}] = true;
        }
        i++;
    }
    cout << hashed.size();
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}
```
</details>

<details>
    <summary>Codeforces - C. Double Profiles</summary>

```c++
// https://codeforces.com/contest/154/problem/C
// https://codeforces.com/contest/154/my
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Copy from nealwu's template - http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0200r0.html
template<class Fun> class y_combinator_result { Fun fun_; public:template<class T> explicit y_combinator_result(T &&fun): fun_(std::forward<T>(fun)) {} template<class ...Args> decltype(auto) operator()(Args &&...args) { return fun_(std::ref(*this), std::forward<Args>(args)...); }}; template<class Fun> decltype(auto) y_combinator(Fun &&fun) { return y_combinator_result<std::decay_t<Fun>>(std::forward<Fun>(fun)); }

#ifdef DEBUG
#include "debug.cpp"
#else
#define dbg(...)
#endif

template<class Iterable>
class Hash{
private:
    vector<ll> pc;
    ll factor = 31; // factor > num_of_character and is a prime.
    ll length;
    vector<ll> inv;
    string s, rs;
public:
    vector<ll> prefix_hash, rprefix_hash;
    char min_char = 0; // xem bảng ascii để lấy ra min_char. Ví dụ string có hoa thường, số -> min_char = '0'
    // a*x ≡ 1 mod m -> find x - xem thêm tại math-compilation snippet
    ll mod_inv(ll a) { ll x, y;auto extended_gcd = [&] (ll a, ll b) -> ll { x = 1; y =0; ll x1 = 0, y1 = 1, a1 = a, b1 = b; while (b1) {ll q = a1 / b1;tie(x, x1) = make_tuple(x1, x - q * x1);tie(y, y1) = make_tuple(y1, y - q * y1);tie(a1, b1) = make_tuple(b1, a1 - q * b1);}return a1;};ll g = extended_gcd(a, mod);if (g != 1) return -1;else x = (x%mod +mod) %mod;return x;}
    Hash(){}
    void build(ll length = 200005){
        // Pre compute 
        ll p = 1;
        for (ll i=0;i<length;i++){
            pc.push_back(p);
            p = (p* factor) % mod;
        }
        for (auto v: pc) inv.push_back(mod_inv(v));
    }
    ll once(Iterable s){
        ll hash_value = 0;
        for (int i=0;i<(int)s.size();i++){
            int v = s[i] - min_char + 1;
            hash_value = (hash_value + 1LL*v*pc[i]) % mod;
        }
        return hash_value; 
    }
    ll ronce(Iterable s){
        reverse(s.begin(), s.end()); // phần này viết giống dạng once nhanh hơn được 1 chút
        return once(s);
    }
    // Precompute O(N) dạng prefix sum để sau tính hash từ l->r với O(1). 
    void load(Iterable s, bool reverse = false){
        vector<ll> *ph;
        string *str;
        if (!reverse) {
            str = &(this->s);
            ph = &prefix_hash;
        } else {
            str = &(this->rs);
            ph = &rprefix_hash;
        }
        *str = s;
        ph->resize(0);
        ph->push_back(0);
        ll hash_value = 0;
        ll start = (!reverse) ? 0 : (int)s.size() -1;
        ll end = (!reverse) ? (int)s.size() : -1;
        ll increment = (!reverse) ? 1 : -1;
        for (int i=start;i!=end;i+=increment){
            int v = str->at(i) - min_char + 1;
            if (!reverse) hash_value = (hash_value + 1LL*v*pc[i]) %mod;
            else hash_value = (hash_value + 1LL*v*pc[s.size()-1-i]) %mod;
            ph->push_back(hash_value);
        }
    }
 
    // hash dạng rolling substr- tức là nếu start+length>s.size() thì sẽ vòng lại lấy từ đầu đi tiếp
    ll substr(ll start, ll length){
        assert(length <= s.size());
        ll ans = 0;
        if (start + length <= s.size()) {
            ans = (prefix_hash[start + length] - prefix_hash[start] + mod) % mod;
            return (ans * inv[start]) % mod;
        }
        ll start2ssize = (prefix_hash[s.size()] - prefix_hash[start] + mod) % mod;
        start2ssize = (start2ssize * inv[start]) % mod;
        ll zero2end = prefix_hash[length + start - s.size()];
        ans = (start2ssize + zero2end * pc[s.size() -start]) % mod;
        return ans;
    }
    // Đoạn này có thể tách xừ ra thành 2 object Hash. reverse_hash(start, length) = hash(s.size()-1-start, length)
    // Nếu tách ra thì đoạn reverse và đoạn load sẽ gọn hơn và sau dễ chỉnh sửa hơn
    ll rsubstr(ll start, ll length){
        assert(length <= rs.size());
        ll ans = 0;
        start = (ll) rs.size() - 1 - start;
        if (start + length <= rs.size()) {
            ans = (rprefix_hash[start + length] - rprefix_hash[start] + mod) % mod;
            return (ans * inv[start]) % mod;
        }
        ll start2ssize = (rprefix_hash[rs.size()] - rprefix_hash[start] + mod) % mod;
        start2ssize = (start2ssize * inv[start]) % mod;
        ll zero2end = rprefix_hash[length + start - rs.size()];
        ans = (start2ssize + zero2end * pc[rs.size() -start]) % mod;
        return ans;
    }
    ll compare_2substrs(ll start1, ll len1, ll start2, ll len2){
        return -1;
    }
};

long long nCr(ll n, ll r) {
    if(r > n - r) r = n - r; // because C(n, r) == C(n, n - r)
    long long ans = 1;
    ll i;
    for(i = 1; i <= r; i++) {
        ans *= n - r + i;
        ans /= i;
    }
    return ans;
}
 
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
 
struct Object{
    ll v, hvalue, rhvalue;
    bool friend operator<(Object x, Object y){
        if (x.hvalue == y.hvalue) return x.rhvalue < y.rhvalue;
        return x.hvalue < y.hvalue;
    }
    bool friend operator==(Object x, Object y){
        if (x.hvalue == y.hvalue && x.rhvalue == y.rhvalue) return true;
        return false;
    }
};
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    ll n, q;
    cin >> n>>q;
    vector<vector<ll>> g(n);
    for (ll i=0;i<q;i++) {
        ll u, v; cin >> u>> v;u--; v--;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    for (auto &v: g){
        sort(v.begin(), v.end());
    }
    Hash<vector<ll>> hash; hash.build(n+5);
    /*
    Bài này yêu cầu tìm ra số cặp đỉnh (u1, u2) mà có các đỉnh kề giống hệt nhau
    2 đỉnh u1, u2 sẽ là double profile nếu u1, u2 có set(đỉnh kề) bằng nhau
    hoặc nếu u1 nối tới u2 thì set(đỉnh kề + chính nó) bằng nhau
    Ví dụ 1<->2 3<->2 => (1,3) là double profile vì set(kề) = {2}
    1<->2 2<->3 3<->1 => (1,3) là double profile vì set(kề + chính nó) = {1,2,3}.
                        nếu ko tính chính nó thì set(kề 1) = {2, 3}, set(kề 3) = {1,2}
    để so sánh 2 set(vector) với nhau ta dùng hash(vector<>). Khi này chỉ cần sắp xếp NlogN
    là ta có thể đếm được có bao nhiêu đỉnh có set(kề)/set(kề+chính nó) bằng nhau.
    -> Với K đỉnh bằng nhau thì có kC2 cặp double profile
    */
    vector<Object> s_with_itself, s_without_itself;
    for (ll i =0;i<n;i++){
        vector<ll> gi = vector(g[i].begin(), g[i].end());
        s_without_itself.push_back(Object{i, hash.once(gi), hash.ronce(gi)});
        gi.push_back(i);
        sort(gi.begin(), gi.end());
        s_with_itself.push_back(Object{i, hash.once(gi), hash.ronce(gi)});
    }
    DSU dsu(n);
    sort(s_with_itself.begin(), s_with_itself.end());
    sort(s_without_itself.begin(), s_without_itself.end());
    for (ll i=1;i<n;i++){
        if (s_with_itself[i] == s_with_itself[i-1]){
            dsu.merge_set(s_with_itself[i].v, s_with_itself[i-1].v);
        }
        if (s_without_itself[i] == s_without_itself[i-1]){
            dsu.merge_set(s_without_itself[i].v, s_without_itself[i-1].v);
        }
    }
    for (ll i=0;i<n;i++) dsu.find_set(i);
    map<ll, int> m;
    for (int i=0;i<n;i++){
        m[dsu.parent[i]]++;
    }
    ll ans = 0;
    for (auto v: m){
        if (v.second > 1){
            ans += nCr(v.second, 2);
        }
    }
    cout << ans;
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}
```
</details>