from skimage.io import imread, imsave
import sys

from UniformQuantization import Uniform_quantization
from MedianCut import Median_cut
from KMeans import KMeans
from VectorQuantization import Vector_quantization
from OCTree import OCTree

img = [[[]]]
img = imread('Algorithms/input.png')

"""
num_regions = 4
dept = 6
K_num = 64
max_iters = 1
cb_size=64
epsilon_value=0.5
d=3
block_width_value = 4
block_height_value = 4
block_value = (block_width_value, block_height_value, d)
palette_value = 64
"""

match sys.argv[1]:
    case '0':
         new_img = Uniform_quantization(img, int(sys.argv[2]))
    case '1':
         new_img = Median_cut(img, int(sys.argv[2]))
    case '2':
         new_img = KMeans(img, int(sys.argv[2]), int(sys.argv[3]))
    case '3':
         new_img = Vector_quantization(img, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    case '4':
         new_img = OCTree(img, int(sys.argv[2]))
    case _:
        new_img = img

#new_img = Uniform_quantization(img, num_regions)
#new_img = Median_cut(img, dept)
#new_img = KMeans(img, K_num, max_iters)
#new_img = Vector_quantization(img, cb_size, epsilon_value, block_value)
#new_img = OCTree(img, palette_value)

imsave('output.png', new_img)