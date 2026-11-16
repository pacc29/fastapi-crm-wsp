from pathlib import Path
from typing import Any, NamedTuple

type JsonB = dict[str, Any]


class MediaPath(NamedTuple):
    absolute: Path
    relative: str
