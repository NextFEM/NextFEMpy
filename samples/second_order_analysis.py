from nextfempy import NextFEMrest

# Connect to the running instance of NextFEM Designer
nf = NextFEMrest()

# Clear the model and set units
nf.newModel()
nf.setUnits('m', 'kN')

# Materials
mat = nf.addMatFromLib('A36')    # E = 200 GPa

# Sections
sec = nf.addSectFromLib('w14x48')

# nodes
n1 = nf.addNode(0.0, 0.0, 0.0)
n2 = nf.addNode(0.0, 0.0, 8.53)

# Elements
nf.addBeam(n1, n2, sec, mat)

# Divide elements
elems = nf.divideLine(
    lines = ['1'],
    fractions = [.25, .5, .75, 1.0]
    )

# Supports
blkd = True; free = False

nf.setBC('1', blkd, blkd, blkd, blkd, blkd, blkd)

# Load case
nf.addLoadCase('P+Q')

P = 890
Q = 4.45

nf.addNodalLoad(
    node = '2', 
    value = -P, 
    direction = 3, 
    loadcase = 'P+Q', 
    local = False
    )

nf.addNodalLoad(
    node = '2', 
    value = Q, 
    direction = 1, 
    loadcase = 'P+Q', 
    local = False
    )

# Set second order analysis
nf.setPDeltaAnalysis('P+Q')

# Run the model
nf.RunModel()

# Refresh the app
nf.refreshDesignerView(0, resize=True)