n = int(input())

# print(type(format(10, 'b')))
def f(number):
    binary_number = format(number, 'b')
    for i in range(len(binary_number)-1, -1,-1):
        if binary_number[i] == '1':
            return len(binary_number) - i-1
def assign(s, index, value):
    return s[:index] + value + s[index+1:]
s = "0" * n
for i in range(1,2**n):
    print(s)
    s = assign(s, f(i), str(1-int(s[f(i)])))
print(s)
"""
https://cses.fi/problemset/task/2205/
Bài toán yêu cầu in ra danh sách các bit string có n kí tự mà 2 chuỗi liền kề khác nhau 1 kí tự
Nhận xét: xét chuỗi số 1->2**n-1 theo dạng bit. 

0001
0010 -> 2 số liền kề chắc chắn có vị trí số 1 xuất hiện lần đầu khác nhau xét từ cuối lên
Nếu a,b có cùng vị trí số 1 đầu tiên từ cuối ngược lại thì nó cách nhau ít nhất 2 đơn vị
1101
1111 -> cách nhau 2 đơn vị (cùng số 1 ở index 3)
1110 -> cách nhau 1 đơn vị (khác số 1 ở index 2, 3)
Lợi dụng tính chất này, 1 vòng lặp từ 1->N. Thay đổi vị giá trị của string s tại vị trí số 1 đó
từ 0 -> 1 và ngược lại -> thỏa mãn tính chất khác nhau 1 kí tự. 
Do phân bố đều nên ko có 2 số nào lặp lại nhau khi biến đổi s
s = 0000.
i=1 = 0001 -> index 3 -> s[3] = 1-s[3] -> s = 0001
i=2 = 0010 -> index 2 -> s[2] = 1-s[2] -> s = 0011
.
.
i = 15 -> 
"""