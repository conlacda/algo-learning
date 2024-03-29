# Một vài nguyên mẫu hàm đơn giản

## Tìm kiếm nhị phân

```C++
// Sử dụng thuật toán chia để trị
#include <iostream>
#include <vector>

using namespace std;

int binary_search(vector<int> list,int target){
    int first = 0;
    int last = list.size()-1;
    int middle;
    while (first < last){
        middle = (first + last) / 2;
        if (list[middle] == target){
            return middle;
        } else if (list[middle] < target){
            first = middle + 1;
        } else if (list[middle] > target){
            last = middle - 1;
        }
    }
    return -1;
}
int main(){
    vector<int> a = {1,2,3,4,5,7,8,9};
    cout << binary_search(a,7);
}
```

## Dynamic Programming

***Bài toán***: Có n đồng xu, để tạo ra X xu thì cần ít nhất bao nhiêu đồng
> Phân tích: Tại đây số xu tạo ra X có thể tính bằng giá trị nhỏ nhất có số xu khi bỏ ra 1 đồng. X = 1 + (X-i) i: đồng xu bị bỏ ra. Lấy min số đồng xu tạo ra X-i rồi cộng 1
```python
Python
def coinsChange(V,list):
    table = [0]
    for i in range(1,V+1):
        _min = float("inf")
        for coin in list:
            if i >= coin:
                _min = min(_min,1 + table[i-coin])
        table.append(_min)
    print(table)

t = coinsChange(11,[1,2,5])
print(t[V])
```

```C++
#include <iostream>
#include <vector>
#include <limits>

using namespace std;

vector<int> coinsChange(int V, vector<int> list){
    vector<int> table = {0};
    int min;
    for(int i=1;i<V+1;i++){
        min = numeric_limits<int>::max();
        for(int j=0; j<list.size();j++){
            if (list[j] <= i){
                if (min > 1 + table[i - list[j]]){
                    min = 1 + table[i - list[j]];
                }
            }
        }
        table.push_back(min);
    }
    return table;
}
int main(){
    vector<int> t = coinsChange(11,{1,2,5});
    for (int i=0;i<t.size();i++){
        cout << t[i] << " ";
    }
    return 1;
}

```

***Bài toán***: Dãy con tăng lớn nhất
> Phân tích: số đằng sau sẽ tính toán dựa vào số những giá trị đằng trước. Nếu với i>j nếu x[i] > x[j] và a[i] < a[j] thì a[i] = a[j] + 1. Mảng a sẽ lưu trữ lại độ dài dãy con tính đến i. Để lấy ra danh sách dãy con thì dùng 1 mảng b để đánh dấu vị trí của phần tử trước đó a[i] = a[j] +1; b[i] = j

```Python
# Dãy con tăng lớn nhất
x = [1,2,6,3,10,4,5,4,1,11]
a = [1] * len(x)
b = [0] * len(x)
if len(x) == 1:
    print(1)
else:
    max, pos = 1,1
    # if x[i] > x[j] and a[j] > max: a[i] = a[j]+ 1
    for i in range(1,len(x)):
        a[i] = 1
        for j in range(0,i):
            if x[i] > x[j] and a[i] <= a[j]:
                a[i] = a[j] + 1
                b[i] = j
                if a[i] > max:
                    max = a[i]
                    pos = i
    # print(a)
    # print(b)
    # print(max, pos)
    for i in range(max):
        print(x[pos])
        pos = b[pos]
```

```C++
#include <iostream>
#include <vector>

using namespace std;
int main(){
    vector<int> x;
    x.assign({1,2,6,5,3,4,9,13,10});
    vector<int> a,b;
    for(int i=0;i<x.size();i++){
        a.push_back(1);
        b.push_back(0);
    }
    int max = 1;
    int pos = 0;
    for (int i=1; i< x.size();i++){
        for (int j=0; j<i;j++){
            if (x[i] > x[j] && a[i] <= a[j]){
                a[i] = a[j] + 1; // tang do dai day con tang
                b[i] = j; // luu vi tri
                if (a[i] > max){
                    max = a[i];
                    pos = i;
                }
            }
        }
    }
    for(int i=0;i< max;i++){
        cout << x[pos] << " ";
        pos = b[pos];
    }
}
```
