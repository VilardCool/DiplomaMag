from skimage.io import imread, imsave
import sys

from UniformQuantization import Uniform_quantization
from MedianCut import Median_cut
from KMeans import KMeans
from VectorQuantization import Vector_quantization
from OCTree import OCTree
from Aglomerative import Aglomerative
from PMedian import PMedian
from SR import SRCNN

img = [[[]]]
img = imread('input.png')

print(sys.argv)

match sys.argv[1]:
    case 'UQ':
         new_img = Uniform_quantization(img, int(sys.argv[2]))
    case 'MC':
         new_img = Median_cut(img, int(sys.argv[2]))
    case 'KM':
         new_img = KMeans(img, int(sys.argv[2]), int(sys.argv[3]))
    case 'VQ':
         new_img = Vector_quantization(img, int(sys.argv[2]), float(sys.argv[3]), (int(sys.argv[4]), int(sys.argv[5]), 3))
    case 'OCT':
         new_img = OCTree(img, int(sys.argv[2]))
    case 'AC':
         new_img = Aglomerative(img, int(sys.argv[2]))
    case 'PM':
         new_img = PMedian(int(sys.argv[2]))
    case 'SRCNN':
         new_img = SRCNN()
    case _:
        new_img = img

imsave('output.png', new_img)