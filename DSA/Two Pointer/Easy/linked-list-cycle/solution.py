class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def hasCycle(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next      
        fast = fast.next.next   
        if slow == fast:          
            return True

    return False                  


# ---test cases ---
if __name__ == '__main__':
    def build_list(values, pos=-1):
        """tạo linked list từ mảng, nối đuôi về vị trí pos để tạo cycle"""
        if not values:
            return None
        nodes = [ListNode(v) for v in values]
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        if pos >= 0:
            nodes[-1].next = nodes[pos]
        return nodes[0]

    print(hasCycle(build_list([1, 2, 3, 4], pos=1)))   
    print(hasCycle(build_list([3, 2, 0, -4], pos=1)))  
    print(hasCycle(build_list([1, 2, 3], pos=-1)))   
    print(hasCycle(build_list([], pos=-1)))          
    print(hasCycle(build_list([1], pos=-1)))           
    print(hasCycle(build_list([1], pos=0)))            