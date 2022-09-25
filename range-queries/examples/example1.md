# Query các số lớn hơn k trong array

## Vấn đề

Cho dãy [a1, a2, a3, ...., an]. Thực hiện 2 thao tác query
* Cập nhật giá trị ai
* Query xem có bao nhiêu số lớn hơn k trong dãy. (nhỏ hơn k làm tương tự)

## Giải quyết
Giả sử các số trong dãy có giá trị < 10^5.  
Dựng 1 `fenwicktree dạng range update, point query` trên a(10^5+5, 0);  
* Với mỗi phần tử ai, ta cập nhật range 1 lần. Cụ thể với ai, thực hiện `fw.update(left=ai, right=a.size(), 1)`. Khi này `fw.query(k)` chính là số giá trị lớn hơn hoặc bằng k trong dãy
* Thao tác cập nhật: ai = x. Thao tác cập nhật đơn giản chia làm 2 bước:  
    * Thao tác cập nhật xóa ai=k (giá trị cũ) đi. `fw.update(k, a.size(),-1)`
    * Thao tác cập nhật gán giá trị x mới vào `fw.update(x, a.size(), +1)`
* Xử lý phần các số trong dãy < 10^5. Dùng `compress coordinator` để chuyển giá trị lớn về 10^5

## Video hướng dẫn
https://github.com/conlacda/algo-video/blob/main/range-queries/examples/example1-query-less-than-k.mp4

## Các vấn đề đã giải
* https://codeforces.com/contest/432/submission/173385873 - bài này cũng hỏi rằng trên z-function với 1 số k thì có bao nhiêu số lớn hơn k trong dãy. Mình đã dùng fenwicktree để truy vấn

## Mở rộng vấn đề
Có 1 vấn đề khó hơn dạng có bao nhiêu số >=k trong range [l:r] chứ không phải trong toàn bộ dãy như này.