from io import BytesIO

from fastapi import HTTPException, UploadFile
from PIL import Image, ImageOps, UnidentifiedImageError
from starlette.status import HTTP_400_BAD_REQUEST


MAX_IMAGE_BYTES = 900_000
MAX_IMAGE_DIMENSION = 1600
JPEG_QUALITIES = [82, 72, 62, 52]


def _to_rgb(image: Image.Image) -> Image.Image:
    if image.mode in ("RGBA", "LA"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        alpha = image.getchannel("A") if "A" in image.getbands() else None
        background.paste(image.convert("RGBA"), mask=alpha)
        return background

    if image.mode != "RGB":
        return image.convert("RGB")

    return image


async def normalize_uploaded_image(upload: UploadFile, max_bytes: int = MAX_IMAGE_BYTES) -> bytes:
    raw_bytes = await upload.read()
    if not raw_bytes:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Bitte ein Foto hochladen.")

    try:
        image = Image.open(BytesIO(raw_bytes))
        image = ImageOps.exif_transpose(image)
        image = _to_rgb(image)
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Das hochgeladene Bild ist ungültig.")

    image.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION))

    for quality in JPEG_QUALITIES:
        output = BytesIO()
        image.save(output, format="JPEG", quality=quality, optimize=True)
        optimized = output.getvalue()
        if len(optimized) <= max_bytes:
            return optimized

    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail="Das Bild ist zu groß. Bitte lade ein kleineres Foto hoch.",
    )
