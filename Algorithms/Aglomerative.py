import numpy as np
from multiprocessing import Pool
from skimage.io import imread, imsave
import math
from itertools import repeat

def find_closest_centroids(X, centroids):
    m = len(X)
    c = [0]*len(X)

    for i in range(m):
        # Find distances
        distances = []
        distance = 0
        for j in range(len(centroids)):
            for k in range(len(centroids[j])):
                distance += (X[i][k] - centroids[j][k])**2
            distances.append(distance)
            distance = 0

        # Assign closest cluster to c[i]
        c[i] = distances.index(min(distances))
    
    return c

def color_sort(img):
    dist = []

    for color in img:
        dist.append((np.linalg.norm(color), color))

    dist.sort(key=lambda c: c[0])

    return dist

def dist_mat(colors):
    mat = []
    
    for i in range(len(colors)):
        row = []
        for j in range(i):
            row.append(math.dist(colors[i], colors[j]))
        mat.append(row)

    return mat

def get_min(mat):
    min = 5
    a = 0
    b = 1
    for i in range(len(mat)):
        for j in range(i):
            if (mat[i][j] < min):
                min = mat[i][j]
                if i<j:
                    a = i
                    b = j
                else:
                    a = j
                    b = i
    return a, b

def change_centroid(mat, colors, a, b):
    centroid = [0, 0, 0]
    for i in range(3):
        centroid[i] = (colors[a][i]+colors[b][i])/2

    for i in range(a+1, len(colors)):
        if i>b: mat[i].pop(b)
        mat[i].pop(a)

    mat.pop(b)
    mat.pop(a)
    colors.pop(b)
    colors.pop(a)

    colors.append(centroid)

    row = []
    for i in range(len(colors)):
        row.append(math.dist(colors[i], centroid))
    mat.append(row)

def find_colors(colors):
    mat = dist_mat(colors)

    while len(mat)>2:
        a, b = get_min(mat)
        change_centroid(mat, colors, a, b)

    return colors

def fin_colors(colors, amount):
    mat = dist_mat(colors)

    while len(mat)>amount:
        a, b = get_min(mat)
        change_centroid(mat, colors, a, b)

    return colors

def CentroidLinkage(img, colors):
    # Indexes for color for each pixel
    idx = find_closest_centroids(img, colors)

    # Reconstruct the image
    res = []
    for i in range(len(idx)):
        for k in range(len(colors)):
            if (idx[i] == k):
                res.append(colors[k])
                break

    res = np.array(res)*255
    res = np.array(res, dtype=np.uint8)
    recolored_img = res.reshape(w,h,d)

    return recolored_img

if __name__ == "__main__":

    photo_name = "input/test.jpg"
    img = imread(photo_name)

    w,h,d = img.shape
    img = img/255

    with Pool() as pool:
      dist = pool.map(color_sort, img)

    colors = []
    amount = len(dist)*len(dist[0])
    while len(colors) < amount:
        least = 100
        for i in range(len(dist)):
            if dist[i] and dist[i][0][0] < least:
                num = i
                least = dist[i][0][0]

        colors.append(dist[num][0][1])
        dist[num].pop(0)

    box_size = 300
    grouped_colors = [colors[box_size*i:box_size*(i+1)] for i in range((len(colors)//box_size)-1)]
    grouped_colors.append(colors[box_size*(len(colors)//box_size):])

    with Pool() as pool:
      colors = pool.map(find_colors, grouped_colors)

    fin_color = []
    for row in colors:
        fin_color.append(row[0])
        fin_color.append(row[1])
    
    colors = fin_colors(fin_color, 20)

    img = img.reshape(w*h, d)

    img = CentroidLinkage(img, colors)

    imsave("out.jpg", img)