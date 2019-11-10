# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#


import math
from PIL import Image,ImageDraw,ImageFont,ImageColor

active_theme = "blue"

def drawBackground(theme_name):
    #print("drawBackground " + theme_name)
    image = Image.new("RGBA", (128, 128), "WHITE")
    if theme_name == "blue":
        innerColor = [80, 80, 255]  # Color at the center
        outerColor = [0, 0, 80]  # Color at the edge
    else: # red
        innerColor = [255, 80, 80]  # Color at the center
        outerColor = [80, 50, 50]  # Color at the edge

    for y in range(image.height):
        for x in range(image.width):
            distanceToCenter = math.sqrt((x - image.width / 2) ** 2 + (y - image.height / 2) ** 2)

            # Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * image.width / 2)

            # Calculate r, g, and b values
            r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
            g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
            b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)

            # Place the pixel
            image.putpixel((x, y), (int(r), int(g), int(b)))

    return image



themes = {}
themes["blue"] = {
    "text_color": "#999999",
    "highlight_text_color": "WHITE",
    "headline_color": "WHITE",
    "cursor_color": "RED",
    "headlinefont": ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 15),
    "font": ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 11),
    "clockfont": ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18),
    "background_image": None # will be created when this theme is loaded for the first time
}

themes["red"] = {
    "text_color": "BLACK",
    "highlight_text_color": "RED",
    "headline_color": "BLACK",
    "cursor_color": "BLACK",
    "headlinefont": ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 15),
    "font": ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 11),
    "clockfont": ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18),
    "background_image": None # will be created when this theme is loaded for the first time
}

theme = themes[active_theme]



def getTheme():
    global theme
    global themes
    global active_theme
    if themes[active_theme]["background_image"] is None:
        themes[active_theme]["background_image"] = drawBackground(active_theme)
    return theme

def changeTheme(new_theme):
    global theme
    global themes
    global active_theme
    active_theme = new_theme
    if themes[active_theme]["background_image"] is None:
        themes[active_theme]["background_image"] = drawBackground(active_theme)
    theme = themes[new_theme]
    print("changeTheme("+new_theme+"): [text_color] " + theme["text_color"])

