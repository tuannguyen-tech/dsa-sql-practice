# 601. Human Traffic of Stadium

🔗 **Link bài toán:** [LeetCode 601](https://leetcode.com/problems/human-traffic-of-stadium/description/)

## 📌 Độ khó & Tags

- **Độ khó:** Hard
- **Tags:** Database, Window Functions, Gaps and Islands, ROW_NUMBER()

---

## 📝 Mô tả đề bài

Cho bảng `Stadium` ghi lại thông tin người đến sân vận động hàng ngày:

| Cột | Kiểu | Mô tả |
|---|---|---|
| `id` | int | Khóa chính, ID duy nhất cho mỗi ngày |
| `visit_date` | date | Ngày có người đến |
| `people` | int | Số lượng người đến sân |

### 🎯 Yêu cầu

Viết truy vấn SQL để tìm **tất cả các bản ghi thuộc về một chuỗi ít nhất 3 ngày liên tiếp** mà tại mỗi ngày, số lượng người (`people`) **lớn hơn hoặc bằng 100**.

**Điều kiện cụ thể:**

1.  Các bản ghi được chọn phải có **ID liên tiếp nhau** (tức là `id` tăng dần không bị ngắt quãng bởi một ngày có `people < 100`).
2.  Mỗi bản ghi trong chuỗi phải có `people >= 100`.
3.  Chuỗi phải có **độ dài tối thiểu là 3**.

**Kết quả trả về:**

| Cột | Mô tả |
|---|---|
| `id` | ID của ngày |
| `visit_date` | Ngày |
| `people` | Số lượng người |

**Thứ tự sắp xếp:** `visit_date` **tăng dần**.

---

## 🧠 Phân tích & Hướng tiếp cận

### 1. Bản chất bài toán: "Gaps and Islands"

Đây là một bài toán kinh điển thuộc dạng **"Gaps and Islands"** (khoảng trống và hòn đảo) trong SQL:
- **Island (hòn đảo):** Một tập hợp các bản ghi **liên tiếp nhau** thỏa mãn một điều kiện nào đó.
- **Gap (khoảng trống):** Các bản ghi **không thỏa mãn** điều kiện, làm ngắt chuỗi liên tiếp.

Bài toán yêu cầu tìm các "hòn đảo" có kích thước **≥ 3**. Khó khăn chính là làm sao **nhóm các bản ghi liên tiếp lại với nhau** mà không cần vòng lặp.

### 2. Giải pháp tối ưu: Kỹ thuật `id - ROW_NUMBER()`

Đây là kỹ thuật mạnh mẽ và phổ biến nhất để giải các bài toán "Gaps and Islands".

#### Ý tưởng cốt lõi

Nếu ta lọc ra các bản ghi có `people >= 100`, sau đó **đánh số thứ tự** (`ROW_NUMBER()`) cho chúng theo `id` tăng dần, thì:

> **Hiệu số giữa `id` và `ROW_NUMBER()` sẽ không đổi** đối với các bản ghi **liên tiếp nhau**.

#### Ví dụ minh họa

Giả sử sau khi lọc (`people >= 100`), ta có bảng tạm:

| id | people | ROW_NUMBER() | id - ROW_NUMBER() |
|---|---|---|---|
| 2 | 109 | 1 | **1** |
| 3 | 150 | 2 | **1** |
| 5 | 145 | 3 | **2** |
| 6 | 1455 | 4 | **2** |
| 7 | 199 | 5 | **2** |
| 8 | 188 | 6 | **2** |

**Quan sát:**
- Các `id` **2, 3** có cùng hiệu số `1` → tạo thành nhóm 1 (2 phần tử, **không đủ** 3 → loại).
- Các `id` **5, 6, 7, 8** có cùng hiệu số `2` → tạo thành nhóm 2 (4 phần tử, **đủ** ≥ 3 → giữ lại).

> 💡 **Tại sao id = 4 bị loại?** Vì ngày `id = 4` có `people = 99 < 100`, nên nó không nằm trong tập lọc. Điều này làm cho `ROW_NUMBER` bị "nhảy" và tạo ra một nhóm mới.

#### Tại sao kỹ thuật này hoạt động?

- `id` là một dãy số **tăng dần** (có thể không liên tục do có ngày bị loại).
- `ROW_NUMBER()` là một dãy số **tăng dần liên tục** (1, 2, 3, ...) trên tập dữ liệu đã lọc.
- Nếu các `id` **liên tiếp nhau**, thì hiệu `id - ROW_NUMBER()` **không đổi**.
- Khi có một "khoảng trống" (một `id` bị loại), hiệu này **thay đổi**, đánh dấu sự bắt đầu của một nhóm mới.

### 3. Các bước giải quyết

Giải pháp sử dụng **CTE (Common Table Expression)** để chia bài toán thành các bước rõ ràng:

#### Bước 1: Lọc và gán nhóm (`reduced_rows`)

- Lọc các bản ghi có `people >= 100`.
- Tính `id - ROW_NUMBER() OVER (ORDER BY id) AS grp` để gán **cùng một giá trị `grp`** cho các bản ghi liên tiếp.

#### Bước 2: Tìm các nhóm hợp lệ

- `GROUP BY grp` và `HAVING COUNT(*) >= 3` để chỉ giữ lại các nhóm có **ít nhất 3 bản ghi**.

#### Bước 3: Lấy lại toàn bộ bản ghi thuộc nhóm hợp lệ

- Join hoặc dùng `WHERE grp IN (...)` để lấy tất cả các bản ghi gốc thuộc nhóm hợp lệ.

#### Bước 4: Sắp xếp

- `ORDER BY visit_date ASC` theo yêu cầu.

### 4. So sánh các cách tiếp cận

| Cách tiếp cận | Ưu điểm | Nhược điểm | Khuyến nghị |
|---|---|---|---|
| **`id - ROW_NUMBER()`** | Ngắn gọn, hiệu quả `O(n)`, xử lý tốt chuỗi dài | Cần hiểu trick toán học | ⭐ **Tối ưu nhất** |
| **`LAG`/`LEAD`** | Trực quan, dễ hiểu | Nhiều điều kiện, khó mở rộng cho chuỗi dài | Tốt nhưng dài dòng |
| **Self Join** | Không cần window functions | `O(n²)` worst case, không scalable | Ít tối ưu |

---
### Giải thích từng phần

| Phần | Ý nghĩa |
|---|---|
| `WHERE people >= 100` | Chỉ giữ lại các ngày có ít nhất 100 người |
| `id - ROW_NUMBER() OVER (ORDER BY id)` | Tạo **group identifier** cho các chuỗi liên tiếp |
| `GROUP BY grp HAVING COUNT(*) >= 3` | Chỉ chọn các nhóm có từ 3 bản ghi trở lên |
| `WHERE grp IN (...)` | Lấy lại tất cả bản ghi thuộc nhóm hợp lệ |
| `ORDER BY visit_date ASC` | Sắp xếp theo ngày tăng dần |

---

## ⏱️ Độ phức tạp

- **Thời gian:** `O(n log n)` – chủ yếu do bước `ORDER BY` khi tính `ROW_NUMBER()`. Các bước còn lại là `O(n)`.
- **Không gian:** `O(n)` – để lưu trữ CTE `reduced_rows`.

---

## 💡 Bài học rút ra

1.  **Kỹ thuật `id - ROW_NUMBER()`** là "vũ khí" kinh điển cho mọi bài toán **"Gaps and Islands"** – không chỉ riêng bài này mà còn áp dụng cho nhiều bài toán tương tự (ví dụ: tìm chuỗi ngày mưa liên tiếp, chuỗi giao dịch liên tiếp, ...).
2.  **Hiểu bản chất toán học** đằng sau kỹ thuật: khi hai dãy số cùng tăng với bước nhảy 1, hiệu của chúng sẽ không đổi nếu không có "khoảng trống".
3.  **CTE giúp code rõ ràng**: chia bài toán thành các bước nhỏ (lọc → gán nhóm → lọc nhóm → lấy kết quả) giúp dễ đọc và dễ bảo trì hơn so với việc viết một câu truy vấn phức tạp.
4.  **`HAVING COUNT(*) >= 3`** là cách tự nhiên để lọc các nhóm có kích thước tối thiểu.
5.  **Luôn kiểm tra với các edge case:**
    - Không có ngày nào đạt `people >= 100` → kết quả rỗng.
    - Đúng 3 ngày liên tiếp → trả về cả 3.
    - Nhiều chuỗi riêng biệt → trả về tất cả các chuỗi hợp lệ.
    - Tất cả các ngày đều đạt → trả về toàn bộ bảng.

---