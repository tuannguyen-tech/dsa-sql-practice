# 3451. Find Invalid IP Addresses

🔗 **Link bài toán:** [LeetCode 3451](https://leetcode.com/problems/find-invalid-ip-addresses/description/)

## 📌 Độ khó & Tags

- **Độ khó:** Hard
- **Tags:** Database, String Manipulation, Regular Expression, Pattern Matching

---

## 📝 Mô tả đề bài

Cho bảng `logs` ghi lại lịch sử truy cập máy chủ:

| Cột | Kiểu | Mô tả |
|---|---|---|
| `log_id` | int | Khóa chính, ID duy nhất của mỗi bản ghi |
| `ip` | varchar | Địa chỉ IP của client (định dạng IPv4) |
| `status_code` | int | Mã trạng thái HTTP trả về |

### 🎯 Yêu cầu

Tìm tất cả các **địa chỉ IP không hợp lệ** (invalid IPv4) và đếm số lần xuất hiện của chúng.

Một địa chỉ IPv4 được coi là **không hợp lệ** nếu **thỏa mãn ít nhất một** trong các điều kiện sau:

| # | Điều kiện không hợp lệ | Ví dụ |
|---|---|---|
| 1 | Có **octet > 255** | `256.1.1.1`, `192.168.1.300` |
| 2 | Có **số 0 đứng đầu** trong một octet | `01.02.03.04`, `192.168.001.1` |
| 3 | **Không có đúng 4 octet** (ít hơn hoặc nhiều hơn 4) | `192.168.1`, `1.2.3.4.5`, `192.168` |

### 📤 Kết quả trả về

| Cột | Mô tả |
|---|---|
| `ip` | Địa chỉ IP không hợp lệ |
| `invalid_count` | Số lần IP đó xuất hiện trong bảng `logs` |

### 🔢 Thứ tự sắp xếp

1. `invalid_count` **giảm dần**.
2. Nếu cùng `invalid_count` → `ip` **giảm dần** (theo thứ tự từ điển/giá trị chuỗi).

---

## 🧠 Phân tích & Hướng tiếp cận

### 1. IPv4 hợp lệ trông như thế nào?

Một địa chỉ IPv4 chuẩn có dạng:

```
A.B.C.D
```

Trong đó:
- Có **đúng 4 octet** (`A`, `B`, `C`, `D`), phân tách bởi **3 dấu chấm**.
- Mỗi octet là một số nguyên trong khoảng **[0, 255]**.
- **Không có số 0 đứng đầu** ở các số có nhiều chữ số:
  - ✅ Hợp lệ: `0`, `5`, `42`, `255`
  - ❌ Không hợp lệ: `00`, `01`, `007`, `0255`

> ⚠️ **Lưu ý:** `0` là hợp lệ (single digit), nhưng `00` hay `01` là không hợp lệ. Đây là điểm dễ sai khi tự viết logic kiểm tra.

### 2. Vì sao nên dùng Regular Expression?

Có hai hướng tiếp cận chính:

| Cách tiếp cận | Ưu điểm | Nhược điểm |
|---|---|---|
| **Regex** (`!~` / `NOT REGEXP`) | Ngắn gọn, 1 câu truy vấn, xử lý gọn mọi điều kiện | Cần hiểu pattern; khó đọc với người mới |
| **Tách octet thủ công** (`split_part`, `string_to_array`, `CAST`) | Rõ ràng logic | Dài dòng, dễ sai với các edge case (ví dụ `0`, số lượng octet) |

Với **PostgreSQL**, regex là lựa chọn **tối ưu nhất** vì:
- Hỗ trợ **POSIX regex** đầy đủ (giống Perl).
- Toán tử `~` (match) và `!~` (not match) rất tiện lợi.
- Không cần join bảng phụ hay subquery phức tạp.

### 3. Xây dựng Regex kiểm tra IPv4 hợp lệ

Ta sẽ xây dựng pattern để **match với IPv4 hợp lệ**, rồi lấy những IP **không match** bằng `!~`.

#### Bước 1: Pattern cho một octet (0–255, không có leading zero)

Một octet hợp lệ thuộc một trong các khoảng:

| Khoảng giá trị | Độ dài | Pattern |
|---|---|---|
| `0` – `9` | 1 chữ số | `[0-9]` |
| `10` – `99` | 2 chữ số, không bắt đầu bằng 0 | `[1-9][0-9]` |
| `100` – `199` | 3 chữ số, bắt đầu bằng 1 | `1[0-9]{2}` |
| `200` – `249` | 3 chữ số, bắt đầu bằng 2, chữ số thứ 2 ≤ 4 | `2[0-4][0-9]` |
| `250` – `255` | 3 chữ số, bắt đầu bằng 25, chữ số cuối ≤ 5 | `25[0-5]` |

Gộp lại (thứ tự ưu tiên từ chặt đến lỏng để tránh match sai):

```
25[0-5] | 2[0-4][0-9] | 1[0-9]{2} | [1-9][0-9] | [0-9]
```

Ta có thể **rút gọn** `[1-9][0-9] | [0-9]` thành `[1-9]?[0-9]`:

- `[1-9]?` là **tùy chọn** (có hoặc không).
- Nếu không có `[1-9]` → match `[0-9]` = 1 chữ số (0–9).
- Nếu có `[1-9]` → match `[1-9][0-9]` = 2 chữ số (10–99).

Vậy pattern cho **một octet** là:

```
(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])
```

#### Bước 2: Pattern cho toàn bộ IPv4

IPv4 = `octet` + `.` lặp lại **3 lần**, sau đó là `octet` cuối cùng.

```
(octet\.){3}octet
```

#### Bước 3: Neo đầu/cuối chuỗi (`^` và `$`)

Rất quan trọng: phải có `^` và `$` để đảm bảo **match toàn bộ chuỗi**, không match một phần. Nếu thiếu, chuỗi `"abc.1.2.3.4"` có thể bị coi là hợp lệ (vì phần `1.2.3.4` match).

```
^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$
```

#### Bước 4: Đảo ngược để lọc IP **không hợp lệ**

Trong PostgreSQL:

- `ip ~ 'pattern'` → IP **hợp lệ**.
- `ip !~ 'pattern'` → IP **không hợp lệ** ← đây là điều kiện ta cần.

### 4. Kiểm tra Pattern với các trường hợp biên

| Input | Có hợp lệ? | Lý do |
|---|---|---|
| `192.168.1.1` | ✅ | Đúng 4 octet, mỗi octet ∈ [0,255], không có leading zero |
| `0.0.0.0` | ✅ | Octet `0` là single digit, hợp lệ |
| `255.255.255.255` | ✅ | Mỗi octet = 255, hợp lệ |
| `256.1.1.1` | ❌ | Octet `256` > 255 |
| `192.168.1.300` | ❌ | Octet `300` > 255 |
| `01.2.3.4` | ❌ | Octet `01` có leading zero |
| `192.168.001.1` | ❌ | Octet `001` có leading zero |
| `192.168.1` | ❌ | Chỉ có 3 octet |
| `1.2.3.4.5` | ❌ | Có 5 octet |
| `192.168.1.1.` | ❌ | Có dấu chấm thừa ở cuối |
| `.1.2.3.4` | ❌ | Có dấu chấm thừa ở đầu |
| `192.168..1` | ❌ | Có octet rỗng |
| `abc.1.2.3` | ❌ | Octet `abc` không phải số |

> 💡 **Mẹo kiểm tra regex:** Có thể dùng [regex101.com](https://regex101.com/) với flavor "Golang" hoặc "PCRE" để test trước khi đưa vào SQL.

### 5. Xử lý sau khi lọc

Sau khi có danh sách IP không hợp lệ, ta cần:

1. **`GROUP BY ip`** – nhóm các IP trùng nhau.
2. **`COUNT(*) AS invalid_count`** – đếm số lần xuất hiện.
3. **`ORDER BY invalid_count DESC, ip DESC`** – sắp xếp theo yêu cầu.

---
## 💡 Bài học rút ra

1. **Regular Expression là vũ khí mạnh** khi cần kiểm tra định dạng chuỗi phức tạp như IPv4, email, số điện thoại… trong SQL.
2. **Luôn neo `^...$`** khi kiểm tra tính hợp lệ toàn chuỗi – nếu thiếu, regex có thể match một phần chuỗi và cho kết quả sai.
3. **Xây dựng pattern theo từng khoảng giá trị** (0–9, 10–99, 100–199, 200–249, 250–255) giúp pattern dễ đọc và dễ kiểm chứng hơn.
4. **Test với các edge case** (`0`, `00`, `255`, `256`, thiếu/thừa octet, dấu chấm thừa) trước khi nộp bài.
5. **PostgreSQL regex** khác MySQL/Oracle về cú pháp toán tử:
   - PostgreSQL: `~` (match), `!~` (not match), `~*` (case-insensitive).
   - MySQL: `REGEXP`, `NOT REGEXP`, `REGEXP_LIKE()`.
6. **Không cần `DISTINCT`** vì `GROUP BY` đã tự loại trùng.

---