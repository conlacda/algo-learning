# Bitwise operator

## Các phép tính

* & : phép và (AND) bằng 1 khi cả 2 bằng 1 || và với 1 thì giữ nguyên
* | : phép hoặc (OR) bằng 1 khi 1 trong 2 bằng 1 || hoặc với 0 thì giữ nguyên
* << : dịch trái (left shift) **a<<b = a\*(2\*\*b)**
* \>> : dịch phải (right shift)  **a>>b = a/(2\*\*b)**
* ~ : NOT 
* ^ : XOR bằng 1 khi 2 số khác nhau

## Interesting facts

### Phép dịch bit a<<b

* Phép dịch bit không sử dụng với toán hạng âm (a,b>=0)

* Chỉ dịch bit với số bit toán hạng có b<=32 nếu a là int32

* Phép dịch trái **a<<b** tương đương với **a\*(2\*\*b)**

* Phép dịch phải a>>b tương đương với **a/(2\*\*b)**

### Phép XOR ^

* **a^b = c <=> a^c=b c^b=a**. Các toán hạng trong XOR có thể thay đổi vị trí

### Phép AND &

* Phép &1 có thể sử dụng để kiểm tra số chẵn lẻ  
**a&1? "Odd" : "Even"**

### Phép NOT ~

* Phép NOT chuyển đổi 0 thành 1 và ngược lại.

Ví dụ: ~1 = 2  
1 = 0000000000000001  
-2 = 1111111111111110

Cẩn thận khi sử dụng vì ~1 không phải là 0

## Some trick/ Practice

### Clear bit

**from i-th to the end**

29 = 00011101 => muốn có được 00010000

1<<N = 00010000  
(1<<N)-1 = 00001111  
~((1<<N)-1) = 11110000  
x&(~((1<<N)-1)) = 00010000  

**from begin to i-th**

215 = 11010111 => muốn có được 00000111

N=4
1<<N = 00010000  
(1<<N)-1 = 00001111  
x&((1<<N)-1) = 00000111  

### Convert char lower case to upper case and opposite
**A..Z -> a..z**  
ch |= ' ';

A = 65  space = 32  A|' ' = 65|32 = 97 = 'a'

**a..z -> A..Z**

ch &= '_’ ;

### Lặp qua các bit

* Bit cuối = x&1
* Xóa bit cuối: x>>1

13 = 1101 -> 13&1 = 000**1** -> 13>>1 = 0**110**

### Tính log của x

Đơn giản dùng phép dịch bit cho tới khi x=0
```c++
while (x>>=1){
    count++;
}
```

### Kiểm tra 1 số có phải mũ của 2 không

x = pow(2,n) = 10...0 -> x-1 = 01...1  
**x&(x-1) = 0**

### Đang xem dở 
https://www.geeksforgeeks.org/bitwise-hacks-for-competitive-programming/