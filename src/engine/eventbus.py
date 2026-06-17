class EventBus:
    def __init__(self):
        self.listeners = {}
    def subscribe(self, event_type: str, callback):
        if callback is None:
            return
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        if callback not in self.listeners[event_type]:
            self.listeners[event_type].append(callback)
    def unsubscribe(self, event_type: str, callback):
        if event_type in self.listeners:
            self.listeners[event_type] = [cb for cb in self.listeners[event_type] if cb != callback]
    def fire(self, event_type: str, data=None):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(event_type, data)
    def clear(self):
        self.listeners.clear()