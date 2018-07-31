from PIL import Image, ImageDraw, ImageFont
from math import ceil
import numpy as np
from typing import List
from sys import argv

from vendor.blockwise_view import blockwise_view

tinierFont = ImageFont.truetype('fonts/tinier/Tinier.ttf', 4)
tinyFont = ImageFont.truetype('fonts/tiny/tiny.ttf', 6)
tiny2xFont = ImageFont.truetype('fonts/tiny/tiny.ttf', 6 * 2)
tiny3xFont = ImageFont.truetype('fonts/tiny/tiny.ttf', 6 * 3)

fonts = [tinierFont, tinyFont, tiny2xFont, tiny3xFont]

width = 28
height = 100


def find_text_font(draw: ImageDraw.ImageDraw, text: str) -> ImageFont:
    best_font = fonts[0]
    for font in fonts:
        if draw.textsize(text, font=font)[0] > width:
            return best_font

        best_font = font

    return best_font


def find_cropped_dimension(target_dimension: int, max=None) -> int:
    """Fits dimension to nearest multiple of 4"""
    fit = 4 * ceil(target_dimension / 4)
    if max and fit > max:
        return max

    return fit


def render_text(words: List[str]) -> Image:
    im = Image.new(mode='RGB', size=(width, height), color='#ffffff')
    draw = ImageDraw.Draw(im)
    offset = 0
    largest_width = 0
    for word in words:
        best_font = find_text_font(draw, word)
        text_w, text_h = draw.textsize(word, font=best_font)
        if text_w > largest_width:
            largest_width = text_w
        draw.text((0, offset), word, fill='#000000', font=best_font)
        offset += text_h + 1

    im = im.convert('1')
    im = im.crop((0, 0, find_cropped_dimension(largest_width, max=width), find_cropped_dimension(offset)))
    return im


def blockshaped(arr, nrows, ncols):
    """

    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    return (arr.reshape(h // nrows, nrows, -1, ncols)
            .swapaxes(1, 2)
            .reshape(-1, nrows, ncols))


def encode_block(block: List[List[int]]) -> str:
    block = np.array(block).flatten()
    return ''.join([('0' if pixel == 255 else '1') for pixel in block])


def encode_pixels(im: Image) -> list:
    width = im.width
    height = im.height
    pixels = np.reshape(im.getdata(), (height, width))
    tiles = blockwise_view(pixels, (2, 2), require_aligned_blocks=True)
    return [[encode_block(block) for block in [col for col in row]] for row in tiles]

def encoded_to_emoji(encoded: List[List[str]]) -> str:
    return '\n'.join([''.join([f':0c_bin_{col}:' for col in row]) for row in encoded])


if __name__ == '__main__':
    im = render_text(argv[1:])
    print(encoded_to_emoji(encode_pixels(im)))
