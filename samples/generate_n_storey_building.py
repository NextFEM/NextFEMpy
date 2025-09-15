'''
This template illustrates how to generate a spatial frame structure using for loops.

The main data are lists of spans, for example:
    
lx = [5.0, 5.0, 5.0]
ly = [6.0, 6.0]
lz = [4.0, 3.0]

It also illustrates how to perform a modal analysis.
'''

from nextfempy import NextFEMrest

# Connect to the open instance of NextFEM Designer
nf = NextFEMrest()

# Clear the model
nf.newModel()

# Set units
nf.setUnits( 'm', 'kN')

# Materials
mat = nf.addMatFromLib('C25/30')

# Sections
pilares = nf.addRectSection(0.30, 0.30)
vigasx = nf.addRectSection(0.20, 0.50)
vigasy = nf.addRectSection(0.20, 0.50)
lajes = nf.addPlanarSection(t=0.20)

# Spans in both directions and floor heights
lx = [5.0, 5.0, 5.0, 2.0, 2.0]
ly = [6.0, 6.0]
lz = [4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]

# Number of bays along x, bays along y, and storeys
nlx = len(lx)
nly = len(ly)
nlz = len(lz)

import numpy as np

# Coords x
x = np.zeros(nlx + 1)
for i in range(1, nlx + 1):
    x[i] = x[i-1] + lx[i-1]

# Coords y
y = np.zeros(nly + 1)
for j in range(1, nly + 1):
    y[j] = y[j-1] + ly[j-1]

# Coords z
z = np.zeros(nlz + 1)
for k in range(1, nlz + 1):
    z[k] = z[k-1] + lz[k-1]

# Nodes
for k in range(nlz + 1):
    for j in range(nly + 1):
        for i in range(nlx + 1):
            nf.addNode(x[i], y[j], z[k])

# Colums
n = 0
for k in range(nlz):
    for j in range(nly + 1):
        for i in range(nlx + 1):
            n = n + 1
            nf.addBeam(str(n), str(n + (nlx+1)*(nly+1)), pilares, mat)

# Beams along x
n = (nlx + 1)*(nly + 1) - 1
for k in range(nlz):
    for j in range(nly + 1):
        n = n + 1
        for i in range(nlx):
            n = n + 1
            nf.addBeam(str(n), str(n+1), vigasx, mat)

# Beams along y
n = (nlx + 1)*(nly + 1) - nlx - 1
for k in range(nlz):
    n = n + nlx + 1
    for j in range(nly):
        for i in range(nlx + 1):
            n = n + 1
            nf.addBeam(str(n), str(n + nlx + 1), vigasy, mat)

# Slab pannels
n = (nlx + 1)*(nly + 1) - nlx - 2
for k in range(nlz):
    n = n + nlx + 1
    for j in range(nly):
        n = n + 1
        for i in range(nlx):
            n = n + 1
            nf.addQuad(str(n), str(n+1), str(n + nlx + 2), str(n + nlx + 1))

# Boundary conditions
for n in range(1, (nlx+1)*(nly+1) + 1):
    nf.setBC(str(n), True, True, True, True, True, True)

# Load cases
for lc in ['pp', 'modal']:
    nf.addLoadCase(lc)

# 'pp'
nf.setSelfWeight('pp')

# Get masses from lc 'pp'
nf.setLoadsToMass('pp')

# Perform modal analysis
nf.setModalAnalysis('modal', 9)

# Analyse the model
nf.RunModel()

# Refresh NextFEM GUI
nf.refreshDesignerView(0, resize=True)
