import numpy as np

RED = 16  # trailing zeroes of 0xFF0000 (red channel bit mask)
GREEN = 8  # trailing zeroes of 0x00FF00 (green channel bit mask)
BLUE = 0  # trailing zeroes of 0x0000FF (blue channel bit mask)
MAX_VAL = 255  # max value for each channel (255 for 8 bits)
GAMMA = 2.4
LINEAR_RGB_THRS = 0.04045
RGB2XYZ = [
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041]
]  # sRGB to XYZ conversion matrix
XYZ2RGB = [
    [3.2404542, -1.5371385, -0.4985314],
    [-0.9692660, 1.8760108, 0.0415560],
    [0.0556434, -0.2040259, 1.0572252]
]   # XYZ to sRGB conversion matrix
REFWHITE = [0.9504, 1.0000, 1.0888]     # D65 reference white


def xyz2lab(xyz_val, ref_white):
    e = 0.008856
    k = 903.3
    normd = [0, 0, 0]
    for i in range(3):
        normd[i] = xyz_val[i][0] / ref_white[i]
    fvals = [0, 0, 0]
    for i in range(3):
        if normd[i] > e:
            fvals[i] = np.cbrt(normd[i])
        else:
            fvals[i] = (k * normd[i] + 16) / 116
    lab_raster = [
        116 * fvals[1] - 16,
        500 * (fvals[0] - fvals[1]),
        200 * (fvals[1] - fvals[2])
    ]
    return lab_raster


def lab2xyz(lab_val, ref_white):
    e = 0.008856
    k = 903.3
    f_y = (lab_val[0] + 16) / 116
    f_x = lab_val[1] / 500 + f_y
    f_z = f_y - lab_val[2] / 200
    if np.power(f_x, 3) > e:
        x_r = np.power(f_x, 3)
    else:
        x_r = (116 * f_x - 16) / k
    if np.power(f_z, 3) > e:
        z_r = np.power(f_z, 3)
    else:
        z_r = (116 * f_z - 16) / k
    if lab_val[0] > (k * e):
        y_r = np.power(((lab_val[0] + 16) / 116), 3)
    else:
        y_r = lab_val[0] / k
    xyz_raster = [
        x_r * ref_white[0],
        y_r * ref_white[1],
        z_r * ref_white[2]
    ]
    return xyz_raster


def linearize_rgb(inputcolor):
    hex_val = int(inputcolor.split("#", 1)[1], 16)
    rgb_val = [[((hex_val >> RED) & 255) / MAX_VAL],
               [((hex_val >> GREEN) & 255) / MAX_VAL],
               [((hex_val >> BLUE) & 255) / MAX_VAL]]

    for i in range(3):
        if rgb_val[i][0] <= LINEAR_RGB_THRS:
            rgb_val[i][0] /= 12.92
        else:
            rgb_val[i][0] = np.power(((rgb_val[i][0] + 0.055) / 1.055), GAMMA)
    return rgb_val


def unlinearize_rgb(inputcolor):
    for i in range(3):
        if inputcolor[i] <= LINEAR_RGB_THRS:
            inputcolor[i] *= 12.92
        else:
            inputcolor[i] = 1.055 * np.power(inputcolor[i], (1 / GAMMA)) - 0.055
    r_comp = int(inputcolor[0] * MAX_VAL) << RED
    g_comp = int(inputcolor[1] * MAX_VAL) << GREEN
    b_comp = int(inputcolor[2] * MAX_VAL) << BLUE
    rgb_val = r_comp + g_comp + b_comp
    rgb_string = '{:06x}'.format(rgb_val)
    return '#'+rgb_string


def rgb2lab(inputcolor):
    rgb_val = linearize_rgb(inputcolor)
    XYZval = np.matmul(RGB2XYZ, rgb_val)
    return xyz2lab(XYZval, REFWHITE)


def lab2rgb(inputcolor):
    return XYZ2rgb(lab2xyz(inputcolor, REFWHITE))


def rgb2XYZ(inputcolor):
    rgb_val = linearize_rgb(inputcolor)
    XYZval = np.matmul(RGB2XYZ, rgb_val)
    return XYZval


def XYZ2rgb(inputcolor):
    linear_rgb = np.matmul(XYZ2RGB, inputcolor)
    rgb_val = unlinearize_rgb(linear_rgb)
    return rgb_val


def rgb2xyY(inputcolor):
    XYZval = rgb2XYZ(inputcolor)
    xyYnorm = XYZval[0] + XYZval[1] + XYZval[2]
    xyYval = np.empty((3, 1))
    for i in range(2):
        xyYval[i][0] = XYZval[i][0] / xyYnorm
    xyYval[2][0] = XYZval[1]
    return xyYval
