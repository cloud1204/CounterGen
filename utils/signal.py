from queue import Queue
import queue
class Signal:
    def __init__(self, type, msg, field = '') -> None:
        self.type = type # succ, fail
        self.msg = msg
        self.field = field
class Signal_Queue:
    def __init__(self) -> None:
        self.queue : Queue [Signal] = Queue()

    def push(self, type, msg, field = ''):
        self.queue.put(Signal(type=type, msg=msg, field=field))
    def check(self):
        try:
            result = self.queue.get_nowait()
            return result
        except queue.Empty:
            return None