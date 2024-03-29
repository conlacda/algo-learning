# Fenwicktree

## Code

### One-based indexing - Point update, range query
```c++
// Reference: https://github.com/galencolin/cp-templates/blob/master/templates/bit.cpp
// Practice: https://atcoder.jp/contests/practice2/tasks/practice2_b
// Format code: https://codebeautify.org/cpp-formatter-beautifier
#include <bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;
// Range query, point update => fw.add(point, val) fw.sum(l,r);
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

### Zero-based indexing (Mainly use)
```c++
// Practice: https://atcoder.jp/contests/practice2/tasks/practice2_b
// Reference: https://cp-algorithms.com/data_structures/fenwick.html#toc-tgt-9
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;
// Range query, point update => fw.add(point, val) fw.sum(l,r);
struct FenwickTree { // Zero-based indexing
    vector<long long> bit;  // binary indexed tree
    int n;

    FenwickTree(int n) {
        this->n = n;
        bit.assign(n, 0); // bit = vector<long long>(n,0);
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
/*
vector<int> a{1,2,3,4,5};
FenwickTree fw(a);
fw.add(index, value); // index from 0 to N-1
fw.sum(l, r) // sum a[l], a[l+1],..., a[r];
*/
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

### Range update, point query
```c++
// Practice: https://www.codechef.com/problems/SPREAD
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Confirmed: https://www.codechef.com/viewsolution/49071966
// Full example: https://github.com/conlacda/algo/blob/master/data-structure/fenwick-tree.md
// Range update - point query
template <typename T>
struct fenwick_tree { // One-based indexing
    vector <T> bit;
    int N;

    fenwick_tree(int n) {
        this->N = n+1;
        bit.assign(n + 1, 0);
    }

    fenwick_tree(vector <T> a) : fenwick_tree(a.size()) {
        int sz = a.size();
        for (int i = 1; i <= sz; ++i) {
            update(i, i, a[i-1]);
        }
    }

    void internal_update(int idx, T val) {
        for (int i = idx; i < N; i += (i & (-i))) {
            bit[i] += val;
        }
    }

    void update(int l, int r, T val) {
        internal_update(l, val);
        internal_update(r + 1, -val);
    }

    T query(int idx) {
        T ans = 0;
        for (int i = idx; i; i -= (i & (-i))) {
            ans += bit[i];
        }
        return ans;
    }

    T query(int l, int r) {
        return query(r) - query(l - 1);
    }

    void original(){
        for (int i=1;i<N;i++){
            cout << query(i) << ' ';
        }
        cout << '\n';
    }
};
/*
vector<ll> a{1,2,3,4,5,6,7};
fenwick_tree<ll> fw(a);
fw.original();
fw.update(1,7,2);
fw.original();
cout << fw.query(7);
*/
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N, Q, V;
    cin >> N >> Q>>V;
    vector<ll> a(N,V);
    fenwick_tree<ll> fw(a);
    while (Q--){
        char s;
        cin >> s;
        if (s == 'Q'){
            int p; cin >> p;
            cout << fw.query(p) << '\n';
        } else {
            int p,q,k;
            cin >> p>>q>>k;
            fw.update(p,q,k);
        }
    }
}
```
### Range query, range update (UNDONE - TODO)
```c++
// Source https://www.geeksforgeeks.org/binary-indexed-tree-range-updates-point-queries/
// C++ program to demonstrate Range Update
// and Range Queries using BIT
#include <bits/stdc++.h>
using namespace std;

// Returns sum of arr[0..index]. This function assumes
// that the array is preprocessed and partial sums of
// array elements are stored in BITree[]
int getSum(int BITree[], int index)
{
    int sum = 0; // Initialize result

    // index in BITree[] is 1 more than the index in arr[]
    index = index + 1;

    // Traverse ancestors of BITree[index]
    while (index>0)
    {
        // Add current element of BITree to sum
        sum += BITree[index];

        // Move index to parent node in getSum View
        index -= index & (-index);
    }
    return sum;
}

// Updates a node in Binary Index Tree (BITree) at given
// index in BITree. The given value 'val' is added to
// BITree[i] and all of its ancestors in tree.
void updateBIT(int BITree[], int n, int index, int val)
{
    // index in BITree[] is 1 more than the index in arr[]
    index = index + 1;

    // Traverse all ancestors and add 'val'
    while (index <= n)
    {
        // Add 'val' to current node of BI Tree
        BITree[index] += val;

        // Update index to that of parent in update View
        index += index & (-index);
    }
}

// Returns the sum of array from [0, x]
int sum(int x, int BITTree1[], int BITTree2[])
{
    return (getSum(BITTree1, x) * x) - getSum(BITTree2, x);
}


void updateRange(int BITTree1[], int BITTree2[], int n,
                int val, int l, int r)
{
    // Update Both the Binary Index Trees
    // As discussed in the article

    // Update BIT1
    updateBIT(BITTree1,n,l,val);
    updateBIT(BITTree1,n,r+1,-val);

    // Update BIT2
    updateBIT(BITTree2,n,l,val*(l-1));
    updateBIT(BITTree2,n,r+1,-val*r);
}

int rangeSum(int l, int r, int BITTree1[], int BITTree2[])
{
    // Find sum from [0,r] then subtract sum
    // from [0,l-1] in order to find sum from
    // [l,r]
    return sum(r, BITTree1, BITTree2) -
        sum(l-1, BITTree1, BITTree2);
}


int *constructBITree(int n)
{
    // Create and initialize BITree[] as 0
    int *BITree =new int[n+1];
    for (int i=1; i<=n; i++)
        BITree[i] = 0;

    return BITree;
}

// Driver Program to test above function
int main()
{
    int n = 5;

    // Construct two BIT
    int *BITTree1, *BITTree2;

    // BIT1 to get element at any index
    // in the array
    BITTree1 = constructBITree(n);

    // BIT 2 maintains the extra term
    // which needs to be subtracted
    BITTree2 = constructBITree(n);

    // Add 5 to all the elements from [0,4]
    int l = 0 , r = 4 , val = 5;
    updateRange(BITTree1,BITTree2,n,val,l,r);

    // Add 2 to all the elements from [2,4]
    l = 2 , r = 4 , val = 10;
    updateRange(BITTree1,BITTree2,n,val,l,r);

    // Find sum of all the elements from
    // [1,4]
    l = 1 , r = 4;
    cout << "Sum of elements from [" << l
        << "," << r << "] is ";
    cout << rangeSum(l,r,BITTree1,BITTree2) << "\n";

    return 0;
}
```
## Reference
* https://cp-algorithms.com/data_structures/fenwick.html#toc-tgt-1

## Practice

[Paractice Exercise here](fenwicktree-practice.md)