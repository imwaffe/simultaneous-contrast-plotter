from Draws.DrawBox import DrawBox
from PIL import Image, ImageDraw
import numpy as np


class DrawGrid:
    drawbox: DrawBox = None
    grid = []
    boxes = []

    def __init__(self, outerSize: int, innerSize: int, img: Image, grid=[1, 1]):
        assert img.size[0] > outerSize * grid[1] and img.size[1] > outerSize * grid[0], "Dimensions mismatch"
        assert grid[1] > 0 and grid[0] > 0, "Grid size must be positive"
        self.drawbox = DrawBox(outerSize, innerSize, img)
        self.grid = grid
        self.boxes = []

    def initBoxes(self):
        outerSize, innerSize = self.drawbox.getSize()
        imageSize = self.drawbox.getImg().size
        xSpacing = np.round((imageSize[0] - outerSize * self.grid[1]) / (self.grid[1] + 1))
        ySpacing = np.round((imageSize[1] - outerSize * self.grid[0]) / (self.grid[0] + 1))
        for row in range(self.grid[1]):
            for col in range(self.grid[0]):
                pos = [xSpacing + (xSpacing + outerSize) * row, ySpacing + (ySpacing + outerSize) * col]
                self.boxes.append(self.drawbox.draw("#d1d1d1", "#3f3f3f", (pos[0], pos[1])))

    def setColor(self, coordinates, fgColor, bgColor, text=None):
        index = coordinates[1] * self.grid[0] + coordinates[0]
        self.boxes[index].draw(fgColor, bgColor, text)

    def setBgImage(self, coordinates, fgColor, bgImg, text=None):
        index = coordinates[1] * self.grid[0] + coordinates[0]
        img = self.drawbox.getImg()
        position = self.boxes[index].getPosition()
        img.paste(bgImg, (int(position[0]), int(position[1])))
        box = ImageDraw.Draw(img)
        outerSize, innerSize = self.drawbox.getSize()
        if text is not None:
            box.text((position[0], position[1] - 15), text)
        newPos = [position[0] + np.round((outerSize - innerSize) / 2),
                  position[1] + np.round((outerSize - innerSize) / 2)]
        box.rectangle([(newPos[0], newPos[1]), (newPos[0] + innerSize, newPos[1] + innerSize)], fgColor)
