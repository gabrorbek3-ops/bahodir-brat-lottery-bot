import base64

from app.core.config import settings

class ImageProcessor:
    @staticmethod
    async def validate_and_process(screenshot_data: str) -> str:
        if not screenshot_data.startswith("data:"):
            raise ValueError("Invalid image format")

        header, encoded = screenshot_data.split(",", 1)
        content_type = header.replace("data:", "").split(";")[0]
        if content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise ValueError("Unsupported image type")

        raw = base64.b64decode(encoded)
        if len(raw) > settings.MAX_UPLOAD_SIZE:
            raise ValueError("File too large")

        return screenshot_data
