from collections import deque

class ShortTermMemory:
    def __init__(self, max_items: int = 5):
        self.max_items = max_items
        self._dq = deque(maxlen=max_items)

    def add(self, item: str):
        self._dq.append(item)

    def get_all(self):
        return list(self._dq)

    def clear(self):
        self._dq.clear()
