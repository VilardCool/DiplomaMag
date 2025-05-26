import numpy as np
from PIL import Image
import math
from amplpy import AMPL
from collections import defaultdict

original_colors = []

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

def load_data_2_ampl(model, colors, representative, p, costs):
    model.set["COLORS"] = colors
    model.set["REPRESENTATIVE"] = representative
    model.param["p"] = p
    model.param["cost"] = costs

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

def find_closest_centroids(X, centroids, m):
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

def PMedian(colNum):
    img = Image.open('input.png')
    img = img.convert("RGB")
    width, height = img.size
    d = len(img.getdata()[0])
    img_pixels = []
    by_color = defaultdict(int)
    for pixel in img.getdata():
        by_color[pixel] += 1
        img_pixels.append(pixel)

    by_color = sorted(by_color.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    
    for pixel in by_color:
        if len(original_colors)<420:
            original_colors.append(pixel[0])

    img = img_pixels

    ampl = AMPL()

    num_colors = len(original_colors)
    num_representative = len(original_colors)
    p = colNum

    ampl.read("Algorithms/pmedian.mod")

    (
        colors,
        representative,
        p,
        costs,
        colors_coordinates,
        representative_coordinates,
    ) = prepare_data(num_colors, num_representative, p)

    load_data_2_ampl(ampl, colors, representative, p, costs)

    ampl.solve(solver="highs")
    ampl.option["display_eps"] = 1e-2

    open_representative, costs = retrieve_solution(ampl)

    d_k = ampl.get_value("total_cost")

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

    print(len(new_colors))

    idx = find_closest_centroids(img, new_colors, width*height)

    res = []
    for i in range(len(idx)):
        for k in range(p):
            if (idx[i] == k):
                res.append(new_colors[k])
                break

    res = np.array(res, dtype=np.uint8)
    res = np.reshape(res, (width, height, d))

    im = Image.fromarray(res)
    im.save("output.png")