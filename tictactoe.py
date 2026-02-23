from typing import List, Optional

class TicTacToe:
    def __init__(self, n: int, m: int, k: int):
        # TODO: Initialize TicTacToe
        self.n = n
        self.m = m
        self.k = k
        self.board = [[0] * m for _ in range(n)]


    def move(self, row: int, col: int, player: int) -> int:
        # TODO: Implement move logic
        DIRS = [(1, 0), (0, 1), (1, 1), (1, -1)]
        self.board[row][col] = player
        for dr, dc in DIRS:
            if self._is_kconsecutive(row, col, player, dr, dc):
                return player
        return 0


    def _is_kconsecutive(self, row, col, player, dr, dc):
        count = 1
        nr, nc = row + dr, col + dc
        while 0 <= nr < self.n and 0 <= nc < self.m and self.board[nr][nc] == player:
            count += 1
            nr += dr
            nc += dc
        nr, nc = row - dr, col - dc
        while 0 <= nr < self.n and 0 <= nc < self.m and self.board[nr][nc] == player:
            count += 1
            nr -= dr
            nc -= dc
        return count == self.k

# Test case 1: 水平 3 连赢（3x4 board, k=3）
game1 = TicTacToe(3, 4, 3)

print(game1.move(0, 0, 1))  # 0
print(game1.move(1, 0, 2))  # 0
print(game1.move(0, 1, 1))  # 0
print(game1.move(1, 1, 2))  # 0
print(game1.move(0, 2, 1))  # 1  <- player 1 在第0行形成水平3连，获胜
