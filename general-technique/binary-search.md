# Binary search
Binary search là 1 thuật toán rất phổ biến, tại đây đề cập tới 1 số dạng bài giải bằng binary search

## Intro
Đơn giản nhất về binary search.  
Cho sorted array [a1, a2, a3, a4, a5, ...]. Tìm kiếm phần từ k có trong array.

```c++
int left = 0, right = arr.size();
while (left < right) {
    int mid = (left + right)/2;
    if (mid == k) return;
    if (mid > k) right = mid-1;
    else left = mid;
}
```

## Binary search để tìm kiếm giá trị phù hợp
Như ví dụ trên ta thấy hàm so sánh để quyết định mid = right|left khá là trực quan.

**Mở rộng hơn ta thấy:**
* `Giá trị tìm kiếm sẽ nằm trong khoảng [left, right]`
* `hàm f(mid) dùng để thu hẹp khoảng giá trị của [left, right]` - cụ thể ở trên là phép so sánh >, <, =

**Code mẫu chung chung:**
```c++
std::function<bool(int)> isGood = [&](int mid){
    return false or true;
};
int left = 0, right = n;
while (left < right - 1) {
    int mid = (left + right) /2;
    if (isGood(mid)) {
        right = mid; // left = mid;
    } else left = mid +1; // right = mid -1;
}
assert(isGood(left) || isGood(right)); // có nhiều bài có thể ko có giá trị thỏa mãn và in ra -1 thì check tại đây
if (isGood(left)) return left; return right; // lấy giá trị nhỏ nhất có thể
// if (isGood(right)) return right; return left; // muốn lấy giá trị lớn nhất có thể
```
### Ví dụ
**[Codeforces - 803D Magazine Ad](https://codeforces.com/contest/803/problem/D)**  
*Vấn đề:*
Cho 1 string s, tách string s thành các string nhỏ hơn - tối đa k string, x là độ dài lớn nhất của các substring. X nhỏ nhất là bao nhiêu.  
*Solution:*  
* x nằm trong khoảng [0, s.size()]
* Với mỗi x dùng xét xem nó có thỏa mãn ko thì thu hẹp dần khoảng giá trị vào. Ở ví dụ dưới dùng `isGood(x)`

<details>
    <summary>Full code</summary>

```c++
// https://codeforces.com/contest/803/problem/D
// backup/codeforces-problems/803D-Codeforces.pdf
#include<bits/stdc++.h>

using namespace std;

#ifdef DEBUG
#include "debug.cpp"
#else
#define dbg(...)
#define destructure(a) #a
#endif

int main(){
    ios::sync_with_stdio(0); cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    /*
    String được tách tại dấu cách, dấu -
    tách được tối đa thành k đoạn
    độ dài nhỏ nhất đạt được là bao nhiêu
    -
    Bản chất - và space là như nhau
    -> chuyển thành mảng của các số [4,3,5,3,3,5,4,3,3]
    -> tách mảng này thành 4 mảng mà sum là nhỏ nhất
    -> min >= sum(arr)/k
    Binary search trên độ dài -> độ dài là x có ổn ko
    */
    int k;
    string s;
    std::getline (std::cin,s);
    k = stoi(s);
    std::getline (std::cin,s);
    dbg(k, s);
    // Chuyển về mảng
    vector<int> arr;
    int cnt = 0;
    for (int i=0;i<s.size();i++){
        if (s[i] == ' ' || s[i] == '-') {
            arr.push_back(cnt+1);
            cnt = 0;
        } else {
            cnt++;
        }
    }
    arr.push_back(cnt);
    dbg(arr);
    std::function<bool(int)> isGood = [&](int len){
        int sum = 0, cnt = 0;
        if (*max_element(arr.begin(), arr.end()) > len) return false;
        for (int i=0;i<arr.size();i++){
            if (sum + arr[i] > len) {
                cnt++;
                sum = arr[i];
            } else {
                sum += arr[i];
            }
        }
        cnt++;
        if (cnt <= k) return true;
        return false;
    };
    int left = 1;
    int right = (int) s.size();
    while (left < right -1) {
        int mid = (left + right) /2;
        if (isGood(mid)) {
            right = mid;
        } else {
            left = mid+1;
        }
    }
    assert(isGood(left) || isGood(right));
    if (isGood(left)) {
        cout << left;
    } else cout << right;
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}
```
</details>