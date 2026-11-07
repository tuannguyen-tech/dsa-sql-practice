# 569. Median Employee Salary

* **Link:** [LeetCode 569 – Median Employee Salary](https://leetcode.com/problems/median-employee-salary/?utm_source=chatgpt.com)
* **Độ khó:** Hard
* **Chủ đề:** Window Function, CTE, Median

---

## 1. Đề bài

Bảng `Employee` gồm các cột:

* `id`: Khóa chính.
* `company`: Tên công ty.
* `salary`: Mức lương của nhân viên.

Với mỗi công ty, tìm (các) dòng chứa mức lương trung vị.

Khi sắp xếp lương trong một công ty mà có giá trị trùng nhau, dùng `id` để phân định thứ tự.

Kết quả gồm các cột `id`, `company`, `salary`, thứ tự bất kỳ.

---

## 2. Cách tiếp cận

### Bước 1. Sắp xếp và đánh số thứ tự nhân viên theo mức lương

Để xác định vị trí trung vị, trước tiên cần sắp xếp nhân viên theo `salary` tăng dần trong từng công ty, sau đó đánh số thứ tự cho mỗi nhân viên.

Sử dụng `ROW_NUMBER()` kết hợp với `PARTITION BY company` và `ORDER BY salary ASC`:

```sql
ROW_NUMBER() OVER (
    PARTITION BY company
    ORDER BY salary ASC
) AS rn

```

Trong đó:

* `PARTITION BY company`: Chia nhân viên thành từng nhóm theo công ty.
* `ORDER BY salary ASC`: Sắp xếp mức lương tăng dần trong mỗi nhóm.
* `ROW_NUMBER()`: Đánh số thứ tự riêng biệt cho từng nhân viên, kể cả khi có cùng mức lương.

### Bước 2. Xác định tổng số nhân viên của mỗi công ty

Để tìm vị trí trung vị, cần biết tổng số nhân viên của từng công ty.

Sử dụng `COUNT(*) OVER (PARTITION BY company)`:

```sql
COUNT(*) OVER (
    PARTITION BY company
) AS total

```

* `COUNT(*)`: Đếm số lượng nhân viên.
* `PARTITION BY company`: Đếm riêng cho từng công ty mà không gộp các dòng dữ liệu.

### Bước 3. Xác định khoảng vị trí trung vị

* Nếu `N` là số lẻ: Vị trí trung vị nằm chính giữa (làm tròn lên từ phép chia `N / 2`).
* Nếu `N` là số chẵn: Trung vị nằm ở hai vị trí liền kề `N / 2` và `N / 2 + 1`.

**Vấn đề đặt ra:** Nếu `N` là số chẵn, làm thế nào để một câu lệnh SQL có thể lấy ra đồng thời cả hai vị trí này?

**Giải pháp:** Nếu xác định được một khoảng mà các vị trí cần tìm trong cả hai trường hợp chẵn và lẻ đều nằm gọn trong đó, bài toán sẽ được giải quyết bằng một phép lọc duy nhất.

### Phân tích khoảng vị trí cần tìm

Trước tiên, xét kết quả của phép chia `N / 2.0` trong hai trường hợp:

- **Với số lẻ (N = 5):**
  - Vị trí trung vị cần lấy là `x = 3`.
  - Phép chia cho kết quả: `5 / 2.0 = 2.5`.

- **Với số chẵn (N = 6):**
  - Hai vị trí trung vị cần lấy là `x = 3` và `x = 4`.
  - Phép chia cho kết quả: `6 / 2.0 = 3.0`.

### Xây dựng khoảng lọc chung

Từ hai trường hợp trên, ta nhận thấy:

- Với số chẵn, cần một khoảng chứa cả hai vị trí `3` và `4`.
- Với số lẻ, cần một khoảng chỉ chứa vị trí `3`.

**Vậy làm thế nào để xây dựng một khoảng duy nhất có thể đáp ứng đồng thời cả hai yêu cầu trên?**

Ta bắt đầu từ trường hợp số chẵn (`N = 6`) vì đây là trường hợp cần lấy hai vị trí liên tiếp:

1. Để chứa cả `3` và `4`, khoảng lọc phải là `[3.0, 4.0]`, tương ứng với `[N / 2.0, N / 2.0 + 1]`.
2. Áp dụng khoảng này cho trường hợp số lẻ (`N = 5`), ta được `[2.5, 3.5]`. Vì vị trí nhân viên luôn là số nguyên, vị trí duy nhất nằm trong khoảng này là `3`.

**Kết luận:** Khoảng `[N / 2.0, N / 2.0 + 1]` có thể xử lý đồng thời cả hai trường hợp chẵn và lẻ.

---

## 3. Ghi chú

1. **Bắt buộc chia cho số thực (`2.0` thay vì `2`)**
Trong PostgreSQL, phép chia giữa hai số nguyên sẽ tự động làm tròn xuống (ví dụ: `5 / 2 = 2`).
Do đó, bắt buộc phải viết `total_employee / 2.0` (hoặc ép kiểu `::numeric`) để ép hệ thống trả về số thực `2.5`, giúp khoảng lọc hoạt động chính xác cho trường hợp số lẻ.
2. **Xử lý trường hợp trùng mức lương**
Trong hàm `ROW_NUMBER()`, nếu hai nhân viên cùng công ty có mức lương bằng nhau, thứ tự xếp hạng giữa họ có thể bị xáo trộn ngẫu nhiên qua các lần chạy.
Việc bổ sung thêm cột `id` vào mệnh đề sắp xếp (`ORDER BY salary, id`) giúp đảm bảo tính nhất quán (deterministic) của dữ liệu.
3. **Bản chất của toán tử `BETWEEN` trong SQL**
Công thức này hoạt động được nhờ đặc tính lấy cả hai đầu mút (`>=` và `<=`) của mệnh đề `BETWEEN`.
