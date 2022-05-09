# Modular inverse (nghịch đảo)

## Khái niệm
Trong phương trình 
```
a * x = 1 mod m
```
* a là số cho sẵn
* m là mod (thường là 1e9+7)
* x là giá trị cần tìm

Ví dụ:
```
2*3 = 6
6 %5 =1
-> 2*3 = 1 mod 5
-> 2 là inverse (nghịch đảo) của 3 theo mod m
```

## Chương trình giải
> Tham khảo: https://cp-algorithms.com/algebra/module-inverse.html   

Tính mod_inv của 1 số riêng lẻ
```c++
// Tính nghịch đảo của a theo mod m
// a*x ≡ 1 mod m (modular inverse)
// Hàm này để sử dụng khi tính toán cho từng số a.
// a nhỏ hơn thì tính nhanh hơn. ví dụ k*mod_inv(i) nhanh hơn mod_inv(k*i)
ll mod_inv(ll a, ll m) {
    ll x, y;
    auto extended_gcd = [&] (ll a, ll b) -> ll {
        x = 1; y =0;
        ll x1 = 0, y1 = 1, a1 = a, b1 = b;
        while (b1) {
            ll q = a1 / b1;
            tie(x, x1) = make_tuple(x1, x - q * x1);
            tie(y, y1) = make_tuple(y1, y - q * y1);
            tie(a1, b1) = make_tuple(b1, a1 - q * b1);
        }
        return a1; // a1 chính là std::gcd(a, b);
    };
    ll g = extended_gcd(a, m);
    if (g != 1) return -1; // -1 là không có nghiệm ví dụ 2*x=1 mod 4 
    else x = (x%m +m) %m;
    return x;
}
```

Tính mod_inv của toàn bộ số từ 1 tới M (tính cả range)

```c++
// Complexity: mlogm. tính toàn bộ inverse x thuộc range(1, m) % mod -> x*inv[x] = 1 mod m
// Lưu ý: mod_inv(x, mod) với for x in range(1,m) sẽ chậm hơn -> nếu tính x lẻ dùng mod_inv, x theo range thì dùng phần này
// Reference: https://cp-algorithms.com/algebra/module-inverse.html
// Verification: https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3055
vector<ll> mod_inv_range(ll m){
    vector<ll> inv(1000003, 1);
    for (int i=2;i<m;i++){
        inv[i] = mod - (mod/i) * inv[mod%i] % mod; // mod = 1e9+7
    }
    return inv;
}
/*
ll M = 1000003;
vector<ll> inv = mod_inv_range(M);
inv[x]; x*inv[x]=1 % mod
*/
```

## Ứng dụng

### Tính nCr
> nCr = (n!)/ ((n-r)! * r!)  

Ở đây có 3 phần cần tính 
* n!
* 1/(n-r)!
* 1/r!

Với `n!` đơn giản dùng
```c++
int maxN = 1e6;
vector<ll> f(maxN);
f[0] = 1; f[1] = 1;
for (int i=2;i<maxN;i++){
    f[i] = (f[i-1] * i) % mod;
}
```

Với `1/(n-r)!` và `1/r!` chung 1 dạng nên có cùng công thức tính 

`1/r!`   
= `1/(r-1)! * 1/r`  
= `1/(r-1)! * mod_inv(r)` 

```c++
int maxN = 1e6;
vector<ll> finv(maxN);
finv[0] = 1; finv[1] = 1;
for (int i=2;i<maxN;i++){
    finv[i] = (finv[i-1] * mod_inv(i)) % mod;
    // finv[i] = mod_inv(f[i] * i % mod); cách này chạy được nhưng với f[i] *i lớn thì tốc độ tính toán chậm hơn mod_inv[i] rất nhiều
}
```

Với việc sử dụng `mod_inv_range()` ta được
```c++
vector<ll> inv = mod_inv_range(maxN);
for (int i=2;i<maxN;i++)
    finv[i] = (finv[i-1] * inv[i]) % mod;
// Độ phức tạp O(1) cho thao tác tính toán
```

Do đó ta có công thức tính nCr
```c++
ll nCr(ll n, ll r, ll mod){
    ll ans = 1;
    ans = (ans * f[n]) % mod;
    ans = (ans * finv[n-r]) % mod;
    ans = (ans * finv[r]) % mod;
    return ans;
}
```
## Bài toán thực tế
<details>
  <summary>One Unit Machine</summary>
  
```c++
// https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3055
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Complexity: mlogm. tính toàn bộ inverse x thuộc range(1, m) % mod -> x*inv[x] = 1 mod m
// Lưu ý: mod_inv(x, mod) với for x in range(1,m) sẽ chậm hơn -> nếu tính x lẻ dùng mod_inv, x theo range thì dùng phần này
// Reference: https://cp-algorithms.com/algebra/module-inverse.html
// Verification: https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3055
vector<ll> mod_inv_range(ll m){
    vector<ll> inv(1000003, 1);
    for (int i=2;i<m;i++){
        inv[i] = mod - (mod/i) * inv[mod%i] % mod; // mod = 1e9+7
    }
    return inv;
}
/*
ll M = 1000003;
vector<ll> inv = mod_inv_range(M);
inv[x]; x*inv[x]=1 % mod
*/
    
vector<ll> f(1000003, 1), finv(1000003, 1);
void pre_compute() {
    vector<ll> inv = mod_inv_range(1000003);
    ll s = 1;
    for (ll i=1;i<=f.size();i++){
        f[i] = (f[i-1] * i) % mod;
        finv[i] = (finv[i-1] * inv[i]) %mod;
    }
}
ll nCr(ll n, ll r){
    return (((f[n] * finv[r]) % mod) * finv[n-r]) % mod;
}
void solve(int t){
    ll N; cin >> N;
    vector<ll> a(N);
    for (ll i=0;i<N;i++){
        cin >> a[i];
    }
    ll ans = 1, s = 0;
    for (ll i=0;i<N;i++){
        ans = (ans * nCr(s+a[i]-1, s)) % mod; 
        s += a[i];
    }
    cout << "Case " << t << ":" << ' ' <<ans << '\n';
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N;
    cin >> N;
    pre_compute();
    for (int t=0;t<N;t++) solve(t+1);

    cerr << "Time: " <<(double)clock() / CLOCKS_PER_SEC <<"s\n";
}
```
</details>

<details>
  <summary>Beautiful Numbers - 300C</summary>
  
```c++
// https://codeforces.com/contest/300/submission/156397027
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

int maxN = 1000003;
vector<ll> mod_inv_range(ll m){
    vector<ll> inv(1000003, 1);
    for (int i=2;i<m;i++){
        inv[i] = mod - (mod/i) * inv[mod%i] % mod; // mod = 1e9+7
    }
    return inv;
}
vector<ll> f(1000003, 1), finv(1000003, 1);
void cal_factor() {
    vector<ll> inv = mod_inv_range(1000003);
    ll s = 1;
    for (ll i=1;i<=f.size();i++){
        f[i] = (f[i-1] * i) % mod;
        finv[i] = (finv[i-1] * inv[i]) %mod;
    }
}
// Verification: https://www.calculator.net/permutation-and-combination-calculator.html - tính ra nCr, nPr
//               https://www.calculator.net/big-number-calculator.html - tính nCr % mod, nPr % mod
ll nCr(ll n, ll r){
    assert(n >= r && "n should be greater than r. Pick r items from n items without order");
    return (((f[n] * finv[r]) % mod) * finv[n-r]) % mod;
}
ll nPr(ll n, ll r){ // P(n, r) = n! / (n−r)!
    assert(n >= r && "n should be greater than r. Pick r items from n items with order");
    return (f[n] * finv[n-r]) % mod;
}

bool is_good(int num, int a, int b){
    while (num != 0){
        if (num % 10 != a && num % 10 !=b){
            return false;
        }
        num = num / 10;
    }
    return true;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    cal_factor();
    int a, b, n;
    ll ans = 0;
    cin >> a >> b >> n;
    for (int i=0;i<=n;i++){
        int sum = a*i + b * (n-i);
        if (is_good(sum, a, b)){
            ans += nCr(n, i);
            ans = ans % mod;
        }
    }
    cout << ans;
    cerr << "Time: " <<(double)clock() / CLOCKS_PER_SEC <<"s\n";
}
```
</details>
