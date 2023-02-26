# Bitmask technique
## Mục đích
Cho 1 tập hợp a{N}. Tìm cách duyệt/ tìm kiếm trong Combination(a) ra 1 tập hợp thỏa mãn điều kiện gì đó.
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

<details>
    <summary>Ví dụ tính tổng</summary>

```c++
vector<int> a{1, 3, 4};
vector<int> sum_collections;
for (int i=0;i<1<<a.size();i++){ // 0 -> 2^3 000 -> 111
    ll sum = 0;
    for (int j=0;j<a.size();j++){ // 0->2
        if (i&(1<<j)) { // 010 & (1<<1) -> 010 & 010 -> true || 010 & (1<<0) -> false. Check xem i có bit 1 tại vị trí j nào. Nếu bit 1 tại j thì a[j] được chọn và sum += a[j]
            sum += a[j];
        }
    }
    sum_collections.push_back(sum);
}
// sum_collections sẽ chứa mọi tổng có được từ a
```
</details>

## Bitmask 0, 1 (phổ biến)
Cho 1 tập các phần tử => tổ hợp (combination) các phần tử đó.  
Khi này sắp xếp các phần tử cạnh nhau và hình dung nó như là hàng đơn vị, hàng chục,... nhưng mỗi hàng chỉ có 2 giá trị 0,1.  
Khi này chọn 1 phần tử vào tập hợp tương đương với số 1 và ko chọn là số 0. Đơn giản chỉ cần for (i = 1..n) rồi chuyển i về dạng base 2.

## Bitmask n phần tử (ít dùng hơn)
Khác 1 chút so với bitmask 0,1. Bitmask 0,1 để chọn ra combination nhưng ko được trùng lặp -> chỉ có chọn(1) or không (0).  
Bitmask n sẽ quyết định chọn phần tử nào tại vị trí đó (n giá trị). 
![image](https://user-images.githubusercontent.com/33364412/219572064-03310d87-1fd5-4822-8b9d-a65cba3b166b.png)
Theo như hình trên thì các phần tử bitmask 0-1 sắp xếp theo hàng ngang và chọn giá trị 0-1, độ dài = a.size()   
Bitmask N thì các phần tử được chọn trên hàng dọc và có độ dài N tùy ý.  
Sử dụng [Decimal To base N](https://github.com/conlacda/noteforprofessionals/blob/master/programming-language/C%2B%2B/snippet/decimal_to_n.sublime-snippet) vì mặc định máy tính chỉ là base 2

Khi này:   
Giả sử N độ dài 5, có 4 giá trị 0, 1, 2, 3 - tương ứng A,B,C,D sẽ được chọn ra  
00000  
00001  
00002  
00003  
00010  
.....  
.....  
33323  
33330  
33331  
33332  
33333  
Các số trên này là base 4, tương ứng với 0 tới 1023 tại base 10.  
```c++
for (int i=0;i<=1023;i++) {
    int k = toBaseN(i, 4);
    // từ k này check từng bit để xem giá trị nào đã được lấy ra
}
```
## Các bài thực hành
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
