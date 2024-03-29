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
        pass

    def remove(self, value):
        # Remove a node by value, depth-first search
        pass

    def get(self, value) -> BstNode:
        # Retrieve a node by value
        pass

    def print(self):
        # Traverse the tree breadth-first and print out the results
        pass

#     3
#   1   5
# -1   4  6
#        7  8

tree = Bst()
tree.insert(3)
tree.insert(1)
tree.insert(5)
tree.insert(6)
tree.insert(7)
tree.insert(-1)