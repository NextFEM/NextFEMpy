from nextfempy import NextFEMrest

# Connect to the running instance of NextFEM Designer
nf = NextFEMrest()

# Clear the model and set units
nf.newModel()
nf.setUnits('m', 'kN')

# Materials
mat = nf.addMatFromLib('C25/30')

# Sections
sec = nf.addRectSection(0.30, 0.5)

# Spans
spans = [4.0, 5.0, 4.0]

# Generate nodes
nelems = len(spans)
nnodes = nelems + 1

nf.addNode(0.0, 0.0, 0.0)
x = 0
for ele in range(nelems):
    x = x + spans[ele]
    nf.addNode(x, 0.0, 0.0)

# Generate elements
for ele in range(1, nelems + 1):
    nf.addBeam(str(ele), str(ele+1), sec, mat)

# Generate supports
blkd = True; free = False

nf.setBC('1', blkd, blkd, blkd, blkd, free, blkd)
for node in range(2, nnodes + 1):
    nf.setBC(str(node), free, blkd, blkd, blkd, free, blkd)

# Load cases
for lc in ['pp', 'sc1']:
    nf.addLoadCase(lc)

# pp
nf.setSelfWeight('pp')
        
# sc1
nf.addBeamLoad(
    elem = '1',
    values = [-10, -10],
    positions = [0.0, spans[0]],
    direction = 2, 
    loadcase = 'sc1', 
    local = True,
    )

# Analyse the model
nf.RunModel()

# Save the model using the same name as Python script
import os
model_name = os.path.basename(__file__)
model_name = model_name.replace('.py', '.nxf')
dir = os.path.dirname(os.path.realpath(__file__)) # get current dir
print(nf.saveModel(dir + '\\' + model_name))

# Refresh the app
nf.refreshDesignerView(0, resize=True)