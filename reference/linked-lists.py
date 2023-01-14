class ListNode:
    def __init__(self, data : int, next : "ListNode" = None):
        self.data = data
        self.next = next

    def insert_after(self, node : "ListNode"):
        pass

    def remove_by_value(self, value : int):
        pass

class SingleList:
    def __init__(self):
        self.head = None

    def get_tail(self) -> "ListNode":
        cur = self.head
        if cur == None:
            return None
        while cur.next != None:
            cur = cur.next
        return cur

    def find_by_val(self, val : int):
        cur = self.head
        if cur == None:
            return None
        while cur != None:
            if cur.data == val:
                break
            cur = cur.next
        return cur

    def push(self, node : "ListNode"):
        if self.head == None:
            self.head = node
        cur = self.head
            
        pass

    def insert_after(self, node : "ListNode", val : int):
        point = self.find_by_val(val)
        if point == None:
            return
        next = point.next
        point.next = node
        node.next = next

    def remove_value(self, val : int):
        cur = self.head
        if cur == None:
            return
        