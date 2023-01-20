class SingleLLNode:
    def __init__(self, data : int, next : "SingleLLNode" = None):
        self.data = data
        self.next = next

class SingleList:
    def __init__(self):
        self.head = None

    def get_tail(self) -> "SingleLLNode":
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

    def insert_at_head(self, val):
        new_head = SingleLLNode(val, self.head)
        self.head = new_head

    def __repr__(self):
        cur = self.head
        out = ""
        while cur != None:
            out += str(cur.data)
            cur = cur.next
            if cur != None:
                out += " > "
        return out

    def insert_after(self, insert_val : int, search_val : int):        
        point = self.find_by_val(search_val)
        if point == None:
            return
        node = SingleLLNode(insert_val, point.next)
        point.next = node

    def remove_value(self, val : int):
        cur = self.head
        prev = None
        if cur == None:
            return
        while cur.data != val and cur != None:
            prev = cur
            cur = cur.next
        
        # Nothing to remove.
        if cur == None:
            return

        # If we're at the head.
        if prev == None:
            self.head = cur.next
            return
        
        # All other cases.
        prev.next = cur.next
            
    
if __name__ == "__main__":
    ll = SingleList()
    for i in range(10):
        ll.insert_at_head(i)
    print(ll)
    five = ll.find_by_val(5)
    print(five.data)
    ll.remove_value(5)
    print(ll)
    ll.insert_after(5,6)
    print(ll)
    tail = ll.get_tail()
    print(tail.data)