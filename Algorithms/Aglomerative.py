import numpy as np
import math

def find_closest_centroids(X, centroids):
    m = len(X)
    c = [0]*m

    for i in range(m):
        distances = []
        distance = 0
        for j in range(len(centroids)):
            for k in range(len(centroids[j])):
                distance += (X[i][k] - centroids[j][k])**2
            distances.append(distance)
            distance = 0

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

def linkage(colors, amount):
    mat = dist_mat(colors)

    while len(mat)>amount:
        a, b = get_min(mat)
        change_centroid(mat, colors, a, b)

    return colors

def reduce(colors, amount_fin, amount, box):
    result = []

    if (amount * len(colors) / box <= amount_fin * box):
        amount = amount_fin
        box = amount + amount // 2 + 1

    for i in range(len(colors) // box):
        part = box
        if len(colors) - box * i < box:
            part = len(colors) - box * i

        resu = linkage(colors[box * i: box*i + part], amount)
        for k in range(len(resu)): result.append(resu[k])

    if (len(result) > amount_fin): result = reduce(result, amount_fin, amount, box)

    return result

def CentroidLinkage(img, colors):
    w,h,d = img.shape

    idx = find_closest_centroids(img.reshape(w*h, d), colors)

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

def Aglomerative(img, colNum):
    w, h, d = img.shape
    img = img/255

    colorsR = set()
    colorsG = set()
    colorsB = set()
    for row in img:
        for pixel in row:
            if (pixel[0] >= pixel[1] and pixel[0] >= pixel[2]):
                colorsR.add(tuple(pixel))
            elif (pixel[1] >= pixel[0] and pixel[1] >= pixel[2]):
                colorsG.add(tuple(pixel))
            else: colorsB.add(tuple(pixel))

    colorsR = color_sort(colorsR)
    colorsG = color_sort(colorsG)
    colorsB = color_sort(colorsB)

    colorsA = []
    colorsA.extend(colorsR)
    colorsA.extend(colorsG)
    colorsA.extend(colorsB)

    colors=[]
    for color in colorsA:
        colors.append(color[1])

    amount = 2
    box = 4
    
    colors = reduce(colors, colNum, amount, box)

    img = CentroidLinkage(img, colors)

    return img