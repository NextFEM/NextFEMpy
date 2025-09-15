'''
This example illustrates how to model a presstressed beam using equivalent loads to the prestress.
'''

from nextfempy import NextFEMrest

# Connect to the open instance of NextFEM Designer
nf = NextFEMrest()

# Clear the model and set units
nf.newModel()
nf.setUnits('m', 'kN')

# Materials
mat = nf.addIsoMaterial(name='betao', E=30e6, ni=0.20, Wden=25)

# Sections
sec = nf.addRectSection(0.40, 0.80)

# Nodes
n1 = nf.addNode( 0.0, 0, 0.0)
n2 = nf.addNode(13.2, 0, 0.0)
n3 = nf.addNode(26.4, 0, 0.0)

# Boundary conditions
blkd = True; free = False

nf.setBC(n1, blkd, blkd, blkd, blkd, free, blkd)
nf.setBC(n2, free, blkd, blkd, blkd, free, blkd)
nf.setBC(n3, free, blkd, blkd, blkd, free, blkd)

# Elements
e1 = nf.addBeam(n1, n2, sec, mat)
e2 = nf.addBeam(n2, n3, sec, mat)

# Load cases
for lc in ['pp', 'pe']:
    nf.addLoadCase(lc)
    
# 'pp' load case
nf.setSelfWeight('pp')
        
# 'pe' load case
P = 1500

# -- Concentrated loads at the left end
H = P
V = -P*2*(0.40 - 0.15)/6.0
M = 0

forces = [H, V, M]

for i, component in enumerate([1, 3, 5]):
    nf.addNodalLoad(
        node = n1,
        value = forces[i], 
        direction = component, 
        loadcase = 'pe', 
        local = False
        )

# -- Concentrated loads at the right end
H = -P
V = -P*2*(0.40 - 0.15)/6.0
M = 0

forces = [H, V, M]

for i, component in enumerate([1, 3, 5]):
    nf.addNodalLoad(
        node = n3,
        value = forces[i], 
        direction = component, 
        loadcase = 'pe', 
        local = False
        )
    
# -- Distributed loads on element e1
q1 = 2*(0.40 - 0.15)*P/6.0**2
q2 = 2*(0.40 - 0.15)*P/3.6**2

nf.addBeamLoadA(
    elem = e1,
    values = [q1, q1, q2, q2, -q2, -q2],
    positions = [0.0, 6.0, 6.0, 9.6, 9.6, 13.2],
    direction = 2,
    loadcase = 'pe',
    local = True
    )

# -- Distributed loads on element e2
nf.addBeamLoadA(
    elem = e2,
    values = [-q2, -q2, q2, q2, q1, q1],
    positions = [0.0, 3.6, 3.6, 7.2, 7.2, 13.2],
    direction = 2,
    loadcase = 'pe',
    local = True
    )

# Analyse the model
nf.RunModel()

# Refresh NextFEM GUI
nf.refreshDesignerView(0, resize=True)

