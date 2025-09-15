'''
This is a very basic example:
a simply supported beam with a span of 5.0 m and a load of 10 kN/m.
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
sec = nf.addRectSection(0.30, 0.40)

# Nodes
n1 = nf.addNode( 0.0, 0.0, 0.0)
n2 = nf.addNode( 5.0, 0.0, 0.0)

# Boundary conditions
blkd = True; free = False

nf.setBC(n1, blkd, blkd, blkd, blkd, free, blkd)
nf.setBC(n2, free, blkd, blkd, blkd, free, blkd)

# Elements
nf.addBeam(n1, n2, sec, mat)

# Load cases
for lc in ['p']:
    nf.addLoadCase(lc)

nf.addBeamLoadU(
	elem = '1',
	value = -10,
	direction = 2,
	loadcase = 'p',
	local = True
    )

# Analyse the model
nf.RunModel()

# Refresh NextFEM GUI
nf.refreshDesignerView(0, resize=True)