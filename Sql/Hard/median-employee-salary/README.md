# 569. Median Employee Salary

- Link: [LeetCode 569 – Median Employee Salary](https://leetcode.com/problems/median-employee-salary/?utm_source=chatgpt.com)
- Độ khó: Hard
- Chủ đề: Window Function, CTE, Median

## 1. Đề bài

Bảng `Employee` gồm các cột:

- `id`: Khóa chính.
- `company`: Tên công ty.
- `salary`: Mức lương của nhân viên.

Với mỗi công ty, tìm (các) dòng chứa mức lương trung vị.

Khi sắp xếp lương trong một công ty mà có giá trị trùng nhau, dùng `id` để phân định thứ tự.

Kết quả gồm các cột `id`, `company`, `salary`, thứ tự bất kỳ.

## 2. Cách tiếp cận

Bước 1. Sắp xếp danh sách nhân viên theo mức lương

Để tìm trung vị, trước tiên danh sách nhân viên cần được sắp xếp theo mức lương tăng dần.

Vì vậy, tôi sử dụng Window Function để sắp xếp nhân viên trong từng công ty theo `salary`.

Bước 2. Đánh số thứ tự cho từng nhân viên

Tôi chọn `ROW_NUMBER()` để đánh số thứ tự vì bài toán không quan trọng việc các nhân viên có mức lương trùng nhau hay không.

Bước 3. Xác định tổng số nhân viên của mỗi công ty

Tiếp theo, tôi cần biết mỗi công ty có tổng cộng bao nhiêu nhân viên để phục vụ cho việc xác định vị trí trung vị:

- Nếu `N` là số lẻ: Vị trí trung vị nằm chính giữa (làm tròn lên từ phép chia `N / 2`).
- Nếu `N` là số chẵn: Trung vị nằm ở hai vị trí liền kề `N / 2` và `N / 2 + 1`.

Vấn đề đặt ra: Nếu `N` là số chẵn, làm thế nào để một câu lệnh SQL có thể lấy ra đồng thời cả hai vị trí này?

Giải pháp: Nếu xác định được một khoảng mà các vị trí cần tìm trong cả hai trường hợp chẵn và lẻ đều nằm gọn trong đó, bài toán sẽ được giải quyết bằng một phép lọc duy nhất.

### Phân tích khoảng vị trí cần tìm

\- Với số lẻ (N = 5):

Vị trí cần lấy là `x = 3`.

&#x20; Trong khi đó, phép chia cho kết quả:

`5 / 2.0 = 2.5`

\- Với số chẵn (N = 6):

Hai vị trí cần lấy là `x = 3` và `x = 4`.

&#x20; Trong khi đó, phép chia tham chiếu cho kết quả:

`6 / 2.0 = 3.0`

Quan sát các con số trên trục số thực, ta thấy:

- Để ôm trọn cả `3` và `4` (khi N = 6), khoảng lọc bắt buộc phải trải dài từ `[3.0, 4.0]`, tức là từ `[N / 2.0, N / 2.0 + 1]`.
- Áp dụng thử khoảng này cho số lẻ (N = 5), ta được đoạn từ `[2.5, 3.5]`. Vì vị trí nhân viên luôn là số nguyên, số duy nhất lọt vào đoạn này chính là `3`.

Kết luận: Khoảng từ `[N / 2.0, N / 2.0 + 1]` chính là lưới lọc chung giải quyết triệt để cả hai trường hợp chẵn và lẻ.

## 3. Ghi chú

1\. Bắt buộc chia cho số thực (`2.0` thay vì `2`)

Trong PostgreSQL, phép chia giữa hai số nguyên sẽ tự động làm tròn xuống (ví dụ: `5 / 2 = 2`).

Do đó, bắt buộc phải viết `total_employee / 2.0` (hoặc ép kiểu `::numeric`) để ép hệ thống trả về số thực `2.5`, giúp khoảng lọc hoạt động chính xác cho trường hợp số lẻ.

2\. Xử lý trường hợp trùng mức lương

Trong hàm `ROW_NUMBER()`, nếu hai nhân viên cùng công ty có mức lương bằng nhau, thứ tự xếp hạng giữa họ có thể bị xáo trộn ngẫu nhiên qua các lần chạy.

Việc bổ sung thêm cột `id` vào mệnh đề sắp xếp (`ORDER BY salary, id`) giúp đảm bảo tính nhất quán (deterministic) của dữ liệu.

3\. Bản chất của toán tử `BETWEEN` trong SQL

Công thức này hoạt động được nhờ đặc tính lấy cả hai đầu mút (`>=` và `<=`) của mệnh đề `BETWEEN`.
