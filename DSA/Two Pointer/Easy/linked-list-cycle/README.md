==============================================================================
Problem: Linked List Cycle
Link: https://leetcode.com/problems/linked-list-cycle/description/
Difficulty: Easy
Topic: Linked List, Two Pointers
==============================================================================
[1] Cách chạy thuật toán (mô tả trực quan)
vì danh sách liên kết chỉ có thể đi một chiều theo con trỏ next và không thể lùi lại
nên tôi nghĩ mình không thể lưu các nút đã thăm (sẽ tốn O(N) bộ nhớ)
và tôi nghĩ đến việc dùng 2 con trỏ với tốc độ khác nhau để "tự phát hiện" vòng tròn
ý tưởng giống 2 người chạy trên đường đua:
    + nếu đường thẳng  => người nhanh sẽ chạm đích (null) trước => không có chu trình
    + nếu đường vòng   => người nhanh sẽ đuổi kịp người chậm       => có chu trình

vd: list = 1 → 2 → 3 → 4 → (quay lại 2)
tôi sẽ dùng 2 con trỏ:
    + slow (rùa) đi 1 bước mỗi lần
    + fast (thỏ) đi 2 bước mỗi lần

[1]→[2]→[3]→[4]
 ↑
slow,fast
B1: slow=1->2, fast=1->3
    slow=2, fast=3 ; slow != fast
    [1]→[2]→[3]→[4]
         ↑    ↑
        slow  fast

B2: slow=2->3, fast=3->2 (3->4->2)
    slow=3, fast=2 ; slow != fast
    [1]→[2]→[3]→[4]
              ↑    ↑
             fast slow

B3: slow=3->4, fast=2->4 (2->3->4)
    slow=4, fast=4 ; slow == fast => có chu trình => return True
    [1]→[2]→[3]→[4]
                   ↑
                slow,fast

ngược lại nếu không có chu trình:
vd: 1 → 2 → 3 → null

[1]→[2]→[3]→null
 ↑
slow,fast
B1: slow=1->2, fast=1->3
    slow=2, fast=3 ; slow != fast
    [1]→[2]→[3]→null
         ↑    ↑
        slow  fast

B2: fast.next = null => dừng while
    => return False (không có chu trình)

[2] Các bước thuật toán
B1. Khởi tạo 2 con trỏ:
        slow <- head (rùa, đi 1 bước)
        fast <- head (thỏ, đi 2 bước)
B2. Lặp while fast and fast.next:
      slow <- slow.next        (rùa đi 1 bước)
      fast <- fast.next.next   (thỏ đi 2 bước)
      Nếu slow == fast:
        return True            (gặp nhau => có chu trình)
B3. Nếu thoát vòng lặp (fast hoặc fast.next là null):
      return False             (không có chu trình)

-Tại sao khi kiểm tra vòng lặp ta phải viết "while fast and fast.next"?
(Bởi vì trong thân vòng lặp ta gọi fast.next.next, nếu fast là nút cuối thì
 fast.next = None, gọi fast.next.next sẽ bị lỗi. Vì vậy phải kiểm tra
 cả fast và fast.next để chắc chắn rằng fast có thể nhảy được 2 bước)

-Tại sao phải so sánh slow == fast (so sánh tham chiếu) chứ không phải slow.val == fast.val?
(vì hai nút khác nhau có thể có cùng giá trị val, so sánh val sẽ báo sai. Ta cần biết
 hai con trỏ có đang trỏ đến cùng một nút hay không, đó là so sánh tham chiếu)

-Tại sao lại là "slow đi 1, fast đi 2" mà không phải "slow đi 1, fast đi 3"?
(vì hiệu tốc độ phải bằng 1 thì fast mới tiến sát slow đúng 1 bước mỗi lần, không thể
 nhảy cóc qua slow. Nếu cho fast đi 3, hiệu tốc độ = 2, thì trong một số trường hợp
 (vd chu trình độ dài chẵn) fast có thể nhảy qua slow mãi mà không bao giờ trùng)

[3] complexity
-Time complexity: O(N) - Vì mỗi nút được slow đi qua tối đa 1 lần
-Space complexity: O(1) - Vì chỉ dùng 2 biến con trỏ slow, fast, không tạo mảng phụ.
==============================================================================
