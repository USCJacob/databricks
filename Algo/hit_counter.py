from typing import Optional


class RollingCounter:
    def __init__(self, window_size: int = 300):
        self.window_size = window_size
        self.times = [0] * window_size
        self.counts = [0] * window_size

    def hit(self, timestamp: int) -> None:
        idx = timestamp % self.window_size

        if self.times[idx] != timestamp:
            self.times[idx] = timestamp
            self.counts[idx] = 1
        else:
            self.counts[idx] += 1

    def count(self, timestamp: int) -> int:
        total = 0
        for i in range(self.window_size):
            if 0 <= timestamp - self.times[i] < self.window_size:
                total += self.counts[i]
        return total

    def average(self, timestamp: int) -> float:
        return self.count(timestamp) / self.window_size


class KeyValueStore:
    def __init__(self):
        self.store = {}
        self.put_counter = RollingCounter()
        self.get_counter = RollingCounter()

    def put(self, key: str, value: str, timestamp: int) -> None:
        self.store[key] = value
        self.put_counter.hit(timestamp)

    def get(self, key: str, timestamp: int) -> Optional[str]:
        self.get_counter.hit(timestamp)
        return self.store.get(key)

    def average_put(self, timestamp: int) -> float:
        return self.put_counter.average(timestamp)

    def average_get(self, timestamp: int) -> float:
        return self.get_counter.average(timestamp)



class RollingCounter:
    def __init__(self, window_size: int = 300):
        self.window_size = window_size
        self.hits = [0] * window_size
        self.total = 0
        self.current_timestamp = -1

    def _advance(self, timestamp: int) -> None:
        if self.current_timestamp == -1:
            self.current_timestamp = timestamp
            return

        if timestamp <= self.current_timestamp:
            return

        if timestamp - self.current_timestamp >= self.window_size:
            self.hits = [0] * self.window_size
            self.total = 0
            self.current_timestamp = timestamp
            return

        while self.current_timestamp < timestamp:
            self.current_timestamp += 1
            idx = self.current_timestamp % self.window_size
            self.total -= self.hits[idx]
            self.hits[idx] = 0

    def hit(self, timestamp: int) -> None:
        self._advance(timestamp)
        idx = timestamp % self.window_size
        self.hits[idx] += 1
        self.total += 1

    def count(self, timestamp: int) -> int:
        self._advance(timestamp)
        return self.total

    def average(self, timestamp: int) -> float:
        return self.count(timestamp) / self.window_size