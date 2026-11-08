from enum import StrEnum


class MessageDirection(StrEnum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"


class MessageStatus(StrEnum):
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"
    RECIEVED = "RECIEVED"


