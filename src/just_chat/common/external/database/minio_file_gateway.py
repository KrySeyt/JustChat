import uuid
from io import BytesIO

import aiohttp
from minio import Minio

from just_chat.common.application.image_gateway import FileGateway
from just_chat.message.domain.message import FileUrl
from just_chat.user.domain.user import UserId


class MinioFileGateway(FileGateway):
    def __init__(self, minio_client: Minio, client_session: aiohttp.ClientSession) -> None:
        self._minio = minio_client
        self._session = client_session

    async def save_user_image_from_url(self, user_id: UserId, url: FileUrl) -> FileUrl:
        bucket_name = "images"
        async with self._session.get(url) as response:
            image_type = response.content_type.split("/")[1]
            object_name = f"{user_id}/{uuid.uuid4()}.{image_type}"
            self._minio.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=BytesIO(await response.read()),
                length=-1,
                part_size=10*1024*1024,
            )
            return self._minio.presigned_get_object(
                bucket_name=bucket_name,
                object_name=object_name,
            )
