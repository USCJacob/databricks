from typing import List
from heapq import heappush, heapreplace
from collections import deque


class RevenueSystem:
    def __init__(self):
        # total revenue for each customer id
        self.revenues: List[int] = []

        # referral tree: children[parent] = list of directly referred customer ids
        self.children: List[List[int]] = []

    def add(self, revenue: int) -> int:
        customer_id = len(self.revenues)
        self.revenues.append(revenue)
        self.children.append([])  # this customer currently has no referrals
        return customer_id

    def addByReferral(self, revenue: int, referrerId: int) -> int:
        if referrerId < 0 or referrerId >= len(self.revenues):
            return -1

        # create new customer
        customer_id = len(self.revenues)
        self.revenues.append(revenue)
        self.children.append([])

        # revenue update for referrer (direct referral only)
        self.revenues[referrerId] += revenue

        # maintain referral relationship
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

        # sort top-k candidates into descending order by revenue
        # tie-break by smaller id first (optional but deterministic)
        pq.sort(key=lambda x: (-x[0], x[1]))
        return [cid for rev, cid in pq]

    def getRelations(self, customerId: int) -> List[List[int]]:
        # invalid customer
        if customerId < 0 or customerId >= len(self.revenues):
            return []

        # no referrals
        if not self.children[customerId]:
            return []

        result: List[List[int]] = []

        # BFS starts from level-1 nodes (direct children)
        q = deque(self.children[customerId])

        while q:
            level_size = len(q)
            level_nodes = []

            for _ in range(level_size):
                node = q.popleft()
                level_nodes.append(node)

                # enqueue next level
                for child in self.children[node]:
                    q.append(child)

            # requirement: IDs sorted ascending within each level
            level_nodes.sort()
            result.append(level_nodes)

        return result