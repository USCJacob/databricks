def solve(background, block, offset):
    m, n = len(background), len(background[0])
    a, b = len(block), len(block[0])

    def ok(top):
        for i in range(a):
            for j in range(b):
                if block[i][j] == 0:
                    continue
                r, c = top + i, offset + j
                if c < 0 or c >= n or r >= m:
                    return False
                if r >= 0 and background[r][c] == 1:
                    return False
        return True

    top = -a
    while ok(top + 1):
        top += 1

    ans = [row[:] for row in background]
    for i in range(a):
        for j in range(b):
            if block[i][j] == 1 and top + i >= 0:
                ans[top + i][offset + j] = 1

    return top + a, ans