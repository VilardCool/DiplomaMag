import numpy as np

class Color(object):
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

class OctreeNode(object):
    def __init__(self, level, parent):
        self.color = Color(0, 0, 0)
        self.pixel_count = 0
        self.palette_index = 0
        self.children = [None for _ in range(8)]
        # add node to current level
        if level < OctreeQuantizer.MAX_DEPTH - 1:
            parent.add_level_node(level, self)

    def is_leaf(self):
        return self.pixel_count > 0

    def get_leaf_nodes(self):
        leaf_nodes = []
        for i in range(8):
            node = self.children[i]
            if node:
                if node.is_leaf():
                    leaf_nodes.append(node)
                else:
                    leaf_nodes.extend(node.get_leaf_nodes())
        return leaf_nodes

    def get_nodes_pixel_count(self):
        sum_count = self.pixel_count
        for i in range(8):
            node = self.children[i]
            if node:
                sum_count += node.pixel_count
        return sum_count

    def add_color(self, color, level, parent):
        if level >= OctreeQuantizer.MAX_DEPTH:
            self.color.red += color.red
            self.color.green += color.green
            self.color.blue += color.blue
            self.pixel_count += 1
            return
        index = self.get_color_index_for_level(color, level)
        if not self.children[index]:
            self.children[index] = OctreeNode(level, parent)
        self.children[index].add_color(color, level + 1, parent)

    def get_palette_index(self, color, level):
        if self.is_leaf():
            return self.palette_index
        index = self.get_color_index_for_level(color, level)
        if self.children[index]:
            return self.children[index].get_palette_index(color, level + 1)
        else:
            # get palette index for a first found child node
            for i in range(8):
                if self.children[i]:
                    return self.children[i].get_palette_index(color, level + 1)

    def remove_leaves(self):
        result = 0
        for i in range(8):
            node = self.children[i]
            if node:
                self.color.red += node.color.red
                self.color.green += node.color.green
                self.color.blue += node.color.blue
                self.pixel_count += node.pixel_count
                result += 1
        return result - 1

    def get_color_index_for_level(self, color, level):
        index = 0
        mask = 0x80 >> level
        if color.red & mask:
            index |= 4
        if color.green & mask:
            index |= 2
        if color.blue & mask:
            index |= 1
        return index

    def get_color(self):
        return Color(
            self.color.red / self.pixel_count,
            self.color.green / self.pixel_count,
            self.color.blue / self.pixel_count)


class OctreeQuantizer(object):
    MAX_DEPTH = 8

    def __init__(self):
        self.levels = {i: [] for i in range(OctreeQuantizer.MAX_DEPTH)}
        self.root = OctreeNode(0, self)

    def get_leaves(self):
        return [node for node in self.root.get_leaf_nodes()]

    def add_level_node(self, level, node):
        self.levels[level].append(node)

    def add_color(self, color):
        # passes self value as `parent` to save nodes to levels dict
        self.root.add_color(color, 0, self)

    def make_palette(self, color_count):
        palette = []
        palette_index = 0
        leaf_count = len(self.get_leaves())
        # reduce nodes
        # up to 8 leaves can be reduced here and the palette will have
        # only 248 colors (in worst case) instead of expected 256 colors
        for level in range(OctreeQuantizer.MAX_DEPTH - 1, -1, -1):
            if self.levels[level]:
                for node in self.levels[level]:
                    leaf_count -= node.remove_leaves()
                    if leaf_count <= color_count:
                        break
                if leaf_count <= color_count:
                    break
                self.levels[level] = []
        # build palette
        for node in self.get_leaves():
            if palette_index >= color_count:
                break
            if node.is_leaf():
                palette.append(node.get_color())
            node.palette_index = palette_index
            palette_index += 1
        return palette

    def get_palette_index(self, color):
        return self.root.get_palette_index(color, 0)

def OCTree(image, palette):
    width = image.shape[1]
    height = image.shape[0]

    octree = OctreeQuantizer()

    # add colors to the octree
    for i in range(height):
        for j in range(width):
            octree.add_color(Color(*image[i, j]))

    # 256 colors for 8 bits per pixel output image
    palette = octree.make_palette(palette)

    # save output image
    out_image = np.copy(image)
    for i in range(height):
        for j in range(width):
            index = octree.get_palette_index(Color(*image[i, j]))
            color = palette[index]
            out_image[i, j] = (color.red, color.green, color.blue)
    
    return out_image