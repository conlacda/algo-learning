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