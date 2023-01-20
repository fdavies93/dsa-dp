class SingleLLNode:
    def __init__(self, data : int, next : "SingleLLNode" = None):
        self.data = data
        self.next = next

class SingleList:
    def __init__(self):
        self.head = None

    def get_tail(self) -> "SingleLLNode":
        pass

    def find_by_val(self, val : int):
        pass

    def insert_at_head(self, val):
        pass

    # This special function controls what is shown on print(ll)
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
        pass

    def remove_value(self, val : int):
        cur = self.head
        prev = None
        if cur == None:
            return
        
        # Find which node to remove by looping through the list.
        # There are 3 separate cases to consider:
        # Nothing to remove.
        # Something to remove, but we're at the head.
        # All other 'normal' cases.
    
if __name__ == "__main__":
    ll = SingleList()
    for i in range(10):
        ll.insert_at_head(i)
    ll.print()
    five = ll.find_by_val(5)
    print(five.data)
    ll.remove_value(5)
    ll.print()
    ll.insert_after(5,6)
    ll.print()
    tail = ll.get_tail()
    print(tail.data)