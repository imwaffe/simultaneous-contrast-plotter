import ColorUtils.RGB2Lab

RED = 16  # trailing zeroes of 0xFF0000 (RGB red channel bit mask)
GREEN = 8  # trailing zeroes of 0x00FF00 (RGB green channel bit mask)
BLUE = 0  # trailing zeroes of 0x0000FF (RGB blue channel bit mask)
MAX_VAL = 255  # max value for each channel (255 for 8 bits)


def RGB2HSL(inputcolor):
    hex_val = int(inputcolor.split("#", 1)[1], 16)
    rgb = [[((hex_val >> RED) & 255) / MAX_VAL],
           [((hex_val >> GREEN) & 255) / MAX_VAL],
           [((hex_val >> BLUE) & 255) / MAX_VAL]]
    C_max = max(rgb)[0]
    C_min = min(rgb)[0]
    delta = C_max - C_min

    HSL = {
        'h': 0,
        's': 0,
        'l': 0
    }

    HSL['l'] = (C_max + C_min) / 2

    if delta == 0:
        HSL['h'] = 0
        HSL['l'] = 0
    else:
        HSL['s'] = delta / (1 - abs(2 * HSL['l'] - 1))
        if C_max == rgb[0]:
            HSL['h'] = 60 * (((rgb[1][0] - rgb[2][0]) / delta) % 6)
        elif C_max == rgb[1]:
            HSL['h'] = 60 * (((rgb[2][0] - rgb[0][0]) / delta) + 2)
        else:
            HSL['h'] = 60 * (((rgb[0][0] - rgb[1][0]) / delta) + 4)

    HSL['s'] *= 100
    HSL['l'] *= 100

    for ch in HSL:
        HSL[ch] = round(HSL[ch])

    return HSL
