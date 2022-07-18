# Đồ thị vô hướng không trọng số# TODO
# Đồ thị có hướng
# Vô hướng có trọng số
# Đồ thị có hướng có trọng số
# Viết gộp chung tất cả vào 1 rồi khi tới cái nào xóa cái đó đi
# DFS
# BFS
# Kiểm tra đồ thị có cycle không https://www.geeksforgeeks.org/detect-cycle-undirected-graph/
    * Ý tưởng: duyệt DFS(). Nếu 1 đỉnh có đỉnh kể đã được duyệt nhưng lại không có quan hệ parent thì 2 điểm đó thuộc 1 cycle
    Bởi vì: 1 đỉnh đó được duyệt từ 2 đỉnh khác nhau. Nếu ko có cycle thì 2 đỉnh đó thuộc 2 nhánh khác nhau