import heapq
from collections import deque
from typing import List, Optional

#Time: O (mn) Space: O(mn)

def findOptimalCommute(grid: List[List[str]], modes: List[str], costs: List[int], times: List[int]) -> str:
    m, n = len(grid), len(grid[0])
    start = (-1, -1)

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'S':
                start = (i, j)
                break

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def bfs(mode_idx: int) -> int:
        mode_char = str(mode_idx + 1)
        q = deque([(start[0], start[1], 0)])   # (r, c, blocks_used)
        visited = [[False] * n for _ in range(m)]
        visited[start[0]][start[1]] = True

        while q:
            r, c, used = q.popleft()

            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < m and 0 <= nc < n):
                    continue
                if visited[nr][nc]:
                    continue

                cell = grid[nr][nc]
                if cell == 'X':
                    continue
                if cell == 'D':
                    return used
                if cell == mode_char:
                    visited[nr][nc] = True
                    q.append((nr, nc, used + 1))

        return -1

    best_mode = ""
    best_pair = (float('inf'), float('inf'))

    for i in range(len(modes)):
        blocks = bfs(i)
        if blocks == -1:
            continue
        pair = (blocks * times[i], blocks * costs[i])
        if pair < best_pair:
            best_pair = pair
            best_mode = modes[i]

    return best_mode

grid = [["3", "3", "S", "2", "X", "X"],
        ["3", "1", "1", "2", "X", "2"],
        ["3", "1", "1", "2", "2", "2"],
        ["3", "1", "1", "1", "D", "3"],
        ["3", "3", "3", "3", "3", "4"],
        ["4", "4", "4", "4", "4", "4"]]
modes = ["Walk", "Bike", "Car", "Train"]
costs = [0, 1, 3, 2]
times = [3, 2, 1, 1]
print(findOptimalCommute(grid, modes, costs, times))



#Time: O(mnklog(mnk)) Space: O(mnk)
import heapq

def findOptimalCommutewithswitch(grid, modes, costs, times, x):
    m, n = len(grid), len(grid[0])
    start = dest = (-1, -1)

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'D':
                dest = (i, j)

    if start == (-1, -1) or dest == (-1, -1):
        return [-1, -1]

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    INF = (float('inf'), float('inf'))

    dist = {(start[0], start[1], -1): (0, 0)}
    pq = [(0, 0, start[0], start[1], -1)]  # (time, cost, r, c, prev_mode)

    while pq:
        time, cost, r, c, prev_mode = heapq.heappop(pq)

        if dist.get((r, c, prev_mode), INF) != (time, cost):
            continue

        if (r, c) == dest:
            return [time, cost]

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < m and 0 <= nc < n):
                continue

            cell = grid[nr][nc]
            if cell == 'X' or cell == 'S':
                continue

            if cell == 'D':
                next_state = (nr, nc, prev_mode)
                next_pair = (time, cost)
                if next_pair < dist.get(next_state, INF):
                    dist[next_state] = next_pair
                    heapq.heappush(pq, (time, cost, nr, nc, prev_mode))
                continue

            mode = int(cell) - 1
            next_time = time + times[mode]
            next_cost = cost + costs[mode]
            if prev_mode != -1 and mode != prev_mode:
                next_cost += x

            next_state = (nr, nc, mode)
            next_pair = (next_time, next_cost)

            if next_pair < dist.get(next_state, INF):
                dist[next_state] = next_pair
                heapq.heappush(pq, (next_time, next_cost, nr, nc, mode))

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