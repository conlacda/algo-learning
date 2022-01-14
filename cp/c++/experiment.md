Với 1 chuỗi s cần duyệt. Thao tác tốt nhất là đảo ngược chuỗi s rồi duyệt xuôi
```C++
#include <bits/stdc++.h>
#define ll long long
using namespace std;
 
int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    #ifdef DEBUG
        freopen("inp.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif
    int N;
    cin >> N;
    vector<int> a;
    string s, max_s;
    ll sum =0;
    for (int i = 0; i < N; ++i)
    {
        int x;
        cin>>x;
        a.push_back(x);
        s+= "0"; max_s +="1";
        sum+=x;
    }
    // Sử dụng thuật toán vét cạn
    ll best = LLONG_MAX;
    for (int i=0;i<pow(2,N);i++){
        s = bitset< 20 >( i ).to_string();
        ll t =0;

        //2
        reverse(s.begin(), s.end());
        for (int j=0;j<N;j++){
            if (s[j] == '1'){
                t +=a[j];
            }
        }
        //2
        // for (int j=s.size()-1;j>=s.size()-N;j--){
            // if (s[j] == '1'){
            //     t += a[20-j-1];
            //     cout << 20-j-1<< ' ' << a[20-j-1] << '\n';
            // }
        // }
        best = min(best, abs(sum- 2*t));
    }
    cout << best;
}
/*
https://cses.fi/problemset/task/1623/
Cho dãy a[N]
Chia dãy thành 2 dãy sao cho độ chênh lệch 2 dãy là nhỏ nhất (tổng)
Thuật toán: sử dụng thuật toán brute force, khởi tạo dãy bit 0101001..
Với số 1 thì lấy số đó vào dãy 1 rồi tính tổng dãy 1 sau đó suy ra độ chênh lệch 2 dãy
Xét 2 block 1,2 bên trên //1 //2
Tại block đang xét dãy bit có dạng 00000..01..0101 có 20 kí tự và chỉ lấy N kí tự cuối
Thuật toán 1 đảo ngược dãy bit 1010...100..000 và duyệt từ 0 tới N cho dãy bit này
Thuật toán 2 duyệt ngược dãy bit luôn từ 19-> 20-N.
Có vẻ giống nhau nhưng thao tác duyệt từ cuối trở lại chậm chạp và gây ra lỗi bộ nhớ
-> ko qua bài test
*/
```