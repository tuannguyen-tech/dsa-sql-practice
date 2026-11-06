# 571. Find Median Given Frequency of Numbers

🔗 **Link bài toán:** [LeetCode 571](https://leetcode.com/problems/find-median-given-frequency-of-numbers/description/)

## 📌 Độ khó & Tags

- **Độ khó:** Hard
- **Tags:** Database, Window Functions, Cumulative Sum, Median

---

## 📝 Mô tả đề bài

Cho bảng `Numbers` lưu giá trị của các số và tần suất xuất hiện của chúng:

| Cột | Kiểu | Mô tả |
|---|---|---|
| `num` | int | Giá trị số (khóa chính) |
| `frequency` | int | Số lần `num` xuất hiện trong cơ sở dữ liệu |

### 🎯 Yêu cầu

Viết truy vấn SQL để tính **trung vị** (median) của tất cả các số sau khi **"giải nén"** bảng `Numbers` (tức là mở rộng mỗi số `num` thành `frequency` lần xuất hiện).

Kết quả trả về một cột duy nhất có tên **`median`**, làm tròn đến **1 chữ số thập phân**.

### 📊 Ví dụ

**Input:**

| num | frequency |
|---|---|
| 0 | 7 |
| 1 | 1 |
| 2 | 3 |
| 3 | 1 |

**Output:**

| median |
|---|
| 0.0 |

**Giải thích:** Nếu giải nén bảng, ta được dãy: `[0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 3]`. Dãy có 12 phần tử (số chẵn), hai vị trí giữa là vị trí thứ 6 và 7, đều là số `0`. Trung vị = `(0 + 0) / 2 = 0.0`.

---

## 🧠 Phân tích & Hướng tiếp cận

### 1. Vì sao không nên "giải nén" bảng?

Cách trực quan nhất là **mở rộng bảng** (mỗi `num` lặp lại `frequency` lần) rồi tính trung vị trên dãy mới. Tuy nhiên, cách này có **hai nhược điểm nghiêm trọng**:

| Vấn đề | Hệ quả |
|---|---|
| **Bùng nổ dữ liệu** | Nếu `frequency` lớn (ví dụ 1 triệu), bảng tạm sẽ có hàng triệu dòng, tốn bộ nhớ và thời gian xử lý. |
| **Không tận dụng được bản chất** | Bảng gốc đã chứa đủ thông tin để xác định trung vị mà không cần mở rộng. |

> 💡 **Nguồn tham khảo:** Phân tích từ sergiorgiraldo nhấn mạnh: *"Why not expand the data? Expanding frequency=1M rows for a single number wastes memory. Instead, use cumulative frequency to find the median position without expansion."*[reference:0]

### 2. Ý tưởng cốt lõi: Tần suất tích lũy (Cumulative Frequency)

Thay vì mở rộng dữ liệu, ta tận dụng **tần suất tích lũy** để xác định **vị trí** của trung vị trong dãy "tưởng tượng".

#### Khái niệm "vị trí" và "quyền sở hữu"

Giả sử tổng số phần tử sau khi giải nén là `T = SUM(frequency)`. Ta tưởng tượng một dãy gồm `T` phần tử đã được sắp xếp tăng dần. Mỗi số `num` sẽ **"sở hữu"** một khoảng vị trí liên tiếp trong dãy này:

- Số `num` đầu tiên sở hữu các vị trí từ `1` đến `frequency` của nó.
- Số `num` tiếp theo sở hữu các vị trí tiếp theo, v.v.

**Ví dụ với bảng đã cho:** `T = 7 + 1 + 3 + 1 = 12`.

| num | frequency | Tần suất tích lũy (cum_freq) | Khoảng vị trí sở hữu |
|---|---|---|---|
| 0 | 7 | 7 | 1 – 7 |
| 1 | 1 | 8 | 8 – 8 |
| 2 | 3 | 11 | 9 – 11 |
| 3 | 1 | 12 | 12 – 12 |

> **Công thức tổng quát:** Với một hàng có `cum_freq` là tần suất tích lũy đến hết hàng đó, số `num` trong hàng **sở hữu các vị trí** từ `(cum_freq - frequency + 1)` đến `cum_freq`.[reference:1]

#### Xác định vị trí trung vị

Trung vị nằm ở **vị trí giữa** của dãy `T` phần tử:

- Nếu `T` **lẻ**: trung vị là giá trị tại vị trí `(T + 1) / 2`.
- Nếu `T` **chẵn**: trung vị là **trung bình cộng** của hai giá trị tại vị trí `T / 2` và `T / 2 + 1`.

> **Quan trọng:** Với `T` chẵn, hai vị trí giữa có thể **thuộc về hai số khác nhau** hoặc **cùng một số**. Nếu cùng một số, trung vị chính là số đó. Nếu khác số, ta lấy trung bình cộng của hai số đó.

### 3. Cách xác định số nào "chứa" vị trí trung vị

Một số `num` được chọn nếu **khoảng vị trí** mà nó sở hữu **bao phủ** vị trí trung vị (hoặc một trong hai vị trí trung vị).

Cụ thể, với mỗi hàng, ta kiểm tra:

- **Vị trí bắt đầu** của khoảng = `cum_freq - frequency + 1`.
- **Vị trí kết thúc** của khoảng = `cum_freq`.

Hàng đó "chứa" vị trí `P` nếu: `cum_freq - frequency < P <= cum_freq`.

Để xử lý **cả trường hợp lẻ và chẵn một cách thống nhất**, ta có thể xác định **cận dưới** (`lower_pos`) và **cận trên** (`upper_pos`) của vị trí trung vị:

- **`lower_pos = FLOOR((T + 1) / 2)`**
- **`upper_pos = CEIL((T + 1) / 2)`**

> **Tại sao dùng `(T + 1) / 2`?**
> - Với `T` lẻ: `(T + 1) / 2` là một số nguyên, `FLOOR` = `CEIL` = vị trí giữa duy nhất.
> - Với `T` chẵn: `(T + 1) / 2` là `.5`, `FLOOR` cho vị trí `T/2`, `CEIL` cho vị trí `T/2 + 1`. Đây chính là hai vị trí giữa cần lấy trung bình.

Sau đó, ta lọc các hàng có khoảng vị trí **giao với** đoạn `[lower_pos, upper_pos]`. Điều kiện chính xác là:

```
cum_freq >= lower_pos   AND   (cum_freq - frequency) < upper_pos
```

> **Giải thích:** `cum_freq >= lower_pos` đảm bảo hàng kết thúc tại hoặc sau vị trí trung vị dưới. `(cum_freq - frequency) < upper_pos` đảm bảo hàng bắt đầu trước vị trí trung vị trên.[reference:2]

### 4. Các bước giải quyết

1.  **Tính tần suất tích lũy** (`cum_freq`) bằng `SUM(frequency) OVER (ORDER BY num)`.
2.  **Tính tổng tần suất** (`total`) bằng `SUM(frequency) OVER ()`.
3.  **Xác định `lower_pos` và `upper_pos`** từ `total`.
4.  **Lọc** các hàng thỏa mãn điều kiện bao phủ vị trí trung vị.
5.  **Tính `AVG(num)`** trên các hàng được lọc (nếu có 2 hàng, `AVG` sẽ tính trung bình cộng; nếu 1 hàng, `AVG` trả về chính giá trị đó).
6.  **Làm tròn** đến 1 chữ số thập phân bằng `ROUND(..., 1)`.

### 5. So sánh các cách tiếp cận

| Cách tiếp cận | Ưu điểm | Nhược điểm | Khuyến nghị |
|---|---|---|---|
| **Cumulative Frequency + Window Functions** | Không mở rộng dữ liệu, hiệu quả `O(N log N)`, xử lý tốt mọi kích thước `frequency` | Cần hiểu logic vị trí | ⭐ **Tối ưu nhất** |
| **Recursive CTE (giải nén)** | Trực quan, dễ hiểu | Bùng nổ dữ liệu, chậm với `frequency` lớn, có thể gây tràn bộ nhớ | Chỉ dùng cho mục đích học tập |

---

## 💻 Code SQL (PostgreSQL)

```sql
WITH freq AS (
    SELECT
        num,
        frequency,
        SUM(frequency) OVER (ORDER BY num) AS cum_freq,
        SUM(frequency) OVER () AS total
    FROM Numbers
),
positions AS (
    SELECT
        num,
        cum_freq,
        frequency,
        FLOOR((total + 1) / 2.0) AS lower_pos,
        CEIL((total + 1) / 2.0)  AS upper_pos
    FROM freq
)
SELECT
    ROUND(AVG(num), 1) AS median
FROM positions
WHERE cum_freq >= lower_pos
  AND (cum_freq - frequency) < upper_pos;
```

### Giải thích từng phần

| Phần | Ý nghĩa |
|---|---|
| `SUM(frequency) OVER (ORDER BY num) AS cum_freq` | Tần suất tích lũy đến hết hàng hiện tại (theo thứ tự `num` tăng dần) |
| `SUM(frequency) OVER () AS total` | Tổng số phần tử sau khi giải nén |
| `FLOOR((total + 1) / 2.0)` | Vị trí trung vị dưới (dùng `2.0` để tránh chia số nguyên) |
| `CEIL((total + 1) / 2.0)` | Vị trí trung vị trên |
| `cum_freq >= lower_pos` | Hàng kết thúc tại hoặc sau vị trí trung vị dưới |
| `(cum_freq - frequency) < upper_pos` | Hàng bắt đầu trước vị trí trung vị trên |
| `AVG(num)` | Trung bình cộng các `num` được chọn (1 hoặc 2 giá trị) |
| `ROUND(..., 1)` | Làm tròn 1 chữ số thập phân |

---

## ⏱️ Độ phức tạp

- **Thời gian:** `O(N log N)` – do bước sắp xếp trong `ORDER BY num` của window function.
- **Không gian:** `O(N)` – lưu trữ kết quả trung gian trong CTE.

---

## 💡 Bài học rút ra

1.  **Không phải lúc nào cũng cần "vật chất hóa" dữ liệu**: Bài toán này là ví dụ kinh điển cho thấy có thể giải quyết vấn đề **mà không cần mở rộng** dữ liệu, bằng cách tận dụng **tần suất tích lũy**.
2.  **Tần suất tích lũy** (`SUM() OVER (ORDER BY ...)`) là kỹ thuật mạnh mẽ để xử lý dữ liệu dạng tần suất, thường xuất hiện trong các bài toán thống kê.
3.  **Xác định vị trí trung vị** cần xử lý **cả trường hợp lẻ và chẵn**. Công thức `FLOOR/CEIL((total + 1) / 2.0)` giúp thống nhất logic.
4.  **Điều kiện `cum_freq >= lower_pos AND (cum_freq - frequency) < upper_pos`** là chìa khóa để xác định đúng số nào "chứa" vị trí trung vị, kể cả khi hai vị trí giữa thuộc hai số khác nhau.
5.  **Luôn kiểm tra với các edge case:**
    - `T` lẻ (trung vị là 1 số).
    - `T` chẵn và hai vị trí giữa thuộc **cùng một số** (ví dụ: `[0,0,0,0]` → trung vị `0`).
    - `T` chẵn và hai vị trí giữa thuộc **hai số khác nhau** (ví dụ: `[0,1]` → trung vị `0.5`).
    - Bảng chỉ có **một hàng**.

---

