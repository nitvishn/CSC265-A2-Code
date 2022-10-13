from tree import Tree 

class TreeNode(Tree):

    def __init__(self, key: int) -> None:
        self.key = key
        self.parent = None
        self.left = None
        self.right = None

    def search(self, k):
        assert self.right is not None or self.left is None # property 2

        if self.right is None:
            return self
        elif self.right.key <= k or self.left is None:
            return self.right.search(k)
        else:
            return self.left.search(k)

    def successor(self):
        assert self.isLeaf() # this is a leaf node

        if self.parent is None:
            return None


        prev = self
        curr = self.parent
        while curr.right == prev:
            prev = curr
            curr = curr.parent 
            if curr is None:
                return None

        curr = curr.right

       
        
        while not curr.isLeaf():
            if curr.left:
                curr = curr.left
            else:
                curr = curr.right
        
        return curr

    def getRightNeighbour(self):
        if self.parent is None:
            return None
        
        prev = self
        curr = self.parent
        count = 1
        while curr.right == prev:
            prev = curr
            curr = curr.parent 
            if curr is None:
                return None
            count += 1

        curr = curr.right
        count -= 1

        while count > 0:
            if curr.left:
                curr = curr.left
            else:
                curr = curr.right
            count -= 1

        return curr


def insert(T: TreeNode, k: int):
    """
    Inserts a node with key k into the tree T and returns a pointer to the 
    (new) root of T.
    """

    if T.isLeaf(): # T is a leaf node
        min_val = min(T.key, k)
        max_val = max(T.key, k)
        T.key = min_val
        T.addRightNode(TreeNode(max_val))
        T.addLeftNode(TreeNode(min_val))
        return T

    found = T.search(k)

    curr = TreeNode(k)

    # Set left and right neighbours.
    
    if k < found.key: # Case D, k is the minimum element.

        left_neighbour = None
        right_neighbour = found
    
    else: # Case A!!!
        
        left_neighbour = found
        right_neighbour = found.successor()

        if left_neighbour and right_neighbour and left_neighbour.parent == right_neighbour.parent:

            new_right_neighbour = right_neighbour.getRightNeighbour()

            p = left_neighbour.parent
            p.addRightNode(curr)
            right_neighbour.parent = None
            left_neighbour = curr
            curr = right_neighbour
            right_neighbour = new_right_neighbour # need to get new right neighbour!

    merged = False 

    while not merged: 

        # grow the tree up one node 
        grown = TreeNode(curr.key)
        grown.addRightNode(curr)
        curr = grown

        assert left_neighbour or right_neighbour

        if left_neighbour and not right_neighbour:
            position = "right"
        elif right_neighbour and not left_neighbour:
            position = "left"
        elif right_neighbour and left_neighbour:
            position = "middle"

        left_neighbour = left_neighbour.parent if left_neighbour else None
        right_neighbour = right_neighbour.parent if right_neighbour else None

        # start checking cases
        if right_neighbour and curr.left is None and right_neighbour.left is None:
            """
            violation I, current subtree and right neighbour both have one node.
            we can merge them, and then forget about curr. No other violations may 
            have been caused at this depth of the tree.
            """
            right_neighbour.addLeftNode(curr.right)
            merged = True
        elif left_neighbour and curr.left is None and left_neighbour.left is None:
            """
            violation II, current subtree and left neighbour both have one node.
            We can merge them, and then forget about curr. No other violations
            caused at this depth.
            """
            left_neighbour.addLeftNode(left_neighbour.right)
            left_neighbour.addRightNode(curr.right)
            merged = True
        elif left_neighbour is None and right_neighbour is None:        
            if position == "left":
                curr.addLeftNode(curr.right)
                curr.addRightNode(T)
            else:
                curr.addLeftNode(T)
            return curr 
        elif right_neighbour is None and curr.left is None:
            """
            we know that left_neighbour has two children.
            
            If it is the root node, then no worries.

            If it is not the root node, it has a left sibling.
            (its parent cannot have just one right child because it is at
            the end of the sequence at its depth.) Either that left sibling
            has one or two children.
            """

            if left_neighbour.parent is None:
                curr.addLeftNode(left_neighbour.right)
                left_neighbour.addRightNode(left_neighbour.left)
                left_neighbour.left = None
            else:
                left_sibling = left_neighbour.parent.left
                if left_sibling.left is not None: # case 1
                    curr.addLeftNode(left_neighbour.right)
                    left_neighbour.addRightNode(left_neighbour.left)
                    left_neighbour.left = None
                else:
                    left_sibling.addLeftNode(left_sibling.right)
                    left_sibling.addRightNode(left_neighbour.left)
                    left_neighbour.addLeftNode(left_neighbour.right)
                    left_neighbour.addRightNode(curr.right)
                    merged = True
        elif left_neighbour and right_neighbour and left_neighbour.parent == right_neighbour.parent:

            new_right_neighbour = right_neighbour.getRightNeighbour()
            p = left_neighbour.parent
            p.addRightNode(curr)
            right_neighbour.parent = None
            left_neighbour = curr
            curr = right_neighbour
            right_neighbour = new_right_neighbour # need to get new right neighbour!



    
    return T
            
            
                


        


# root = TreeNode(4)
# root.left = TreeNode(4)
# root.right = TreeNode(12)
# root.left.parent = root
# root.right.parent = root

# # root.right.addLeftNode(TreeNode(8))
# root.right.addRightNode(TreeNode(12))

# # root.left.left = TreeNode(2)
# root.left.right = TreeNode(4)
# # root.left.left.parent = root.left
# root.left.right.parent = root.left

# root.display()

# # node = root.left.right
# # print(node.getRightNeighbour())

import random

root = TreeNode(1)

vals = []
for i in range(20):
    vals.append(random.randint(1, 100))

# vals = [1, 8, 11, 14]

for val in vals:
    print(f"Inserting {val} into T.")
    root = insert(root, val)
    root.display()
    print(vals)