from typing import List
from heapq import heappush, heapreplace
from collections import deque


class RevenueSystem:
    def __init__(self):
        self.revenues: List[int] = []

        self.children: List[List[int]] = []

    def add(self, revenue: int) -> int:
        customer_id = len(self.revenues)
        self.revenues.append(revenue)
        self.children.append([])
        return customer_id

    def addByReferral(self, revenue: int, referrerId: int) -> int:
        if referrerId < 0 or referrerId >= len(self.revenues):
            return -1

        customer_id = len(self.revenues)
        self.revenues.append(revenue)
        self.children.append([])

        self.revenues[referrerId] += revenue

        self.children[referrerId].append(customer_id)

        return customer_id

    def getTopKCustomer(self, k: int, minRevenue: int) -> List[int]:
        if k <= 0:
            return []

        pq = []  # min-heap of (revenue, id)

        for cid, rev in enumerate(self.revenues):
            if rev < minRevenue:
                continue

            if len(pq) < k:
                heappush(pq, (rev, cid))
            elif rev > pq[0][0]:
                heapreplace(pq, (rev, cid))

        pq.sort(key=lambda x: (-x[0], x[1]))
        return [cid for rev, cid in pq]

    def getRelations(self, customerId: int) -> List[List[int]]:
        if customerId < 0 or customerId >= len(self.revenues):
            return []

        if not self.children[customerId]:
            return []

        result: List[List[int]] = []

        q = deque(self.children[customerId])

        while q:
            level_size = len(q)
            level_nodes = []

            for _ in range(level_size):
                node = q.popleft()
                level_nodes.append(node)

                for child in self.children[node]:
                    q.append(child)

            level_nodes.sort()
            result.append(level_nodes)

        return result