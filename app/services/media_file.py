from app.models.media_file import MediaFile
from app.repository.media_file import MediaFileRepository
from app.schemas.media_file import MediaFileCreate


class MediaFileService:
    def __init__(self, media_file_repository: MediaFileRepository) -> None:
        self.media_file_repository = media_file_repository

    async def create(self, media_file_create: MediaFileCreate) -> MediaFile:
        media_file = MediaFile.model_validate(media_file_create)
        return await self.media_file_repository.create(media_file)
