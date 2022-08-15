# Trie

![images/trie.png](images/trie.png)

String s và tập hợp các string k. Tìm pattern matching - s được tạo thành bởi các string nào trong k.

## Naive approach
```c++
for (auto sub: k){
    // find k in s using rabin karp,...
}
// Độ phức tạp cho rabin karp là O(s.size())
// Toàn bộ O(s.size()) * k.size() -> 10^5*10^5
```
## Sử dụng trie
Nhìn vào hình trên thì chỉ cần duyệt string và trie
* Dựng trie: tổng độ dài các string trong k (max ~ 10^6)
* Match s với trie: O(s.size())  
=> `O(tổng độ dài các string s+k) ~ O(10^6)` 
## Template
[Trie on string](https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/snippet/string-trie.sublime-snippet)
## Tham khảo
* https://www.hackerearth.com/practice/data-structures/advanced-data-structures/trie-keyword-tree/tutorial/
* Coursera - algorithm on strings
## practice problem
<details>
    <summary>Word Combinations - CSES</summary>

```c++
// https://cses.fi/problemset/task/1731/
// Cho string s và tập hợp k gồm các string nhỏ hơn. Có bao nhiêu cách ghép s từ các str trong k. 
/*
Input:
ababc
4
ab
abab
c
cb
Output:
2
Explanation: The possible ways are ab+ab+c and abab+c.
*/
#include<bits/stdc++.h>
 
typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double
 
using namespace std;
 
struct Node{
    char val;
    bool is_leaf = false;
    vector<Node*> childs{};
    Node(char val){
        this->val = val;
    }
    Node* find_child(char val){
        for (auto &n: this->childs){
            if (n->val == val){
                return n;
            }
        }
        return nullptr;
    }
    Node* get_or_create_child(char val){
        // Tìm
        Node* child = find_child(val);
        if (child != nullptr) return child;
        // Tạo mới
        Node* new_child = new Node(val);
        this->childs.push_back(new_child);
        return new_child;
    }
};
 
struct Trie{
    Node root = Node(0); // 0 là root, 'a', 'b' bắt đầu từ 1, 2,...
    Trie(){}
    void insert(string s){
        Node* cur = &root;
        for (auto c: s){
            cur = cur->get_or_create_child(c);
        }
        cur->is_leaf = true;
    }
 
    int ans = 0;
    void match_word(string word){
        /* Tại mỗi điểm tính các cái match tại điểm đó - tức là những string nào bắt đầu từ đó được
        */
        vector<ll> way(word.size()+1, 0);
        way[0] = 1;
        for (int i=0;i<word.size();i++){
            // Tìm match tại điểm này
            Node* cur = &root;
            int index = i;
 
            while (true){
                cur = cur->find_child(word[index]);
                if (cur == nullptr) break;
                index++;
                if (cur->is_leaf) {
                    way.at(index) += way.at(i);
                    way[index] %= mod;
                }
            }
        }
        cout << way[word.size()]<<'\n';
    }
};
 
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    string s;
    cin >> s;
    int n; cin >> n;
    Trie trie;
    for (int i=0;i<n;i++){
        string x; cin >> x;
        trie.insert(x);
    }
    trie.match_word(s);
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}
```
</details>

<details>
    <summary>Search Engine - hackerearth.com</summary>

```c++
#include<bits/stdc++.h>

typedef long long ll;
const ll mod = 1e9 + 7;
#define ld long double

using namespace std;

// https://github.com/conlacda/algo-learning/blob/master/string/trie.md
struct Node{
    char val;
    bool is_leaf = false;
    vector<Node*> childs{};
    int weight = 0;
    Node(char val){
        this->val = val;
    }
    Node* find_child(char val){
        for (auto &n: this->childs){
            if (n->val == val){
                // n->weight = max(n->weight, weight);
                return n;
            }
        }
        return nullptr;
    }
    Node* get_or_create_child(char val, int weight){
        // Tìm
        Node* child = find_child(val);
        if (child != nullptr) {
            child->weight = max(child->weight, weight);
            return child;
        }
        // Tạo mới qdpph
        Node* new_child = new Node(val);
        new_child->weight = weight;
        this->childs.push_back(new_child);
        return new_child;
    }
};
 
struct Trie{
    Node root = Node(0); // 0 là root, 'a', 'b' bắt đầu từ 1, 2,...
    Trie(){}
    void insert(string s, int weight){
        Node* cur = &root;
        for (auto c: s){
            cur = cur->get_or_create_child(c, weight);
        }
        cur->is_leaf = true;
    }
    int find(string s){
        Node* cur = &root;
        int ans = 0;
        for (int i=0;i<s.size();i++){
            cur = cur->find_child(s[i]);
            if (cur == nullptr){
                return -1;
            }
            ans = cur->weight;
        }
        return ans;
    }
};
/*
Trie trie;
trie.insert("string");
Node *cur = &root;
cur = cur->find_child(char c);
if (cur == nullptr) tại đây là đi tới cuối trie mà ko match được với kí tự c trong s
if (cur->if_leaf) {} // tại đây match với 1 string trong k
*/

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int n, q; cin >> n >> q;
    Trie trie;
    for (int i=0;i<n;i++){
        string s; int w;
        cin >> s >> w;
        trie.insert(s, w);
    }
    for (int i=0;i<q;i++){
        string s;
        cin >> s;
        cout << trie.find(s)<<'\n';
    }
    cerr << "Time : " << (double)clock() / (double)CLOCKS_PER_SEC << "s\n";
}

```
</details>