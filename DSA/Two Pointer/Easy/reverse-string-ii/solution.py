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
    
