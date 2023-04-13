from collections import deque
from typing import Union

class BstNode:
    def __init__(self, value: int):
        self.value = value
        self.left : Union[BstNode, None] = None
        self.right : Union[BstNode, None] = None


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
        prev_node = None
        prev_left = False
        cur_node : Union[BstNode, None] = self.head
        while cur_node != None:
            if cur_node.value == value:
                # remove the node
                # if two children, swap VALUE of rightmost leaf of left subtree with current node
                # then delete rightmost node of left subtree, recursing as needed
                if cur_node.left is not None and cur_node.right is not None:
                    to_promote = cur_node.left
                    while to_promote.right != None:
                        to_promote = to_promote.right
                    temp = to_promote.value
                    self.remove(temp)
                    old_value = cur_node.value
                    cur_node.value = temp
                    return BstNode(old_value)
                # as the others are simple, non-recursive cases, we can simplify logic
                to_promote : Union[BstNode, None] = None
                # if no children, just remove it
                # we don't need an explicit case for this, just leave to_promote as None
                # if one child, promote the left-hand child
                if cur_node.left is None and cur_node.right is not None:
                    to_promote = cur_node.right
                elif cur_node.left is not None and cur_node.right is None:
                    to_promote = cur_node.left
                # finally shift nodes as appropriate
                if cur_node == self.head:
                    self.head = to_promote
                elif prev_left:
                    prev_node.left = to_promote
                elif not prev_left:
                    prev_node.right = to_promote
                return BstNode(cur_node.value)
            prev_node = cur_node
            if cur_node.value >= value:
                # go left
                cur_node = cur_node.left
                prev_left = True
            elif cur_node.value < value:
                # go right
                cur_node = cur_node.right
                prev_left = False

        return None

    def get(self, value) -> BstNode:
        # Retrieve a node by value
        cur_node = self.head
        while cur_node != None:
            if cur_node.value == value:
                return cur_node
            elif cur_node.value >= value:
                cur_node = cur_node.left
            elif cur_node.value < value:
                cur_node = cur_node.right
        return cur_node # i.e. None

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

    def balance(self, node : BstNode):
        return self.height(node.right) - self.height(node.left)
    
    def height(self, node : BstNode):
        if node is None:
            return 0
        return max(self.height(node.left), self.height(node.right)) + 1

tree = Bst()
tree.insert(3)
tree.insert(1)
tree.insert(5)
tree.insert(6)
tree.insert(7)
tree.insert(-1)

#     3
#   1   5
# -1      6
#           7

tree.print()

tree.remove(3)
tree.remove(1)
tree.remove(5)
tree.remove(-1)
tree.remove(6)
tree.remove(7)
tree.remove(0)

tree.print()