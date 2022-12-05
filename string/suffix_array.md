# Suffix array

## Khái niệm
Suffix array là 1 mảng chứa thứ tự đã sắp xếp của các suffix của string s  
Xét string: `ababba`
```
    6*       "" (empty)
0*  5   0    a               -> substr = s.substr(suffix_array[idx]) - idx (left, right) dùng trong binary search
1   0   1    ababba          -> suffix_array + cyclic_substr.size() = s.size() (cột 2 + cột4)
2   2   2    abba
0   4   3    ba
2   1   4    babba
1   3   5    bba
lcp suf idx  cyclic substr
Dấu * nghĩa là nó mang tính biểu tượng (hình dung), sẽ không xuất hiện trong mảng thực tế
```
**Suffix array** là cột 2 trong bảng trên.   
suffix_array = [5, 0, 2, 4, 1, 3] nghĩa là s.substr(5) < s.substr(0) < s.substr(2) < s.substr(4) < ...  
Nếu muốn lấy vị trí của substr(x) thì chỉ cần dùng 1 mảng m(s.size())
```c++
for (int i=0;i<n;i++) {
    m[suffix_array[i]] = i; // m ở đây cũng tương tự hệt như map(suffix_array -> index)
}
```
**LCP** (longest common prefix) là 1 mảng chứa độ dài chung lớn nhất của 2 string liền kề trong bảng trên  
```
    6        "" (empty)
0*  5   0    a          // 0 = common_prefix(a, "").size()
1   0   1    ababba     // 1 = common_prefix(a, ababba).size() = a.size()
2   2   2    abba       // 2 = common_prefix(ababba, abba).size() = ab.size()
0   4   3    ba         // 0 = common_prefix(abba, ba).size() = "".size()
2   1   4    babba      // 2 = common_prefix(ba, babba).size() = ba.size()
1   3   5    bba        // 1 = common_prefix(babba, bba).size() = b.size()
```
## Ứng dụng

### Tính số substring
Dựa vào bảng trên ta thấy, string `a` và `ababba` có `lcp = 1`. Thế thì tại string ababba có đc `5 substring` khác nhau `ab, aba, abab, ababb, ababba` ngoại trừ phần đầu chung `a`. Tương tự `ababba` và `abba` có `lcp = 2` thế thì `abba` có thể sinh ra đc 2 substring `abb` và `abba`.  
-> Công thức tính số substr sẽ là 
```c++
int substr_num = 0;
substr_num += n - suffix_array[0]; // phần tử đầu tiên (a) sẽ sinh ra a.size() substring
for (int i=1;i<n;i++){
    substr_num += (n - suffix_array[i]) - lcp[i-1]; // do suffix_array.size() = n nhưng lcp chỉ có n-1 phần tử
}
```

### Tìm 1 substring trong s (trả về index)
> Bài này có thể giải bằng rabin karp dùng rolling hash với độ phức tạp O(n)

**Thuật toán**: nhìn vào bảng trên ta thấy string đã được sắp xếp theo thứ tự tăng dần. Muốn tìm 1 string thì ta sẽ dùng `binary search` để tìm như thể 1 dãy số tăng dần.  
**Độ phức tạp**: `O(logN) * substr.size()`. logN cho binary search, substr.size() cho thao tác so sánh string

### Tìm số lần xuất hiện của substr trong s
> Bài này cũng có thể làm bằng Rabin karp. Với bài dạng query thì rabin karp sẽ ko được. 

**Thuật toán**: 1 substr xuất hiện ở string s thì sẽ là phần prefix của các string trong bảng trên. Tương tự như tìm 1 substring ở trên. Ở đây ko chỉ tìm ra 1 vị trí mà phải tìm ra lower_bound và upper_bound.  
Tương tự như dãy số {1, 2, 2, 2, 4, 5}. Số 2 thì có lower_bound = 1, upper_bound = 4. -> có 4-1 = 3 số 2.  
**Độ phức tạp**: `O(logN)`. logN cho lower_bound và logN cho upper_bound

### Tìm longest common prefix của substrings
`Xét 2 substring s1, s2. Max(common_prefix(s1, s2)) = ??`  
Xét `lcp` ta có được `common_prefix` của 2 substr liên tiếp. Do đã sắp xếp nên 2 string càng gần nhau thì càng có `common_prefix` dài.  
Ví dụ: babba, ba, bba -> thứ tự là ba, babba, bba. common_prefix của (ba, bba) sẽ nhỏ hơn (ba, babba) và (babba, bba).

**Thuật toán**: với 2 index l, r (substr(l), substr(r)) tìm ra vị trí index trên bảng rồi query min(l, r) dùng RMQ hoặc segmenttree là được

### Tìm longest common substring của 2 string
Với 2 string s1, s2. Tìm substring chung dài nhất của s1, s2.  
**Thuật toán**: Lấy s = s1 + '|' + s2. rồi dựng SuffixArray của s. lcp là độ dài common prefix của các substring trong s. Với 2 substring a, b trong bảng trên. Điều kiện để a, b ko cùng nằm ở s1 hoặc s2 chính là suffix_array(a) và suffix_array(b) 1 cái phải nhỏ hơn vị trí | và 1 cái lớn hơn vị trí |.   
Tóm lại:
```c++
ll signal_index = s.find('|') - s.begin(); // vị trí dấu |
ll max = 0;string ans = "";
for (int i=0;i<lcp.size();i++){
    if (max < lcp[i] && (suffix_array[i-1] - signal_index) * (suffix_array[i] - signal_index) <0){ // a*b<0 là điều kiện để 2 cái trái dấu
        max = lcp[i];
        ans = s.substr(suffix_array[i-1], lcp[i]);
        // nếu muốn tìm giá trị nhỏ nhất của ans thì chỉ cần if, else >=
    }
```
**Validation**: [Longest common substring - codeforces edu](https://codeforces.com/edu/course/2/lesson/2/5/practice/contest/269656/submission/167728749)  
**Thông tin thêm**: kí tự `|` được thêm vào tham khảo tại https://www.rapidtables.com/code/text/ascii-table.html - là kí tự đứng ngay đằng sau abcd.. 
## Template
[Suffix array](https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/snippet/string-suffix-array.sublime-snippet)

## Reference
* Codeforces edu: https://codeforces.com/edu/course/2/lesson/2


## Các problems đã giải quyết
* [Sonya and string shifts - hacker eartch](https://github.com/conlacda/algo-practice/blob/master/hackerearth/suffix_array/Sonya%20and%20string%20shifts.cpp)
* [Cses - string distribution](https://github.com/conlacda/algo-practice/blob/master/cses/string/Substring%20Distribution.cpp)
* [Codeforces edu compilation](https://github.com/conlacda/algo-practice/tree/master/code-force/education/suffix_array)
* [Katis - string multimatching](https://github.com/conlacda/algo-practice/blob/master/katis/string/string%20multimatching.cpp)
* [Maximum binary numbers.cpp](https://github.com/conlacda/algo-practice/blob/master/hackerearth/suffix_array/Maximum%20binary%20numbers.cpp)
* [Atcoder - I - Number of Substrings](https://atcoder.jp/contests/practice2/submissions/36926535)
## TODO problems
* https://www.hackerearth.com/practice/data-structures/advanced-data-structures/suffix-arrays/practice-problems/

## Video hướng dẫn
* https://github.com/conlacda/algo-video/blob/main/string/suffix_array.mp4 (mình tự soạn)
