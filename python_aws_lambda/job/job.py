class Job:
    def __init__(self, data):
        self.data = data

    def handle(self):
        raise NotImplementedError("Subclasses must implement this method")
