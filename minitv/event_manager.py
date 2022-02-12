class EventManager:
    def __init__(self):
        self._handlers = {}

    def add_handler(self, event_name, handler):
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        print(f"Added handler {handler}")

    def remove_handler(self, event_name, handler):
        self._handlers[event_name].remove(handler)
        print(f"Removed handler {handler}")

    def emit(self, event_name):
        for handler in self._handlers[event_name]:
            print(f"Emitting {event_name}")
            handler()


manager = EventManager()
