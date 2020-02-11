#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import math
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon, Point, MultiPoint
from shapely.ops import cascaded_union, nearest_points
from scipy.spatial import Voronoi
from itertools import combinations
import networkx as nx
import numpy as np
 
class poly_voro:
    def __init__(self, poly):
        self.poly = poly
        self.ridges = []
        self.__preproc()
        print(len(self.ridges))
 
    def __extract_obstacles(self):
        facets = []
        if self.poly.type == 'Polygon':
            v = [list(p) for p in self.poly.exterior.coords[:]]
            facets.append([list(s) for s in zip(v[:-1], v[1:])])
            for i in self.poly.interiors:
                v = [list(p) for p in i.coords[:]]
                facets.append([list(s) for s in zip(v[:-1], v[1:])])
        elif self.poly.type == 'MultiPolygon':
            self.poly = self.poly.geoms[1]
            v = [list(p) for p in self.poly.exterior.coords[:]]
            facets.append([list(s) for s in zip(v[:-1], v[1:])])
            for i in self.poly.interiors:
                v = [list(p) for p in i.coords[:]]
                facets.append([list(s) for s in zip(v[:-1], v[1:])])
        else:
            raise ValueError('Unhandled geometry type: ' + repr(self.poly.type))
        return facets
 
    def __is_ridge(self, p, q):
        return self.poly.contains(p) and self.poly.contains(q)
 
    def __preproc(self):
        sites = []
        for lol in self.__extract_obstacles(): 
            sites += self.__subdivide(lol) 
        vor = Voronoi(sites)
        V = vor.vertices
        for i, ridge in enumerate(vor.ridge_vertices):
            if -1 in ridge:
                continue
            p, q = V[ridge[0]], V[ridge[1]]
            if self.__is_ridge(Point(p), Point(q)):
                self.ridges.append([p.tolist(), q.tolist()])
 
    def draw(self):
        fig, ax = plt.subplots()
        ax.axis('equal')
        #ax.set_aspect('equal', adjustable='box')
        patch = PolygonPatch(self.poly, facecolor='#6699cc', linewidth=2)
        ax.add_patch(patch)
        ax.add_collection(mc.LineCollection(self.ridges, linewidths=1))
        from IPython.terminal import embed; ipshell=embed.InteractiveShellEmbed(config=embed.load_default_config())(local_ns=locals())

        #ax.autoscale()
        ax.margins(0.1)
        plt.show()
 
    def __length(self, l):
        x0, y0 = l[0]
        x1, y1 = l[1]
        return math.sqrt((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1))
 
    def __subdivide(self, list_of_lines):
        sub_points = []
        for l in list_of_lines:
            n = self.__length(l) / 0.01
            dx = (l[1][0] - l[0][0]) / n
            dy = (l[1][1] - l[0][1]) / n
            sub_points += [l[0]]
            for i in range(1, int(n)):
                sub_points.append([l[0][0] + dx * i, l[0][1] + dy * i])
        return sub_points
 
class ridge_graph:
    def __init__(self, ridges):
        self._ridges = ridges
        self.__g = self.__const_graph()
 
    def __const_graph(self):
        edges = []
        g = nx.Graph()
        for s, t in combinations(range(len(self._ridges)), 2):
            if self.__is_connected(s, t):
                g.add_node(s, pos=(self._ridges[s][0], self._ridges[s][1]))
                g.add_node(t, pos=(self._ridges[t][0], self._ridges[t][1]))
                edges.append((s, t, self.__length(s) + self.__length(t)))
        g.add_weighted_edges_from(edges)
        return g
 
    def __is_connected(self, i, j):
        si = self._ridges[i][0]
        ti = self._ridges[i][1]
        sj = self._ridges[j][0]
        tj = self._ridges[j][1]
        return True if si == sj or si == tj or ti == sj or ti == tj else False
 
    def __length(self, i):
        sx, sy = self._ridges[i][0]
        tx, ty = self._ridges[i][1]
        return math.sqrt((sx-tx)**2 + (sy-ty)**2)
 
    def get_sp_ridges(self, s, t):
        return [self._ridges[i] \
                for i in nx.shortest_path(self.__g, s, t, 'weight')]

    def get_candidate_point(self, xy, r):
        xy = [0.52, 0.84]
        p = nearest_points(Point(), MultiPoint(np.array(rg._ridges).reshape(-1, 2)))[1]
        #p = nearest_points(Point(xy), np.unique(np.reshape(self._ridges, (2, -1)), axis=1))[0]


if __name__ == '__main__':
    with open('data3.pkl', 'rb') as f:
        o = pickle.load(f)
    #floor_sketch = cascaded_union([Polygon(p) for p in o])
    surroundingrect = Polygon([[-3, -3], [3, -3], [3, 3], [-3, 3]])
    floor_sketch = surroundingrect.difference(cascaded_union(o))
    pv = poly_voro(floor_sketch)
    #rg = ridge_graph(pv.ridges)

    pv.draw()

