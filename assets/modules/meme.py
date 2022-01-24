from PIL import Image, ImageDraw, ImageFont, ImageSequence
import assets.config as cf
from discord import File
from io import BytesIO

from time import perf_counter

def draw_on_frame(topString, bottomString, frame, fontname = cf.font_path):
    img = frame.convert("RGBA")
    imageSize = img.size

    fontSize = int(imageSize[1] / 5)
    font = ImageFont.truetype(fontname, fontSize)

    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)

    while topTextSize[0] > imageSize[0] - 20 or bottomTextSize[0] > imageSize[0] - 20:
        fontSize = fontSize - 1
        font = ImageFont.truetype(fontname, fontSize)

        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)

    topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)

    bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

    draw = ImageDraw.Draw(img)

    outlineRange = int(fontSize / 15)
    for x in range(-outlineRange, outlineRange+1):
        for y in range(-outlineRange, outlineRange+1):
            draw.text((topTextPosition[0] + x, topTextPosition[1] + y), topString, (0, 0, 0), font = font)
            draw.text((bottomTextPosition[0] + x, bottomTextPosition[1] + y), bottomString, (0, 0, 0), font = font)

    draw.text(topTextPosition, topString, (255, 255, 255), font = font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font = font)

    return img

def make_meme(topString, bottomString, template):
    image = Image.open(template)
    frames = []

    for i, frame in enumerate(ImageSequence.Iterator(image)):
        timer = perf_counter()
        frame = draw_on_frame(topString, bottomString, frame)
        stream = BytesIO()

        frame.save(stream, format="GIF", quality=2, optimize=True)
        frame = Image.open(stream)
        frames.append(frame)
        print(f"Edited frame {i + 1} | Time taken: {perf_counter() - timer}")
    
    return frames

async def convert_to_file(frames, name = cf.default_meme_name):
    with BytesIO() as stream:
        frames[0].save(stream, format="GIF", save_all=True, append_images=frames[1:], optimize=True)
        stream.seek(0)
        return File(fp = stream, filename = name)

