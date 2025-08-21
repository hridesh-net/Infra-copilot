import threading
from typing import Any, Callable


class Context:
    """
    A thread-safe, application-wide context store with pub/sub support.
    Agents and other components can import the global `context` instance
    to share state and listen for updates.
    """

    def __init__(self):
        self._data: dict[str, Any] = {}
        self._lock = threading.Lock
        self._subscribers: list[Callable[[str, Any], None]] =[]

    def subscribers(self, callback: Callable[[str, Any], None]) -> None:
        """
        Register a callback to be invoked on every key update.
        Callback signature: (key: str, value: Any)
        """

        with self._lock:
            self._subscribers.append(callback)

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the context and notify subscribers.
        """
        with self._lock:
            self._data[key] = value
            subs = list(self._subscribers)

        # Notify subscribers outside the lock to avoid deadlocks
        for callback in subs:
            try:
                callback(key, value)
            except Exception:
                # Optionally log or ignore subscriber errors
                pass

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value from the context, returning default if not present.
        """
        with self._lock:
            return self._data.get(key, default)

    def all(self) -> dict[str, Any]:
        """
        Return a shallow copy of the entire context data.
        """
        with self._lock:
            return dict(self._data)


context = Context()
