import typing as _t
from dataclasses import dataclass
from enum import IntEnum


class NoticeLevel(IntEnum):
    INFO = 1
    WARNING = 2
    ERROR = 3

    @property
    def name(self):
        if self == NoticeLevel.INFO:
            return "info"
        elif self == NoticeLevel.WARNING:
            return "warning"
        elif self == NoticeLevel.ERROR:
            return "error"


@dataclass
class Notice:
    level: NoticeLevel
    message: str

    header: _t.Union[str, bool] = True

    @classmethod
    def info(cls, *args, **kwargs):
        return Notice(NoticeLevel.INFO, *args, **kwargs)

    @classmethod
    def warning(cls, *args, **kwargs):
        return Notice(NoticeLevel.WARNING, *args, **kwargs)

    @classmethod
    def error(cls, *args, **kwargs):
        return Notice(NoticeLevel.ERROR, *args, **kwargs)
