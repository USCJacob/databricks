from collections import defaultdict
from queue import Queue
import threading


class UserSession:
    def __init__(self, conn):
        self.conn = conn
        self.inbox = Queue()
        self.alive = True


class ChatServer:
    def __init__(self):
        self.channel_subscribers = defaultdict(set)   # channel -> users
        self.user_sessions = {}                       # user -> session
        self.lock = threading.Lock()

    def connect(self, user, conn):
        session = UserSession(conn)
        with self.lock:
            self.user_sessions[user] = session
        threading.Thread(target=self.delivery_loop, args=(session,), daemon=True).start()

    def subscribe(self, user, channel):
        with self.lock:
            self.channel_subscribers[channel].add(user)

    def unsubscribe(self, user, channel):
        with self.lock:
            self.channel_subscribers[channel].discard(user)

    def publish(self, sender, channel, content):
        msg = f"[{channel}] {sender}: {content}"

        with self.lock:
            subscribers = list(self.channel_subscribers[channel])

        for user in subscribers:
            with self.lock:
                session = self.user_sessions.get(user)
            if session and session.alive:
                session.inbox.put(msg)

    def delivery_loop(self, session):
        while session.alive:
            msg = session.inbox.get()
            session.conn.send(msg)