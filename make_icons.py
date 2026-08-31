from PIL import Image, ImageDraw, ImageFont
import os

def make_icon(size, path):
    img = Image.new('RGB', (size, size), color='#2563eb')
    draw = ImageDraw.Draw(img)
    # Draw simple "SP" text
    text = 'SP'
    try:
        font = ImageFont.truetype('arial.ttf', int(size * 0.4))
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) // 2
    y = (size - th) // 2
    draw.text((x, y), text, fill='white', font=font)
    img.save(path)
    print(f'Saved {path}')

make_icon(192, r'C:\Users\sayefate\Desktop\Familien Schulplaner\icon-192.png')
make_icon(512, r'C:\Users\sayefate\Desktop\Familien Schulplaner\icon-512.png')
