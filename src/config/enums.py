"""
Holds application wide enums.
"""

from enum import Enum as PyEnum


class ProcessingStatus(PyEnum):
    """Document processing status states"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class MessageRole(PyEnum):
    """Chat message role types"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
