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
<details>
  <summary>Sonya and string shifts - hacker rank</summary>
  
```c++
// https://www.hackerearth.com/practice/data-structures/advanced-data-structures/suffix-arrays/practice-problems/algorithm/sonya-and-string-shifts-code-monk-triesuffix-structures/
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

// Copy from: https://cp-algorithms.com/string/suffix-array.html
struct SuffixArray{
    string s; int n;
    vector<int> suffix_array, lcp;
    SuffixArray(string s){
        this->s = s; n = s.size();
        suffix_array = cal_suffix_array(s + '$');
        lcp = cal_lcp();
    }
    vector<int> cal_suffix_array(string s){
        int n = s.size();
        const int alphabet = 256;

        vector<int> p(n), c(n), cnt(max(alphabet, n), 0);
        for (int i = 0; i < n; i++)
            cnt[s[i]]++;
        for (int i = 1; i < alphabet; i++)
            cnt[i] += cnt[i-1];
        for (int i = 0; i < n; i++)
            p[--cnt[s[i]]] = i;
        c[p[0]] = 0;
        int classes = 1;
        for (int i = 1; i < n; i++) {
            if (s[p[i]] != s[p[i-1]])
                classes++;
            c[p[i]] = classes - 1;
        }
        vector<int> pn(n), cn(n);
        for (int h = 0; (1 << h) < n; ++h) {
            for (int i = 0; i < n; i++) {
                pn[i] = p[i] - (1 << h);
                if (pn[i] < 0)
                    pn[i] += n;
            }
            fill(cnt.begin(), cnt.begin() + classes, 0);
            for (int i = 0; i < n; i++)
                cnt[c[pn[i]]]++;
            for (int i = 1; i < classes; i++)
                cnt[i] += cnt[i-1];
            for (int i = n-1; i >= 0; i--)
                p[--cnt[c[pn[i]]]] = pn[i];
            cn[p[0]] = 0;
            classes = 1;
            for (int i = 1; i < n; i++) {
                pair<int, int> cur = {c[p[i]], c[(p[i] + (1 << h)) % n]};
                pair<int, int> prev = {c[p[i-1]], c[(p[i-1] + (1 << h)) % n]};
                if (cur != prev) classes++;
                cn[p[i]] = classes - 1;
            }
            c.swap(cn);
        }
        p.erase(p.begin());
        return p;
    }
    vector<int> cal_lcp(){
        vector<int> rank(n, 0);
        for (int i = 0; i < n; i++)
            rank[suffix_array[i]] = i;

        int k = 0;
        vector<int> lcp(n-1, 0);
        for (int i = 0; i < n; i++) {
            if (rank[i] == n - 1) {
                k = 0;
                continue;
            }
            int j = suffix_array[rank[i] + 1];
            while (i + k < n && j + k < n && s[i+k] == s[j+k])
                k++;
            lcp[rank[i]] = k;
            if (k)
                k--;
        }
        return lcp; 
    }
    // Tính tổng số substr có trong s - https://cses.fi/problemset/result/4386205/ - https://codeforces.com/edu/course/2/lesson/2/5/practice/contest/269656/submission/167497445
    ll number_of_substr(){
        ll ans = n - suffix_array[0];
        for (int i=1;i<n;i++){
            ans += (n - suffix_array[i]) - lcp[i-1];
        }
        return ans;
    }
    // check if string s contains sub? - đưa ra vị trí của sub trong s (index) - https://codeforces.com/edu/course/2/lesson/2/3/practice/contest/269118/submission/167503987
    ll find_substr(string sub){
        ll left = 0, right = n-1;
        // suffix_array được sắp xếp nên muốn tìm 1 sub thì chỉ cần binary search.
        while (left < right) {
            ll mid = (left + right) /2;
            string _s = s.substr(suffix_array[mid], sub.size());
            if (_s < sub) left = mid+1;
            else right = mid;
        }
        if (s.substr(suffix_array[right], sub.size()) == sub){
            dbg(right);
            return suffix_array[right]; 
        }
        return -1;
    }
    // đếm xem substring xuất hiện trong string bao nhiêu lần. Trong prefix đã sắp xếp tìm phần tử nhỏ nhất và lớn nhất bằng sub - https://codeforces.com/edu/course/2/lesson/2/3/practice/contest/269118/submission/167527106
    ll occurrence(string sub){
        ll lower_bound, upper_bound;
        ll left = 0, right = n-1;
        // Get lower_bound of substring on subfix_array strings - tìm lower_bound, upper_bound https://www.geeksforgeeks.org/implementing-upper_bound-and-lower_bound-in-c/
        while (left < right) {
            ll mid = left + (right - left) /2;
            string _s = s.substr(suffix_array[mid], sub.size());
            if (sub <= _s) right = mid;
            else left = mid + 1;
        }
        if (left < n && s.substr(suffix_array[left], sub.size()) < sub) left++;
        lower_bound = left;
        // Get upper_bound
        left = 0, right = n-1;
        while (left < right){
            ll mid = left + (right - left) /2;
            if (sub >= s.substr(suffix_array[mid], sub.size())){
                left = mid+1;
            } else right = mid;
        }
        if (left < n && s.substr(suffix_array[left], sub.size()) <= sub) left++;
        upper_bound = left;
        return upper_bound - lower_bound;
    }
    void longest_common_prefix_of_substrs(ll a, ll b){ // s1 = s.substr(a); s2 = s.substr(b);
        // TODO - dùng segment tree hoặc RMQ để query trên lcp.
    }
};
/*
SuffixArray suf(s);
cout << suf.suffix_array;
cout << suf.lcp;
cout << suf.number_of_substr();
cout << suf.find_substr("abc"); // index of substring in s
cout << suf.occurrence("abc"); // how many times "abc" appears in s
    6*       "" (empty)
0*  5   0    a               -> substr = s.substr(suffix_array[idx]) - idx (left, right) dùng trong binary search
1   0   1    ababba          -> suffix_array + cyclic_substr.size() = s.size() (cột 2 + cột4)
2   2   2    abba
0   4   3    ba
2   1   4    babba
1   3   5    bba
lcp suf idx  cyclic substr
Dấu * nghĩa là nó mang tính biểu tượng (hình dung), sẽ không xuất hiện trong mảng thực tế
*/
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int n;
    cin >> n;
    string s; cin >> s;
    int t;
    cin >> t;
    SuffixArray suf(s);
    dbg(suf.suffix_array);
    vector<int> m(s.size());
    for (int i=0;i<suf.suffix_array.size();i++){
        m[suf.suffix_array[i]] = i;
    }
    dbg(m);
    vector<int> ans(s.size());
    int _min = m[0], ind = 0;
    ans[0] = 0;
    for (int i=1;i<s.size();i++){
        if (m[i] < _min) {
            _min = m[i];
            ind = i;
        }
        ans[i] = ind;
    }
    dbg(ans);
    for (int i=0;i<t;i++) {
        int q; cin >> q;
        cout << ans[q] <<'\n';
    }
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}

```
</details>

* 1 số bài tập tại: https://codeforces.com/edu/course/2/lesson/2

* [Cses - string distribution](https://github.com/conlacda/algo-practice/blob/master/cses/string/Substring%20Distribution.cpp)
* [Codeforces education- Sorting Substrings](https://github.com/conlacda/algo-practice/blob/master/cses/string/C.%20Sorting%20Substrings.cpp)
## TODO problems
* https://www.hackerearth.com/practice/data-structures/advanced-data-structures/suffix-arrays/practice-problems/