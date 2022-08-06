# Bitmask technique

## Sơ lược
Cho tập hợp n số a (a1,a2,a3,...,an). Tìm ra toàn bộ các subset của a (lặp qua toàn bộ subset của a).

Xét subset của a:
* {} - 0
* {3} -> {0,0,3} -> {1}
* {2} -> {0,2,0} -> {2}
* {2,3} -> {0,2,3} -> {3}
* {1} -> {1, 0, 0} -> {4}
* {1,3} -> {1,0,3} -> {5}
* {1,2} -> {1, 2, 0} -> {6}
* {1,2,3} -> {1, 2, 3} -> {7}  
Khi này việc duyệt qua subset chỉ là việc duyệt từ 0->1<<n

## Mã giả
```c++
for (int i=0;i<1<<a.size();i++){ // 1<<a.size() = 2^n
    for (int j=0;j<a.size();j++){
        if (i&(1<<j)) { // nếu i có bit 1 tại j
            // some thing to do
            // j -> a[j]
            cout << a[j] << "in this subset"<<'\n';
        }
    }
}
```
với 1 vòng for ta sẽ duyệt qua được toàn bộ subset. với vòng for bên trong ta sẽ lấy ra được trong subset đó có những phần tử nào. 

# Các bài thực hành
<details>
  <summary>CSES - Prime Multiples</summary>
  
```c++
/* https://cses.fi/problemset/task/2185/
Cho số n và 1 tập hợp các số nguyên tố a. Hỏi từ 1->n có bao nhiêu số chia hết cho ít nhất 1 số trong a
Ví dụ: n = 20, a ={2,5}
Ta có  2,4,5,6,8,10,12,14,15,16,18,20 là 12 số -> in ra 12
Phân tích: bài này mình phải lấy ra được toàn bộ các subset của a. Với subset có lẻ số thì tính xem có bao nhiêu số chia hết rồi cộng vào và subset chẵn số thì sẽ trừ đi. -> dùng bitmask vào cho a
*/
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

int main(){
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    ll n, k;
    cin >> n >> k;
    vector<ll> a(k);
    for (auto &x: a) cin >> x;
    ll ans = 0;
    for (ll i=1;i<1<<a.size();i++){
        // bitmask
        ll cnt = 0;
        ll _n = n;
        for (ll j=0;j<a.size();j++){
            if (i&(1<<j)){
                cnt++;
                _n /= a[j];
            }
        }
        if (cnt %2 == 1) ans+= _n;
        else ans -= _n;
    }
    cout << ans;
    
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}

```
</details>