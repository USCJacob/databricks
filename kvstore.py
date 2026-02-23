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

    def count_last_5min(self, timestamp: int) -> int:
        total = 0
        for i in range(self.window_size):
            if timestamp - self.times[i] < self.window_size:
                total += self.counts[i]
        return total

    def average(self, timestamp: int) -> float:
        return self.count_last_5min(timestamp) / float(self.window_size)


class KeyValue:
    def __init__(self):
        self.kv = {}
        self.put_calls = RollingCounter()
        self.get_calls = RollingCounter()

    def put(self, key: str, value: str, timestamp: int) -> None:
        self.kv[key] = value
        self.put_calls.hit(timestamp)

    def get(self, key: str, timestamp: int) -> Optional[str]:
        self.get_calls.hit(timestamp)
        return self.kv.get(key)

    def averagePut(self, timestamp: int) -> float:
        return self.put_calls.average(timestamp)

    def averageGet(self, timestamp: int) -> float:
        return self.get_calls.average(timestamp)