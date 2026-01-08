from dotenv import load_dotenv
from imagekitio import ImageKit
import os
load_dotenv()
imageKitClient = ImageKit(
    os.environ["IMAGEKIT_PRIVATE_KEY"],
    os.environ["IMAGEKIT_PUBLIC_KEY"],
    os.environ["IMAGEKIT_URL"]
)