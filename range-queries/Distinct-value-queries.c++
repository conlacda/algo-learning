// Distinct Values Queries
//https://cses.fi/problemset/result/2787915/
/*
https://atcoder.jp/contests/abc174/tasks/abc174_f
https://www.spoj.com/problems/DQUERY/
Bài toán dùng fenwicktree tính tổng
Offline query.
Sắp xếp tất cả các query theo r
Đầu vào fenwicktree chính là 1 mảng rỗng
Sau đó duyệt từ 0 tới N (đầu tới cuối mảng)
Với 1 số. Nếu nó chưa xuất hiện thì tại vị trí đó tăng lên 1 (update)
Nếu đã xuất hiện thì vị trí trước đó trừ đi 1.
Với 1 query thì tính tổng từ l->r.
Đẩy kết quả vào 1 mảng rồi sắp xếp lại rồi trả về
*/
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
};
 
struct Query{
    int index, l, r;
};
bool cmp(Query a, Query b){
    return a.r < b.r; // min -> max 1 2 3 4
}
 
bool cmp_ans(pair<int,int>a ,pair<int,int> b){
    return a.first < b.first;
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
    vector<int> a(N);
    vector<Query> q;
    for (int i=0;i<N;i++) cin >> a[i];
    for (int i=0;i<Q;i++){
        int l , r;
        cin >> l >> r;
        l--;r--;
        q.push_back(Query{i, l, r});
    }
    sort(q.begin(), q.end(), cmp);
    vector<pair<int,int>> ans; // index, answer
    vector<int> b(N, 0);
    FenwickTree fw(b);
    map<int, int>last_pos;
 
    int cur_index = 0;
    for (int i=0;i<N;i++){
        if (last_pos.count(a[i]) ==0){
            last_pos[a[i]] = i;
            fw.add(i, 1);
        } else {
            int old_pos = last_pos[a[i]];
            fw.add(old_pos, -1);
            last_pos[a[i]] = i; // new position
            fw.add(i, 1);
        }
        if (cur_index < q.size() ) {
            // cout << cur_index<<'\n';
            while (i==q[cur_index].r) {
                int v = fw.sum(q[cur_index].l, q[cur_index].r);
                ans.push_back({q[cur_index].index, v});
                cur_index++;
            }
        } 
    }
    sort(ans.begin(), ans.end(), cmp_ans);
    for (auto v: ans) cout << v.second<<'\n';
}
 
/*
Mô tả dữ liệu
input a = 3 2 3 1 2
Query: 
1 3 sort 1 3
2 5 -->  1 4
1 4      2 5
Thao tác sort này gọi là offline query. 
Thay vì query bất kỳ thì query theo thứ tự duyệt mảng và sắp lại lại rồi mới in ra
 
Fenwick 0 0 0 0 0
        1 0 0 0 0  last_pos[3] = 0
        1 1 0 0 0  last_pos[2] = 1
        0 1 1 0 0  last_pos[3] = 2
        0 1 1 1 0  last_pos[1] = 3
        0 1 0 1 1  last_pos[2] = 4
Duyệt từ đầu tới cuối mảng a (for auto v:a). 
Nếu tồn tại last_pos[v] thì vị trí last_pos[v] đó trừ đi 1. Còn vị trí mới +1
Ví dụ: 3 2 3 1 2
Duyệt tới số 3 thứ 2 -> old_position = last_pos[3] = 0 => fw.add(old_postion, -1)
                        new_position = i = 2 => fw.add(new_position, 1), last_post[v] = new_position
 
Thao tác sắp xếp trả về kết quả
1 vector chứa các query thì chứa theo cả index 
Query<index, l, r>. ban đầu sắp xếp thì so sánh r
Sau đó có vector<pair<int, int>>ans. Với pair<int, int> = <index, value>
-> Sắp xếp lại theo index rồi in ra value là được.
 
Tham khảo phần này: https://stackoverflow.com/questions/39787455/is-it-possible-to-query-number-of-distinct-integers-in-a-range-in-olg-n
Bài này có thể giải được bài cho dãy A(N).
Query (l,r, value) hỏi rằng có bao nhiêu số trong khoảng [l,r] có giá trị lớn hơn value
Bài này: có 1 phần giải https://www.geeksforgeeks.org/number-of-elements-greater-than-k-in-the-range-l-to-r-using-fenwick-tree-offline-queries/
Nhưng ko hiểu rõ
Cách đơn giản hơn sử dụng Segment tree (xem snippet segment tree https://github.com/conlacda/noteforprofessionals/blob/master/language/C%2B%2B/snippet/segmenttree.sublime-snippet)
Xét template T với T là 1 vector<int>, hàm merge() là hàm cộng vector()
Khi đó ta sẽ có 1 merge sort tree
|1 1 2 4 5 6 7 8|
|1 2 5 6|1 4 7 8|
|1 5|2 6|4 8|1 7|
|1|5|2|6|8|4|7|1|
Khi thực hiện 1 truy vấn l,r,k
-> Truy vấn l,r tới segment tree sẽ trả về vector đã sắp xếp.
Và sử dụng binary search để tìm số lượng phần tử lớn hơn k trong 1 mảng đã sắp xếp
Lưu ý*: thao tác cộng vector là 1 thao tác chậm chạp. Ví dụ 1 2 5 6 + 4 8.
Cộng vào rồi mới binary search sẽ gây ra thao tác O(N) cho mỗi hàm merge và log(N) cho thao tác binary search
Do đó thay vì merge() 2 vector có thể tính luôn binary search cho 1 2 5 6, 4 8 rồi cộng 2 kết quả lại là được.
*/