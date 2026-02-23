from typing import List, Optional
from heapq import heappush, heappop
class RevenueSystem:
    def __init__(self, ):
        # TODO: Initialize RevenueSystem
        self.revenues = []

    def add(self, revenue: int) -> int:
        # TODO: Implement add logic
        self.revenues.append(revenue)
        return len(self.revenues) - 1

    def addByReferral(self, revenue: int, referrerId: int) -> int:
        # TODO: Implement addByReferral logic
        if referrerId < 0 or referrerId >= len(self.revenues):
            return -1
        self.revenues.append(revenue)
        self.revenues[referrerId] += revenue
        return len(self.revenues) - 1


    def getTopKCustomer(self, k: int, minRevenue: int) -> List[int]:
        # TODO: Implement getTopKCustomer logic
        pq = []
        for i in range(len(self.revenues)):
            if self.revenues[i] >= minRevenue:
                if len(pq) < k: 
                    heappush(pq, (self.revenues[i], i))
                elif self.revenues[i] > pq[0][0]:
                    heappop(pq)
                    heappush(pq, (self.revenues[i], i))
        pq.sort(key = lambda x: x[0], reverse = True)
        return [cid for rev, cid in pq]