import numpy as np
from PIL import Image

img = Image.open('512x512.jpg')
img = img.convert("RGB")
width, height = img.size
d = len(img.getdata()[0])
img_pixels = []
from collections import defaultdict
by_color = defaultdict(int)
for pixel in img.getdata():
    by_color[pixel] += 1
    img_pixels.append(pixel)

by_color = sorted(by_color.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

original_colors = []
for pixel in by_color:
    if len(original_colors)<420:
        original_colors.append(pixel[0])

img = img_pixels

"""
col = np.asarray(original_colors)
np.savetxt("original_colors.txt", col.astype(int), fmt='%i', delimiter=",")

df = pd.DataFrame(original_colors)

mat = pd.DataFrame(distance_matrix(df.values, df.values).round(0).astype(int), index=df.index, columns=df.index)

mat.to_csv('out.csv')

np.savetxt("out.txt", mat.values.astype(int), fmt='%i', delimiter=",")

"""
import math

from amplpy import AMPL

ampl = AMPL()

# Class for the p-median problem
class PMedianInstance:
    def __init__(
        self,
        num_colors,
        num_representative,
        p,
    ):
        self.num_colors = num_colors
        self.num_representative = num_representative
        self.p = p
        self.representative = range(num_representative)
        self.colors = range(num_colors)
        self.colors_coordinates = {}
        self.representative_coordinates = {}
        self.distances = {}
        self.costs = {}
        self.generate_instance(self.d3)

    def generate_instance(self, distance):
        for i in self.colors:
            self.colors_coordinates[i] = original_colors[i]
        for i in self.representative:
            self.representative_coordinates[i] = original_colors[i]

        for c_id, c_coord in self.colors_coordinates.items():
            for f_id, f_coord in self.representative_coordinates.items():
                self.distances[(c_id, f_id)] = round(distance(c_coord, f_coord))
                self.costs[(c_id, f_id)] = self.distances[(c_id, f_id)]

    def d3(self, coord1, coord2):
        return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2 + (coord1[2] - coord2[2]) ** 2)

    def get_p(self):
        return self.p

    def get_colors(self):
        return list(self.colors)

    def get_colors_coordinates(self):
        return self.colors_coordinates

    def get_representative(self):
        return list(self.representative)

    def get_representative_coordinates(self):
        return self.representative_coordinates

    def get_distances(self):
        return self.distances

    def get_distances(self):
        return self.distances

    def get_costs(self):
        return self.costs

    def print_instance(self):
        print("Colors coordinates:")
        for c_id, c_coord in self.colors_coordinates.items():
            print(f"Color {c_id}: {c_coord}")

        print("\nRepresentatives coordinates:")
        for f_id, f_coord in self.representative_coordinates.items():
            print(f"Representative {f_id}: {f_coord}")

        print("\nCosts:")
        for (c_id, f_id), cost in self.costs.items():
            print(f"Cost from Color {c_id} to Representative {f_id}: {cost}")


instance = PMedianInstance(5, 5, 2)
instance.print_instance()

# Prepare data to send to the optimization engine
def prepare_data(num_colors, num_representative, p):
    instance = PMedianInstance(num_colors, num_representative, p)
    return (
        instance.get_colors(),
        instance.get_representative(),
        instance.get_p(),
        instance.get_costs(),
        instance.get_colors_coordinates(),
        instance.get_representative_coordinates(),
    )

# send data directly from python data structures to ampl
def load_data_2_ampl(model, colors, representative, p, costs):
    model.set["COLORS"] = colors
    model.set["REPRESENTATIVE"] = representative
    model.param["p"] = p
    model.param["cost"] = costs

num_colors = len(original_colors)
num_representative = len(original_colors)
p = 64

ampl.read("pmedian.mod")

# get data
(
    colors,
    representative,
    p,
    costs,
    colors_coordinates,
    representative_coordinates,
) = prepare_data(num_colors, num_representative, p)

# load data into ampl
load_data_2_ampl(ampl, colors, representative, p, costs)

# solve with highs
ampl.solve(solver="highs")
ampl.option["display_eps"] = 1e-2
ampl.display("x, y")

# retrieve dictionaries from ampl with the solution
def retrieve_solution(model):
    open = model.var["y"].to_dict()
    rounded_open = {key: int(round(value)) for key, value in open.items()}

    costs = model.getData(
        "{i in COLORS, j in REPRESENTATIVE} cost[i,j] * x[i,j]"
    ).to_dict()
    rounded_costs = {
        key: float(round(value, 2))
        for key, value in costs.items()
        if costs[key] >= 5e-6
    }
    return rounded_open, rounded_costs


open_representative, costs = retrieve_solution(ampl)

print(costs)

d_k = ampl.get_value("total_cost")

K = 101
ks = 1
d_k1 = 2*d_k - 1

x_o = [[ None for _ in range(num_representative)] for _ in range(num_colors)]
x_o_v = ampl.get_variable("x")

for i in range(num_colors):
    for j in range(num_representative):
        x_o[i][j] = x_o_v[i,j].value()

new_colors = []
y_v = ampl.get_variable("y")

for i in range(num_representative):
    if y_v[i].value() == 1:
        new_colors.append(original_colors[i])

ampl.close()

#Finding all solutions

ampl = AMPL()

ampl.read("pmedian_2.mod")

# get data
(
    colors,
    representative,
    p,
    costs,
    colors_coordinates,
    representative_coordinates,
) = prepare_data(num_colors, num_representative, p)

# load data into ampl
load_data_2_ampl(ampl, colors, representative, p, costs)

ampl.param["ks"] = ks
ampl.param["K"] = K
ampl.param["d_k1"] = d_k1
xs_v = ampl.param["xs"]

for i in range(num_colors):
    for j in range(num_representative):
       xs_v[0,i,j] = round(x_o[i][j])

res = []
res = [x_o]
res_y = []
new_colors_all = []

for k in range(K-1):
   ampl.solve(solver="highs")
   d_k = ampl.get_value("total_cost")
   xs_v = ampl.param["xs"]
   x_v = ampl.get_variable("x")
   y_v = ampl.get_variable("y")
   if (d_k > round((d_k1+1)/2)): break

   xs = [[[ None for _ in range(num_representative)] for _ in range(num_colors)] for _ in range( K )]
   x = [[ None for _ in range(num_representative)] for _ in range(num_colors)]

   for c in range(ks):
    for i in range(num_colors):
        for j in range(num_representative):
            xs[c][i][j] = xs_v[c,i,j]

   for i in range(num_colors):
    for j in range(num_representative):
        x[i][j] = x_v[i,j].value()
   
   new_colors_y = []
   for i in range(num_representative):
    if y_v[i].value() == 1:
        new_colors_y.append(original_colors[i])
   new_colors_all.append(new_colors_y)

   dist = 0
   for i in range(num_colors):
      for j in range(num_representative):
        dist = dist + abs(xs[k][i][j] - x[i][j])

   if (dist < 1): break
   
   for i in range(num_colors):
    for j in range(num_representative):
        x[i][j] = round(x[i][j])

   xs[k+1] = x

   ks = ks + 1
   
   for i in range(num_colors):
    for j in range(num_representative):
       xs_v[k+1,i,j] = xs[k+1][i][j]

   ampl.param["ks"] = ks

   res = xs

for c in range(ks):
    print("\n", c)
    for i in range(num_colors):
        print(res[c][i])

#Result image

def find_closest_centroids(X, centroids):
    m = width*height
    c = [0]*m

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

idx = find_closest_centroids(img, new_colors)

res = []
for i in range(len(idx)):
    for k in range(p):
        if (idx[i] == k):
            res.append(new_colors[k])
            break

res = np.array(res, dtype=np.uint8)
res = np.reshape(res, (width, height, d))

im = Image.fromarray(res)
im.save("out.jpg")

for n in range(K-1):
    idx = find_closest_centroids(img, new_colors_all[n])

    res = []
    for i in range(len(idx)):
        for k in range(p):
            if (idx[i] == k):
                res.append(new_colors_all[n][k])
                break

    res = np.array(res, dtype=np.uint8)
    res = np.reshape(res, (width, height, d))

    im = Image.fromarray(res)
    im.save("res_all\out_"+str(n)+".jpg")