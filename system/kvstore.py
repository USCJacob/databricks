class Request:
    key
    value
    done = Event()
    success = False

class ShardedMemtable:
    def __init__(self, num_shards=16):
        self.shards = [{} for _ in range(num_shards)]
        self.locks  = [Lock() for _ in range(num_shards)]
        self.n      = num_shards

    def _shard(self, key):
        return hash(key) % self.n       # key 决定去哪个 shard

    def get(self, key):
        i = self._shard(key)
        with self.locks[i]:
            return self.shards[i].get(key)

    def put(self, key, value):
        i = self._shard(key)
        with self.locks[i]:
            self.shards[i][key] = value


class KVStore:
    def __init__(self, path):
        self.memtable = {}
        self.queue    = BlockingQueue()
        self.wal      = open_append_only(path)
        start_thread(self.writer_loop)

    def put(key, value):
        req = Request(key, value)
        queue.put(req)
        req.done.wait()
        if not req.success:
            raise IOError

    def get(key):
        return memtable.get(key)

    def writer_loop():
        while True:
            # 1. 收集 batch
            batch = [queue.get()]
            while len(batch) < MAX_BATCH:
                try:
                    batch.append(queue.get_nowait())
                except Empty:
                    break

            # 2. 写 WAL
            payload = concat(encode(r.key, r.value) for r in batch)
            try:
                write(wal, payload)
                fdatasync(wal)
                success = True
            except:
                success = False

            # 3. 唤醒等待线程
            for req in batch:
                req.success = success
                if success:
                    memtable[req.key] = req.value  # 落盘后再更新内存
                req.done.set()

            # 4. 失败则退出
            if not success:
                while queue not empty:
                    req = queue.get_nowait()
                    req.success = False
                    req.done.set()
                return