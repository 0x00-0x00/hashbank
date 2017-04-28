class Queue(object):
    def __init__(self, max_items=200):
        self.tasks = list()
        self.is_empty = self._is_empty()
        self.max_items = max_items

    def pop(self):
        return self.tasks.pop()

    def push(self, item):
        return self.tasks.append(item)

    def _is_empty(self):
        return True if len(self.tasks) is 0 else False
