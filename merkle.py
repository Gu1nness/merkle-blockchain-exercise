"""
Author : Neha Oudin
Licence : GPLv3
Date : 01/03/2021

A simple Merkle Tree implementation
"""

from typing import List
import hashlib

class Node:
    def __init__(self, left, right, value: str) -> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value

    @staticmethod
    def hash(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    @staticmethod
    def fullhash(val: str) -> str:
        return Node.hash(Node.hash(val))

class MerkleTree:
    def __init__(self, values: List[str]) -> None:
        self.root = None
        self._buildtree(values)

    def _buildtree(self, values: List[str]) -> None:
        leaves: List[Node] = [Node(None, None, Node.fullhash(elt)) for elt in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[:-1][0]) # duplicate last element for even number of leaves
        self.root: Node = self._buildtreerec(leaves)

    def _buildtreerec(self, nodes: List[Node]) -> Node:
        split: int = len(nodes) // 2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.fullhash(nodes[0].value + nodes[1].value))

        left_branch: Node = self._buildtreerec(nodes[:split])
        right_branch: Node = self._buildtreerec(nodes[split:])
        value: str = Node.fullhash(left_branch.value + right_branch.value)

        return Node(left_branch, right_branch, value)

    def printtree(self) -> None:
        self._printtreerec(self.root)

    def _printtreerec(self, node, offset='|') -> None:
        if node is not None:
            print("%s%s" % (offset,node.value))
            self._printtreerec(node.left, offset= offset + " " * 4  + "|")
            self._printtreerec(node.right, offset= offset + " " * 4 + "|")
        # Nothing to do otherwise

    @property
    def getroothash(self)-> str:
        return self.root.value

def test() -> None:
    elems = ["Hello", "Mx", "Neha"]
    mtree = MerkleTree(elems)
    mtree.printtree()
    print()
    print("Root hash is %s" % mtree.getroothash)

if __name__ == "__main__":
    test()
