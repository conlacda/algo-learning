# Tổng hợp 1 số thuật toán sắp xếp

## Merge sort

### Khái niệm

### Diễn giải

Mergesort có 3 phần chính: chia (divide), sắp xếp (sort), hợp lại (conquer)

1. Nếu có 1 phần tử thì trả về, dừng (điểm móc)
2. Chia đôi thành 2 phần tại điểm giữa (devide)
3. Sắp xếp từng phần (sort)
4. Hợp lại (conquer)

### Code

***Python***
```python
m = [12,5,9,7,1,10]
def merge(left, right):
    result = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else: 
            result.append(right[right_index])
            right_index += 1
   
    if left_index == len(left):
        result.extend(right[right_index:])
    else:
        result.extend(left[left_index:])
    return result

def merge_sort(m):
    if len(m) == 1:
        return m
    middle = len(m) // 2
    left = m[:middle]
    right = m[middle:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)

print(merge_sort(m))
```

***C++***
```C++
#include <iostream>
#include <vector>

using namespace std;

vector<int> merge(vector<int> left,vector<int> right){
    vector<int> result;
    int left_index = 0, right_index = 0;
    while (left_index < left.size() && right_index < right.size()){
        if (left[left_index] < right[right_index]){
            result.push_back(left[left_index]);
            left_index +=1;
        } else {
            result.push_back(right[right_index]);
            right_index +=1;
        }
    }
    if (left_index == left.size()) {
        for (int i=right_index;i< right.size();i++){
            result.push_back(right[i]);
        }
    } else if (right_index == right.size()){
        for (int i=left_index;i< left.size();i++){
            result.push_back(left[i]);
        }
    }
    return result;
}

vector<int> merge_sort(vector<int> arr){
    if (arr.size() == 1){
        return arr;
    }
    vector<int> left, right;
    int middle;
    middle = arr.size() / 2;
    for(int i=0;i<middle;i++){
        left.push_back(arr[i]);
    }
    for(int j= middle;j<arr.size();j++){
        right.push_back(arr[j]);
    }
    left = merge_sort(left);
    right = merge_sort(right);
    return merge(left, right);
}

int main(){
    vector<int> a = {1,5,3,2,6,4};
    a = merge_sort(a);
    for(int i=0;i<a.size();i++){
        cout << a[i] << " ";
    }
    return 0;
}
```