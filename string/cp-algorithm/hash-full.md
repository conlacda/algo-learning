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

[Hash string template](https://github.com/conlacda/noteforprofessionals/blob/master/programming-language/C%2B%2B/snippet/hash-string.sublime-snippet)

### Giải thích code có trong template

**Các tham số cần lưu ý:**
* `min_char`: min(s.begin(), s.end()). Hiện tại `min_char = char(0)` chạy được cho `string, number`. (trước đó dùng a cho alphabet, 0 cho số tự nhiên)
* `factor`: là số nguyên tố lớn hơn không gian kí tự của S, ví dụ không gian mẫu alphabet là 26, toàn bộ bảng [Ascii](https://www.asciitable.com/) có 127 kí tự -> chọn `137`   
    Giải thích: `string s = ab; hash = a+b*factor`. Nếu `factor < max_char - min_char` thì `a+b*factor = c+d*factor`. Ví dụ `factor = 10 < 26. a+10b = c+10d => a=b=1,c=11,d=0` -> ab, cd collsion ngay tại 2 chữ số chứ chưa cần tới collision trong không gian 10^6 phần tử. 

**Đầu ra của hash:**  
Hash nhận đầu vào là string hoặc (start, length) đánh dấu vị trí substr và trả ra pair<ll, ll> = {hash_toward, hash_backward} (hash xuôi và ngươc)  

**Các hàm sử dụng và mục đích:**  

* `Hash<string> hash; hash.build();` để khởi tạo.  
    `hash.build(s.size());` được sử dụng để tiết kiệm thời gian tính toán hơn  
**Hash 1 lần - O(N)**
* `hash.hash(s);` pair{hash xuôi, hash ngược cho s}.  
**Hash nhiều lần - load O(N) - hash O(1)**  
* `hash.load(s)`: chuẩn bị cho việc hash substring của s  
* `hash.substr(start, length)`: lấy giá trị hash của s.substr(start, length) - hash dạng vòng tròn   
    Ví dụ: `string s = "abcd";` thì `hash.substr(0, 3) = hash.hash("abc");` `hash.substr(2, 3) = hash.hash("cda");`  
    Để đảm bảo trong bài hash dạng thông thường ko bị hash tràn biên kiểu rolling hash thì dùng:   
    `assert(length <= (ll) s.size());`: dùng cho rolling hash  
    `assert(start+length <= (ll) s.size());` sẽ dùng cho hash thông thường  
* Khi muốn so sánh 2 substr/vector/set,... thì cần so sánh 2 hash xuôi và ngược cùng 1 lúc (đổi template nhưng chưa cập nhật đoạn này)  
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

* [Codeforces - D. Good Substrings](https://github.com/conlacda/algo-practice/blob/master/code-force/medium1600-2100/271D%20-%20%20Good%20Substrings.cpp)
* [Codeforces - C - Double Profile -2k3 - div1](https://github.com/conlacda/algo-practice/blob/master/code-force/hard-from-2200/154C%20-%20Double%20Profiles.cpp)
* [Codeforces - E. Games on a CD - 2300](https://github.com/conlacda/algo-practice/blob/master/code-force/hard-from-2200/727E%20-%20Games%20on%20a%20CD.cpp)
* [Codeforces - 25E - TEST - 2200](https://github.com/conlacda/algo-practice/blob/master/code-force/hard-from-2200/25E-Test.cpp)
* [Codeforces - 1056_E._Check_Transcription - 2100](https://github.com/conlacda/algo-practice/blob/master/code-force/medium1600-2100/1056_E._Check_Transcription.cpp) 
* [Codeforces - 858-D.Polycarp's phone book.cpp - 1600](https://github.com/conlacda/algo-practice/blob/master/code-force/medium1600-2100/858-D.Polycarp's%20phone%20book.cpp)
<details>
    <summary>USACO 2017 US Open Contest, Gold Problem 1. Bovine Genomics</summary>

```c++
#include<bits/stdc++.h>
typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double
using namespace std;

#ifdef DEBUG
#include "debug.cpp"
#else
#define dbg(...)
#endif

template<class Iterable> // chỉ chạy với 64bit.
class Hash{
private:
    vector<ll> pc;
    ll factor = 31; // factor > num_of_character and is a prime.
    ll length;
    vector<ll> inv;
    Iterable s, rs;
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
        for (int i=0;i< (int) s.size();i++){
            int v = s[i] - min_char + 1;
            hash_value = (hash_value + 1LL*v*pc[i]) % mod;
        }
        return hash_value; 
    }
    ll ronce(Iterable s){
        reverse(s.begin(), s.end()); // phần này viết giống dạng once nhanh hơn được 1 chút
        return once(s);
    }
    // lấy ra luôn 1 lúc hash ngược và hash xuôi
    pair<ll, ll> both_once(Iterable s){
        return make_pair(once(s), ronce(s));
    }

    // Precompute O(N) dạng prefix sum để sau tính hash từ l->r với O(1). 
    void load(Iterable s, bool reverse = false){
        vector<ll> *ph;
        Iterable *str;
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
        ll start = (!reverse) ? 0 : (ll) s.size() -1;
        ll end = (!reverse) ? (ll) s.size() : -1;
        ll increment = (!reverse) ? 1 : -1;
        for (int i=start;i!=end;i+=increment){
            int v = str->at(i) - min_char + 1;
            if (!reverse) hash_value = (hash_value + 1LL*v*pc[i]) %mod;
            else hash_value = (hash_value + 1LL*v*pc[(int) s.size()-1-i]) %mod;
            ph->push_back(hash_value);
        }
    }
    void rload(Iterable s){ return load(s, true);} // alias for load(reverse=true);
    void both_load(Iterable s) { load(s); rload(s);}
    // hash dạng rolling substr- tức là nếu start+length> s.size() thì sẽ vòng lại lấy từ đầu đi tiếp
    ll substr(ll start, ll length){
        assert(length <= (ll) s.size()); // assert(start+length <= (ll) s.size()); nếu chỉ muốn range thông thường ko phải dạng rolling
        ll ans = 0;
        if (start + length <= (ll) s.size()) {
            ans = (prefix_hash[start + length] - prefix_hash[start] + mod) % mod;
            return (ans * inv[start]) % mod;
        }
        ll start2ssize = (prefix_hash[s.size()] - prefix_hash[start] + mod) % mod;
        start2ssize = (start2ssize * inv[start]) % mod;
        ll zero2end = prefix_hash[length + start - (ll) s.size()];
        ans = (start2ssize + zero2end * pc[(ll) s.size() -start]) % mod;
        return ans;
    }
    // Đoạn này có thể tách xừ ra thành 2 object Hash. reverse_hash(start, length) = hash(s.size()-1-start, length)
    // Nếu tách ra thì đoạn reverse và đoạn load sẽ gọn hơn và sau dễ chỉnh sửa hơn
    ll rsubstr(ll start, ll length){
        assert(length <= (ll) rs.size()); // assert(start+length <= (ll) rs.size()); nếu chỉ muốn range thông thường ko phải dạng rolling
        ll ans = 0;
        start = (ll) rs.size() - 1 - start;
        if (start + length <= (ll) rs.size()) {
            ans = (rprefix_hash[start + length] - rprefix_hash[start] + mod) % mod;
            return (ans * inv[start]) % mod;
        }
        ll start2ssize = (rprefix_hash[(ll) rs.size()] - rprefix_hash[start] + mod) % mod;
        start2ssize = (start2ssize * inv[start]) % mod;
        ll zero2end = rprefix_hash[length + start - (ll) rs.size()];
        ans = (start2ssize + zero2end * pc[(ll) rs.size() -start]) % mod;
        return ans;
    }
    // Lấy ra luôn hash ngược và xuôi
    pair<ll, ll> both_substr(ll start, ll length){
        ll end = (start + length >= (ll) s.size()) ? (start + length - (ll) s.size() -1) : (start+length-1);
        return make_pair(substr(start, length), rsubstr(end, length)); 
    }
    // so sánh 2 substring. 1,0,-1 tương ứng lớn, bằng, nhỏ hơn (chưa kiểm duyệt)
    ll compare_2substrs(ll st1, ll len1, ll st2, ll len2){ // s.substr(st1, len1) <=> s.substr(st1, len2)
        ll size = min(len1, len2);
        ll left = 0, right = size;
        while (left < right - 1){
            ll mid = (left + right) /2;
            if (substr(st1, st1 + mid) != substr(st2, st2 + mid)){
                right = mid-1;
            } else left = mid;
        }
        while (left < size && s[st1 + left] == s[st2 + left]) left++;
        if (left == size) {
            if (len1 > len2) return 1;
            else if (len1 < len2) return -1;
            else return 0;
        }
        if (s[st1 + left] > s[st2 + left]) return 1;
        else if (s[st1 + left] < s[st2 + left]) return -1;
        return 0;
    }
};
struct IntPairHash {
    static_assert(sizeof(int) * 2 == sizeof(size_t));
    size_t operator()(pair<ll, ll> p) const noexcept {
        return size_t(p.first) << 32 | p.second; // <<32 chỉ chạy với 64 bit.
    }
};

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #else
        ifstream cin("cownomics.in");
        ofstream cout("cownomics.out");
    #endif
/*
Yêu cầu bài toán. 
Tìm ra range [l-r] sao cho đoạn từ l-r của phần trên và phần dưới không trùng nhau
Check lần lượt từ trái qua phải
Tại mỗi index tính xem giá trị tối thiểu tại đó là bao nhiêu
*/
    int n, m;
    cin >> n >> m;
    vector<string> spot(n), nospot(n);
    string spot_string = "", nospot_string = "";
    for (int i=0;i<n;i++) {
        cin >> spot[i];
        spot_string += spot[i];
    }
    for (int i=0;i<n;i++) {
        cin >> nospot[i];
        nospot_string += nospot[i];
    }
    Hash<string> hash;
    hash.build(spot_string.size());
    Hash<string> hspot = hash;
    Hash<string> hnospot = hash;
    hspot.both_load(spot_string);
    hnospot.both_load(nospot_string);
    std::function<bool(int, int)> check = [&](int index, int len){
        // Kiểm tra xem index và len này có được không
        unordered_map<pair<ll, ll>, bool, IntPairHash> um;        
        // Kiểm tra xem đoạn này có được không
        /*Dùng binary search để xem 
        Nếu index to được thì giảm đi 1 nửa*/
        for (int i=0;i<n;i++){
            um[hspot.both_substr(index + i*m, len)] = true;
        }
        for (int i=0;i<n;i++){
            if (um.find(hnospot.both_substr(index + i*m, len)) != um.end()){
                return false;
            }
        }
        return true;
    };
    int ans = INT_MAX;
    for (int i=0;i<m;i++){
        // Tìm ra giá trị phù hợp
        int left = 1, right = m-i;
        while (left < right-1){
            int mid = (left + right) /2;
            if (!check(i, mid)){
                left = mid + 1;
            } else right = mid;
        }
        if (check(i, left)){
            ans = min(ans, left);
        } else if (check(i, right)){
            ans = min(ans, right);
        }
    }
    cout << ans;
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}
/*
Problem: http://www.usaco.org/index.php?page=viewproblem2&cpid=741
Bài này cần tìm ra range [l:r] sao cho các đoạn từ [l:r] của các string có spot và
các string không có spot không có string nào trùng nhau
Ví dụ:
3 8
AATCCCAT
ACTTGCAA
GGTCGCAA
ACTCCCAG
ACTCGCAT
ACTTCCAT

Xét bất kỳ 1 đoạn string độ dài 3 nào thì 3 string trên và 3 string dưới luôn trùng nhau
Ví dụ: l=0, r=2 -> trùng ACT
       l=1, r=3 -> trùng CTT
       l=2, r=4 -> trùng TCC
       l=3, r=5 -> trùng CGC
       ...
Với độ dài = 4 thì đoạn l=1, r = 4 là không trùng nhau -> kết quả là 4
( [ATCC,CTTG,GTCG] x [CTCC, CTCG, CTTC] = {}  x là giao nhau/intersect)
Ban đầu mình tính với mỗi index tìm ra độ dài tối thiểu cần để nó ko intersect là bao nhiêu
Tăng dần length lên, đạt thì dừng và cập nhật ans = min(ans, result)
Nhưng với cách này với mỗi index O(N) sẽ có length = 1->N là N^2 phép kiểm tra
-> Tối ưu:
Dễ nhận thấy nếu với (index, len) thỏa mãn điều kiện thì (index, s.size()) cũng thỏa mãn điều kiện
Nghĩa là nếu index =1 và độ dài trên kia là 4 thỏa mãn thì index =1 và độ dài >4 cũng thỏa mãn
-> Dùng binary search để tìm. left = 1, right = m-i. Khi này kiểm tra mid có thỏa mãn hay không để điều chỉnh lại left, right  

Nói ngắn gọn:
Với mỗi index (O(N))ta dùng binary search để tìm ra len thỏa mãn (O(logN))
-> độ phức tạp O(NlogN)
*/
```
</details>

## Video
* [Video tự quay](https://github.com/conlacda/algo-video/blob/main/string/cp-algorithm/hash-string.mp4) - [Video trên youtube](https://youtu.be/h63aZD-ta-Q)
