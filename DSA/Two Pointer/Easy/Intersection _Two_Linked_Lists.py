"""
==============================================================================
Problem: Intersection of Two Linked Lists
Link: https://leetcode.com/problems/intersection-of-two-linked-lists/
Difficulty: Easy
Topic: Linked List, Two Pointers
==============================================================================
[1] Cách chạy thuật toán (mô tả trực quan)

  🎯 Ý TƯỞNG GỐC: "Hai cuộn phim dán vào nhau"

  Tưởng tượng mỗi danh sách là một cuộn phim (dải ô vuông):
    - Cuộn A dài m ô
    - Cuộn B dài n ô
    - Hai cuộn có thể chia sẻ một đoạn ĐUÔI CHUNG (cùng object!)

  Nếu chỉ cho 2 con trỏ chạy song song trên A và B:
    → A, B dài ngắn KHÁC NHAU → LỆCH PHA
    → con trỏ tới giao điểm ở 2 thời điểm khác nhau → TRƯỢT

  💡 Giải pháp: DÁN A+B và B+A lại!
    - Dải 1 = A + B  (dài m + n)
    - Dải 2 = B + A  (dài n + m)
    → CẢ HAI DẢI DÀI BẰNG NHAU
    → Ô giao nằm ở CÙNG VỊ TRÍ trên cả 2 dải
    → 2 ngón tay lướt cùng tốc độ → CHẮC CHẮN CHẠM

  ---------------------------------------------
  VÍ DỤ NHỎ NHẤT: A=[1,2], B=[3,2]  (giao tại 2)
  ---------------------------------------------

  A: [1] → [2]
  B: [3] → [2]      (2 của A và 2 của B là CÙNG object)

  Dán A+B:  [1] [2] [3] [2]
  Dán B+A:  [3] [2] [1] [2]
  Vị trí:    0   1   2   3

  Nhìn cột vị trí 3: cả 2 dải đều có [2] (cùng object)
  → 2 ngón lướt cùng tốc độ → gặp nhau ở vị trí 3

  pa (đi A+B): 1 → 2 → 3 → 2*     (* = giao điểm, lần 2)
  pb (đi B+A): 3 → 2 → 1 → 2*     (* = cùng object với pa)

  B0: pa=1, pb=3    ; pa != pb
  B1: pa=2, pb=2*   ; pa != pb  ⚠️ pb tới giao LẦN 1, pa tới LẦN 1 → trượt!
  B2: pa=3, pb=1    ; pa != pb
  B3: pa=2*, pb=2*  ; pa == pb  ✅ GẶP Ở LẦN 2

  🔑 CÁI "CLICK":
  Mỗi người đi qua giao điểm 2 lần.
  Lần 1: lệch thời điểm → trượt.
  Lần 2: trùng thời điểm → GẶP.
  Vì sao lần 2 trùng? Vì cả 2 đi CÙNG TỔNG QUÃNG ĐƯỜNG (m+n).

  ---------------------------------------------
  VÍ DỤ KHÔNG GIAO: A=[1,2,3], B=[4,5]
  ---------------------------------------------

  A: [1] → [2] → [3] → null
  B: [4] → [5] → null

  pa (A+B): 1 → 2 → 3 → 4 → 5 → null
  pb (B+A): 4 → 5 → 1 → 2 → 3 → null

  B0: pa=1, pb=4
  B1: pa=2, pb=5
  B2: pa=3, pb=1    (pb hết B → nhảy sang A)
  B3: pa=4, pb=2
  B4: pa=5, pb=3
  B5: pa=null, pb=null  ✅ pa == pb == null → không giao → return null

  ---------------------------------------------
  🔑 TẠI SAO "NHẢY SANG LIST KIA" LÀ Ý TƯỞNG HAY?
  ---------------------------------------------
  Không cần đếm độ dài trước (không cần biết m, n)
  Không cần nhớ list nào dài hơn
  Không cần căn chỉnh thủ công
  → TỰ ĐỘNG căn chỉnh nhờ tổng quãng đường bằng nhau

  Chỉ 5 dòng code, không bug. Đó là lý do nó là lời giải thanh lịch nhất.


[2] Các bước thuật toán

  B1. Khởi tạo 2 con trỏ:
        pa <- headA
        pb <- headB

  B2. Lặp while pa != pb:
        Nếu pa == None:  pa <- headB     (hết A → nhảy sang B)
        Ngược lại:        pa <- pa.next
        Nếu pb == None:  pb <- headA     (hết B → nhảy sang A)
        Ngược lại:        pb <- pb.next

  B3. Thoát vòng lặp (pa == pb):
        return pa            (có thể là node giao, hoặc None)


  ❓ Tại sao sau (m+n) bước cả 2 LUÔN gặp nhau (hoặc cùng None)?
  (pa đi: m bước trên A + n bước trên B = m+n bước
   pb đi: n bước trên B + m bước trên A = m+n bước
   → cùng quãng đường. Nếu có giao điểm, cả 2 đều đứng tại đó sau m+n bước.
   Nếu không giao, cả 2 đều là None sau m+n bước → pa == pb == None)

  ❓ Tại sao dùng "while pa != pb" mà không cần điều kiện gì thêm?
  (Vì pa == pb đã đủ: cùng là 1 node thật thì đó là giao điểm,
   cùng là None thì không giao. Không cần kiểm tra gì khác)

  ❓ Tại sao so sánh "pa == pb" mà không phải "pa.val == pb.val"?
  (Vì 2 nút khác object có thể cùng giá trị val. Phải so sánh THAM CHIẾU
   để biết chúng có trỏ đến cùng 1 vị trí bộ nhớ hay không. Đề bài có ví dụ
   cảnh báo: nút '1' trong A và nút '1' trong B là 2 object khác nhau,
   KHÔNG phải giao điểm. Nếu so val sẽ báo sai)

  ❓ Tại sao KHÔNG dùng Hash Set cho đơn giản?
  (Hash Set đúng về thời gian O(m+n) nhưng tốn O(m) bộ nhớ → vi phạm
   yêu cầu Follow-up: O(1) memory. Bài này bắt buộc dùng 2 con trỏ)

  ❓ Tại sao KHÔNG đảo ngược list để tìm giao điểm?
  (Đảo list sẽ SỬA cấu trúc list. Đề yêu cầu "retain original structure"
   → không được phép thay đổi next của bất kỳ node nào)

  ❓ Nếu dùng cách "đếm độ dài + căn chỉnh" thì sao?
  (Đúng về độ phức tạp O(m+n) time, O(1) space. NHƯNG code dài hơn:
   2 vòng đếm + căn chỉnh + so sánh = 3-4 vòng lặp. Dễ bug (đảo nhánh if/else,
   lệch 1 đơn vị). Cách "nhảy list" gọn hơn, ít bug hơn)


[3] complexity
  -Time complexity: O(m + n) - Mỗi con trỏ đi tối đa m+n bước
  -Space complexity: O(1) - Chỉ dùng 2 biến con trỏ pa, pb, không mảng phụ
==============================================================================
"""


class Solution:
    def getIntersectionNode(self, headA, headB):
        pa, pb = headA, headB

        while pa != pb:
            # hết A → nhảy sang B ; ngược lại tiến 1 bước
            pa = headB if pa is None else pa.next
            # hết B → nhảy sang A ; ngược lại tiến 1 bước
            pb = headA if pb is None else pb.next

        return pa   # node giao, hoặc None nếu không giao


# ---test cases ---
if __name__ == '__main__':
    class ListNode:
        def __init__(self, x):
            self.val = x
            self.next = None

    def build_intersect(valsA, valsB, skipA, skipB):
        """
        Tạo 2 linked list giao nhau.
        valsA[skipA:] và valsB[skipB:] là phần CHUNG (cùng object).
        """
        # tạo phần đuôi chung
        common_nodes = [ListNode(v) for v in valsA[skipA:]]
        for i in range(len(common_nodes) - 1):
            common_nodes[i].next = common_nodes[i + 1]
        common_head = common_nodes[0] if common_nodes else None

        # tạo phần riêng của A
        a_nodes = [ListNode(v) for v in valsA[:skipA]]
        for i in range(len(a_nodes) - 1):
            a_nodes[i].next = a_nodes[i + 1]
        if a_nodes:
            a_nodes[-1].next = common_head
            headA = a_nodes[0]
        else:
            headA = common_head

        # tạo phần riêng của B
        b_nodes = [ListNode(v) for v in valsB[:skipB]]
        for i in range(len(b_nodes) - 1):
            b_nodes[i].next = b_nodes[i + 1]
        if b_nodes:
            b_nodes[-1].next = common_head
            headB = b_nodes[0]
        else:
            headB = common_head

        return headA, headB

    sol = Solution()

    # Example 1: giao tại 8
    a, b = build_intersect([4, 1, 8, 4, 5], [5, 6, 1, 8, 4, 5], 2, 3)
    res = sol.getIntersectionNode(a, b)
    print(res.val if res else None)          # 8

    # Example 2: giao tại 2
    a, b = build_intersect([1, 9, 1, 2, 4], [3, 2, 4], 3, 1)
    res = sol.getIntersectionNode(a, b)
    print(res.val if res else None)          # 2

    # Example 3: không giao
    a, b = build_intersect([2, 6, 4], [1, 5], 3, 2)
    res = sol.getIntersectionNode(a, b)
    print(res.val if res else None)          # None

    # test thêm: giao ngay đầu
    a, b = build_intersect([1, 2, 3], [1, 2, 3], 0, 0)
    res = sol.getIntersectionNode(a, b)
    print(res.val if res else None)          # 1

    # test thêm: một list rỗng
    a, b = build_intersect([], [1, 2], 0, 2)
    res = sol.getIntersectionNode(a, b)
    print(res.val if res else None)          # None