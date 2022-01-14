## Python vs Pypy3

Ưu tiên lựa chọn python. Nếu bị time exceeded thì mới thử tới pypy3.

Xét ví dụ: https://codeforces.com/problemset/problem/1539/C

```python
from math import ceil
n, add, diff = [int(i) for i in input().split()]
a = [int(i) for i in input().split()]
a.sort()
dis = []
for i in range(1, len(a)):
    if a[i] - a[i-1] > diff:
        dis.append((a[i] -a[i-1]-1)//diff)

ans = len(dis)+1
dis.sort()
for it in dis:
    if it <= add:
        ans -=1
        add -= it
        if add <=0:
            break
    
print(ans)
```
Đoạn code này hoạt động tốt với python3 nhưng ko thể hoạt động được với pypy3 (TLE - time exceeded error)

**=>** Đối với bài A,B,C giới hạn lớn (10^18) thì nên chọn python thay vì C++ để tránh bị lỗi tràn bộ nhớ.  
string sử dụng python cũng tiện hơn với biểu thức str[a:b], str+= "a", for it in str