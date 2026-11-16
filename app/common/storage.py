from collections.abc import AsyncGenerator, Awaitable
from pathlib import Path
from typing import NamedTuple
from uuid import uuid4

import aiofiles

from app.core.settings import settings


class MediaPath(NamedTuple):
    absolute: Path
    relative: str


def build_media_path(
    relative_dir: str,
    extension: str | None,
    *,
    root: Path | None = None,
) -> MediaPath:
    base = root if root is not None else settings.MEDIA_ROOT
    relative = Path(relative_dir) / f"{uuid4().hex}{extension or '.bin'}"
    return MediaPath(base / relative, relative.as_posix())


async def save_file_to_path(
    stream: Awaitable[AsyncGenerator[bytes]], path: Path
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(str(path), "wb") as f:
        async for chunk in await stream:
            await f.write(chunk)
