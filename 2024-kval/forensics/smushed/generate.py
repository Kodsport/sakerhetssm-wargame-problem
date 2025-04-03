import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
import string
import zipfile
import os


response = requests.get(
    f"https://unsplash.com/napi/search/photos?query=road&orientation=landscape&xp=&per_page=5&page=1",
)
img_urls = [image["urls"]["small"] for image in response.json()["results"]]

images = []
for url in img_urls:
    response = requests.get(url)
    images.append(response.content)

img = Image.effect_noise((1000, 200), 8).convert("RGB")
d = ImageDraw.Draw(img)
font = ImageFont.load_default(size=50)
text = "SSM{y0u_un5mu5h3d_17}"
text_box = d.textbbox((0, 0), text, font=font)
text_position = ((1000 - text_box[2]) // 2, (200 - text_box[3]) // 2)
d.text(text_position, text, fill=(0, 0, 0), font=font)
img.save("image_flag.jpg")


with zipfile.ZipFile("challenge.zip", "w") as zipf:
    for i, img in enumerate(images):
        img_filename = f"image_{i+1}.jpg"
        Path(img_filename).write_bytes(img)
        zipf.write(img_filename)

    zipf.write("image_flag.jpg")

part_size = 35 * 1024  # 35KB
mapping = [5, 3, 1, 2, 4]
with open("challenge.zip", "rb") as source:
    part = 0
    while True:
        data = source.read(part_size)
        if not data:
            break
        with open(f"part{mapping[part]}", "wb") as target:
            target.write(data)
        part += 1
