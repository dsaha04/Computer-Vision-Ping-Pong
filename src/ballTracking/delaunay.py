import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri
import matplotlib.collections

numSeeds = 24
radius = 100
seeds = radius * np.random.random((numSeeds, 2))
print("seeds:\n", seeds)
print("BBox Min:", np.amin(seeds, axis=0),"Bbox Max: ", np.amax(seeds, axis=0))

center = np.mean(seeds, axis=0)
print("Center:", center)
center = np.asarray(center)

# Create coordinates for the corners of the frame
coords = [center+radius*np.array((-1, -1)),center+radius*np.array((+1, -1)),center+radius*np.array((+1, +1)),center+radius*np.array((-1, +1))]


def circumcenter( tri):
    pts = np.asarray([coords[v] for v in tri])
    pts2 = np.dot(pts, pts.T)
    A = np.bmat([[2 * pts2, [[1], [1], [1]]], [[[1, 1, 1, 0]]]])
    b = np.hstack((np.sum(pts * pts, axis=1), [1]))
    x = np.linalg.solve(A, b)
    bary_coords = x[:-1]
    center = np.dot(bary_coords, pts)
    # radius = np.linalg.norm(pts[0] - center) # euclidean distance
    radius = np.sum(np.square(pts[0] - center))  # squared distance
    return (center, radius)

# Create two dicts to store triangle neighbours and circumcircles.
triangles = {}
circles = {}

# Create two CCW triangles for the frame
T1 = (0, 1, 3)
T2 = (2, 3, 1)
triangles[T1] = [T2, None, None]
triangles[T2] = [T1, None, None]

def inCircleFast( tri, p):
    center, radius = circles[tri]
    return np.sum(np.square(center - p)) <= radius

# Compute circumcenters and circumradius for each triangle
for t in triangles:
    circles[t] = circumcenter(t)

def addPoint(p):
