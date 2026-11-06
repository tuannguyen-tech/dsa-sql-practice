# 262. Trips and Users

🔗 **Link bài toán:** [LeetCode 262](https://leetcode.com/problems/trips-and-users/description/)

## 📌 Độ khó & Tags

- **Độ khó:** Hard
- **Tags:** Database, JOIN, Aggregation, Conditional Logic

---

## 📝 Mô tả đề bài

Cho hai bảng: `Trips` và `Users`.

### Bảng `Trips`

| Cột | Kiểu | Mô tả |
|---|---|---|
| `id` | int | Khóa chính |
| `client_id` | int | ID người dùng (client) đặt chuyến |
| `driver_id` | int | ID tài xế |
| `city_id` | int | ID thành phố |
| `status` | enum | Trạng thái: `completed`, `cancelled_by_driver`, `cancelled_by_client` |
| `request_at` | varchar | Ngày yêu cầu (định dạng `YYYY-MM-DD`) |

### Bảng `Users`

| Cột | Kiểu | Mô tả |
|---|---|---|
| `users_id` | int | Khóa chính |
| `banned` | enum | `Yes` hoặc `No` |
| `role` | enum | `client`, `driver`, `partner` |

### 🎯 Yêu cầu

Viết truy vấn SQL tính **tỷ lệ hủy chuyến** (`Cancellation Rate`) của các chuyến đi **mà cả client và driver đều không bị cấm** (`banned = 'No'`), trong khoảng thời gian từ **`2013-10-01`** đến **`2013-10-03`**.

**Công thức tính tỷ lệ hủy:**

```
Cancellation Rate = Số chuyến bị hủy (bởi client hoặc driver) / Tổng số chuyến
```

Chỉ xét các chuyến có **cả client và driver đều không bị banned**. Kết quả làm tròn đến **2 chữ số thập phân**.

### 📤 Kết quả trả về

| Cột | Mô tả |
|---|---|
| `Day` | Ngày (`request_at`) |
| `Cancellation Rate` | Tỷ lệ hủy (làm tròn 2 chữ số thập phân) |

> **Lưu ý:** Chỉ những ngày có **ít nhất một chuyến đi hợp lệ** mới xuất hiện trong kết quả. Thứ tự trả về không bắt buộc.

---

## 🧠 Phân tích & Hướng tiếp cận

### 1. Điểm mấu chốt của bài toán

Bài toán có hai yêu cầu lọc dữ liệu quan trọng:

1.  **Cả client và driver đều không bị banned.** Điều này có nghĩa là ta phải kiểm tra trạng thái `banned` của **hai người dùng khác nhau** trong cùng một chuyến đi: `client_id` và `driver_id`.
2.  **Chỉ xét các chuyến trong khoảng thời gian từ `2013-10-01` đến `2013-10-03`.**

### 2. Vì sao cần JOIN bảng `Users` hai lần?

Đây là **cốt lõi** của bài toán. Nếu chỉ JOIN `Users` một lần, ta chỉ có thể kiểm tra trạng thái banned của **một trong hai** người (client hoặc driver), không thể đảm bảo **cả hai** đều không bị cấm.

> 💡 **Cách hình dung:** Hãy tưởng tượng bạn là nhân viên kiểm soát cửa vào. Bạn cần kiểm tra **cả hai** người (client và driver) đều không nằm trong danh sách đen. Nếu chỉ kiểm tra một người, bạn không thể khẳng định "cả hai đều được phép".

Do đó, ta cần **JOIN bảng `Users` hai lần**:
- Lần 1: JOIN với `client_id` để lấy thông tin của client.
- Lần 2: JOIN với `driver_id` để lấy thông tin của driver.

Sau đó, áp dụng điều kiện `banned = 'No'` cho **cả hai** bảng `Users` đã JOIN.

### 3. Công thức tính `Cancellation Rate`

Tỷ lệ hủy được tính bằng:

```
SUM(CASE WHEN status IN ('cancelled_by_driver', 'cancelled_by_client') THEN 1 ELSE 0 END)
-----------------------------------------------------------------------------------------
                                    COUNT(*)
```

- **Tử số:** Đếm số chuyến bị hủy (bởi client hoặc driver).
- **Mẫu số:** Tổng số chuyến hợp lệ trong ngày.

Sử dụng `ROUND(..., 2)` để làm tròn đến 2 chữ số thập phân.

### 4. Các bước giải quyết

1.  **JOIN `Trips` với `Users` (lần 1)** để lấy thông tin client (`client_id = users_id`).
2.  **JOIN `Trips` với `Users` (lần 2)** để lấy thông tin driver (`driver_id = users_id`).
3.  **Lọc** các chuyến có `client.banned = 'No'` và `driver.banned = 'No'`.
4.  **Lọc** các chuyến trong khoảng `request_at BETWEEN '2013-10-01' AND '2013-10-03'`.
5.  **`GROUP BY request_at`** để nhóm theo ngày.
6.  **Tính `Cancellation Rate`** bằng `SUM(CASE...) / COUNT(*)`, làm tròn 2 chữ số.
7.  **Sắp xếp** (không bắt buộc, nhưng nên `ORDER BY Day` để kết quả nhất quán).

### 5. So sánh các cách tiếp cận

| Cách tiếp cận | Ưu điểm | Nhược điểm | Khuyến nghị |
|---|---|---|---|
| **JOIN `Users` hai lần** | Rõ ràng, dễ hiểu, kiểm tra độc lập cả hai người dùng | Cần viết JOIN hai lần | ⭐ **Tối ưu nhất** |
| **JOIN một lần với điều kiện `OR`** | Ngắn gọn hơn | Dễ sai logic, khó kiểm soát | Không khuyến khích |
| **Subquery cho mỗi người dùng** | Trực quan | Chậm hơn, khó đọc | Ít tối ưu |


### Giải thích từng phần

| Phần | Ý nghĩa |
|---|---|
| `JOIN Users client ON t.client_id = client.users_id` | Lấy thông tin của **client** cho mỗi chuyến |
| `JOIN Users driver ON t.driver_id = driver.users_id` | Lấy thông tin của **driver** cho mỗi chuyến |
| `WHERE client.banned = 'No' AND driver.banned = 'No'` | **Cả hai** đều không bị cấm |
| `BETWEEN '2013-10-01' AND '2013-10-03'` | Giới hạn khoảng thời gian |
| `SUM(CASE WHEN status IN (...) THEN 1 ELSE 0 END)` | Đếm số chuyến bị hủy |
| `COUNT(*)` | Tổng số chuyến hợp lệ trong ngày |
| `::numeric` | Ép kiểu để phép chia trả về số thực (PostgreSQL) |
| `ROUND(..., 2)` | Làm tròn 2 chữ số thập phân |
| `GROUP BY t.request_at` | Nhóm theo ngày |
| `ORDER BY t.request_at` | Sắp xếp theo ngày (tùy chọn, giúp kết quả nhất quán) |

---

## ⏱️ Độ phức tạp

- **Thời gian:** `O(N)` – quét bảng `Trips` một lần và thực hiện hai phép JOIN với `Users` cho mỗi dòng (với chỉ mục trên `users_id`, mỗi JOIN là `O(1)`).
- **Không gian:** `O(N)` – để lưu kết quả sau khi lọc và nhóm.

---

## 💡 Bài học rút ra

1.  **JOIN nhiều lần cùng một bảng** là kỹ thuật quan trọng khi cần so sánh hoặc kiểm tra nhiều **vai trò khác nhau** của cùng một thực thể (ở đây là client và driver).
2.  **Điều kiện `WHERE` trên bảng JOIN** cần được đặt đúng chỗ: nếu đặt trong `ON` của `LEFT JOIN` sẽ cho kết quả khác với `INNER JOIN` + `WHERE`.
3.  **`SUM(CASE WHEN ... THEN 1 ELSE 0 END)`** là pattern chuẩn để đếm có điều kiện trong SQL, linh hoạt hơn `COUNT(CASE WHEN ... THEN 1 END)` (vì `COUNT` bỏ qua `NULL`).
4.  **Ép kiểu `::numeric`** (PostgreSQL) hoặc `1.0 *` là cần thiết để tránh phép chia số nguyên trả về `0` thay vì số thập phân.
5.  **Luôn kiểm tra với các edge case:**
    - Ngày không có chuyến hợp lệ nào → không xuất hiện trong kết quả.
    - Tất cả chuyến đều bị hủy → `Cancellation Rate = 1.00`.
    - Không có chuyến nào bị hủy → `Cancellation Rate = 0.00`.

---
