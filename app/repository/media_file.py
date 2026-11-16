from app.common.mixins.base_repository import BaseRepository
from app.models.media_file import MediaFile


class MediaFileRepository(BaseRepository[MediaFile]):
    def __init__(self, session):
        super().__init__(session, MediaFile)
