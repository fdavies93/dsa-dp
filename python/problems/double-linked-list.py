from dataclasses import dataclass

@dataclass
class DoubleLLNode:
    data : object
    next : "DoubleLLNode"
    prev : "DoubleLLNode"

class DoubleLL:
    def __init__(self):
        self.head : DoubleLLNode = None
        self.tail : DoubleLLNode = None

    def push_tail(self, node : DoubleLLNode):
        node.prev = self.tail
        node.next = None
        if self.tail != None:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node

    def push_head(self, node : DoubleLLNode):
        node.next = self.head
        node.prev = None
        if self.head != None:
            self.head.prev = node
        else:
            self.tail = node
        self.head = node

    def pop_head(self) -> DoubleLLNode:
        if self.head == None:
            return None
        old_head = self.head
        if self.head.next != None:
            self.head.next.prev = None
        else:
            # there's only one item, and we're removing it
            self.tail = None
        self.head = self.head.next
        return old_head

    def pop_tail(self):
        if self.tail == None:
            return None
        old_tail = self.tail
        if self.tail.prev != None:
            self.tail.prev.next = None
        else:
            # there's only one item, and we're removing it
            self.head = None
        self.tail = self.tail.prev
        return old_tail
    
    def reverse(self):
        # this process is much simpler than the single LL equivalent
        # for each node, swap the next and prev pointers
        # finally, swap the head and tail of the list
        pass

    def __repr__(self) -> str:
        cur_node = self.head
        accumulate : list[str] = []
        while cur_node != None:
            accumulate.append(str(cur_node.data))
            cur_node = cur_node.next
        return " <-> ".join(accumulate)

node_data = [1,2,3,4,5]

# insert forwards
ls = DoubleLL()

for data in node_data:
    node = DoubleLLNode(data, None, None)
    ls.push_tail(node)

print(ls)

ls.reverse()
print(ls)
ls.reverse()
print(ls)

tail = ls.pop_tail().data
head = ls.pop_head().data

print(f"Head: {head}")
print(f"Tail: {tail}")

print(ls)

while ls.head != None:
    ls.pop_head()

# insert backwards
for data in node_data:
    node = DoubleLLNode(data, None, None)
    ls.push_head(node)

print(ls)

tail = ls.pop_tail().data
head = ls.pop_head().data

print(f"Head: {head}")
print(f"Tail: {tail}")

while ls.tail != None:
    ls.pop_tail()

ls.push_head(DoubleLLNode(3,None,None))
print(ls)