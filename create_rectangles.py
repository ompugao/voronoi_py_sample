#!/usr/bin/env python
import pickle
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon
from shapely.ops import cascaded_union

filename =input('filename > ')

#df = pd.read_csv('/home/leus/sandbox/linear_mpc_mecanum_wheel/path.csv')
fig = plt.figure()
ax  = fig.add_subplot(111)
#ax.plot(np.array(df['cx']), np.array(df['cy']))

w = 0.4
h = 0.4

b_load = True
polygons = []
patches = []

if b_load:
    with open('data2.pkl', 'rb') as f:
        polygons = pickle.load(f)
    for polygon in polygons:
        patch = PolygonPatch(polygon, facecolor='#6699cc', alpha=0.5)
        patches.append(patch)
        ax.add_patch(patch)

def onclick(event):
    global ax
    #print 'event.button=%d,  event.x=%d, event.y=%d, event.xdata=%f, event.ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata)
    if event.button == 1:
        rect = [[event.xdata-w/2, event.ydata-h/2],
                [event.xdata-w/2, event.ydata+h/2],
                [event.xdata+w/2, event.ydata+h/2],
                [event.xdata+w/2, event.ydata-h/2]]
        print(rect)
        polygon = Polygon(rect)
        polygons.append(polygon)

        patch = PolygonPatch(polygon, facecolor='#6699cc', alpha=0.5)
        patches.append(patch)
        ax.add_patch(patch)
        plt.draw()
    elif event.button == 3:
        print('remove')
        patches[-1].remove()
        del patches[-1]
        del polygons[-1]
        plt.draw()
    elif event.button == 2:
        print('quit')
        with open(filename, 'wb') as f:
            pickle.dump(polygons, f)
        import sys
        sys.exit(0)

def on_motion(event):
    pass

cid = fig.canvas.mpl_connect('button_press_event', onclick)
cidmotion = fig.canvas.mpl_connect( 'motion_notify_event', on_motion)

plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.axis('equal')
plt.show()

if __name__ == '__main__':
    pass
    # with open('001.txt', 'r') as f:
        # o = pickle.load(f)
    #fig, ax = plt.subplots()
 
    #polygons = [Polygon(p) for p in o]
    #for p in polygons:
    #    patch = PolygonPatch(p, facecolor='#6699cc', alpha=0.5)
    #    ax.add_patch(patch)
 
    #boundary = cascaded_union(polygons)
    #print(boundary.type)
    #patch = PolygonPatch(boundary, facecolor='#6699cc', edgecolor='r',
    #                     linewidth=3, alpha=0.5, zorder=2)
    #ax.add_patch(patch)
 
    #ax.set_aspect('equal')
    #ax.autoscale()
    #ax.margins(0.1)
    #plt.show()
