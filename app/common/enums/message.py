from enum import StrEnum


class MessageDirection(StrEnum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"


class MessageStatus(StrEnum):
    SENT = "SENT"


class MessageType(StrEnum):
    TEXT = "TEXT"
