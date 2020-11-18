# Tổng hợp 1 số thuật toán sắp xếp

## Merge sort

### Khái niệm

### Diễn giải

Mergesort có 3 phần chính: chia (divide), sắp xếp (sort), hợp lại (conquer)

1. Nếu có 1 phần tử thì trả về, dừng
2.

### Code

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