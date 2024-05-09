from PIL import Image, ImageFont, ImageDraw, ImageFilter
from secret import FLAG

assert FLAG.startswith("SSM{") and FLAG.endswith("}")
assert all(ch in "abcdefghijklmnopqrstuvxyzåäö0123456789_" for ch in FLAG[4:-1])

FONT_SIZE = 30
BLUR_SIZE = 6
IMAGE_SIZE =  (1000, 70)

font = ImageFont.truetype("SAX.ttf", size=FONT_SIZE)

flag_image = Image.new("RGB", IMAGE_SIZE)

draw = ImageDraw.Draw(flag_image)
draw.rectangle([(0, 0), flag_image.size], fill=(255, 255, 255))

draw.text((0, (IMAGE_SIZE[1] - FONT_SIZE)//2), FLAG, font=font, fill=(0, 0, 0))

filter = ImageFilter.GaussianBlur(radius=BLUR_SIZE)
flag_image = flag_image.filter(filter)

flag_image.save("flag.png")
