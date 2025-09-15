'''
This example illustrates how to model a slab supported on beams.

It also illustrates how to use meshing methods available in NextFEM designer.

Live loads are applied separately to each panel and then properly combined to get maximum internal forces.
'''

from nextfempy import NextFEMrest

# Connect to the open instance of NextFEM Designer
nf = NextFEMrest()

# Clear model
nf.newModel()

# Set units
nf.setUnits('m', 'kN')

# Materials
mat = nf.addIsoMaterial(name='betao', E=30e6, ni=0.20, Wden=25)

# Sections
viga = nf.addRectSection(0.30, 0.5)
laje = nf.addPlanarSection(t=0.23)

# Modify beam section properties to simulate pinned supports
# added = nf.setSectionProperty(str(viga), 'Jxc', 100)
added = nf.setSectionProperty(str(viga), 'Jt', 0)

# Nodes
n1  = nf.addNode( 6.0,  0.0, 0.0)
n2  = nf.addNode(12.0,  0.0, 0.0)
n3  = nf.addNode( 0.0,  6.0, 0.0)
n4  = nf.addNode( 6.0,  6.0, 0.0)
n5  = nf.addNode(12.0,  6.0, 0.0)
n6  = nf.addNode(14.0,  6.0, 0.0)
n7  = nf.addNode( 0.0, 12.0, 0.0)
n8  = nf.addNode( 6.0, 12.0, 0.0)
n9  = nf.addNode(12.0, 12.0, 0.0)
n10 = nf.addNode(14.0, 12.0, 0.0)
n11 = nf.addNode( 6.0, 14.0, 0.0)
n12 = nf.addNode(12.0, 14.0, 0.0)

# Boundary conditions
blkd = True; free = False

for n in range(1,12+1):
    nf.setBC(str(n), blkd, blkd, blkd, free, free, free)

for n in [n6, n10, n11, n12]:
    nf.removeBC(n)

# Beams
b1  = nf.addBeam(n1, n2, viga, mat)
b2  = nf.addBeam(n3, n4, viga, mat)
b3  = nf.addBeam(n4, n5, viga, mat)
b4  = nf.addBeam(n7, n8, viga, mat)
b5  = nf.addBeam(n8, n9, viga, mat)

b6  = nf.addBeam(n3, n7, viga, mat)
b7  = nf.addBeam(n1, n4, viga, mat)
b8  = nf.addBeam(n4, n8, viga, mat)
b9  = nf.addBeam(n2, n5, viga, mat)
b10 = nf.addBeam(n5, n9, viga, mat)

# Macro quads
A = nf.addQuad(n3, n4, n8, n7, laje, mat)
B = nf.addQuad(n4, n5, n9, n8, laje, mat)
C = nf.addQuad(n1, n2, n5, n4, laje, mat)

cons1 = nf.addQuad(n5, n6, n10,  n9, laje, mat)
cons2 = nf.addQuad(n8, n9, n12, n11, laje, mat)

# Divide macro quads
quadsA = nf.divideQuad(quadID=A, divX=12, divY=12)
quadsB = nf.divideQuad(quadID=B, divX=12, divY=12)
quadsC = nf.divideQuad(quadID=C, divX=12, divY=12)

quads_cons1 = nf.divideQuad(quadID=cons1, divX=12, divY= 4)
quads_cons2 = nf.divideQuad(quadID=cons2, divX= 4, divY=12)

# Merge overlapped nodes in the model
nf. mergeOverlappedNodes()

# Mesh beams at quad nodes
nf.checkLineElements()

### LOAD CASES ###

# pp
nf.addLoadCase('pp')
nf.setSelfWeight('pp')

# rcp
nf.addLoadCase('rcp')

quads = list(quadsA) + list(quadsB) + list(quadsC)
for ele in quads:
    nf.addSurfaceLoad(
    	elem = ele,
    	values =  [-3.0],
    	direction = 3, 
    	loadcase = 'rcp', 
    	local = False,
        )

quads = list(quads_cons1) + list(quads_cons2)
for ele in quads:
    nf.addSurfaceLoad(
    	elem = ele,
    	values =  [-1.0],
    	direction = 3, 
    	loadcase = 'rcp', 
    	local = False,
        )

# scA
nf.addLoadCase('scA')
for ele in quadsA:
    nf.addSurfaceLoad(
    	elem = ele,
    	values =  [-2.0],
    	direction = 3, 
    	loadcase = 'scA',
    	local = False,
        )

# scB
nf.addLoadCase('scB')
for ele in quadsB:
    nf.addSurfaceLoad(
    	elem = ele,
    	values =  [-2.0],
    	direction = 3, 
    	loadcase = 'scB',
    	local = False,
        )

# scC
nf.addLoadCase('scC')
for ele in quadsC:
    nf.addSurfaceLoad(
    	elem = ele,
    	values =  [-2.0],
    	direction = 3, 
    	loadcase = 'scC',
    	local = False,
        )

# sc_cons1
nf.addLoadCase('sc_cons1')
for ele in quads_cons1:
    nf.addSurfaceLoad(
    	elem = ele,
    	values =  [-2.0],
    	direction = 3, 
    	loadcase = 'sc_cons1',
    	local = False,
        )

# sc_cons2
nf.addLoadCase('sc_cons2')
for ele in quads_cons2:
    nf.addSurfaceLoad(
    	elem = ele,
    	values =  [-2.0],
    	direction = 3, 
    	loadcase = 'sc_cons2',
    	local = False,
        )

### LOAD COMBINATIONS ###

# Maximum positive moment at pannel A
nf.addLoadCase('uls_maxMposA')

nf.setCombination('uls_maxMposA',  'pp', 1.35)
nf.setCombination('uls_maxMposA', 'rcp', 1.35)

nf.setCombination('uls_maxMposA', 'scA', 1.50)
nf.setCombination('uls_maxMposA', 'scC', 1.50)
nf.setCombination('uls_maxMposA', 'sc_cons1', 1.50)
nf.setCombination('uls_maxMposA', 'sc_cons2', 1.50)

# Maximum negative momento at border AB
nf.addLoadCase('uls_maxMnegAB')

nf.setCombination('uls_maxMnegAB',  'pp', 1.35)
nf.setCombination('uls_maxMnegAB', 'rcp', 1.35)

nf.setCombination('uls_maxMnegAB', 'scA', 1.50)
nf.setCombination('uls_maxMnegAB', 'scB', 1.50)

# Maximum positive momento at pannel B
nf.addLoadCase('uls_maxMposB')

nf.setCombination('uls_maxMposB',  'pp', 1.35)
nf.setCombination('uls_maxMposB', 'rcp', 1.35)

nf.setCombination('uls_maxMposB', 'scB', 1.50)

# Sobrecarga em todos os painéis
nf.addLoadCase('uls_sc_all')

nf.setCombination('uls_sc_all',  'pp', 1.35)
nf.setCombination('uls_sc_all', 'rcp', 1.35)

nf.setCombination('uls_sc_all', 'scA', 1.50)
nf.setCombination('uls_sc_all', 'scB', 1.50)
nf.setCombination('uls_sc_all', 'scC', 1.50)
nf.setCombination('uls_sc_all', 'sc_cons1', 1.50)
nf.setCombination('uls_sc_all', 'sc_cons2', 1.50)

# Analyse the model
nf.RunModel()

# Refresh NextFEM GUI
nf.refreshDesignerView(0, resize = True)