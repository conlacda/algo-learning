# Fenwicktree

## Code
```c++
// Reference: https://github.com/galencolin/cp-templates/blob/master/templates/bit.cpp
// Practice: https://atcoder.jp/contests/practice2/tasks/practice2_b
// Format code: https://codebeautify.org/cpp-formatter-beautifier
#include <bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;
struct FenwickTree { // One-based indexing
    int n;
    vector < long long > bitree;

    FenwickTree(int N) {
        bitree = vector < long long > (N + 1, 0);
        n = N;
    }
    FenwickTree(vector < int > v): FenwickTree(v.size()) {
        for (int i = 0; i < n; i++) {
            add(i + 1, v[i]);
        }
    }
    void add(int loc, long long x) {
        if (loc <= 0)
            return;
        while (loc <= n) {
            bitree[loc] += x;
            loc += loc & (-loc);
        }
    }

    long long sum(int index) {
        long long sum = 0;
        while (index > 0) {
            sum += bitree[index];
            index -= index & (-index);
        }
        return sum;
    }
    long long range(int left, int right) {
        return sum(right) - sum(left);
    }
};

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
    freopen("inp.txt", "r", stdin);
    freopen("out.txt", "w", stdout);
    #endif
    int N, M;
    cin >> N >> M;
    FenwickTree fw(N);
    for (int i = 0; i < N; i++) {
        int x;
        cin >> x;
        fw.add(i + 1, x);
    }
    // vector < int > a;
    // for (int i = 1; i <= N; i++) {
    //     int x;
    //     cin >> x;
    //     a.push_back(x);
    // }
    // FenwickTree fw(a);
    while (M--) {
        int q, l, r;
        cin >> q >> l >> r;
        if (q == 0)
            fw.add(l + 1, r);
        else {
            // cout << fw.range(l, r) << '\n';
            cout << fw.sum(r) - fw.sum(l) << '\n';
        }
    }
}
```

```c++
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

struct FenwickTree {
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
int main(){
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N, M;
    cin >> N >> M;
    vector<int> a;
    for (int i=0;i<N;i++){
        int x; cin >> x;
        a.push_back(x);
    }
    FenwickTree fw(a);
    
    while (M--){
        int q,l,r;
        cin >> q>>l>>r;
        if (q ==0){
            fw.add(l, r);
        } else {
            cout << fw.sum(l,r-1) << '\n';
        }
    }
}
```
## Reference
* https://cp-algorithms.com/data_structures/fenwick.html#toc-tgt-1