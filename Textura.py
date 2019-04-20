import struct
from SR1 import *

class Textura(object):
    def __init__(self, path):
        self.path = path
        self.read()
    
    def read(self):
        image = open(self.path, "rb")
        image.seek(10)
        HS = struct.unpack("=l", image.read(4))[0]
        image.seek(18)
        self.width = struct.unpack("=l", image.read(4))[0]
        self.height = struct.unpack("=l", image.read(4))[0]
        self.pixels = []
        image.seek(HS)
        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                #self.pixels[y].append(glColor(b, g, r))
                self.pixels[y].append(color(r,g,b))
        image.close()

    def get_colors(self, tvx, tvy, intensity = 1):
        #print(tvx)
        #print(tvy)
        #print(self.pixels)
        x = int(tvx)
        y = int(tvy)
        #return(color(255,0,0))
        return bytes(
            map(
                lambda b: round(b * intensity)
                    if (b * intensity) > 0 else 0,
                self.pixels[y][x]
            )
        )
        