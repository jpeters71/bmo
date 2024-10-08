from dataclasses import dataclass
from queue import Queue

_EVENT_QUEUE = Queue()


@dataclass
class BmoEvent:
    event_name: str
    event_data: dict = None


def add_event(ev: BmoEvent):
    _EVENT_QUEUE.put(ev)


def get_next_event() -> BmoEvent:
    if _EVENT_QUEUE and not _EVENT_QUEUE.empty():
        return _EVENT_QUEUE.get(block=False)
    else:
        return None
