from dataclasses import dataclass


@dataclass
class Event:
    """
    Base class for events.
    """

    pass


@dataclass
class StartEvent(Event):
    """
    Event for the start of processing.
    """

    message: str


@dataclass
class FileProcessedEvent(Event):
    """
    Event for a file being processed.
    """

    filename: str
    relative_path: str
    content: str


@dataclass
class OutlineCreatedEvent(Event):
    """
    Event for the outline being created.
    """

    content: str


@dataclass
class EndEvent(Event):
    """
    Event for the end of processing.
    """

    message: str
