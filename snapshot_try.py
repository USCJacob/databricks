from typing import Dict, List, Iterator


class SnapshotSet:
    class _Node:
        def __init__(self, val, born):
            self.val = val
            self.born = born
            self.dead = None
            self.next = None

    class SnapshotIterator:
        def __init__(self, outer: 'SnapshotSet'):
            self._cur = outer._head
            self._snap = outer.version
            self._advance_to_valid()

        def _is_visible_in_snapshot(self, node):
            if node is None:
                return False
            if node.dead and node.dead <= self._snap:
                return False
            if node.born > self._snap:
                return False
            return True

        def _advance_to_valid(self):
            while self._cur and self._is_visible_in_snapshot(self._cur):
                self._cur = self._cur.next

        def __iter__(self):
            return self

        def __next__(self):
            if not self.hasnext():
                raise ValueError("wrong")
            ans = self._cur.val
            self._cur = self._cur.next
            self._advance_to_valid()
            return ans

        def hasnext(self):
            return self._cur.next is not None

    def __init__(self):
        self.version = 0
        self._live: Dict[int, SnapshotSet._Node] = {}
        self._head = None
        self._tail = None

    def add(self, val):
        if val in self._live:
             return False
        node = SnapshotSet._Node(val, self.version)
        self.version += 1
        if self._head is None and self._tail is None:
            self._head = self._tail = node
        elif self._head and self._tail:
            self._tail.next = node
            self._tail = self._tail.next

    def remove(self, val):
        if val not in self._live:
            return False
        node = self._live[val]
        node.dead = self.version

    def contains(self, val):
        if val in self._live and self._live[val].dead is not None:
            return True
        return False

    def getIterator(self) -> Iterator[int]:
        # Snapshot = current version (the state "now")
        return SnapshotSet.SnapshotIterator(self)


def iterateAllElements(it) -> List[int]:
    return list(it)

def test1():
    print("======== test 1: =========")
    s = SnapshotSet()
    print(s.add(1))  # Expected: True
    print(s.add(2))  # Expected: True
    print(s.add(3))  # Expected: True
    print(s.add(4))  # Expected: True
    print(s.add(1))  # Expected: False
    it1 = s.getIterator()
    print(s.remove(1))  # Expected: True
    print(s.remove(3))  # Expected: True
    print(s.remove(5))  # Expected: False
    it2 = s.getIterator()

    print(iterateAllElements(it1))  # Expected: [1, 2, 3, 4]
    print(iterateAllElements(it2))  # Expected: [2, 4]

test1()




