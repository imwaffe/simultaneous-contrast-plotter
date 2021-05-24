import numpy

class RGB2Lab:
    RED = 16  # trailing zeroes of 0xFF0000 (RGB BufferedImage red channel bit mask)
    GREEN = 8  # trailing zeroes of 0x00FF00 (RGB BufferedImage green channel bit mask)
    BLUE = 0  # trailing zeroes of 0x0000FF (RGB BufferedImage blue channel bit mask)
    MAX_VAL = 255  # max value for each channel (255 for 8 bits)
    GAMMA = 2.4
    LINEAR_RGB_THRS = 0.04045
    RGB2XYZ = [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ]  # sRGB to XYZ conversion matrix
    REFWHITE = [0.9504, 1.0000, 1.0888]

    def xyz2lab(self, xyz_val, ref_white):
        e = 0.008856
        k = 903.3
        normd = [0, 0, 0]
        for i in range(3):
            normd[i] = xyz_val[i][0] / ref_white[i]
        fvals = [0, 0, 0]
        for i in range(3):
            if normd[i] > e:
                fvals[i] = numpy.cbrt(normd[i])
            else:
                fvals[i] = (k * normd[i] + 16) / 116

        lab_raster = [
            116 * fvals[1] - 16,
            500 * (fvals[0] - fvals[1]),
            200 * (fvals[1] - fvals[2])
        ]

        return lab_raster

    def rgb2lab(self, inputcolor):
        hex_val = int(inputcolor.split("#", 1)[1], 16)
        rgb_val = [[((hex_val >> self.RED) & 255) / self.MAX_VAL],
                   [((hex_val >> self.GREEN) & 255) / self.MAX_VAL],
                   [((hex_val >> self.BLUE) & 255) / self.MAX_VAL]
                   ]

        for i in range(3):
            if rgb_val[i][0] <= self.LINEAR_RGB_THRS:
                rgb_val[i][0] /= 12.92
            else:
                rgb_val[i][0] = numpy.power(((rgb_val[i][0] + 0.055) / 1.055), self.GAMMA)

        XYZval = numpy.matmul(self.RGB2XYZ, rgb_val)
        return self.xyz2lab(self, XYZval, self.REFWHITE)