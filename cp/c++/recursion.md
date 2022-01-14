# Recursion - đệ quy

## Cấu trúc

**Hàm đệ quy không trả về giá trị**
```python
def explore(u):
    if f(u) return;
    if u->v:
        explore(v)
```

**Hàm đệ quy có trả về giá trị**
```c++
int solve(x){
    if (...) return 1;
    return solve(f(x))
}
```

**Hàm đệ quy đuôi - tail recursion (không quan trọng lắm)**

Hàm đệ quy f(x) = k + f(...x) là hàm đệ quy bình thường. 
```c++
int f(x){
    if ... return ...;
    return f(x-1...);
}
```
Hàm này gọi là đệ quy đuôi vì nó trả về giá trị hoặc 1 hàm chứ ko có thêm 1 giá trị theo cái hàm đó. Tham khảo tại [đây](https://stackoverflow.com/questions/33923/what-is-tail-recursion)

## Tối ưu đệ quy

Xét bài CF https://codeforces.com/contest/1600/problem/E

Cách giải dưới đây tại [submission này](https://codeforces.com/contest/1600/submission/133457234) có 1 `vector<int>a` để trong hàm solve khiến nó bị `clone` làm tràn bộ nhớ
```c++
#include<bits/stdc++.h>
using namespace std;

int _count(vector<int> a, bool re = false){
    if (re) reverse(a.begin(), a.end());
    int ans =1;
    for (int i=1;i<a.size();i++){
        if (a[i] > a[i-1]) ans++;
        else break;
    }
    return ans;
}

int cl, cr;
int solve(vector<int> a, int l, int r, int player, int _min, int _cl, int _cr){
    if (a[l] <= _min && a[r] <= _min) return 1-player;
    if (a[l] <= _min && a[r] > _min) {
        if (_cr %2 ==1) return player; else return 1-player;
    }
    if (a[r] <= _min && a[l] > _min){
        if (_cl %2 == 1) return player; else return 1-player;
    }
    if (l==r) return player;
    if (a[l] <= a[r] && _cr %2 ==1) return player;
    if (a[l] >= a[r] && _cl %2 ==1) return player;
    if (a[l] <= a[r] && a[l] <= _min) return 1-player;
    if (a[r] >= a[l] && a[r] <= _min) return 1-player;
    if (a[l] <= a[r]) return solve(a, l+1, r, 1-player, a[l], _cl-1, _cr);
    else return solve(a, l, r-1, 1-player, a[r], _cl, _cr-1);
}

int main(){
    int N;
    cin >> N;
    vector<int> a(N);
    for (int i=0;i<N;i++) cin >> a[i];
    cl = _count(a);
    cr = _count(a, true);
    if (solve(a, 0, a.size()-1, 0, -1, cl, cr) == 0) {
        cout << "Alice";
    } else cout << "Bob";
}
```

Sửa lại 1 chút để `vector<int> a` làm biến toàn cục để tham chiếu vào [accepted submission](https://codeforces.com/contest/1600/submission/133457720)

```c++
vector<int> a;
int solve(int l, int r, int player, int _min, int _cl, int _cr){
    // cout << l << ' ' << r <<' '<<player << ' '<< _min << ' '<< _cr<<' '<< _cl<<'\n';
    if (a[l] <= _min && a[r] <= _min) return 1-player;
    if (a[l] <= _min && a[r] > _min) {
        if (_cr %2 ==1) return player; else return 1-player;
    }
    if (a[r] <= _min && a[l] > _min){
        if (_cl %2 == 1) return player; else return 1-player;
    }
    if (l==r) return player;
    if (a[l] <= a[r] && _cr %2 ==1) return player;
    if (a[l] >= a[r] && _cl %2 ==1) return player;
    if (a[l] <= a[r] && a[l] <= _min) return 1-player;
    if (a[r] >= a[l] && a[r] <= _min) return 1-player;
    if (a[l] <= a[r]) return solve(l+1, r, 1-player, a[l], _cl-1, _cr);
    else return solve(l, r-1, 1-player, a[r], _cl, _cr-1);
}
int main(){
    (solve(0, a.size()-1, 0, -1, cl, cr) == 0)
}
```

### Kết luận:
Trên đây là cách tối ưu đơn giản cho recursion, đẩy mọi giá trị chung ra ngoài, và chỉ mang theo index, các giá trị chạy theo.

### Cách viết 1 hàm recursion

Hàm recursion trên về cơ bản là khá nhiều tham số và khá rối. Bắt đầu từ đầu.
* Xác định mối liên hệ căn bản của 2 hàm recursion 
* Thêm dần các tham số vào rồi viết if else return + chỉnh lại phần gọi recursion phía dưới
* Sau đó bỏ các tham số lớn dùng chung ra ngoài

```
6
5 8 2 1 10 9
```
Nếu như `Alice` chọn số 9 thì `Bob` chọn 10 là thua. Nên Alice buộc chọn 5. (xét số phần tử dãy tăng lẻ)  
Khi này mình sẽ giải quyết dãy `8 2 1 10 9` nhưng `Bob` chọn.

Hàm recursion sẽ có dạng
```c++
vector<int> a;
int solve(l, r, player, cl, cr){
    // l, r: đánh dấu phạm vi còn lại của dãy có thể chọn
    // player: đánh dấu xem lượt của ai
    // cl, cr: đánh dấu số phần tử dãy tăng từ trái, phải qua
    if (a[l], .. a[r], .., cl%2==1, cr%2==1) return player || 1- player.
    // Tại đây đánh dấu player là 0,1 thì đối phương luôn là 1 - this.player
    return solve(l+1, r, 1-player, cl-1,cr) or solve(l, r-1, 1-player, cl,cr-1);
    // trường hợp người chơi đã chọn 1 giá trị left thì left+1, cl-1 còn nếu chọn phải thì right-1, cr-1
}
```