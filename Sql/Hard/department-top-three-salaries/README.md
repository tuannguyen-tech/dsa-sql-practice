# 185. Department Top Three Salaries

🔗 **Link bài toán:** [LeetCode 185](https://leetcode.com/problems/department-top-three-salaries/description/)

## 📌 Độ khó & Tags

- **Độ khó:** Hard
- **Tags:** Database, Window Functions, DENSE_RANK, JOIN, CTE

---

## 📝 Mô tả đề bài

Cho hai bảng: `Employee` và `Department`.

### Bảng `Employee`

| Cột | Kiểu | Mô tả |
|---|---|---|
| `id` | int | Khóa chính |
| `name` | varchar | Tên nhân viên |
| `salary` | int | Mức lương |
| `departmentId` | int | ID phòng ban (khóa ngoại tham chiếu `Department.id`) |

### Bảng `Department`

| Cột | Kiểu | Mô tả |
|---|---|---|
| `id` | int | Khóa chính |
| `name` | varchar | Tên phòng ban |

### 🎯 Yêu cầu

Một **"high earner"** trong một phòng ban là nhân viên có mức lương thuộc **top 3 mức lương cao nhất** (không tính trùng lặp – **top 3 unique salaries**) của phòng ban đó.

Viết truy vấn SQL để tìm **tất cả nhân viên là high earner trong từng phòng ban**.

### 📤 Kết quả trả về

| Cột | Mô tả |
|---|---|
| `Department` | Tên phòng ban |
| `Employee` | Tên nhân viên |
| `Salary` | Mức lương |

> **Lưu ý về thứ tự:** Kết quả có thể trả về theo bất kỳ thứ tự nào.

---

## 🧠 Phân tích & Hướng tiếp cận

### 1. Điểm mấu chốt: "Top 3 salaries", không phải "Top 3 employees"

Đề bài nói rõ: **"top three unique salaries"** – tức là **3 mức lương cao nhất khác nhau**. Điều này dẫn đến hệ quả quan trọng:

> **Nếu có nhiều nhân viên cùng mức lương (ties), tất cả họ đều được đưa vào kết quả**, miễn là mức lương đó nằm trong top 3 mức lương cao nhất của phòng ban.

Ví dụ: Nếu mức lương cao thứ 2 trong phòng được hưởng bởi 2 nhân viên, cả 2 nhân viên đó đều xuất hiện trong kết quả. Kết quả có thể có **nhiều hơn 3 dòng** cho một phòng ban.[reference:0]

### 2. Vì sao phải dùng `DENSE_RANK()`?

Đây là **cốt lõi** của bài toán. Có ba hàm xếp hạng phổ biến trong SQL, nhưng chỉ có `DENSE_RANK()` xử lý đúng yêu cầu "top 3 unique salaries":

| Hàm | Cách xử lý khi có ties | Kết quả với bài toán này |
|---|---|---|
| `ROW_NUMBER()` | Gán số thứ tự **tùy ý** cho các hàng bằng nhau (không ổn định) | ❌ **Sai**: một nhân viên có cùng lương có thể bị loại oan |
| `RANK()` | Gán **cùng hạng** cho các hàng bằng nhau, nhưng **bỏ qua** hạng tiếp theo | ❌ **Sai**: nếu 2 người đồng hạng 2, hạng 3 bị bỏ qua → mất nhân viên lương cao thứ 3 |
| `DENSE_RANK()` | Gán **cùng hạng** cho các hàng bằng nhau, **không bỏ qua** hạng | ✅ **Đúng**: xử lý hoàn hảo ties và vẫn giữ đủ 3 mức lương |

**Ví dụ minh họa:**

Giả sử phòng IT có lương: `90000`, `85000`, `85000`, `70000`, `69000`.

| Salary | ROW_NUMBER | RANK | DENSE_RANK |
|---|---|---|---|
| 90000 | 1 | 1 | 1 |
| 85000 | 2 | 2 | 2 |
| 85000 | 3 | 2 | 2 |
| 70000 | 4 | 4 | 3 |
| 69000 | 5 | 5 | 4 |

- `ROW_NUMBER`: chỉ giữ 1 trong 2 nhân viên lương `85000` (sai).
- `RANK`: bỏ qua hạng 3, nhân viên lương `70000` bị loại oan (sai).
- `DENSE_RANK`: cả 2 nhân viên `85000` đều hạng 2, nhân viên `70000` hạng 3 → tất cả đều được giữ (đúng).[reference:1][reference:2]

### 3. Vì sao cần Subquery hoặc CTE?

Không thể viết trực tiếp `WHERE DENSE_RANK() OVER (...) <= 3`. Lý do:

> **Window functions không được phép xuất hiện trong mệnh đề `WHERE`** vì `WHERE` được đánh giá **trước khi** window function được tính toán.[reference:3]

Do đó, ta cần **vật chất hóa** (materialize) kết quả xếp hạng trong một subquery hoặc CTE, rồi mới lọc `rank <= 3` ở truy vấn bên ngoài.

### 4. Các bước giải quyết

1.  **Tạo CTE `ranked_salaries`:**
    - `JOIN` bảng `Employee` với `Department` để lấy tên phòng ban.
    - Tính `DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) AS rnk`.
    - `PARTITION BY departmentId` đảm bảo xếp hạng được **reset cho mỗi phòng ban**.
2.  **Lọc `rnk <= 3`** ở truy vấn bên ngoài CTE.
3.  **Chọn các cột** `Department`, `Employee`, `Salary`.

### 5. So sánh các cách tiếp cận

| Cách tiếp cận | Ưu điểm | Nhược điểm | Khuyến nghị |
|---|---|---|---|
| **`DENSE_RANK()` + CTE/subquery** | Ngắn gọn, hiệu quả `O(n log n)`, xử lý ties hoàn hảo | Cần hiểu window functions | ⭐ **Tối ưu nhất** |
| **Correlated Subquery** (đếm số lương cao hơn) | Không cần window functions (tương thích SQL cũ) | Chậm hơn `O(n²)` worst case, khó đọc | Ít tối ưu |
| **Self Join** | Trực quan | Rất chậm, không scalable | Không khuyến khích |

---

### Giải thích từng phần

| Phần | Ý nghĩa |
|---|---|
| `WITH ranked_salaries AS (...)` | CTE để tính hạng trước khi lọc (do window function không dùng được trong `WHERE`) |
| `DENSE_RANK() OVER (PARTITION BY e.departmentId ORDER BY e.salary DESC)` | Xếp hạng lương **trong từng phòng ban**, lương cao hơn hạng nhỏ hơn, **không nhảy hạng** khi có ties |
| `JOIN Department d ON e.departmentId = d.id` | Lấy tên phòng ban từ bảng `Department` |
| `WHERE rnk <= 3` | Chỉ giữ các nhân viên thuộc **top 3 mức lương** của phòng ban |

---

## ⏱️ Độ phức tạp

- **Thời gian:** `O(N log N)` – do bước sắp xếp bên trong window function (`ORDER BY salary DESC` trong mỗi partition).[reference:4]
- **Không gian:** `O(N)` – để lưu trữ kết quả xếp hạng trung gian trong CTE.

---

## 💡 Bài học rút ra

1.  **Phân biệt rõ `ROW_NUMBER()`, `RANK()`, và `DENSE_RANK()`** là kỹ năng sống còn khi giải các bài toán xếp hạng trong SQL. Bài toán này là ví dụ kinh điển cho thấy `DENSE_RANK()` là lựa chọn đúng đắn khi đề bài nói đến **"top N unique values"**.
2.  **Window functions không thể dùng trực tiếp trong `WHERE`** – luôn cần bọc trong subquery hoặc CTE.
3.  **`PARTITION BY`** rất quan trọng: nó đảm bảo phép tính được thực hiện **trong phạm vi từng nhóm** (ở đây là từng phòng ban), không phải toàn bảng.
4.  **Luôn đọc kỹ đề bài** để xác định xem yêu cầu là "top N **rows**" (dùng `ROW_NUMBER`) hay "top N **distinct values**" (dùng `DENSE_RANK`).
5.  **Kiểm tra với các edge case:**
    - Phòng ban chỉ có 1 hoặc 2 nhân viên → tất cả đều được trả về.
    - Nhiều nhân viên cùng lương ở vị trí thứ 3 → tất cả đều được trả về.
    - Phòng ban không có nhân viên nào → không xuất hiện trong kết quả.

---
