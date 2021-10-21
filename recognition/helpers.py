import mimetypes
from typing import Union


def image_extension(content_type: str) -> Union[str, None]:
    if content_type not in ['image/jpeg', 'image/png']:
        return None

    return mimetypes.guess_extension(content_type)
