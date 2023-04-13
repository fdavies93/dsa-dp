from collections import deque
from typing import Union

class BstNode:
    def __init__(self, value: int):
        self.value = value
        self.left : Union[BstNode, None] = None
        self.right : Union[BstNode, None] = None

class AvlTree:
    def __init__(self, values = [], autobalance = True):
        self.head = None
        self.autobalance = autobalance
        for val in values:
            self.insert(val)

    def insert(self, value):
        # Insert a node by value, depth-first search
        if self.head is None:
            self.head = BstNode(value)
            return
        cur_node = self.head
        visited = [] # maintain a stack to rebalance back up to root
        while cur_node != None:
            visited.append(cur_node)
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
            
            while self.autobalance and next_node is None and len(visited) > 0:
                prev = visited.pop()
                if len(visited) == 0:
                    # we're at head
                    self.head = AvlTree.rebalance(prev)
                elif visited[-1].left == prev:
                    visited[-1].left = AvlTree.rebalance(prev)
                elif visited[-1].right == prev:
                    visited[-1].right = AvlTree.rebalance(prev)
                        
            cur_node = next_node

    def remove(self, value):
        # Remove a node by value, depth-first search
        prev_node = None
        prev_left = False
        cur_node : Union[BstNode, None] = self.head
        visited = []
        while cur_node != None:
            visited.append(cur_node)
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

                while self.autobalance and len(visited) > 0:
                    prev = visited.pop()
                    if len(visited) == 0:
                        # we're at head
                        self.head = AvlTree.rebalance(prev)
                    elif visited[-1].left == prev:
                        visited[-1].left = AvlTree.rebalance(prev)
                    elif visited[-1].right == prev:
                        visited[-1].right = AvlTree.rebalance(prev)

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

    @classmethod
    def balance(cls, node : BstNode):
        return AvlTree.height(node.right) - AvlTree.height(node.left)
    
    @classmethod
    def height(cls, node : BstNode):
        if node is None:
            return 0
        return max(AvlTree.height(node.left), AvlTree.height(node.right)) + 1

    @classmethod
    def rotate_l_at(cls, node : BstNode):
        new_parent = node.right
        old_left = new_parent.left
        new_parent.left = node 
        node.right = old_left
        return new_parent

    @classmethod
    def rotate_lr_at(cls, node : BstNode):
        node.left = AvlTree.rotate_l_at(node.left)
        return AvlTree.rotate_r_at(node)

    @classmethod
    def rotate_r_at(cls, node : BstNode):
        new_parent = node.left
        old_right = new_parent.right
        new_parent.right = node
        node.left = old_right
        return new_parent
    
    @classmethod
    def rotate_rl_at(cls, node : BstNode):
        node.right = AvlTree.rotate_r_at(node.right)
        return AvlTree.rotate_l_at(node)
    
    @classmethod
    def rebalance(cls, node : BstNode):
        if AvlTree.balance(node) > 1:
            # right subtree is too tall
            if AvlTree.height(node.right.right) > AvlTree.height(node.right.left):
                # right right
                # fix right subtree w left rotation
                return AvlTree.rotate_l_at(node)
            else:
                # right left
                # fix left subtree w right-left rotation
                return AvlTree.rotate_rl_at(node)
        elif AvlTree.balance(node) < -1:
            # left subtree is too tall
            if AvlTree.height(node.left.right) > AvlTree.height(node.left.left):
                # left right
                # fix left subtree w left-right rotation
                return AvlTree.rotate_lr_at(node)
            else:
                # left left
                # fix right subtree w right rotation
                return AvlTree.rotate_r_at(node)
        return node

def l_test():
    tree = AvlTree([3,1,5,6,7,-1,-2], False)
    tree.head.right = tree.rotate_l_at(tree.head.right)

    #     3
    #   1   6
    # -1   5  7

    tree.print()

def r_test():
    tree = AvlTree([3,1,5,6,7,-1,-2], False)
    tree.head.left = tree.rotate_r_at(tree.head.left)

    #      3
    #   -1    5
    # -2  1     6
    #             7

    tree.print()

def rl_test():
    tree = AvlTree([3,1,5,7,6,-1,0], False)
    tree.head.right = tree.rotate_rl_at(tree.head.right)
    #       3
    #     1   6
    #   -1   5  7
    #     0   
    tree.print()

def lr_test():
    tree = AvlTree([3,1,5,7,6,-1,0], False)
    tree.head.left = tree.rotate_lr_at(tree.head.left)
    #       3
    #     0   5
    #   -1  1   7
    #          6
    tree.print()

def autobalance_test():
    tree = AvlTree([3,1,5,6,7,-1,-2], True)
    #       3
    #     -1   6
    #   -2  1 5  7
    tree.remove(1)
    tree.remove(-1)
    tree.remove(-2)
    tree.print()

lr_test()