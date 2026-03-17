from threading import Lock, Condition, Event
import queue

class BlockingQueue:
    def __init__(self):
        self.queue = []
        self.lock = Lock()
        self.cv = Condition(self.lock)

    def put(self, item):
        with self.cv:
            self.queue.append(item)
            self.cv.notify()        # 唤醒等待的 get

    def get(self):
        with self.cv:
            while not self.queue:
                self.cv.wait()      # 没数据就等
            return self.queue.pop(0)


class Request:
    def __init__(self, data):
        self.data = data
        self.done = Event()
        self.success = False


class DataWriter:
    def __init__(self, path):
        self.file = open(path, "ab")
        self.q = queue.Queue()
        start_background_thread(self.writer_loop)
        self.failed = Event()

    def push(self, data):
        if self.failed.is_set():
            raise IOError
        req = Request(data)
        self.q.put(req)
        if not req.done.wait(timeout=5):
            raise TimeoutError
        if not req.success:
            raise IOError

    def writer_loop(self):
        BATCH_SIZE = 64
        while True:
            batch = [self.q.get()]
            while len(batch) < BATCH_SIZE:
                try:
                    req = self.q.get_nowait()
                    batch.append(req)
                except queue.Empty:
                    break


            payload = b"".join(self.encode(r.data) for r in batch)

            try:
                write(self.file, payload)
                fdatasync(self.file)
            except:
                self.failed.set()
                for r in batch:
                    r.success = False
                    r.done.set()
                while True:
                    try:
                        req = self.q.get_nowait()
                        if req is not None:
                            req.success = False
                            req.done.set()
                    except queue.Empty:
                        break
                return

            for r in batch:
                r.success = True
                r.done.set()

    def encode(self, data):
        body = int_to_4bytes(len(data)) + data
        return MAGIC + body + crc32(body)

    def recover(path):
        pos = 0
        while True:
            rec = try_read_one_record(path, pos)
            if rec is INVALID:
                break
            replay(rec.data)
            pos = rec.end_offset

        truncate(path, pos)