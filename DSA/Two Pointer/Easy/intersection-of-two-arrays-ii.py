"""
==============================================================================
Problem: Intersection of Two Arrays II
Link: https://leetcode.com/problems/intersection-of-two-arrays-ii/description/
Difficulty: Easy
Topic: Array, Hash Table, Two Pointers, Binary Search, Sorting
==============================================================================

[1] CÁCH CHẠY THUẬT TOÁN (MÔ TẢ TRỰC QUAN)
------------------------------------------------------------------------------
Ý tưởng: Đếm tần suất các phần tử của mảng NHỎ hơn, rồi duyệt mảng LỚN,
mỗi phần tử nếu "còn hàng trong kho" thì lấy và giảm tồn kho đi 1.

Ẩn dụ: Hai giỏ kẹo. Mỗi viên có một màu (con số). Ta muốn biết màu nào có
ở cả hai giỏ, và mỗi màu lấy BAO NHIÊU viên. Quy tắc: lấy min(số ở giỏ 1,
số ở giỏ 2). Nếu giỏ 1 có 3 viên đỏ, giỏ 2 có 5 viên đỏ -> chỉ lấy 3 viên.

Vì sao không dùng 2 vòng lồng nhau?
    Với mỗi phần tử nums1, quét cả nums2 để tìm -> O(n*m). Với n=m=1000
    là 1.000.000 phép so sánh. Quá chậm.
    -> Dùng Hash Map (Counter) để đếm sẵn 1 lần, tra cứu về sau là O(1).

Vì sao đếm mảng NHỎ hơn?
    Counter chiếm bộ nhớ tỉ lệ với số phần tử của mảng được đếm.
    Đếm mảng nhỏ -> Counter nhỏ -> tiết kiệm RAM.
    Đây chính là câu trả lời cho follow-up #2 của đề.

Ví dụ: nums1 = [4,9,5], nums2 = [9,4,9,8,4]

    Bước A: len(nums1)=3 < len(nums2)=5 -> giữ nguyên, không hoán đổi.

    Bước B: Counter(nums1) = {4:1, 9:1, 5:1}

    Bước C: duyệt nums2 = [9,4,9,8,4]
        x=9: count[9]=1>0 -> lấy 9, count[9]=0   -> result = [9]
        x=4: count[4]=1>0 -> lấy 4, count[4]=0   -> result = [9,4]
        x=9: count[9]=0   -> BỎ QUA (đã hết hàng)
        x=8: count[8]=0   -> BỎ QUA (không có trong kho)
        x=4: count[4]=0   -> BỎ QUA (đã hết hàng)

    Kết quả: [9, 4]  (hoặc [4,9] đều đúng, thứ tự không quan trọng)

    Nhìn dòng thứ 3: số 9 xuất hiện lần 2 ở nums2 nhưng BỎ QUA vì nums1
    chỉ có 1 cái 9. Đó chính là min(1, 2) = 1.

Ví dụ 2 (case kinh điển phân biệt với bài #349):
    nums1 = [1,2,2,1], nums2 = [2,2]
    Counter(nums1) = {1:2, 2:2}
    Duyệt nums2: 2 -> lấy, count[2]=1; 2 -> lấy, count[2]=0
    Kết quả: [2, 2]   (bài #349 sẽ ra [2] vì chỉ lấy unique)


[2] CÁC BƯỚC THUẬT TOÁN
------------------------------------------------------------------------------
B1. Đảm bảo nums1 là mảng NHỎ hơn:
        Nếu len(nums1) > len(nums2): hoán đổi nums1, nums2

B2. Đếm tần suất mảng nhỏ:
        count <- Counter(nums1)

B3. Duyệt mảng lớn, thu hoạch:
        Với mỗi x trong nums2:
            Nếu count[x] > 0:        (còn hàng trong kho)
                result.append(x)
                count[x] -= 1        (đã dùng 1 viên)


>> Tại sao phải hoán đổi để đếm mảng nhỏ hơn?
    Counter chiếm bộ nhớ O(số phần tử khác nhau của mảng được đếm).
    Giỏ 1 có 10 viên, giỏ 2 có 1.000.000 viên:
        - Đếm giỏ 1: Counter nhỏ -> tốt
        - Đếm giỏ 2: Counter lớn -> tốn RAM
    -> Luôn hoán đổi để nums1 là mảng nhỏ. Bộ nhớ O(min(n,m)).

>> Tại sao dùng Counter mà không dùng dict thường?
    Counter là dict đặc biệt: count[x] tự trả 0 nếu x chưa có, KHÔNG báo
    KeyError như dict thường. Nhờ vậy code gọn hơn (không cần "if x in
    count" trước khi truy cập).

>> Tại sao dòng "count[x] -= 1" là LINH HỒN của bài?
    Chính nó hiện thực hóa "lấy min". Khi count[x] về 0, mảng nhỏ đã
    "cạn" phần tử x -> không lấy thêm được nữa. Nếu QUÊN dòng này, ta sẽ
    lấy quá số lượng (ví dụ nums1=[1,1,1], nums2=[1,1] sẽ ra [1,1,1] SAI
    thay vì [1,1]).

>> Tại sao điều kiện là "count[x] > 0" mà không phải "x in count"?
    "x in count" chỉ kiểm tra x có tồn tại trong kho hay không, KHÔNG
    kiểm tra còn hàng hay đã hết. Phải dùng "count[x] > 0" để gộp cả hai:
    vừa biết x có trong kho (Counter tự trả 0 nếu không), vừa biết còn
    hàng để lấy.


[3] COMPLEXITY
------------------------------------------------------------------------------
    - Time  : O(n + m)
              Đếm nums1 mất O(n), duyệt nums2 mất O(m). Mỗi phần tử được
              xử lý đúng 1 lần.
    - Space : O(min(n, m))
              Counter chỉ lưu mảng nhỏ hơn (nhờ bước hoán đổi). Kết quả
              O(min(n,m)) là bắt buộc phải có để trả về.

    So sánh 3 cách:
        Brute force           : O(n*m) thời gian              - tệ nhất
        Sort + Two Pointers   : O(n log n + m log m)          - tốt khi đã sort
        Hash Map (Counter)    : O(n + m) thời gian, O(min)    - tốt nhất tổng quát
==============================================================================
"""

from collections import Counter


def intersect(nums1: list[int], nums2: list[int]) -> list[int]:
    """Trả về giao của hai mảng, giữ đúng số lần xuất hiện tối thiểu."""
    # Bước A: đảm bảo nums1 là mảng nhỏ hơn -> tiết kiệm bộ nhớ
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    # Bước B: đếm tần suất mảng nhỏ
    count = Counter(nums1)

    # Bước C: duyệt mảng lớn, lấy nếu còn hàng
    result = []
    for x in nums2:
        if count[x] > 0:            # vừa "có trong kho" vừa "còn hàng"
            result.append(x)
            count[x] -= 1           # đã dùng 1 viên -> giảm tồn kho

    return result


# --- TEST ---
if __name__ == '__main__':
    print(intersect([1, 2, 2, 1], [2, 2]))              # [2, 2]
    print(intersect([4, 9, 5], [9, 4, 9, 8, 4]))        # [9, 4] hoặc [4, 9]
    print(intersect([1, 2, 3], [4, 5, 6]))              # []
    print(intersect([1, 1, 1], [1, 1]))                 # [1, 1]
    print(intersect([1], [1]))                          # [1]
    print(intersect([3, 3, 3], [3, 3, 3]))              # [3, 3, 3]