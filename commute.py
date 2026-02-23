import heapq
from collections import deque
from typing import List, Optional

#Time: O (mnk) Space: O(mn)
class Solution:
    def findOptimalCommute(self, grid: List[List[str]], modes: List[str], costs: List[int], times: List[int]) -> str:
        m, n = len(grid), len(grid[0])
        start, dest = (-1,-1), (-1,-1)
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 'S':
                    start = (i, j)
                elif grid[i][j] == 'D':
                    dest = (i, j)
        DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def bfs(mode_idx):
            nonlocal start
            mode_char = str(mode_idx + 1)
            q = deque([(start[0], start[1], 0)])
            visited = set([start])

            while q:
                x, y, blocks = q.popleft()
                for dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < m and 0 <= ny < n):
                        continue
                    if (nx, ny) in visited:
                        continue
                    cell = grid[nx][ny]
                    if cell == "D":
                        return blocks
                    elif cell == mode_char:
                        visited.add((nx, ny))
                        q.append((nx, ny, blocks + 1))
            return -1

        total = float('inf')
        ans = -1
        for i in range(len(modes)):
            t = bfs(i)
            if t < total:
                ans = i
                total = t
        if ans == -1:
            return "IMPOSSIBLE"
        return modes[ans]



grid = [["3", "3", "S", "2", "X", "X"],
        ["3", "1", "1", "2", "X", "2"],
        ["3", "1", "1", "2", "2", "2"],
        ["3", "1", "1", "1", "D", "3"],
        ["3", "3", "3", "3", "3", "4"],
        ["4", "4", "4", "4", "4", "4"]]
modes = ["Walk", "Bike", "Car", "Train"]
costs = [0, 1, 3, 2]
times = [3, 2, 1, 1]
print(Solution().findOptimalCommute(grid, modes, costs, times))



#Time: O(mnklog(mnk)) Space: O(mnk)
def findOptimalCommutewithswitch(grid, modes, costs, times, x):
    m, n = len(grid), len(grid[0])
    start, dest = (-1, -1), (-1, -1)
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'D':
                dest = (i, j)
    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    INF = (float('inf'), float('inf'))
    dist = {}
    dist[(start[0], start[1], -1)] = (0, 0)
    pq = [(0, 0, start[0], start[1], -1)]

    while pq:
        time, cost, r, c, prev = heapq.heappop(pq)
        state = (r, c, prev)
        if dist.get(state, INF) != (time, cost):
            continue
        if (r, c) == dest:
            return [time, cost]
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= m or nc < 0 or nc >= n:
                continue
            if grid[nr][nc] == "S" or grid[nr][nc] == 'X':
                continue
            if grid[nr][nc] == "D":
                next_state = (nr, nc, prev)
                next_pair = (time, cost)
                if next_pair < dist.get(next_state, INF):
                    dist[next_state] = next_pair
                    heapq.heappush(pq, (time, cost, nr, nc, prev))
                continue

            else:
                mode = int(grid[nr][nc]) - 1
                ntime = time + times[mode]
                ncost = cost + costs[mode]
                if prev != -1 and mode != prev:
                    ncost += x
                old_time, old_cost = dist.get((nr, nc, mode), INF)
                if (ntime, ncost) < (old_time, old_cost):
                    dist[(nr, nc, mode)] = (ntime, ncost)
                    heapq.heappush(pq,(ntime, ncost, nr, nc, mode))
    return [-1, -1]

grid = [["3", "3", "S", "2", "X", "X"],
        ["3", "1", "1", "2", "X", "2"],
        ["3", "1", "1", "2", "2", "2"],
        ["3", "1", "1", "1", "D", "3"],
        ["3", "3", "3", "3", "3", "4"],
        ["4", "4", "4", "4", "4", "4"]]
modes = ["Walk", "Bike", "Car", "Train"]
costs = [0, 1, 3, 2]
times = [3, 2, 1, 1]
print(findOptimalCommutewithswitch(grid, modes, costs, times, 1))