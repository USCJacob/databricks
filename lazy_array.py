from typing import Callable, List


class LazyArray:
    def __init__(self, arr: List[int], funcs=None):
        self.arr = arr
        self.funcs = funcs if funcs is not None else []

    def map(self, fn: Callable[[int], int]) -> "LazyArray":
        return LazyArray(self.arr, self.funcs + [fn])

    def indexOf(self, target: int) -> int:
        for i, x in enumerate(self.arr):
            val = x
            for fn in self.funcs:
                val = fn(val)
            if val == target:
                return i
        return -1

from typing import Callable, List, Optional


class LazyArray:
    def __init__(
        self,
        arr: List[int],
        fn: Optional[Callable[[int], int]] = None,
        prev: Optional["LazyArray"] = None
    ):
        self.arr = arr
        self.fn = fn
        self.prev = prev

    def map(self, fn: Callable[[int], int]) -> "LazyArray":
        return LazyArray(self.arr, fn, self)

    def _collect_funcs(self):
        funcs = []
        cur = self
        while cur is not None and cur.fn is not None:
            funcs.append(cur.fn)
            cur = cur.prev
        funcs.reverse()
        return funcs

    def indexOf(self, target: int) -> int:
        funcs = self._collect_funcs()
        for i, x in enumerate(self.arr):
            val = x
            for fn in funcs:
                val = fn(val)
            if val == target:
                return i
        return -1


if __name__ == "__main__":
    # Test case 1
    arr1 = LazyArray([10, 20, 30, 40, 50])
    print(arr1.map(lambda n: n * 2).indexOf(40))  # Expected: 1

    # Test case 2
    arr2 = LazyArray([10, 20, 30, 40, 50])
    print(arr2.map(lambda n: n * 2).map(lambda n: n * 3).indexOf(240))  # Expected: 3

    # Test case 3
    arr3 = LazyArray([1, 2, 3, 4, 5])
    print(arr3.map(lambda n: n + 10).indexOf(100))  # Expected: -1

    # Test case 4
    arr4 = LazyArray([5, 10, 15, 20, 25])
    print(arr4.map(lambda n: n * 2).map(lambda n: n + 5).map(lambda n: n // 3).indexOf(11))  # Expected: 2

    # Test case 5
    arr5 = LazyArray([-5, 1, 2, -1, 10])
    print(arr5.map(lambda n: n * 3).map(lambda n: n + 4).map(lambda n: n - 2).indexOf(8))  # Expected: 2