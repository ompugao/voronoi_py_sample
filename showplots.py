#!/usr/bin/env python
import pickle
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon

if __name__ == '__main__':
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.axis('equal')
    with open('data2.pkl', 'rb') as f:
        o = pickle.load(f)
    for poly in o:
        patch = PolygonPatch(Polygon(poly), facecolor='#6699cc', alpha=0.5)
        ax.add_patch(patch)
    plt.show()
