#Time: O(order), Space: O(order)
def solve(order, source, target):
    subtrees = [0] * (order + 1)
    subtrees[0] = 1
    subtrees[1] = 1

    for i in range(2, order + 1):
        subtrees[i] = 1 + subtrees[i - 1] + subtrees[i - 2]

    def findpath(curr, curr_order, target):
        if curr == target:
            return ""
        leftsize = subtrees[curr_order - 2]
        rightsize = subtrees[curr_order - 1]
        if target > curr + leftsize:
            return "r" + findpath(curr + leftsize + 1, curr_order - 1, target)
        else:
            return "l" + findpath(curr + 1, curr_order - 2, target)

    a = findpath(0, order, source)
    b = findpath(0, order, target)

    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1

    return "U" * len(a[i:]) + b[i:]


order = 5
source = 5
dest = 7
# expected = "RR"
print(solve(order, source, dest))