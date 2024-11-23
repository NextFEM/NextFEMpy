# NextFEMpy

NextFEM REST API wrapper in pure Python, to be used with NextFEM Designer or NextFEM Server. 
It is a complete set of REST API call, wrapped in Python functions, distinguishing between mandatory and optional arguments.

If you're looking for NextFEMpy source, look into /nextfempy folder.

## Installation instructions

```
pip install nextfempy
```

## Usage

Before using with your local installation of NextFEM Designer, start the plugin REST API Server.

```
from nextfempy import NextFEMrest
# connect to local copy of NextFEM Designer
nf=NextFEMapiREST.NextFEMrest()
```

To handle a property:
```
nf.autoMassInX=False
print(str(nf.autoMassInX))
```

To call a NextFEM API method:

```
nf.addOrModifyCustomData("test","Test")
print(nf.getCustomData("test"))
```