# Một số cấu trúc dữ liệu trong C++
https://alyssaq.github.io/stl-complexities/
## Multiset

Là 1 tập hợp chứa các phần tử đã sắp xếp và có thể trùng nhau (set thì sẽ là ko trùng nhau)

**Các đặc điểm:**
* Các phần tử được sắp xếp sẵn
* Thao tác tìm kiếm O(logN)
* Thao tác xóa O(1) với *index và O(logN) với giá trị
* Thao tác thêm O(logN)
* Sử dụng cho 1 tập hợp ko quan tâm thứ tự và yêu cầu nhiều thao tác tìm kiếm và xóa phần tử 

**Các hàm**
```c++
multiset<int> z;
z.insert(3);
z.upper_bound(x);
z.upper_bound(x) == z.begin() // x không có trong multiset này
p = z.upper_bound(x); *prev(p) // lấy giá trị nhỏ hơn gần nhất với x. {1,5,9} x = 3 -> *prev(p) = 1
z.erase(prev(p)); z.erase(z.begin());// xóa 1 phần tử với con trỏ O(1)
z.erase(10);// xóa phần tử với giá trị O(logN)
z.find(10);
z.count(x);
z.lower_bound(x);
```
