## Offline query

Verification:
* https://cses.fi/problemset/result/2787915/
* https://github.com/conlacda/algo/blob/master/range-queries/Distinct-value-queries.c%2B%2B  
2 link đều của cùng 1 bài (fallback)

Các ý chính của offline query:
* Không thể query theo l,r bất kỳ
* Sắp xếp toàn bộ query theo 1 thứ tự. Giả sử là sắp xếp theo r
* Duyệt mảng ban đầu theo thứ tự từ đầu tới cuối mảng [dòng này](https://github.com/conlacda/algo/blob/master/range-queries/Distinct-value-queries.c%2B%2B#L90). Đồng thời trong vòng lặp xử lý luôn query [dòng này](https://github.com/conlacda/algo/blob/master/range-queries/Distinct-value-queries.c%2B%2B#L102).   
Pseudo code 
```c++
for (int i=0;i<N;i++){
    if (a[i]...) update_range();
    if (query[0].r == i ... or some condition){
        cout << query_range();
        delete query[0];
    } 
}
Giải thích: duyệt từ đầu tới cuối mảng, cập nhật range. Nếu mà range tới vị trí query[0] thì sẽ xử lý query đó. rồi xóa query đó đi. Thao tác xóa có thể là cur_index=0. query_range(); cur_index++; Tăng index đang cần xử lý lên 1. vì thao tác xóa mảng là thao tác chậm chạp do dịch index. Thao khảo tại https://cses.fi/problemset/task/1749
```