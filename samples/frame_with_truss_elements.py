'''
This example illustrates a plane frame with beam and truss elements.
'''

from nextfempy import NextFEMrest

# Connect to the running instance of NextFEM Designer
nf = NextFEMrest()

# Clear the model and set units
nf.newModel()
nf.setUnits('m', 'kN')

# Materials
mat = nf.addIsoMaterial(name='betao', E=30e6, ni=0.20, Wden=25)

# Sections
sec1 = nf.addRectSection(1.00, 0.40)
sec2 = nf.addRectSection(0.30, 0.30)

# Nodes
n1 = nf.addNode( 0.0, 0, 0.0)
n2 = nf.addNode( 5.0, 0, 0.0)
n3 = nf.addNode(13.0, 0, 0.0)
n4 = nf.addNode(18.0, 0, 0.0)
n5 = nf.addNode( 3.0, 0, 2.5)
n6 = nf.addNode( 9.0, 0, 4.5)
n7 = nf.addNode(15.0, 0, 2.5)

# Boundary conditions
blkd = True; free = False

nf.setBC(n1, blkd, blkd, blkd, blkd, free, blkd)
nf.setBC(n4, free, blkd, blkd, blkd, free, blkd)

# Constraint RY in nodes with only truss elements
nf.setBC(n5, free, blkd, free, blkd, blkd, blkd)
nf.setBC(n6, free, blkd, free, blkd, blkd, blkd)
nf.setBC(n7, free, blkd, free, blkd, blkd, blkd)

# Elements
e1 = nf.addBeam(n1, n2, sec1, mat)
e2 = nf.addBeam(n2, n3, sec1, mat)
e3 = nf.addBeam(n3, n4, sec1, mat)

e4  = nf.addTruss(n1, n5, sec2, mat)
e5  = nf.addTruss(n5, n6, sec2, mat)
e6  = nf.addTruss(n6, n7, sec2, mat)
e7  = nf.addTruss(n7, n4, sec2, mat)
e8  = nf.addTruss(n5, n2, sec2, mat)
e9  = nf.addTruss(n2, n6, sec2, mat)
e10 = nf.addTruss(n6, n3, sec2, mat)
e11 = nf.addTruss(n3, n7, sec2, mat)

# Load cases
for lc in ['p']:
    nf.addLoadCase(lc)

# 'p'
for ele in [e1, e2, e3]:
    ln = float(nf.getElementProperty(ele,'lun'))
    nf.addBeamLoadA(
        elem = ele,
        values = [-10, -10],
        positions = [0.0, ln],
        direction = 2, 
        loadcase = 'p', 
        local = True,
        )

# Analyse the model
nf.RunModel()

# Refresh NextFEM GUI
nf.refreshDesignerView(0, resize=True)
