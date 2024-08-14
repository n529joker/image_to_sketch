import urllib.request
import os

from fastapi import APIRouter
from .sketch import ImageProcessor
from pydantic import BaseModel

from typing import Tuple

router = APIRouter(
    tags=["sketch"],
    responses={404: {"description": "Not found"}},
)

class SketchRequest(BaseModel):
    image_url: str
    image_brightness: float = 0.9
    image_color: Tuple[int, int, int] = (0, 0, 255)
    

def download_image(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


@router.post("/", status_code=200)
def get_sketch(request: SketchRequest):
    image_filename = "image.jpg"
    if download_image(request.image_url, image_filename):
        try:
            image_processor = ImageProcessor(
                image_filename, request.image_brightness , request.image_color
            )
            sketch = image_processor.get_sketch()
            os.remove(image_filename)
            return sketch
        except Exception as e:
            print(f"Error processing image: {e}")
            return {"message": "Error processing image"}
    else:
        return {"message": "Error downloading image"}
