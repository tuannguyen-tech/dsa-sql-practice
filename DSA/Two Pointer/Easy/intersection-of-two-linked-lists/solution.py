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