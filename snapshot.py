from typing import Dict, List, Iterator, Optional


class SnapshotSet:
    class _Node:
        __slots__ = ("val", "born", "dead", "next")

        def __init__(self, val: int, born: int):
            self.val = val
            self.born = born           # version when this insertion happened
            self.dead = None           # version when removed (exclusive), None if still alive
            self.next = None           # next node in global append-only insertion history

    def __init__(self):
        # Global version, incremented only on successful add/remove
        self._version: int = 0

        # Current live elements: value -> latest live node
        self._live: Dict[int, SnapshotSet._Node] = {}

        # Append-only linked list of all successful insertions (preserves insertion order history)
        self._head: Optional[SnapshotSet._Node] = None
        self._tail: Optional[SnapshotSet._Node] = None

    def add(self, n: int) -> bool:
        # Already present in current set
        if n in self._live:
            return False

        self._version += 1
        node = SnapshotSet._Node(n, self._version)

        if self._head is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node

        self._live[n] = node
        return True

    def remove(self, n: int) -> bool:
        node = self._live.get(n)
        if node is None:
            return False

        self._version += 1
        node.dead = self._version
        del self._live[n]
        return True

    def contains(self, n: int) -> bool:
        return n in self._live

    def getIterator(self) -> Iterator[int]:
        # Snapshot = current version (the state "now")
        return SnapshotSet.SnapshotIterator(self)

    class SnapshotIterator:
        def __init__(self, outer: 'SnapshotSet'):
            # Freeze snapshot version at creation time
            self._snap = outer._version
            self._cur = outer._head
            self._advance_to_valid()

        def _is_visible_in_snapshot(self, node: Optional['SnapshotSet._Node']) -> bool:
            if node is None:
                return False
            # visible iff born <= snap and (not dead yet at snap)
            if node.born > self._snap:
                return False
            if node.dead is not None and node.dead <= self._snap:
                return False
            return True

        def _advance_to_valid(self) -> None:
            while self._cur is not None and not self._is_visible_in_snapshot(self._cur):
                self._cur = self._cur.next

        def __iter__(self) -> 'SnapshotSet.SnapshotIterator':
            return self

        def __next__(self) -> int:
            if self._cur is None:
                raise StopIteration
            ans = self._cur.val
            self._cur = self._cur.next
            self._advance_to_valid()
            return ans

        def hasNext(self) -> bool:
            return self._cur is not None


# Helper function to iterate all elements in the iterator for easier visualization
def iterateAllElements(it: Iterator[int]) -> List[int]:
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


def test2():
    print("======== test 2: =========")
    s = SnapshotSet()
    it1 = s.getIterator()
    print(s.add(10))  # Expected: True
    it2 = s.getIterator()
    print(s.add(20))  # Expected: True
    it3 = s.getIterator()
    print(s.add(30))  # Expected: True
    it4 = s.getIterator()
    print(s.remove(30))  # Expected: True
    it5 = s.getIterator()
    print(s.remove(20))  # Expected: True
    it6 = s.getIterator()
    print(s.remove(10))  # Expected: True
    it7 = s.getIterator()

    print(iterateAllElements(it1))  # Expected: []
    print(iterateAllElements(it2))  # Expected: [10]
    print(iterateAllElements(it3))  # Expected: [10, 20]
    print(iterateAllElements(it4))  # Expected: [10, 20, 30]
    print(iterateAllElements(it5))  # Expected: [10, 20]
    print(iterateAllElements(it6))  # Expected: [10]
    print(iterateAllElements(it7))  # Expected: []


def test3():
    print("======== test 3: =========")
    s = SnapshotSet()
    print(s.remove(5))  # Expected: False
    print(s.add(5))  # Expected: True
    print(s.remove(5))  # Expected: True
    print(s.add(5))  # Expected: True
    print(iterateAllElements(s.getIterator()))  # Expected: [5]


def test4():
    print("======== test 4: =========")
    s = SnapshotSet()
    print(s.add(1))  # Expected: True
    print(s.add(2))  # Expected: True
    print(s.add(3))  # Expected: True
    print(s.add(4))  # Expected: True
    print(s.add(5))  # Expected: True
    it1 = s.getIterator()
    print(s.remove(2))  # Expected: True
    print(s.remove(4))  # Expected: True
    print(s.add(6))  # Expected: True
    it2 = s.getIterator()
    print(iterateAllElements(it1))  # Expected: [1, 2, 3, 4, 5]
    print(iterateAllElements(it2))  # Expected: [1, 3, 5, 6]


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()