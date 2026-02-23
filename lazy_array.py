class LazyArray:
    def __init__(self, arr, funcs = None):
        # TODO: Implement __init__ logic.
        self.arr = arr
        self.funcs = funcs[:] if funcs else []

    def map(self, fn):
        # TODO: Implement map logic.
        return LazyArray(self.arr, self.funcs + [fn])

    def indexOf(self, target):
        # TODO: Implement indexOf logic.
        for i, x in enumerate(self.arr):
            val = x
            for fn in self.funcs:
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