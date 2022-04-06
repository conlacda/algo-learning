# Z-function
> https://cp-algorithms.com/string/z-function.html

## Overview
* Đầu vào: string s
* Đầu ra: 1 mảng z[] độ dài bằng s.size()  
Z[i] thể hiện `z[0:z[i]] == z[i+z[i]]`  
Ví dụ:
"aaabaab" -> [0,2,1,0,2,1,0]  
  - z[0] được xét mặc định là 0
  - z[1] = 2 -> z[0:2] == z[1:3] = 'aa'
  - z[2] = 1 -> z[2:3] = 'a' = z[0]
## Code
```c++
vector<int> z_function(string s) {
    int n = (int) s.length();
    vector<int> z(n);
    for (int i = 1, l = 0, r = 0; i < n; ++i) {
        if (i <= r)
            z[i] = min (r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]])
            ++z[i];
        if (i + z[i] - 1 > r)
            l = i, r = i + z[i] - 1;
    }
    return z;
}
```

## Ứng dụng