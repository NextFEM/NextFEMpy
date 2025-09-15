'''
This example illustrates how to analyze a pile foundation. The soil is modeled using spring elements.

The pile has free ends, and is subjected to a horizontal force and
a moment, both applied at the top of it.

The pile is divided in 10 elements.

The spring stiffness are calculated as the product between the
soil modulus of elasticity and the element length.
'''

# ======================================================================
# Main data
# ======================================================================

L  = 20.0   # pile lenght, m
d  = 1.5    # pile diameter, m

Es = 9e3    # Soil modulus of elasticity, kN/m**2
Ec = 31e6   # Concrete modulus of elasticity, kN/m**2

F  = 100.0  # Horizontal force at the top, kN
M  = 100.0  # Moment at the top, kNm

# ======================================================================
# Build the model and analyze it
# ======================================================================

from nextfempy import NextFEMrest

# Connect to the running instance of NextFEM Designer
nf = NextFEMrest()

# Clear the current model and set units
nf.newModel()
nf.setUnits('m', 'kN')

# Material
mat = nf.addIsoMaterial(name='betao', E=Ec, ni=0.20, Wden=25)

# Section
sec = nf.addCircSection(d)

# Generate nodes
nf.addNode(0.0, 0.0, 0.0)
z = 0
for ele in range(10):
    z = z + L/10
    nf.addNode(0.0, 0.0, z)

# Generate elements
for ele in range(1, 10+1):
    nf.addBeam(str(ele), str(ele+1), sec, mat)

# Boundary conditions
blkd = True; free = False

nf.setBC( '1', free, blkd, blkd, blkd, free, blkd)
nf.setBC('11', free, blkd, blkd, blkd, free, blkd)

# Add springs at the ends - stiffness equal to half of the inner ones
nf.addSpringProperty(
    name = 'outer',
    Kx = Es*L/10*0.5,
    Ky = 0,
    Kz = 0,
    Krx = 0,
    Kry = 0,
    Krz = 0,
    local=False
    )

for n in ['1', '11']:
    nf.addNodalSpring(n, propName='outer')
    
# Add inner springs
nf.addSpringProperty(
    name = 'inner',
    Kx = Es*L/10,
    Ky = 0,
    Kz = 0,
    Krx = 0,
    Kry = 0,
    Krz = 0,
    local=False
    )

for n in range(2, 10+1):
    nf.addNodalSpring(str(n), propName='inner')

# Loads
nf.addLoadCase('lc')

nf.addNodalLoad(
    node = '11',
    value = F,
    direction = 1,
    loadcase = 'lc',
    local = False
    )

nf.addNodalLoad(
    node = '11',
    value = -M,
    direction = 5,
    loadcase = 'lc',
    local = False
    )

# Solve the model
nf.RunModel()

# Refresh NextFEM GUI
nf.refreshDesignerView(0, resize=True)
