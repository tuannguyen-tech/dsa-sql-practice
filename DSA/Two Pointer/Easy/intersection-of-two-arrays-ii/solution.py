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