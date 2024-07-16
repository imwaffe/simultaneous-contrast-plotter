from PIL import Image, ImageDraw
import numpy as np


class DrawBox:
    outerSize = 0
    innerSize = 0
    img: Image = None

    def __init__(self, outerSize: int, innerSize: int, img: Image):
        assert innerSize < outerSize, "inner size must be less then outer size"
        self.outerSize = outerSize
        self.innerSize = innerSize
        self.img = img

    def draw(self, fgColor, bgColor, position, text=None):
        box = Box(position, self)
        box.draw(fgColor, bgColor, text)
        return box

    def getSize(self):
        return self.outerSize, self.innerSize

    def getImg(self):
        return self.img


class Box:
    position = []
    drawbox: DrawBox = None
    fgColor: str = None
    bgColor: str = None

    def __init__(self, position, drawbox: DrawBox):
        self.position = position
        self.drawbox = drawbox

    def draw(self, fgColor, bgColor, text=None):
        box = ImageDraw.Draw(self.drawbox.getImg())
        outerSize, innerSize = self.drawbox.getSize()
        box.rectangle([self.position, (self.position[0] + outerSize, self.position[1] + outerSize)], bgColor)
        if text is not None:
            box.text((self.position[0], self.position[1] - 15), text)
        newPos = [self.position[0] + np.round((outerSize - innerSize) / 2),
                  self.position[1] + np.round((outerSize - innerSize) / 2)]
        box.rectangle([(newPos[0], newPos[1]), (newPos[0] + innerSize, newPos[1] + innerSize)], fgColor)

    def getPosition(self):
        return self.position
