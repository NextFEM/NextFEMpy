'''
Example of a continuous 3 equal span beam, subject to a thermal gradient in the
local y direction.
'''

from nextfempy import NextFEMrest

# Connect to the running instance of NextFEM Designer
nf = NextFEMrest()

# Clear the current model and set units
nf.newModel()
nf.setUnits('m', 'kN')

# Materials
mat = nf.addMatFromLib('C25/30')

# Sections
b = 0.30; h = 0.60
sec = nf.addRectSection(b, h)
I = b*h**3/12

# Nodes
L = 7.0
n1 = nf.addNode(0.0, 0, 0.0)
n2 = nf.addNode(  L, 0, 0.0)
n3 = nf.addNode(2*L, 0, 0.0)
n4 = nf.addNode(3*L, 0, 0.0)

# Boundary conditions
blkd = True; free = False

nf.setBC(n1, blkd, blkd, blkd, blkd, free, blkd)
nf.setBC(n2, free, blkd, blkd, blkd, free, blkd)
nf.setBC(n3, free, blkd, blkd, blkd, free, blkd)
nf.setBC(n4, free, blkd, blkd, blkd, free, blkd)

# Elements
e1 = nf.addBeam(n1, n2, sec, mat)
e2 = nf.addBeam(n2, n3, sec, mat)
e3 = nf.addBeam(n3, n4, sec, mat)

# Load cases
nf.addLoadCase('vdt')

# Thermal load definition
DeltaT = 10
for e in [e1, e2, e3]:
    nf.addThermalDistLoad(
    	elem = e, 
    	values = [0, 0, DeltaT],    # [uniform, gradient_z, gradient_y]
    	loadcase = 'vdt'
        )

# Solve the model
nf.RunModel()

# Get material properties
alphaT = float(nf.getMaterialProperty(str(mat), 'alphaT'))
E = float(nf.getMaterialProperty(str(mat), 'E'))

# Get the moment in the 2nd span
M_nf = nf.getBeamForce(num=e2, loadcase='vdt', time='1', type=6, station=3)

print('\n---------------------------------------------------')
print('Moment in the 2nd span due to the thermal gradient:')
print(f'- Solution by NextFEM:  M = {M_nf:.3f} kNm')

# Theoretical solution
M_theor = (6/5)*alphaT*(DeltaT/h)*(E*I)

print(f'- Theoretical solution: M = {M_theor:.3f} kNm')
print('---------------------------------------------------')
print('')

# Refresh NextFEM GUI
nf.refreshDesignerView(0, resize=True)
