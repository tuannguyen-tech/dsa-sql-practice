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