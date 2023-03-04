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
* [USACO 2017 US Open Contest, Gold
Problem 1. Bovine Genomics](https://github.com/conlacda/algo-practice/blob/master/usaco/Bovine%20Genomics.cpp)

## Video
* [Video tự quay](https://github.com/conlacda/algo-video/blob/main/string/cp-algorithm/hash-string.mp4) - [Video trên youtube](https://youtu.be/h63aZD-ta-Q)
