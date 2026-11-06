# 569. Median Employee Salary

🔗 **Link bài toán:** [LeetCode 569](https://leetcode.com/problems/median-employee-salary/description/)

## 📌 Độ khó & Tags

- **Độ khó:** Hard
- **Tags:** Database, Window Functions, ROW_NUMBER, CTE

---

## 📝 Mô tả đề bài

Cho bảng `Employee` chứa thông tin nhân viên của nhiều công ty:

| Cột | Kiểu | Mô tả |
|---|---|---|
| `id` | int | Khóa chính |
| `company` | varchar | Tên công ty |
| `salary` | int | Mức lương |

### 🎯 Yêu cầu

Viết truy vấn SQL để tìm **các dòng chứa mức lương trung vị** (median salary) của **từng công ty**.

> **Quy tắc quan trọng:** Khi tính trung vị, nếu các mức lương bị trùng (ties), hãy **phá vỡ ties bằng `id`**. Điều này có nghĩa là thứ tự sắp xếp phải là `(salary, id)`.

### 📤 Kết quả trả về

| Cột | Mô tả |
|---|---|
| `id` | ID nhân viên |
| `company` | Tên công ty |
| `salary` | Mức lương |

**Thứ tự:** Kết quả có thể trả về theo **bất kỳ thứ tự nào** (any order).

### 📊 Ví dụ

**Input:**

| id | company | salary |
|---|---|---|
| 1 | A | 2341 |
| 2 | A | 341 |
| 3 | A | 15 |
| 4 | A | 15314 |
| 5 | A | 451 |
| 6 | A | 513 |
| 7 | B | 15 |
| 8 | B | 13 |
| 9 | B | 1154 |
| 10 | B | 1345 |
| 11 | B | 1221 |
| 12 | B | 234 |
| 13 | C | 2345 |
| 14 | C | 2645 |
| 15 | C | 2645 |
| 16 | C | 2652 |
| 17 | C | 65 |

**Output:**

| id | company | salary |
|---|---|---|
| 5 | A | 451 |
| 6 | A | 513 |
| 12 | B | 234 |
| 9 | B | 1154 |
| 14 | C | 2645 |

**Giải thích:**

- **Công ty A** có 6 nhân viên (số chẵn). Sau khi sắp xếp theo `(salary, id)`: `15, 341, 451, 513, 2341, 15314`. Hai vị trí giữa là **451** (id=5) và **513** (id=6). Cả hai đều được trả về.
- **Công ty B** có 6 nhân viên (số chẵn). Sắp xếp: `13, 15, 234, 1154, 1221, 1345`. Hai vị trí giữa là **234** (id=12) và **1154** (id=9). Cả hai đều được trả về.
- **Công ty C** có 5 nhân viên (số lẻ). Sắp xếp: `65, 2345, 2645, 2645, 2652`. Vị trí giữa là **2645**. Có **hai nhân viên** cùng mức lương 2645 (id=14 và id=15), nhưng chỉ có **một vị trí trung vị**. Theo quy tắc phá ties bằng `id`, nhân viên có `id` nhỏ hơn (id=14) đứng ở vị trí trung vị. Kết quả chỉ trả về **id=14** cho công ty C.

---

## 🧠 Phân tích & Hướng tiếp cận

### 1. Bài toán trung vị trong SQL có gì đặc biệt?

Trung vị (median) là giá trị nằm ở **giữa** của một tập dữ liệu đã sắp xếp:
- Nếu số phần tử **lẻ**: trung vị là phần tử ở vị trí `(n+1)/2`.
- Nếu số phần tử **chẵn**: trung vị thường là **trung bình cộng** của hai phần tử ở vị trí `n/2` và `n/2 + 1`.

Tuy nhiên, **bài toán này không yêu cầu tính giá trị trung bình**. Thay vào đó, nó yêu cầu **trả về các dòng (rows) chứa mức lương trung vị**. Đây là điểm khác biệt cốt lõi:
- Với số phần tử **lẻ**: trả về **1 dòng** (vị trí giữa).
- Với số phần tử **chẵn**: trả về **2 dòng** (hai vị trí giữa).
- **Không tính trung bình cộng** – mỗi dòng giữ nguyên `id`, `company`, `salary` gốc.

### 2. Vì sao phải "phá ties bằng `id`"?

Đề bài nói rõ: *"when you sort the salaries of the company, break the ties by `id`"*.

Điều này rất quan trọng vì:
- Nếu hai nhân viên có **cùng mức lương**, thứ tự của họ trong bảng sắp xếp là **không xác định** nếu chỉ `ORDER BY salary`.
- Việc thêm `id` vào `ORDER BY` đảm bảo **thứ tự nhất quán** và **duy nhất** cho mỗi dòng, giúp xác định chính xác vị trí trung vị.

**Ví dụ với công ty C:** có hai nhân viên cùng lương `2645` (id=14 và id=15). Nếu không phá ties bằng `id`, cả hai có thể được coi là "trung vị" hoặc không ai cả, tùy vào cách viết truy vấn. Với `ORDER BY salary, id`, nhân viên id=14 đứng trước id=15, và vị trí giữa (vị trí thứ 3 trong 5 phần tử) thuộc về id=14.

### 3. Hướng tiếp cận: Window Functions

Có nhiều cách để xác định vị trí trung vị trong SQL, nhưng **Window Functions** là cách gọn gàng và hiệu quả nhất.

#### Ý tưởng cốt lõi

1.  **Đánh số thứ tự** (`ROW_NUMBER()`) cho các dòng trong mỗi công ty, sắp xếp theo `(salary, id)`.
2.  **Đếm tổng số nhân viên** (`COUNT(*) OVER`) trong mỗi công ty.
3.  **Xác định (các) vị trí trung vị** dựa trên tổng số nhân viên:
    - Nếu `n` lẻ: vị trí `(n+1)/2`.
    - Nếu `n` chẵn: vị trí `n/2` và `n/2 + 1`.
4.  **Lọc** các dòng có `rn` (số thứ tự) bằng với (các) vị trí trung vị.

### 4. Các bước giải quyết chi tiết

#### Bước 1: Tạo CTE `ranked`

```sql
WITH ranked AS (
    SELECT
        id,
        company,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY company
            ORDER BY salary, id
        ) AS rn,
        COUNT(*) OVER (PARTITION BY company) AS cnt
    FROM Employee
)
```

- `PARTITION BY company`: chia dữ liệu theo từng công ty.
- `ORDER BY salary, id`: sắp xếp lương tăng dần, phá ties bằng `id`.
- `rn`: số thứ tự của từng nhân viên **trong công ty của họ**.
- `cnt`: tổng số nhân viên trong công ty.

#### Bước 2: Lọc các dòng trung vị

```sql
SELECT id, company, salary
FROM ranked
WHERE
    -- Trường hợp lẻ: lấy đúng 1 vị trí giữa
    (cnt % 2 = 1 AND rn = (cnt + 1) / 2)
    OR
    -- Trường hợp chẵn: lấy 2 vị trí giữa
    (cnt % 2 = 0 AND rn IN (cnt / 2, cnt / 2 + 1))
ORDER BY company, salary;
```

- Với `cnt` lẻ: chỉ có `rn = (cnt + 1) / 2` thỏa mãn.
- Với `cnt` chẵn: cả `rn = cnt / 2` và `rn = cnt / 2 + 1` đều thỏa mãn.

### 5. So sánh các cách tiếp cận

| Cách tiếp cận | Ưu điểm | Nhược điểm | Khuyến nghị |
|---|---|---|---|
| **`ROW_NUMBER()` + `COUNT()`** (đề xuất) | Ngắn gọn, dễ hiểu, xử lý ties chính xác nhờ `ORDER BY salary, id` | Cần hiểu window functions | ⭐ **Tối ưu nhất** |
| **`ROW_NUMBER()` ASC + DESC** | Không cần `COUNT()` | Khó xử lý ties, dễ sai với số chẵn/lẻ | Không khuyến khích |
| **Self Join / Correlated Subquery** | Không cần window functions | Chậm `O(n²)`, dài dòng | Ít tối ưu |

---

## 💻 Code SQL (PostgreSQL)

```sql
WITH ranked AS (
    SELECT
        id,
        company,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY company
            ORDER BY salary, id
        ) AS rn,
        COUNT(*) OVER (PARTITION BY company) AS cnt
    FROM Employee
)
SELECT
    id,
    company,
    salary
FROM ranked
WHERE
    (cnt % 2 = 1 AND rn = (cnt + 1) / 2)
    OR
    (cnt % 2 = 0 AND rn IN (cnt / 2, cnt / 2 + 1))
ORDER BY company, salary;
```

### Giải thích từng phần

| Phần | Ý nghĩa |
|---|---|
| `ROW_NUMBER() OVER (PARTITION BY company ORDER BY salary, id)` | Đánh số thứ tự trong từng công ty, sắp xếp theo lương và `id` để phá ties |
| `COUNT(*) OVER (PARTITION BY company)` | Đếm tổng số nhân viên trong mỗi công ty |
| `cnt % 2 = 1 AND rn = (cnt + 1) / 2` | Trường hợp số lẻ: lấy đúng vị trí giữa |
| `cnt % 2 = 0 AND rn IN (cnt / 2, cnt / 2 + 1)` | Trường hợp số chẵn: lấy hai vị trí giữa |
| `ORDER BY company, salary` | Sắp xếp kết quả (tùy chọn, giúp dễ đọc) |

---

## ⏱️ Độ phức tạp

- **Thời gian:** `O(N log N)` – do bước sắp xếp bên trong window function (`ORDER BY salary, id` trong mỗi partition).
- **Không gian:** `O(N)` – để lưu trữ kết quả trung gian trong CTE `ranked`.

---

## 💡 Bài học rút ra

1.  **Phân biệt rõ "trung vị là giá trị" và "trung vị là dòng"**: Bài toán này yêu cầu **các dòng** chứa lương trung vị, không phải tính trung bình cộng. Với số phần tử chẵn, kết quả có thể có **nhiều hơn 1 dòng** cho mỗi công ty.
2.  **`ORDER BY salary, id`** là chìa khóa để xử lý ties một cách chính xác, đảm bảo thứ tự duy nhất và nhất quán.
3.  **Window functions** (`ROW_NUMBER`, `COUNT OVER`) là công cụ mạnh mẽ để giải các bài toán "trung vị", "top N", "phân vị" trong SQL mà không cần self-join phức tạp.
4.  **Luôn kiểm tra với cả trường hợp số lẻ và số chẵn**, cũng như trường hợp có ties (nhiều nhân viên cùng lương).
5.  **Kỹ thuật này có thể mở rộng** cho các bài toán tìm **phân vị bất kỳ** (percentile) bằng cách thay đổi điều kiện `rn`.

---

## 📚 Tài liệu tham khảo

- [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [PostgreSQL `ROW_NUMBER()`](https://www.postgresql.org/docs/current/functions-window.html)
- [LeetCode 569 – Official Solutions](https://leetcode.com/problems/median-employee-salary/solutions/)