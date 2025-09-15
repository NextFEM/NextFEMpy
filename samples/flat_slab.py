'''
This example creates a flat slab model. The columns are simulated by pinned supports.
'''

from nextfempy import NextFEMrest

# Connect to the running instance of NextFEM Designer
nf = NextFEMrest()

# Clear the current model and set units
nf.newModel()
nf.setUnits('m', 'kN')

# Materials
mat = nf.addIsoMaterial(name='betao', E=30e6, ni=0.20, Wden=25)

# Sections
laje = nf.addPlanarSection(t=0.28)

# Generate mesh elements
nf.addMeshedWall(
    ID = 1,
    origX = 0.0,
    origY = 0.0,
    origZ = 0.0,
    div1 = 54,
    div2 = 54,
    plan = 'XY',
    leng = 27.0,
    hei = 27.0,
    angle = 0,              # optional
    tilt = '0',             # optional
    nodeOffset = 0,         # optional
    isHorizontal = False    # optional
    )

# Assign material and section to elements
for ele in nf.elemsList:
    nf.assignMaterialToElement(ele, mat)
    nf.assignSectionToElement(ele, laje)

# Boundary conditions
blkd = True; free = False

for n in [1, 13, 28, 43, 55]:
    nf.setBC(str(n), blkd, blkd, blkd, free, free, free)

for n in [661, 673, 688, 703, 715]:
    nf.setBC(str(n), blkd, blkd, blkd, free, free, free)
    
for n in [1486, 1498, 1513, 1528, 1540]:
    nf.setBC(str(n), blkd, blkd, blkd, free, free, free)

for n in [2311, 2323, 2338, 2353, 2365]:
    nf.setBC(str(n), blkd, blkd, blkd, free, free, free)

for n in [2971, 2983, 2998, 3013, 3025]:
    nf.setBC(str(n), blkd, blkd, blkd, free, free, free)

# Load
nf.addLoadCase('pEd')

for ele in range(1, int(nf.elemsNumber)+1):
    nf.addSurfaceLoad(
     	elem = str(ele),
     	values =  [-18.0],
     	direction = 3, 
     	loadcase = 'pEd', 
     	local = False,
        )

# Analyse the model
nf.RunModel()

# Refresh NextFEM GUI
nf.refreshDesignerView(0, resize=True)