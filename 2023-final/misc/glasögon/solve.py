import concurrent.futures

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import numpy as np
import string
from tqdm import tqdm

from queue import PriorityQueue

charset = "abcdefghijklmnopqrstuvxyzåäö0123456789_{}"

FONT_SIZE = 30
BLUR_SIZE = 6
IMAGE_SIZE =  (1000, 70)

font = ImageFont.truetype("SAX.ttf", size=FONT_SIZE)

def draw_flag(FLAG):
    flag_image = Image.new("RGB", IMAGE_SIZE)

    draw = ImageDraw.Draw(flag_image)
    draw.rectangle([(0, 0), flag_image.size], fill=(255, 255, 255))

    width = font.getlength(FLAG)
    draw.text((0, (IMAGE_SIZE[1] - FONT_SIZE)//2), FLAG, font=font, fill=(0, 0, 0))

    filter = ImageFilter.GaussianBlur(radius=BLUR_SIZE)
    flag_image = flag_image.filter(filter)

    return np.array(flag_image), width

def image_diff(a, b):
    return ((a - b) ** 2).sum() / a.shape[0]

real = Image.open("flag.png")
real_np = np.array(real)

def value(flag):
    flag_drawn, text_width = draw_flag(flag)
    return image_diff(real_np[:int(text_width)], flag_drawn[:int(text_width)])

front = PriorityQueue()
front.put((0, "SSM{"))

tested = {}

RUN_AMOUNT = 3000

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    while True:
        to_test = []
        while len(to_test) < RUN_AMOUNT:
            if front.empty():
                break
            _, item = front.get()
            for c1 in charset:
                item_ = item + c1
                if item_ in tested:
                    continue
                to_test.append(item_)
            for i in range(len(item)):
                for c1 in charset:
                    item_ = item[:i] + c1 + item[i+1:]
                    if item_ in tested:
                        continue
                    to_test.append(item_)

        print("best", to_test[0])
        print("testing", len(to_test), ", ", front.qsize(), "in queue")

        futures = {
            executor.submit(value, item): item
            for item in to_test
        }

        for fut in concurrent.futures.as_completed(futures):
            item = futures[fut]
            res = fut.result()

            front.put((res, item))
            tested[item] = res


        # for _ in range(100):

        #     best = None, float("inf")


        #     known = known + best[0]
        #     print(known)
