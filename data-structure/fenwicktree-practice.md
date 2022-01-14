## Ctrick
https://www.spoj.com/problems/CTRICK/  
Bài này hiện đang chưa tối ưu (chạy mất 8s so với limit 3.5s với maxN = 20000)

**Đề bài**:
```text
The magician shuffles a small pack of cards, holds it face down and performs the following procedure:

The top card is moved to the bottom of the pack. The new top card is dealt face up onto the table. It is the Ace of Spades.
Two cards are moved one at a time from the top to the bottom. The next card is dealt face up onto the table. It is the Two of Spades.
Three cards are moved one at a time…
This goes on until the nth and last card turns out to be the n of Spades.
This impressive trick works if the magician knows how to arrange the cards beforehand (and knows how to give a false shuffle). Your program has to determine the initial order of the cards for a given number of cards, 1 ≤ n ≤ 20000.

Input: 
On the first line of the input is a single positive integer, telling the number of test cases to follow. Each case consists of one line containing the integer n.  
Output: 
For each test case, output a line with the correct permutation of the values 1 to n, space separated. The first number showing the top card of the pack, etc…
Input:
3
4
5
50 

Output:
2 1 4 3
3 1 4 5 2
41 1 45 39 2 9 17 15 3 25 24 36 26 4 23 19 13 43 10 5 47 46 27 22 30 44 6 48 33 34 16 28 11 21 7 18 14 42 32 50 40 35 38 8 37 29 20 12 31 49
```

```c++
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Range query, point update
struct FenwickTree { // Zero-base indexing
    vector<long long> bit;  // binary indexed tree
    int n;

    FenwickTree(int n) {
        this->n = n;
        bit.assign(n, 0);
    }

    FenwickTree(vector<int> a) : FenwickTree(a.size()) {
        for (size_t i = 0; i < a.size(); i++)
            add(i, a[i]);
    }

    long long sum(int r) {
        if (r==-1) return 0;
        long long ret = 0;
        for (; r >= 0; r = (r & (r + 1)) - 1)
            ret += bit[r];
        return ret;
    }

    long long sum(int l, int r) {
        return sum(r) - sum(l-1);
    }

    void add(int idx, int delta) {
        for (; idx < n; idx = idx | (idx + 1))
            bit[idx] += delta;
    }
};

int number_zero(FenwickTree fw, int idx){
    int s = fw.sum(idx);
    return idx+1-s;
}
int main(){
    int t;
    cin >> t;
    while (t--){
        int N; cin >> N;
        vector<int> a(N, 0), ans(N,0);
        if (N==1) {
            cout << 1 << '\n';
        } else {
            a[1] = 1; ans[1] = 1;
            FenwickTree fw(a);
            int cp =1;
            for (int i=2;i<=N;i++){
                int total_zero = N - i + 1; // number_zero(fw, N-1)
                int left_zero = number_zero(fw, cp);
                int right_zero = total_zero - left_zero;
                int step = (i+1) % total_zero;
                if (step == 0) step = total_zero;
                int kth;
                if (step <= right_zero) kth = left_zero + step;
                else kth = step- right_zero;
                int l, r, mid;
                l = 0; r = N-1;
                
                // Binary search for k-th zero number 0 1 0 0 -> 3-th zero in index 3
                while (l<=r) {
                    mid = (l+r) /2;
                    if (number_zero(fw, mid) > kth) r = mid-1;
                    else if (number_zero(fw, mid) < kth) l = mid+1;
                    else {
                        r = mid;
                        if (r == l) break;
                    }
                }
                fw.add(r, 1); // r is the position of k-th zero
                ans[r] = i; // update ans[]
                cp = r; // update current point
            }
            for (auto v: ans) cout << v<< " "; cout <<'\n';
        }
    }
}
```


**Thuật toán**: Xét vector a {0,0,....,0}  
Mỗi quân bài được lật đồng nghĩa với giá trị 1. Đảo từ trên xuống dưới nhưng theo vòng tròn thì thứ tự các quân bài vẫn hệt như nhau.  
Bài toán đưa về tìm giá trị 0 thứ k trong dãy.  
a = {0,1,0,1,0,0} thì giá trị 0 thứ 4 sẽ có index 5

Ta có thể dùng Fenwicktree range query, point update.  
Range query để tính tổng từ 0->x để tính số số 0 đã có trong đoạn.  
Point update: gán giá trị 0 k-th index bằng 1 cho fwtree và i cho answer[]  

Rangequery: {0,1,0,0,2,0,0}.  
số 3 tiếp theo sẽ được điền tại index 0.  
Current position=4. left_zero tính bằng 4+1-fw.sum(index=4) = 3. -> right_zero = total_zero-left_zero.  
Dựa vào đó sẽ biết được số 3 sẽ điền vào số 0 thứ 1 của dãy hiện tại. 0(*3) 1 0 0 2 0(*1) 0(*2)  
Để tìm 0 k-th sử dụng binary search với giá trị tìm kiếm là số số 0 đang có bên trái middle. Nếu số số 0 nhỏ hơn k thì left->mid, ngược lại right->mid.  
Nếu tại mid có đủ k số 0. Right sẽ gán bằng mid để chặn đầu. {0,0,1,1,1}. Tìm vị trí 0 số 2 -> mid=2 sẽ thỏa mãn nhưng ans[2] = 1 không điền được nên cần dịch mid về bên trái. Nếu sử dụng while (ans[mid] != 0) mid--; sẽ làm độ phức tạp tăng. Tiếp tục binary search cho tới khi l==r. r chính là vị trí cần tìm.  
Cập nhật giá trị tại fw là đc.


## Kth zero (need to optimize)

Bài này giống hệt bài trên, đều chạy với thời gian 7-8s vượt quá mức cho phép là 2s. kết quả chạy ra hoàn toàn đúng
```c++
//https://www.hackerrank.com/contests/modena-coding-oct-2017/challenges/kthzero/forum
// Binary search chạy quá thời gian - kết quả đúng nhưng quá thời gian chạy
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Full example: https://github.com/conlacda/algo/blob/master/data-structure/fenwick-tree.md
// Range query, point update
struct FenwickTree { // Zero-base indexing
    vector<long long> bit;  // binary indexed tree
    int n;

    FenwickTree(int n) {
        this->n = n;
        bit.assign(n, 0); // bit = vector<long long> (n, 0);
    }

    FenwickTree(vector<int> a) : FenwickTree(a.size()) {
        for (size_t i = 0; i < a.size(); i++)
            add(i, a[i]);
    }

    long long sum(int r) {
        if (r==-1) return 0;
        long long ret = 0;
        for (; r >= 0; r = (r & (r + 1)) - 1)
            ret += bit[r];
        return ret;
    }

    long long sum(int l, int r) {
        return sum(r) - sum(l-1);
    }

    void add(int idx, int delta) {
        for (; idx < n; idx = idx | (idx + 1))
            bit[idx] += delta;
    }

    vector<int> original(){ // Return original value of input vector
        vector<int> a;
        for (int i=0;i<this->n;i++){
            a.push_back(sum(i,i));
        }
        for (auto v: a) cout << v<< ' '; cout << '\n';
        return a;
    }
};
/*
Initialize:
vector<long long> a{1,2,3,4,5};
FenwickTree fw(a);
---OR---
FenwickTree fw(N);
for (int i=0;i<N;i++){
    int x; cin >> x;
    fw.add(i,x);
}
Sum: fw.sum(r) // from 0->r (includes r)
     fw.sum(l,r) // from l->r (includes l,r)
Add: fw.add(r, k) // a[r] = a[r] + k
*/
int number_zero(FenwickTree fw, int idx){
    int s = fw.sum(idx);
    return idx+1-s;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N, Q;
    cin >> N >> Q;
    vector<int> a(N, 0);
    for (int i=0;i<N;i++){
        int x; cin >> x;
        if (x !=0) a[i] = 1;
    }
    FenwickTree fw(a);
    while (Q--){
        int q, p, v;
        cin >> q;
        if (q==1){
            cin >> p;
            // Find k-th index
            if (number_zero(fw,N-1) <p){
                cout << "NO" << '\n';
            } else{
                int left=0, right=N-1;
                while (left<=right) {
                    int mid = (left+right)/2;
                    int z = number_zero(fw, mid);
                    if (z < p){
                        left = mid+1;
                    } else if(z > p){
                        right = mid-1;
                    } else {
                        right = mid;
                        if (right==left) break;
                    }
                }
                cout << right << '\n';
            }
        } else { // q == 2
            cin >> p >> v;
            if (v!=0) v=1;
            if (a[p] !=v){
                int delta = v - a[p];
                fw.add(p, delta);
                a[p] = v;
            }
            // fw.original();
        }
    }
}

// Duy tri so luong so 0 hien co
// Neu number of 0 < k -> in ra NO
// Tìm vị trí số k
// Binary search -> left, right
```
