def sortedSquares(nums: list[int]) -> list[int]:
    """Trả về bình phương các phần tử, sắp xếp không giảm (O(n), 1 vòng lặp)."""
    n = len(nums)
    res = [0] * n                    # mảng kết quả, điền từ cuối về đầu
    left, right = 0, n - 1           # hai con trỏ ở hai đầu mảng gốc
    index = n - 1                    # vị trí điền trong res (từ cuối)

    while left <= right:
        # So sánh độ lớn thực (trị tuyệt đối) của hai đầu
        if abs(nums[left]) > abs(nums[right]):
            # Bên trái lớn hơn → chọn trái → nhích left (vùng chưa xử lý co từ trái)
            res[index] = nums[left] ** 2
            left += 1
        else:
            # Bên phải lớn hơn/hoặc bằng → chọn phải → nhích right (co từ phải)
            res[index] = nums[right] ** 2
            right -= 1
        index -= 1

    return res


# --- TEST ---
if __name__ == '__main__':
    print(sortedSquares([-4, -1, 0, 3, 10]))       # [0, 1, 9, 16, 100]
    print(sortedSquares([-7, -3, 2, 3, 11]))       # [4, 9, 9, 49, 121]
    print(sortedSquares([-5, -4, -3]))             # [9, 16, 25]
    print(sortedSquares([1, 4, 9]))                # [1, 16, 81]
    print(sortedSquares([0]))                      # [0]
    print(sortedSquares([-1]))                     # [1]
    print(sortedSquares([-1, 1]))                  # [1, 1]
    print(sortedSquares([-2, -1, 0, 1, 2]))        # [0, 1, 1, 4, 4]