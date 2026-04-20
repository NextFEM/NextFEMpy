'''
This sample illustrates how to build and solve a plane strain problem.
It is very common to use the theory of elasticity with elements in a
plane strain state in geotechnical problems.

The model consists of a soil mass with a length of 20 m and a height of 10 m.
It is subject to its self-weight and a load of 10 kN/m2 on its top.

The problem is defined in the XY plane, which is mandatory in NextFEM
for this kind of problem.
'''

from nextfempy import NextFEMrest

# Connect to the open instance of NextFEM Designer and create the nf object
nf = NextFEMrest(_msg=False)

# Clear the model
nf.newModel()

# Set units
nf.setUnits('m', 'kN')

# Materials
solo = nf.addIsoMaterial(name='solo', E=40e3, ni=0.30, Wden=18)

# Thickness of the quad elements
sec = nf.addPlanarSection(t=1.00)

# Nodes
n1  = nf.addNode( 0.0,  0.0, 0.0)
n2  = nf.addNode(20.0,  0.0, 0.0)
n3  = nf.addNode( 0.0, 10.0, 0.0)
n4  = nf.addNode(20.0, 10.0, 0.0)

# Macro quad element
A = nf.addQuad(n1, n2, n4, n3, sect=sec, mat=solo)

# Generate the mesh
quads = nf.divideQuad(quadID=A, divX=10, divY=20)

# Set elements as plane strain elements
for ele in quads:
    nf.setPlaneStrainElement(ele, isPlaneStrain=True)

# Boundary conditions
blkd = True; free = False

nf.setBC(n1, blkd, blkd, blkd, free, free, free)
nf.setBC(n2, blkd, blkd, blkd, free, free, free)

nf.setBC(n3, blkd, free, blkd, free, free, free)
nf.setBC(n4, blkd, free, blkd, free, free, free)

for n in range(5, 23+1, 1):
    nf.setBC(str(n), free, blkd, blkd, free, free, free)

for n in range(24, 192+1, 21):
    nf.setBC(str(n), blkd, free, blkd, free, free, free)

for n in range(44, 212+1, 21):
    nf.setBC(str(n), blkd, free, blkd, free, free, free)

# g load
nf.addLoadCase('g')
nf.setSelfWeightDirection(direction=-2)
nf.setSelfWeight('g')

# q load
nf.addLoadCase('q')
for ele in range(182, 201+1, 1):
    nf.addEdgeLoad(
        elem = str(ele),
        values = [-10.0],
        edge = 3,
        direction = 2,
        loadcase = 'q',
        local = False
        )

# Analyse the model
nf.RunModel()

# Refresh NextFEM GUI
nf.refreshDesignerView(0, resize=True)