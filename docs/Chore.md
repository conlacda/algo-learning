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