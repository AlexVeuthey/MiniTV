class EventManager:
    def __init__(self):
        self._handlers = {}

    def add_handler(self, event_name, handler):
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        print(f"Added handler {handler}")

    def remove_handler(self, event_name, handler):
        if event_name in self._handlers:
            self._handlers[event_name].remove(handler)
            print(f"Removed handler {handler}")
        else:
            print(f"Handler {handler} was not in list")

    def emit(self, event_name, *args):
        if event_name in self._handlers:
            print(f"Emitting {event_name} ({args})")
            for handler in self._handlers[event_name]:
                handler(*args)


manager = EventManager()
