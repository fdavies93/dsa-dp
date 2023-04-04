from collections import deque

class BstNode:
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None


class Bst:
    def __init__(self):
        self.head = None

    def insert(self, value):
        # Insert a node by value, depth-first search
        if self.head is None:
            self.head = BstNode(value)
            return
        cur_node = self.head
        while cur_node != None:
            if cur_node.value >= value:
                next_node = cur_node.left
                if next_node is None:
                    # insert left
                    cur_node.left = BstNode(value)
            if cur_node.value < value:
                next_node = cur_node.right
                # insert right
                if next_node is None:
                    cur_node.right = BstNode(value)
            cur_node = next_node

    def remove(self, value):
        # Remove a node by value, depth-first search
        pass

    def get(self, value) -> BstNode:
        # Retrieve a node by value
        pass

    def print(self):
        # Traverse the tree breadth-first and print out the results
        if self.head is None:
            return
        next_nodes : deque[BstNode] = deque([self.head])
        # print(len(next_nodes))
        while len(next_nodes) > 0:
            cur_node = next_nodes.popleft()
            print(cur_node.value)
            if cur_node.left is not None:
                next_nodes.append(cur_node.left)
            if cur_node.right is not None:
                next_nodes.append(cur_node.right)

tree = Bst()
tree.insert(3)
tree.insert(1)
tree.insert(5)
tree.insert(6)
tree.insert(7)
tree.insert(-1)

tree.print()