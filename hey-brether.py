#!/usr/bin/env python3

import fire
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


def find_text_font(draw: ImageDraw.ImageDraw, text: str, width: int) -> ImageFont:
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


def render_text(words: List[str], width: int, height: int) -> Image:
    im = Image.new(mode='RGB', size=(width, height), color='#ffffff')
    draw = ImageDraw.Draw(im)
    offset = 0
    largest_width = 0
    for word in words:
        best_font = find_text_font(draw, word, width)
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


def encode_block_block_el(block: List[List[int]]) -> str:
    block = np.array(block).flatten()
    binary = int('0b' + ''.join([('0' if pixel == 255 else '1') for pixel in block]), 2)
    hex_map = {
        0b0000: 0x2003,
        0b0001: 0x2597,
        0b0010: 0x2596,
        0b0011: 0x2584,
        0b0100: 0x259D,
        0b0101: 0x2590,
        0b0110: 0x259E,
        0b0111: 0x259F,
        0b1000: 0x2598,
        0b1001: 0x259A,
        0b1010: 0x258C,
        0b1011: 0x2599,
        0b1100: 0x2580,
        0b1101: 0x259C,
        0b1110: 0x259B,
        0b1111: 0x2588,
    }
    return chr(hex_map[binary])


def encode_pixels_block_el(im: Image) -> list:
    width = im.width
    height = im.height
    pixels = np.reshape(im.getdata(), (height, width))
    tiles = blockwise_view(pixels, (2, 2), require_aligned_blocks=True)
    return [[encode_block_block_el(block) for block in [col for col in row]] for row in tiles]


def encode_block_braile(block: List[List[int]]) -> str:
    block = np.array(block).flatten()
    bit_strings = [(0 if pixel == 255 else 1) for pixel in block]
    hex_map = {
        0: 0x1,
        1: 0x8,
        2: 0x2,
        3: 0x10,
        4: 0x4,
        5: 0x20,
        6: 0x40,
        7: 0x80
    }
    block = 0x2800
    offset = sum([hex_map[i] if bit == 1 else 0 for i, bit in enumerate(bit_strings)])
    codepoint = block + offset
    return chr(codepoint)


def encode_pixels_braile(im: Image) -> list:
    width = im.width
    height = im.height
    pixels = np.reshape(im.getdata(), (height, width))
    tiles = blockwise_view(pixels, (4, 2), require_aligned_blocks=True)
    return [[encode_block_braile(block) for block in [col for col in row]] for row in tiles]


def stringify_encoded_array(encoded: List[List[str]]) -> str:
    return '\n'.join([''.join([col for col in row]) for row in encoded])


def encode_block_emoji(block: List[List[int]]) -> str:
    block = np.array(block).flatten()
    return ''.join([('0' if pixel == 255 else '1') for pixel in block])


def encode_pixels_emoji(im: Image) -> list:
    width = im.width
    height = im.height
    pixels = np.reshape(im.getdata(), (height, width))
    tiles = blockwise_view(pixels, (2, 2), require_aligned_blocks=True)
    return [[encode_block_emoji(block) for block in [col for col in row]] for row in tiles]


def encoded_to_emoji(encoded: List[List[str]]) -> str:
    return '\n'.join([''.join([f':0c_bin_{col}:' for col in row]) for row in encoded])


class HeyBrether(object):
    def blocks(self, *items):
        im = render_text(list(items), 34*2, 100)
        print('```')
        print(stringify_encoded_array(encode_pixels_block_el(im)))
        print('```')

    def braile(self, *items):
        im = render_text(list(items), 30*2, 100)
        print('```')
        print(stringify_encoded_array(encode_pixels_braile(im)))
        print('```')

    def emoji(self, *items):
        im = render_text(list(items), 14 * 2, 100)
        print(encoded_to_emoji(encode_pixels_emoji(im)))


if __name__ == '__main__':
    fire.Fire(HeyBrether)
