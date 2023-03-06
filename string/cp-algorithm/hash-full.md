# String hash
> Tài liệu gốc tham khảo tại [Cp-algorithm Hashstring](https://cp-algorithms.com/string/string-hashing.html#improve-no-collision-probability)

## Overview
Hash 1 string/vector/set mục đích để việc so sánh từ O(N) chuyển về O(1) khi này có thể dùng sort() và so sánh các cặp đôi một.

### Vấn đề
Khi dùng hash từ không gian mẫu lớn về không gian mẫu nhỏ (thông thường là 1 số nguyên tố 1e9+7). Khi này nếu có 1 triệu phần tử thì tỉ lệ collision ~ 1. (Tương tự bài toán sinh nhật có 27 người tỉ lệ cặp có trùng ngày sinh đã là 50%)
### Giải quyết
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

## Evolution
### Hash sơ khai
Từ bài viết [hash-string](https://cp-algorithms.com/string/string-hashing.html) mình dựng 1 hash với output là `int`, `factor=31`, `min_char=a`, `mod=1e9+7`.  
Tại phần so sánh 2 hash của substr họ ko tính cụ thể hash của substr. Mình đã tính cụ thể hash của substr với `mod_inv` lấy được từ phần toán.  
**Vấn đề**:  
* Không gian hash quá nhỏ (MAX_INT) - collision ~ 10^-6, với 100 test case độ dài 10^5 thì chắc chắn sẽ fail  
* Chỉ chạy được với alphabet  
### Optimization 1
* Mở rộng không gian hash lên `long long` thay vì `int`
* Mở rộng `min_char` theo bảng [Acsii](https://www.asciitable.com/) -> `min_char=0`, `factor = prime > 'z'-'0'`, `mod= 1 số prime ở khoảng 1e9->MAX_LLONG`  

**Vấn đề**:  
* mod lớn làm việc chia lấy phần dư cho mod rất chậm
* Liên tục phải thay đổi factor và mod để fit với test case của từng bài - tỷ lệ collision thấp đi nhưng quá nhiều test case, nó ko thể fit được cho mọi bài -> thay đổi mod, factor cho từng bài rất vất vả, đôi khi lỗi nằm trong code mà lại đi sửa mod, factor thì ko có ý nghĩa gì
### Optimization 2
* Thêm mask vào cho hash. Thay vì hash trực tiếp ra thì giờ mình gắn `str_len, first_char, last_char (min, max_char)`  
->  Việc gắn thêm các thông tin kia làm giảm collision đi khá nhiều vì str1 != str2 có hash(str1) == hash(str2) tỉ lệ 10^-6 mà thêm độ dài, first, last_char thì khá thấp

**Vấn đề**:  
* Việc gắn 1 thông tin vào hash là số int thì phải dùng phép tính trên int, hoặc là chuyển qua string rồi cộng -> `tốc độ tính toán chậm`
```c++
ha = a[0] + a[-1] + a.size() + hash.hash(a);
```
* Không gian long long có 18 chữ số nhưng tốn 3 chữ số cho thông tin thêm, ví dụ first_char là 20, last_char là 15, len là 100 -> tốn 2+2+3=7 chữ số cho thông tin thêm -> chả khác gì hash ban đầu là mấy (ban đầu có 9 chữ số lưu hash) tại đây có `11 chữ số lưu hash` nhưng `tốc độ ì ạch` -> `ko hiệu quả`  
* Fail tại bài codeforces tại đó đề cập biên của string là toàn bộ ACSII
### Optimization 3
* Dùng 1 cặp hash `{hash_toward, hash_forward}` để lưu hash -> tỉ lệ collision sẽ là `10^-6*10^-6=10^-12` đủ nhỏ
* Mở rộng `min_char=char(0)` là kí tự thấp nhất trong bảng ACSII, `factor=137` - là số nguyên tố và bảng [ACSII](https://www.asciitable.com/) chỉ có 127 kí tự
* Hash 1 chiều chuyển về int -> tốc độ tính toán nhanh hơn
* mod luôn cố định là 1e9 cho hash ra int

**Vấn đề**:
* Khi đếm số lượng substr của 1 string bất kỳ ta phải tính mọi hash của nó rồi nhét vào 1 set, map rồi in ra set.size(), map.size() -> set, map tốc độ chậm nhưng unordered_set, unordered_map không cho phép 1 struct là phần tử mà ko có hàm hash tự build
### Optimization 4
* Thêm `IntPairHash` có thể merge `hash_forward, hash_toward` vào thành 1 số
```c++
size_t(p.first) << 32 | p.second; // merge 2 số 32 bit thành 1 số 64 bit với O(1)
```
Khi này `unordered_map<pair<ll, ll>, bool, IntPairHash> m;` cho tốc độ cực kì nhanh (nhanh gấp 3-10 lần với việc dùng `map<pair<ll, ll>, bool> m;`) - https://codeforces.com/contest/271/submission/172361578
### Extra
Với hash xuôi, ngược mọi tham số gần như cố định, tốc độ tính toán nhanh, chưa gặp trường hợp collision.  

**Mở rộng**:
* Hash mở rộng ra tính substr với tốc độ O(1)
* Tính substr tràn biên cũng với tốc độ O(1)
* Hash mở rộng ra với cả vector (bất kỳ cấu trúc nào có thể lặp qua) - Hash<vector<int>> hash;
