# String hash

## Template

```c++
class Hash {
private:
    vector<ll> pc;
    ll factor = 31;
    ll length;
    vector<ll> inv;
    string s;
public:
    char min_character = 'a';
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
    // hash này tương đối dễ collision nên có thể dùng thêm once(revesed(s)) để so sánh kèm
    // https://codeforces.com/contest/271/submission/171688510 - nên chạy với C++20 64bit;
    ll once(string s){ // hash 1 lần O(N)
        ll hash_value = 0;
        for (int i=0;i<(int)s.size();i++){
            int v = s[i] - min_character + 1;
            hash_value = (hash_value + 1LL*v*pc[i]) % mod;
        }
        return hash_value; 
    }
    // https://codeforces.com/contest/154/submission/171832462
    ll once(vector<ll> s){
        s.push_back(s.size());
        ll hash_value = 0;
        for (ll i=0;i<(int) s.size();i++){
            hash_value = (hash_value + s[i]*pc[i]) % mod;
        }
        return hash_value;
    }
    ll reversed(vector<ll> s){
        s.push_back(s.size());
        ll hash_value = 0;
        for (ll i=(ll) s.size()-1;i>=0;i--){
            hash_value = (hash_value + s[i]*pc[(ll) s.size() - i -1]) % mod;
        }
        return hash_value;
    }
    // a*x ≡ 1 mod m -> find x
    // a nhỏ hơn thì tính nhanh hơn. ví dụ k*mod_inv(i) nhanh hơn mod_inv(k*i)
    ll mod_inv(ll a) {
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
        ll g = extended_gcd(a, mod);
        if (g != 1) return -1;
        else x = (x%mod +mod) %mod;
        return x;
    }

    vector<ll> prefix_hash;
    void load(string s){
        this->s = s;
        // Precompute để lần sau tính hash value của mọi substring của s
        prefix_hash.resize(0);
        ll hash_value = 0;
        for (int i=0;i<(int)s.size();i++){
            int v = s[i] - min_character + 1;
            hash_value = (hash_value + 1LL*v*pc[i]) %mod;
            prefix_hash.push_back(hash_value);
        }
    }
    // Hash string và gắn mask vào kết quả sau string. hash_with_mask = length + s[l] + s[r] + hash_value(s[l:r]) -> long long. Nếu chỉ có hash_value(s[l:r]) thì tỉ lệ collison ~ 1 vì string 1k kí tự -> có 1tr substr -> so 1tr string đôi 1 trong không gian mẫu mod (1 tỷ) thì tỷ lệ collision ~ 1 (bài toán sinh nhật - 40 người tỉ lệ collision ngày sinh là 70%)
    ll substr(ll l, ll r){
        assert(0<=l && l <= r && r <= prefix_hash.size());
        string mask = "";
        mask += to_string(r-l+1);
        mask += to_string(s[l] - min_character + 1);
        mask += to_string(s[r] - min_character + 1);
        if (l == 0) return stoll(mask + to_string(prefix_hash[r]));
        ll ans = (prefix_hash[r] - prefix_hash[l-1] + mod) % mod;
        return stoll(mask + to_string((ans * inv[l]) % mod));
    }
    // So sánh 2 substring của s
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
/*
Hash hash;
hash.build(); // hash.build(s.size() + 5); mặc định độ dài string tới 2*1e5 
hash.once(str); trả ra giá trị hash của str
hash.once(vector) và hash.reversed(vector); LƯU Ý: nên dùng 2 giá trị cùng lúc để so sánh
// Khi muốn tính hash của mọi substring của s
hash.load(s); // O(n)
hash.substr(l, r); // = hash.once(s[l, r]); bao gồm l, r O(1) cho mỗi query
hash.compare_2substrs(index1, len1, index2, len2); // a>b trả ra 1, a<b trả ra -1, a=b trả ra 0
*/
```

## Sơ lược
Hash 1 string/1 vector hay 1 set mục đích để việc so sánh từ O(N) chuyển về O(1) khi này có thể dùng sort() và so sánh các cặp đôi một.
### Vấn đề
Khi dùng hash từ không gian mẫu lớn về không gian mẫu nhỏ (thông thường là 1 số nguyên tố 1e9+7). Khi này nếu có 1 triệu phần tử thì tỉ lệ collision ~ 1. (Tương tự bài toán sinh nhật có 27 người tỉ lệ cặp có trùng ngày sinh đã là 50%)
### Giải quyết
* Thêm mask vào sau khi hash. Ví dụ string thì thêm s.size(), s[0], s[s.size()-1] thêm vào hash_value để làm giảm collision. Cách này nhiều lúc vẫn collsion và khi cộng vào làm hash_value có độ dài tăng lên đáng kể (lưu ý ll chỉ có 18 chữ số)
* Dùng `hash xuôi` và `hash ngược` làm 1 cặp để so sánh. Khi này tỉ lệ mà 2 giá trị khác nhau có hash xuôi collision là 1/1e6. Tỉ lệ hash ngược là 1/1e6. Tỉ lệ collision chung là 1/1e12 cực kì nhỏ và đáng tin cậy. Cách này dùng trong template (xem bài Double profile codeforce sẽ thấy có tận 50 submit chỉ để tìm ra cách này)
## Bài giải mẫu
* 1 số bài giải tại https://cp-algorithms.com/string/string-hashing.html#improve-no-collision-probability (TODO thêm vào cụ thể)