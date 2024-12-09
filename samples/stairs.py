from math import cos, atan
from nextfempy import NextFEMrest

# Connect to the running instance of NextFEM Designer
nf = NextFEMrest()

# Clear the model
nf.newModel()
nf.setUnits('m', 'kN')

# Materials
mat = nf.addMatFromLib('C25/30')

# Sections
sec = nf.addRectSection(Lz = 1.00, Ly = 0.27)

# Nodes
n1 = nf.addNode(0.0, 0, 0.0)
n2 = nf.addNode(3.0, 0, 1.7)
n3 = nf.addNode(4.5, 0, 1.7)

# Boundary conditions
blkd = True; free = False

nf.setBC(n1, blkd, blkd, blkd, blkd, free, blkd)
nf.setBC(n3, free, blkd, blkd, blkd, free, blkd)

# Common constratins for plane structures
# nf.setBC(n2, free, blkd, free, blkd, free, blkd)
# nf.setBC(n3, free, blkd, free, blkd, free, blkd)

# Elements
e1 = nf.addBeam(n1, n2, sec, mat)
e2 = nf.addBeam(n2, n3, sec, mat)

# Load cases
for lc in ['p']:
    nf.addLoadCase(lc)

# 'p'
ph = 18.32
pl = ph*cos(atan(1.7/3.0))

ele_len = float(nf.getElementProperty(e1,'lun'))

nf.addBeamLoad(
    elem = e1,
    values = [-pl, -pl],
    positions = [0.0, ele_len],
    direction = 3, 
    loadcase = 'p',
    local = False
    )

# Analyse teh model
nf.RunModel()

# Refresh the app
nf.refreshDesignerView(0, resize=True)