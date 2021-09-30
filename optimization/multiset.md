# Tối ưu thuật toán với multiset

## Vấn đề
Xét bài toán [List removal](https://cses.fi/problemset/task/1749)  
`
Bài toán cho một dãy a1,a2..,an  
Cho dãy p(n). Với mỗi pi xóa a[pi] và in ra số đó
`   
Bài toán này sử dụng `Fenwick tree` xem tại [đây](https://cses.fi/problemset/result/2693128/) đánh dấu phần tử nào còn hay đã bị xóa. Tính tổng range cho tới khi tổng đó bằng `pi` thì cập nhật điểm đó về 0    

**=>** Bài toán nêu ra việc xóa 1 phần tử của vector/array là 1 thao tác O(N) vì việc dịch trái toàn bộ các phần tử sau index bị xóa.

## Tối ưu 
Trên ví dụ là 1 vector ko sắp xếp. Nếu vector đã sắp xếp, ta xét đến `multiset`.        

**Các đặc điểm:**
* Các phần tử được sắp xếp sẵn
* Thao tác tìm kiếm O(logN)
* Thao tác xóa O(1) với *index và O(logN) với giá trị
* Thao tác thêm O(logN)

**=>** Giải quyết bài toán cho 1 dãy không quan tâm thứ tự và thực hiện thao tác xóa và tìm kiếm

### Ví dụ

Xét vấn đề https://cses.fi/problemset/task/1091/     
Tóm tắt: cho 2 dãy, dãy thứ nhất là giá vé, dãy 2 là số tiền mà mỗi người có. Lần lượt theo thứ tự mỗi người sẽ vào mua 1 vé gần với số tiền mình có nhất ví dụ: tickets{1, 5}. money=3 -> chọn vé = 1. In ra giá vé của từng người, nếu ko có giá trị phù hợp in ra -1 (mọi vé đều vượt qua số tiền)

**Giải với vector (TLE)**
```c++
// https://cses.fi/problemset/result/2820867/#test5
#include <bits/stdc++.h>
using namespace std;
 
int n,m;
vector<int> z;
 
int main() {
    ios_base::sync_with_stdio(0); cin.tie(0);
    cin >> n >> m;
    for (int i=0; i<(n); i++){
        int t; cin >> t;
        z.push_back(t);
    }
    sort(z.begin(), z.end());
    for (int i=0; i<(m); i++) {
        int x; cin >> x;
        int it = upper_bound(z.begin(), z.end(), x) - z.begin();
        if (it == 0) cout << "-1\n";
        else {
            cout << z[it-1] << '\n';
            z.erase(z.begin()+it-1);
        }
    }
}
```

**Giải với multiset(AC)**
```c++
// https://cses.fi/problemset/result/2820825/
#include <bits/stdc++.h>
using namespace std;
 
const int MOD = 1000000007;
 
int n,m;
multiset<int> z;
 
int main() {
    ios_base::sync_with_stdio(0); cin.tie(0);
    #ifdef DEBUG
        freopen("in.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    cin >> n >> m;
    for (int i=0; i<(n); i++){
        int t; cin >> t;
        z.insert(t);
    }
    for (int i=0; i<(m); i++) {
        int x; cin >> x;
        auto it = z.upper_bound(x);
        if (it == z.begin()) cout << "-1\n";
        else {
            cout << *prev(it) << "\n";
            z.erase(prev(it));
        }
    }
}
```