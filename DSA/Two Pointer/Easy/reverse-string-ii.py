"""
==============================================================================
Problem: Reverse String II
Link: https://leetcode.com/problems/reverse-string-ii/description/
Difficulty: Easy
Topic: Two Pointers, String
==============================================================================

[1] CÁCH CHẠY THUẬT TOÁN (MÔ TẢ TRỰC QUAN)
------------------------------------------------------------------------------
Ý tưởng: Chia chuỗi thành từng CỤM 2k ký tự. Trong mỗi cụm, đảo ngược k
ký tự ĐẦU, giữ nguyên k ký tự SAU. Cụm cuối nếu thiếu thì linh động xử lý.

Ẩn dụ: Một hàng binh lính xếp ngang, mỗi người cầm một tấm bảng có chữ.
    - Cứ 2k người lập thành 1 TIỂU ĐỘI (2k = 4 người nếu k=2).
    - Trong mỗi tiểu đội: k người ĐẦU QUAY 180 ĐỘ (đảo thứ tự), k người
      SAU đứng yên.
    - Tiểu đội cuối có thể thiếu người:
        * Đủ 2k      -> đảo k đầu, giữ k sau (bình thường).
        * Từ k đến <2k -> đảo k đầu, giữ phần lẻ còn lại.
        * Dưới k     -> đảo hết những gì còn lại.

Vì sao không dùng if/elif/else cho 3 trường hợp?
    Vì đề có VÔ SỐ cụm (không chỉ 1 cụm). Viết if cho từng trường hợp sẽ
    phải lặp lại logic cho từng cụm -> code dài, dễ bỏ sót (như quên
    trường hợp "nhiều hơn 2 cụm"). Cách đúng: dùng VÒNG LẶP bước nhảy 2k.

Vì sao dùng vòng lặp for i in range(0, n, 2k)?
    Nó tự động "nhảy" qua từng cụm: i = 0, 4, 8, ... Mỗi lần chỉ cần xử
    lý 1 việc duy nhất: đảo k ký tự từ vị trí i. Không cần if kiểm tra
    độ dài, vì Python slicing TỰ CẮT khi vượt biên.

Ví dụ: s = "abcdefg", k = 2  (n = 7, 2k = 4)

    Bước A: char = ['a','b','c','d','e','f','g']

    Bước B: range(0, 7, 4) = [0, 4]  -> chạy 2 lần

    Bước C: lần 1 (i=0):
        char[0:2] = ['a','b'] -> đảo -> ['b','a']
        char = ['b','a','c','d','e','f','g']

    Bước D: lần 2 (i=4):
        char[4:6] = ['e','f'] -> đảo -> ['f','e']
        char = ['b','a','c','d','f','e','g']

    Bước E: vòng lặp dừng (i tiếp = 8 > 7)
    Kết quả: "bacdfeg"

    Nhìn cụm 2: chỉ còn 3 ký tự "efg" (k=2 <= 3 < 2k=4). Vẫn đảo "ef"
    -> "fe", giữ "g". Đó chính là tính linh động của slicing tự cắt.

Ví dụ 2 (case "dưới k" - đảo toàn bộ):
    s = "a", k = 5  (n = 1, 2k = 10, k = 5)
    char = ['a']
    range(0, 1, 10) = [0]  -> chạy 1 lần
    i=0: char[0:5] = ['a'] (Python tự cắt vì list chỉ có 1 phần tử)
         đảo ['a'] = ['a']
    Kết quả: "a"

Ví dụ 3 (case "nhiều cụm" - quan trọng nhất):
    s = "abcdefgh", k = 2  (n = 8, 2k = 4)
    range(0, 8, 4) = [0, 4]  -> 2 cụm
    i=0: đảo "ab" -> "ba"  -> "bacd efgh"
    i=4: đảo "ef" -> "fe"  -> "bacd fegh"
    Kết quả: "bacdfegh"   (2 cụm đầy đủ)


[2] CÁC BƯỚC THUẬT TOÁN
------------------------------------------------------------------------------
B1. Chuyển chuỗi thành list (vì string trong Python bất biến):
        char <- list(s)

B2. Duyệt từng cụm với bước nhảy 2k:
        Với i trong range(0, len(char), 2*k):
            char[i : i+k] <- đảo_ngược(char[i : i+k])

B3. Ghép list lại thành chuỗi:
        return "".join(char)


>> Tại sao phải chuyển sang list?
    String trong Python là BẤT BIẾN (immutable) - không thể gán char[i] =
    'x'. Nếu làm với string, mỗi lần "sửa" sẽ tạo string mới -> O(n) mỗi
    lần -> tổng O(n²). Dùng list: sửa tại chỗ O(1), tổng O(n).

>> Tại sao dùng range(0, n, 2k) mà không phải vòng lặp while?
    range(..., step) tự động sinh dãy i = 0, 2k, 4k, ... rất gọn. Dùng
    while phải tự quản lý biến đếm và điều kiện dừng -> dễ sai, code dài
    hơn. Cả hai đều O(n/2k) lần lặp, nhưng for gọn và ít lỗi hơn.

>> Tại sao "char[i:i+k] = char[i:i+k][::-1]" xử lý được CẢ 3 trường hợp?
    Đây là LINH HỒN của bài - nhờ Python slicing TỰ CẮT:
        - Nếu i+k <= n: lấy đủ k phần tử -> đảo k đầu (TH bình thường).
        - Nếu i+k > n:  lấy những gì còn lại từ i đến cuối
          -> tự động đảo hết phần còn lại (TH cụm cuối thiếu).
    Không cần if kiểm tra độ dài. Cứ "đảo k ký tự từ i", phần thừa
    Python lo.

>> Tại sao không cần if len(s) < 2k ở đầu hàm?
    Vì range(0, n, 2k) tự dừng:
        - n < 2k -> range chỉ có [0] -> chạy đúng 1 lần -> xử lý cụm duy
          nhất.
        - n >= 2k -> range có nhiều giá trị -> xử lý nhiều cụm.
    Vòng lặp đã là "if tổng quát" rồi. Thêm if chỉ làm code rối.

>> Tại sao [::-1] đảo ngược mà không cần hàm reverse()?
    [::-1] là cú pháp slicing với step = -1: duyệt list từ cuối về đầu.
    Vừa ngắn, vừa nhanh (C-level), vừa tạo list mới (không sửa list gốc
    - quan trọng vì ta đang gán đè lên chính slice đó).


[3] COMPLEXITY
------------------------------------------------------------------------------
    - Time  : O(n)
              Mỗi ký tự được "chạm" đúng 1 lần trong suốt quá trình (mỗi
              cụm đảo k ký tự, cộng lại = n ký tự). join(char) cũng O(n).
              => Tổng O(n).
    - Space : O(n)
              list(char) tạo bản sao O(n). Slice char[i:i+k] tạo list tạm
              O(k) mỗi lần, nhưng giải phóng ngay -> đỉnh O(n).
              join(char) tạo string kết quả O(n).
              => Tổng O(n). Không thể tốt hơn vì kết quả phải trả về
              chuỗi dài n.

    So sánh các cách:
        Dùng if/elif/else thủ công  : O(n) nhưng DỄ SAI, khó mở rộng
                                      (dễ bỏ sót trường hợp nhiều cụm)
        Two Pointers tại chỗ (list) : O(n), O(n) space - tương đương
                                      nhưng code dài hơn
        For + Slicing (cách này)    : O(n), O(n) space - NGẮN NHẤT, ít lỗi
                                      nhất, tự xử lý mọi edge case
==============================================================================
"""


def reverseStr(s: str, k: int) -> str:
    """Đảo k ký tự đầu trong mỗi cụm 2k ký tự liên tiếp."""
    # Bước A: chuyển chuỗi sang list để có thể sửa tại chỗ
    char = list(s)

    # Bước B: duyệt từng cụm, bước nhảy 2k
    for i in range(0, len(char), 2 * k):
        # Đảo k ký tự bắt đầu từ i (Python tự cắt nếu vượt cuối chuỗi)
        char[i:i + k] = char[i:i + k][::-1]

    # Bước C: ghép list lại thành chuỗi
    return "".join(char)


# --- TEST ---
if __name__ == '__main__':
    print(reverseStr("abcdefg", 2))      # "bacdfeg"
    print(reverseStr("abcd", 2))         # "bacd"
    print(reverseStr("abc", 2))          # "bac"
    print(reverseStr("ab", 2))           # "ba"
    print(reverseStr("a", 2))            # "a"
    print(reverseStr("abcdefgh", 2))     # "bacdfegh"
    print(reverseStr("abcdefghij", 3))   # "cbadefihgj"
    print(reverseStr("hello", 3))        # "lehlo"
    
