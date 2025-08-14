from queue import Queue
import queue, threading
class Signal:
    def __init__(self, type, msg, field = '') -> None:
        self.type = type # succ, fail
        self.msg = msg
        self.field = field
class Signal_Queue:
    def __init__(self) -> None:
        self.queue : Queue [Signal] = Queue()
        self.shutdown_signal = threading.Event()
        self.main_thread : threading.Thread = None

    def push(self, type, msg, field = ''):
        self.queue.put(Signal(type=type, msg=msg, field=field))
    def check(self):
        try:
            result = self.queue.get_nowait()
            return result
        except queue.Empty:
            return None
    def shutdown_is_set(self) -> bool:
        return self.shutdown_signal.is_set()
    def shutdown(self):
        self.shutdown_signal.set()
    def reset(self):
        self.shutdown_signal.clear()
        self.queue = Queue()