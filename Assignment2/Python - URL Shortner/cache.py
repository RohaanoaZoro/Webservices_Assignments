class Cache:
    def __init__(self, size):
        self.cache_size = size
        self.sid = []
        self.urls = []

    def is_empty(self):
        return len(self.sid) == 0

    def enqueue(self, sid, url):
        if len(self.sid)+1 > self.cache_size:
            self.dequeue()

        self.sid.append(sid)
        self.urls.append(url)

    def dequeue(self):
        if self.is_empty():
            return None
        
        self.urls.pop(0)
        return self.sid.pop(0)

    def deleteItem(self, sid):
        for i in range(0, len(self.sid)):
            if sid == self.sid[i]:
                mysid = self.sid.pop(i)
                self.urls.pop(i)

                return mysid
        return -1

    def check(self, sid):
        for i in range(0, len(self.sid)):
            if sid == self.sid[i]:
                return self.urls[i]
        return -1

    def size(self):
        return len(self.sid)
