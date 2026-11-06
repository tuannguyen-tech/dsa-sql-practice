# 3482. Analyze Organization Hierarchy

🔗 **Link bài toán:** [LeetCode 3482](https://leetcode.com/problems/analyze-organization-hierarchy/)

## 📌 Độ khó & Tags

- **Độ khó:** Hard
- **Tags:** Database, Recursive CTE, Tree Hierarchy, Aggregation

## 📝 Mô tả đề bài (tóm tắt)

Cho bảng `Employees` mô tả cấu trúc tổ chức dạng cây:

| Cột | Kiểu | Mô tả |
|---|---|---|
| `employee_id` | int | ID nhân viên (khóa chính) |
| `employee_name` | varchar | Tên nhân viên |
| `manager_id` | int | ID quản lý trực tiếp (NULL nếu là CEO) |
| `salary` | int | Mức lương |
| `department` | varchar | Phòng ban |

Yêu cầu viết truy vấn trả về **5 cột** cho mỗi nhân viên:

1. **`employee_id`** – ID nhân viên.
2. **`employee_name`** – Tên nhân viên.
3. **`level`** – Cấp bậc trong tổ chức:
   - CEO (`manager_id IS NULL`) có `level = 1`.
   - Nhân viên báo cáo trực tiếp cho CEO có `level = 2`.
   - Cứ mỗi cấp dưới trực tiếp, `level` tăng thêm 1.
4. **`team_size`** – Tổng số nhân viên **cấp dưới** (cả trực tiếp và gián tiếp).
   - Nhân viên không có cấp dưới → `team_size = 0`.
   - **Không bao gồm chính nhân viên đó**.
5. **`budget`** – Tổng ngân sách lương của **toàn bộ nhóm** do nhân viên đó quản lý, **bao gồm cả lương của chính họ**.
   - Nếu không có cấp dưới → `budget = salary`.
   - Nếu có cấp dưới → `budget = salary + tổng salary của tất cả cấp dưới`.

**Thứ tự sắp xếp kết quả:**
1. `level` **tăng dần**.
2. Nếu cùng `level` → `budget` **giảm dần**.
3. Nếu cùng `level` và `budget` → `employee_name` **tăng dần** (theo bảng chữ cái).

## 🧠 Phân tích & Hướng tiếp cận

### Vì sao cần Recursive CTE?

Cấu trúc tổ chức là một **cây tự tham chiếu** (`manager_id` trỏ đến `employee_id`). Độ sâu của cây **không xác định trước**, nên không thể dùng số lượng `JOIN` cố định. Giải pháp tự nhiên là **Recursive CTE** để duyệt cây.

### Các bước giải quyết

Giải pháp sử dụng **3 CTE**:

1. **`hierarchy_levels`** – Tính `level` cho từng nhân viên.
   - **Anchor:** Chọn CEO (`manager_id IS NULL`) với `level = 1`.
   - **Recursive:** Join `Employees` với CTE hiện tại để tìm cấp dưới trực tiếp và tăng `level` lên 1.

2. **`manager_descendants`** – Xây dựng bảng ánh xạ **quản lý → tất cả nhân viên trong cây con** (bao gồm cả chính quản lý).
   - **Anchor:** Mỗi nhân viên tự quản lý chính mình (`manager_id = employee_id`).
   - **Recursive:** Từ mỗi cặp `(manager_id, employee_id)`, tìm những nhân viên báo cáo trực tiếp cho `employee_id` và thêm vào cặp `(manager_id, cấp_dưới_mới)`.
   - Kết quả: với mỗi quản lý, ta có **tất cả** nhân viên (trực tiếp + gián tiếp) trong cây con của họ.

3. **`aggregated`** – Tính `team_size` và `budget` từ `manager_descendants`.
   - `team_size = COUNT(*) - 1` (trừ đi chính quản lý).
   - `budget = SUM(salary)` của tất cả nhân viên trong cây con (bao gồm quản lý).

4. **Truy vấn cuối** – Join `hierarchy_levels` với `aggregated` để lấy đầy đủ 5 cột, xử lý `NULL` bằng `COALESCE`, và sắp xếp theo yêu cầu.