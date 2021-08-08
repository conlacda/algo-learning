# Dsu applications

## Solved problems

<details>
<summary>25D Roads not only in Berland</summary>
<p>

```c++
//https://codeforces.com/contest/25/problem/D
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

class DSU {
 public:
  vector<int> parent, _rank;
  DSU(int N) {
    this->parent.resize(N);
    this->_rank.resize(N);
    for (int i = 0; i < N; i++) {
      this->make_set(i);
    }
  }

  void make_set(int v) {
    this->parent[v] = v;
    this->_rank[v] = 0;
  }

  int find_set(int v) {
    if (v == parent[v]) {
      return v;
    }
    return parent[v] = find_set(parent[v]);
  }

  void merge_set(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
      if (_rank[a] < _rank[b]) {
        swap(a, b);
      }
      parent[b] = a;
      if (_rank[a] == _rank[b]) {
        _rank[a]++;
      }
    }
  }
};

int main(){
    int N;
    cin >> N;
    DSU dsu(N+1);
    vector<pair<int,int>> closure, new_build;
    while (N-->1){
        int a,b;
        cin >> a>>b;
        int f1 = dsu.find_set(a), f2 = dsu.find_set(b);
        if (f1 == f2){
            closure.push_back({a,b});
        } else {
            dsu.merge_set(a,b);
        }
    }
    for (int i=2;i<dsu.parent.size();i++){
        if (dsu.parent[i] != dsu.parent[i-1]){
            dsu.find_set(i);
            dsu.find_set(i-1);
            if (dsu.parent[i] != dsu.parent[i-1]){
                new_build.push_back({i, i-1});
                dsu.merge_set(i, i-1);
            }
        }
    }
    cout << new_build.size() << '\n';
    for (int i=0;i< new_build.size(); i++){
        cout << closure[i].first << ' '<<closure[i].second << ' '<< new_build[i].first << ' ' <<new_build[i].second<<'\n';
    }
}

```
</p>
</details>  

<details>
<summary>Unbelievable Array</summary>
<p>

```c++
// Problem: https://toph.co/p/unbelievable-array 
// Verification: https://toph.co/s/729405
// DSU:
// Cho 1 tập hợp cố định các số
// Mỗi số là 1 tập hợp - make_set
// Gắn 2 số vào thành 1 set - union_set
// Tra xem 2 số có thuộc 1 set hay không - find_set

// -----

// Cho mỗi index là 1 tập hợp - make_set
// 2 số có giá trị trùng nhau thì ghép 2 index vào 1 - union_set
// tìm ra set của index này rồi tra vào bảng giá trị - find_set

/*
Thuật toán tại đây:
Coi mỗi index trong vector là 1 node - make_set
Index nào có giá trị giống nhau thì sẽ dùng merge_set

Sử dụng 1 mảng value2index để đánh dấu giá trị nào đang ở vị trí nào
    Ví dụ: value2index[2] = 3. Nghĩa là giá trị 2 sẽ ở index 3. và index 3 chính là root (find_set) của set đó
           value2index[2] = -1 nghĩa là ko có giá trị 2 trong mảng - thao tác thay thế x->y thì value2index[x] = -1 và value2index[y] = root của set mới
Thao tác thay đổi x->y
    Thao tác này sẽ dùng value2index để tìm ra root_x, root_y.
    Nếu root_x = -1 thì bỏ qua
    Nếu root_y = -1 thì a[root_x] = y - mảng a hiện giờ chỉ lưu giữ giá trị tại các đỉnh root
                        value2index[y] = root_x - giá trị y bây giờ sẽ đánh dấu tại index root_x
                        value2index[x] = -1 - vì thay thế x bằng y nên ko còn x
    Nếu root_y = 1 thì merge 2 set của root_x và root_y lại. dsu.merge_set(root_x, root_y)
    value2index[x] = -1
    value2index[y] = p với p = new_root_of_set = dsu.find_set(root_x)
    a[p] = y - đánh dấu giá trị đỉnh p với giá trị mới là y

Lưu ý: nên xử lý các trường hợp ngoại lệ luôn bên ngoài
Ví dụ: value2index[x] = -1 - x ko tồn tại trong dãy -> bỏ qua luôn
       x = y -> thay 2 giá trị như nhau -> bỏ qua luôn
*/
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// Full example:
// https://github.com/conlacda/algo-practice/blob/master/atcoder/beginner-acl/disjoint-union-set.md
class DSU {
 public:
  vector<int> parent, _rank;
  DSU(int N) {
    this->parent.resize(N);
    this->_rank.resize(N);
    for (int i = 0; i < N; i++) {
      this->make_set(i);
    }
  }

  void make_set(int v) {
    this->parent[v] = v;
    this->_rank[v] = 0;
  }

  int find_set(int v) {
    if (v == parent[v]) {
      return v;
    }
    return parent[v] = find_set(parent[v]);
  }

  void merge_set(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
      if (_rank[a] < _rank[b]) {
        swap(a, b);
      }
      parent[b] = a;
      if (_rank[a] == _rank[b]) {
        _rank[a]++;
      }
    }
  }
};
/*
DSU dsu(N);
dsu.merge_set(u,v);
dsu.find_set(u) == dsu.find_set(v); // check if u,v in the same SCC
*/
void solve(int i){
    cout << "Case "<< i << ":\n";
    int N, qr;
    cin >> N >> qr;
    DSU dsu(N);
    vector<int> a(N), value2index(100001, -1);
    for (int i=0;i<N;i++){
        cin >> a[i];
        if (value2index[a[i]] ==-1) { // nếu chưa xuất hiện
            value2index[a[i]] = i;
        } else { // nếu xuất hiện rồi thì merge 2 phần tử lại
            dsu.merge_set(value2index[a[i]], i);
        }
    }
    while (qr--){
        int q, x, y;
        cin >> q;
        if (q==1){
            cin >> x >> y;
            if (x == y) continue;
            // Replace x by y
            int ix = value2index[x];
            int iy = value2index[y];
            if (ix != -1){
                if (iy == -1){
                    int rootx = dsu.find_set(ix);
                    a[rootx] = y;
                    value2index[x] = -1;
                    value2index[y] = rootx;
                } else if (iy != -1){
                    int rootx = dsu.find_set(ix);
                    int rooty = dsu.find_set(iy);
                    dsu.merge_set(rootx, rooty);
                    int p = dsu.find_set(rootx);
                    value2index[y] = p;
                    value2index[x] = -1;
                    a[p] = y;
                }
            } // ix == -1 means ix not exists.
        } else {
            cin >> x; x--;
            // print a[x]
            int root = dsu.find_set(x);
            cout << a[root] << '\n';
        }
    }
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int t;
    cin >> t;
    for (int i=1;i<=t;i++){
        solve(i);
    }
}
```
</p>
</details>  

<details>
<summary>Lexicographically minimal string
</summary>
<p>

```c++
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double
const int maxN = 100001;

using namespace std;

class DSU {
 public:
  vector<int> parent, _rank;
  DSU(int N) {
    this->parent.resize(N);
    this->_rank.resize(N);
    for (int i = 0; i < N; i++) {
      this->make_set(i);
    }
  }

  void make_set(int v) {
    this->parent[v] = v;
    this->_rank[v] = 0;
  }

  int find_set(int v) {
    if (v == parent[v]) {
      return v;
    }
    return parent[v] = find_set(parent[v]);
  }

  void merge_set(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
      if (_rank[a] < _rank[b]) {
        swap(a, b);
      }
      parent[b] = a;
      if (_rank[a] == _rank[b]) {
        _rank[a]++;
      }
    }
  }
};

int indexOf(char c, string al){
    for (int i=0;i<al.size();i++) {
        if (al[i] == c) return i;
    }
    return -1;
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    string a,b,c;
    cin >> a >> b>>c;
    string alphabet = "abcdefghijklmnopqrstuvwxyz";
    vector<char> min_value(alphabet.size());
    for (int i=0;i<alphabet.size();i++){
        min_value[i] = alphabet[i];
    }
    DSU dsu(alphabet.size());
    for (int i=0;i<a.size();i++){
        int ai = indexOf(a[i], alphabet);
        int bi = indexOf(b[i], alphabet);
        char a_minvalue = min_value[dsu.find_set(ai)];
        char b_minvalue = min_value[dsu.find_set(bi)];
        dsu.merge_set(ai, bi);
        int p = dsu.find_set(ai);
        min_value[p] = min(a_minvalue, b_minvalue);
    }
    for (int i=0;i<c.size();i++){
        int indx = indexOf(c[i], alphabet);
        int p = dsu.find_set(indx);
        c[i] = min_value[p];
    }
    cout << c;
}

```
</p>
</details>  
## Unsolved problem

<details>
<summary>CHAIN - Strange Food Chain</summary>
<p>

```c++
// https://www.spoj.com/problems/CHAIN/
/*
Ý tưởng:
* Dựng 2 DSU
    - 1 DSU lưu lại tất cả các điểm đã xuất hiện (trong query)
    - 1 DSU đánh dấu type[] của các set
* Dùng 2 mảng lưu lại quan hệ cha con giữa các set
* Đánh dấu type cho các set
    - Nếu a b cùng loại thì đánh dấu là 1 nếu chưa có loại
        không thì phụ thuộc vào loại của a,b
    - Nếu a ăn b thì đánh dấu 1>2, hoặc phụ thuộc a,b đã biết
    - Sau khi đánh dấu 2 đỉnh sẽ đánh lại hết loại cho tập con, cha của nó
-> Ví dụ: 1>2 3>4 -> lúc này type(1)=type(3) = 1, type(2) = type(4) = 2
(>: kí hiệu là ăn)
Giờ 1>3 -> type(3) = 2 = type(1)+1. Dùng 2 mảng chứa tập con của 3 và cha của 3
rồi đánh dấu lại hết.
while (eats[b] != b) { #remark type }
while (ate[b] != b) { #remark type }
*/
/*
USER: zobayer
TASK: CHAIN
ALGO: disjoint set
*/
// Phần code này của người khác code - có thể gõ CHAIN - Strange Food Chain solution
#include<bits/stdc++.h>
using namespace std;

const int MAX = 50001;

int root[MAX], d[MAX];

int find(int u) {
	if(u == root[u]) return u;
	int tmp = root[u];
	root[u] = find(root[u]);
	d[u] = d[tmp] + d[u];
	return root[u];
}

int main() {
	//READ("in.txt");
	//WRITE("out.txt");
	int test, cs, n, k, i, t, x, y, px, py, ans, tmp;
	scanf("%d", &test);
	for(cs = 1; cs <= test; cs++) {
		scanf("%d %d", &n, &k);
		for(i = 1; i <= n; i++) {
			root[i] = i;
			d[i] = 0;
		}
		ans = 0;
		while(k--) {
			scanf("%d %d %d", &t, &x, &y);
			if(x > n || y > n) { ans++; continue; }
			px = find(x);
			py = find(y);
			t--;
			if(px == py) {
				tmp = (d[x] - d[y]) % 3; if(tmp < 0) tmp += 3;
				if(tmp != t) ans++;
			}
			else {
				root[px] = py;
				i = (d[x] - d[y] - t) % 3;
				d[px] = i < 0? -i : -i+3;
			}
		}
		printf("%d\n", ans);
	}
	return 0;
}

```
</p>
</details>  