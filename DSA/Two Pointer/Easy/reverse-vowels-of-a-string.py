"""
==============================================================================
Problem: Reverse Vowels of a String
Link: https://leetcode.com/problems/reverse-vowels-of-a-string/description/
Difficulty: Easy
Topic: Two Pointers, String
==============================================================================

[1] CÁCH CHẠY THUẬT TOÁN (MÔ TẢ TRỰC QUAN)
------------------------------------------------------------------------------
Ý tưởng: Đảo ngược CHỈ các nguyên âm, giữ nguyên mọi ký tự khác.
Ta tưởng tượng chuỗi là dãy ghế, mỗi ghế ngồi một ký tự. Ta CHỈ đổi chỗ những
"người" là nguyên âm, phụ âm thì đứng yên tại ghế của mình.

Vì sao dùng hai con trỏ?
    Ta cần lấy nguyên âm ĐẦU TIÊN (bên trái) ghép với nguyên âm CUỐI CÙNG
    (bên phải), rồi đưa vào trong. Đây đúng là công việc của hai con trỏ
    tiến vào giữa.

    left ->                        <- right
      h   e   l   l   o
          ^           ^
      nguyên âm   nguyên âm   -> hoán đổi

Nguyên âm: a, e, i, o, u (cả HOA và thường).
    LƯU Ý: KHÔNG dùng được khoảng ASCII 97..117 để kiểm tra, vì các nguyên âm
    KHÔNG liền nhau (a=97, e=101, i=105, o=111, u=117). Nếu dùng khoảng sẽ
    bắt nhầm phụ âm b,c,d,f,g,h,... -> phải kiểm tra theo TẬP HỢP cụ thể.

Ví dụ 1: s = "hello"
    chars = ['h','e','l','l','o'], left=0, right=4, kỳ vọng "holle"

    Vòng 1: chars[left]='h' không phải NN -> left++ (left=1)
            chars[right]='o' là NN         -> dừng
            left<right -> swap e<->o
            chars = ['h','o','l','l','e'], left=2, right=3

    Vòng 2: chars[left]='l' không phải NN -> left++ (left=3)
            chars[left]='l' vẫn không phải NN -> left++ (left=4)
            Điều kiện left < right (4 < 3) sai -> dừng vòng con
            -> while ngoài cũng dừng (left >= right)

    Kết quả: "holle"

Ví dụ 2: s = "bcaa"  (test case hay bị sai!)
    chars = ['b','c','a','a'], left=0, right=3, kỳ vọng "bcaa"

    Vòng 1: chars[left]='b' không phải NN -> left++ (left=1)
            chars[left]='c' không phải NN -> left++ (left=2)
            chars[left]='a' là NN -> dừng
            chars[right]='a' là NN -> dừng
            left<right -> swap a<->a (không đổi)
            chars = ['b','c','a','a'], left=3, right=2
    -> left >= right -> DỪNG. Kết quả: "bcaa"

    NẾU swap ngay khi vừa nhích left (không đợi cả hai bên là NN):
        B1: 'b' không phải NN -> left=1, RỒI SWAP chars[1]='c' với chars[3]='a'
            -> ['b','a','a','c'] -> kết quả "baac" SAI.
    Đây chính là lỗi phổ biến nhất ở bài này.


[2] CÁC BƯỚC THUẬT TOÁN
------------------------------------------------------------------------------
B1. Chuẩn bị:
        chars  <- list(s)              (Python: str bất biến -> phải chuyển list)
        vowels <- set("aeiouAEIOU")    (tra cứu O(1), gồm cả hoa & thường)
        left   <- 0
        right  <- len(chars) - 1

B2. Lặp while left < right:
        (a) Nhích left sang phải cho tới khi gặp nguyên âm:
                while left < right and chars[left] not in vowels: left += 1
        (b) Nhích right sang trái cho tới khi gặp nguyên âm:
                while left < right and chars[right] not in vowels: right -= 1
        (c) Lúc này CẢ HAI đều đang đứng ở nguyên âm -> swap:
                chars[left], chars[right] = chars[right], chars[left]
        (d) Nhích tiếp để tìm cặp kế tiếp:
                left += 1 ; right -= 1

B3. Trả về "".join(chars).


>> Tại sao phải kiểm tra left < right TRƯỚC khi truy cập chars[left]/chars[right]?
    Nếu viết ngược lại: chars[left] not in vowels and left < right
    -> khi left == right hoặc left > right, ta vẫn đọc chars[left] trước.
    Python không crash nhưng logic sẽ sai (có thể swap thừa, vòng lặp chạy
    quá). Trong C/Java có thể crash.
    -> Luôn đặt left < right LÊN TRƯỚC.

>> Tại sao dùng set("aeiouAEIOU") thay vì chuỗi "aeiouAEIOU"?
    - 'c in set' là O(1) (hash table) thay vì O(k) (duyệt tuần tự).
    - Diễn đạt đúng Ý ĐỊNH: "đây là TẬP hợp để kiểm tra thành viên".
    - Khi tập mở rộng (thêm ă, â, ê, ô, ơ, ư...) thì set vẫn giữ O(1).
    Với 10 ký tự thì hiệu năng gần như tương đương, nhưng dùng set là
    THÓI QUEN TỐT mang sang bài khác.

>> Tại sao phải chuyển str -> list -> str?
    Python str là IMMUTABLE: không thể gán s[i] = 'x'.
    -> list(s) để có list mutable, swap trên đó, rồi "".join(chars) trả str.
    Bộ nhớ phụ O(n) này BẮT BUỘC trong Python; về bản chất thuật toán vẫn là
    O(1) vì chỉ thêm vài biến con trỏ. Với C++/C/Java thì có thể swap thực sự
    trên string/char[] -> O(1) tuyệt đối.


[3] COMPLEXITY
------------------------------------------------------------------------------
    - Time  : O(n)
              Mỗi ký tự bị con trỏ left HOẶC right quét qua TỐI ĐA 1 lần.
              Tổng số bước nhích của cả hai con trỏ <= n.
    - Space : O(n) trong Python (do list(s) bắt buộc)
              O(1) nếu xét thuần thuật toán, hoặc O(1) tuyệt đối nếu ngôn ngữ
              cho phép sửa chuỗi tại chỗ.
==============================================================================
"""


def reverse_vowels(s: str) -> str:
    """Đảo ngược vị trí các nguyên âm trong chuỗi s, giữ nguyên phần còn lại."""
    chars = list(s)                   # str bất biến -> chuyển sang list
    vowels = set("aeiouAEIOU")        # tra cứu O(1), gồm cả hoa & thường
    left, right = 0, len(chars) - 1

    while left < right:
        # (a) nhích left tới nguyên âm gần nhất bên trái
        while left < right and chars[left] not in vowels:
            left += 1
        # (b) nhích right tới nguyên âm gần nhất bên phải
        while left < right and chars[right] not in vowels:
            right -= 1
        # (c) cả hai đều là nguyên âm -> swap
        chars[left], chars[right] = chars[right], chars[left]
        # (d) nhích tiếp
        left += 1
        right -= 1

    return "".join(chars)


# --- TEST ---
if __name__ == '__main__':
    print(reverse_vowels("hello"))     # holle
    print(reverse_vowels("leetcode"))  # leotcede
    print(reverse_vowels("bcaa"))      # bcaa
    print(reverse_vowels("a.b"))       # a.b
    print(reverse_vowels("aeiou"))     # uoiea
    print(reverse_vowels("bcdfg"))     # bcdfg
    print(reverse_vowels("aA"))        # Aa