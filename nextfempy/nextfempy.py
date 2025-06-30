import requests,json,urllib,os,urllib3

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sbool(arg):
    if arg=="True":
        return True
    else:
        return False

def qt(s):
    try:
        return str(urllib.parse.quote(s, safe=''))
    except:
        return str(s)

class NextFEMrest:
    headers = {}

    def __init__(self,_baseUrl=None,_user="",_msg=True):
        if _baseUrl is None:
            self.baseUrl="http://localhost:5151"
        else:
            self.baseUrl=str(_baseUrl)
        self.user=_user
        self.msg=_msg
        if self.user != "": self.headers["user"]=self.user

    def setHeaders(self, headersDict):
        ''' Set headers for the requests '''
        if not(headersDict is None):
            for dd in headersDict:
                self.headers[dd]=headersDict[dd]

    def nfrest(self, method, command, body=None, heads=None):
        url = self.baseUrl + command
        hds=dict()
        for dd in self.headers:
            hds[dd]=self.headers[dd]
        if not(heads is None):
            for dd in heads:
                hds[dd]=heads[dd]
        if method == "POST":
            response = requests.post(url=url, headers=hds, json=body, verify=False)
        elif method == "PUT":
            response = requests.put(url=url, headers=hds, json=body, verify=False)
        elif method == "GET":
            response = requests.get(url=url, headers=hds, verify=False)
        elif method == "DELETE":
            response = requests.delete(url=url, headers=hds, verify=False)
        # print request and return response
        if self.msg: print("*** " + self.user + " :: " + method, command, response.status_code)
        return response.text

    def nfrestB(self, method, command, body=None, heads=None):
        # return bytes
        url = self.baseUrl + command
        hds=dict()
        for dd in self.headers:
            hds[dd]=self.headers[dd]
        if not(heads is None):
            for dd in heads:
                hds[dd]=heads[dd]
        if method == "POST":
            response = requests.post(url=url, headers=hds, json=body, verify=False)
        elif method == "PUT":
            response = requests.put(url=url, headers=hds, json=body, verify=False)
        elif method == "GET":
            response = requests.get(url=url, headers=hds, verify=False)
        elif method == "DELETE":
            response = requests.delete(url=url, headers=hds, verify=False)
        return response.content

    # methods and properties for Server
    def saveUser(self): 
        ''' Save the model on server '''
        return sbool(self.nfrest('GET', '/op/saveuser'))
    # get file from server, return bytes
    def userFile(self, filename, localPath):
        ''' Get a file from server, return bytes
        
        Args:
            filename: Name of the file to get
            localPath: Path where to save the file
        
        Returns:
            Bytes
        '''
        bts=self.nfrestB('GET', '/op/userfile', None, dict([("path",filename)]))
        if bts==b'False': 
            return False
        with open(localPath, "wb") as binary_file:
            binary_file.write(bts)
        return True
    # send file to server, return string
    def sendFile(self,localPath,remoteFolder=None):
        ''' Send file to server, return string
        
        Args:
            localPath: Path of the file to send
            remoteFolder: Optional. Folder on server where to save the file. If not set, the file will be saved in the default folder.
        
        Returns:
            String
        '''
        filename = os.path.basename(localPath)
        files = {
            'file': (filename, open(localPath, 'rb'), 'application/octet-stream')
        }
        headers = self.headers.copy()
        headers['path'] = remoteFolder
        url = self.baseUrl + '/op/userfile'
        try:
            response = requests.post(url, headers=headers, files=files, verify=False)
            if self.msg:
                print("*** " + self.user + " :: POST /op/userfile", response.status_code)
            return response.text
        except Exception as e:
            return f"Error in sending file: {str(e)}"
        finally:
            files['file'][1].close()
    # get file list from server fo current user
    def userFiles(self)->list:
        ''' Get file list from server for current user
        
        Returns:
            List of files
        '''
        try:
            return json.loads(self.nfrest('GET', '/op/userfiles', None, None))
        except Exception as e:
            return ["User not logged-in"]

    # methods and properties
    def activeBarsDiameters(self):
        ''' Get a list of active rebar diameters in the model
        
        
        Returns:
            Array of Int32
        '''
        return json.loads(self.nfrest('GET', '/element/rebar/barsdiam', None, None))
    def activeHoopsDiameters(self):
        ''' Get a list of active bar diameters for hoops/stirrups
        
        
        Returns:
            Array of Int32
        '''
        return json.loads(self.nfrest('GET', '/element/rebar/hoopsdiam', None, None))
    def addBeam(self, n1, n2, sect=0, mat=0, sect2=0):
        ''' Add a new beam to the model. Existing results will be deleted.
        
        Args:
            n1: First node ID
            n2: Second node ID
            sect (optional): Optional section ID
            mat (optional): Optional material ID
            sect2 (optional): Optional section ID of the section at the end of the beam

        Returns:
            The ID of the added elem
        '''
        return self.nfrest('GET', '/element/add/beam/'+qt(n1)+'/'+qt(n2)+'/'+str(sect)+'/'+str(mat)+'/'+str(sect2)+'', None, None)
    def addBeamLoad(self, elem, value1, value2, position1, position2, direction, loadcase, local=False):
        ''' Add a distributed load on the specified beam
        
        Args:
            elem: Beam element retaining the load
            value1: Initial value
            value2: Final value
            position1: Initial position
            position2: Final position
            direction: Direction of the load: 1=X, 2=Y, 3=Z, 4=RX, 5=RY, 6=RZ
            loadcase: Name of the loadcase
            local (optional): Optional, default is false. True if load has been defined locally

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/element/beamadd/'+qt(elem)+'/'+str(value1)+'/'+str(value2)+'/'+str(position1)+'/'+str(position2)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', None, None))
    def addBeamLoadA(self, elem, values:list, positions:list, direction, loadcase, local=False):
        ''' Add a distributed load on the specified beam
        
        Args:
            elem: Beam element retaining the load
            values: Array of load values
            positions: Array of load positions
            direction: Direction of the load: 1=X, 2=Y, 3=Z, 4=RX, 5=RY, 6=RZ
            loadcase: Name of the loadcase
            local (optional): Optional, default is false. True if load has been defined locally

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/element/beamaddA/'+qt(elem)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', None, dict([("values",json.dumps(values)),("positions",json.dumps(positions))])))
    def addBeamLoadU(self, elem, value, direction, loadcase, local=False):
        ''' Add a uniformly distributed load on the specified beam
        
        Args:
            elem: Beam element retaining the load
            value: Load value
            direction: Direction of the load: 1=X, 2=Y, 3=Z, 4=RX, 5=RY, 6=RZ
            loadcase: Name of the loadcase
            local (optional): Optional, default is false. True if load has been defined locally

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/element/beamaddU/'+qt(elem)+'/'+str(value)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', None, None))
    def addBeamWithID(self, n1, n2, ID, sect=0, mat=0, sect2=0):
        ''' Add a new beam to the model with the desired ID. Existing results will be deleted.
        
        Args:
            n1: First node ID
            n2: Second node ID
            ID: Element ID
            sect (optional): Optional section ID
            mat (optional): Optional material ID
            sect2 (optional): Optional section ID of the section at the end of the beam

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/element/add/beamwithid/'+qt(n1)+'/'+qt(n2)+'/'+qt(ID)+'/'+str(sect)+'/'+str(mat)+'/'+str(sect2)+'', None, None))
    def addBoxSection(self, Lz, Ly, tw, tf1, tf2):
        ''' Add a new beam box section to the model.
        
        Args:
            Lz: Outer base
            Ly: Outer height
            tw: Wall thickness
            tf1: Top flange thickness
            tf2: Bottom flange thickness

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/box/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(tf2)+'', None, None))
    def addCircleInSection(self, sectionID, diameter, centerX, centerY, isEmpty=False, material=0, doNotCenter=False):
        ''' Add a circular figure in the selected section
        
        Args:
            sectionID: ID of the section
            diameter: Diameter
            centerX: Center X
            centerY: Center Y
            isEmpty (optional): Optional, True if figure is a hole
            material (optional): Optional, ID of the figure material
            doNotCenter (optional): Optional, avoid section centering

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/add/addcirc/'+str(sectionID)+'/'+str(diameter)+'/'+str(centerX)+'/'+str(centerY)+'/'+str(isEmpty)+'/'+str(material)+'/'+str(doNotCenter)+'', None, None))
    def addCircSection(self, D):
        ''' Add a new beam circular section to the model.
        
        Args:
            D: Diameter D

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/circ/'+str(D)+'', None, None))
    def addCSection(self, Lz, Ly, tw, tf1, tf2, Lz2=0):
        ''' Add a new beam C section to the model.
        
        Args:
            Lz: Outer base
            Ly: Outer height
            tw: Wall thickness
            tf1: Top flange thickness
            tf2: Bottom flange thickness
            Lz2 (optional): Outer bottom base, if different from top

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/cshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(tf2)+'/'+str(Lz2)+'', None, None))
    def addDCSection(self, Lz, Ly, tw, tf1, tf2, gap, Lz2=0):
        ''' Add a new beam double-C section to the model.
        
        Args:
            Lz: Outer base
            Ly: Outer height
            tw: Wall thickness
            tf1: Top flange thickness
            tf2: Bottom flange thickness
            gap: Gap between single profiles
            Lz2 (optional): Outer bottom base, if different from top

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/doublecshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(tf2)+'/'+str(gap)+'/'+str(Lz2)+'', None, None))
    def addDesignMatFromLib(self, name):
        ''' Add a design material from library
        
        Args:
            name: 

        Returns:
            ID of the added material, 0 if not found
        '''
        return int(self.nfrest('POST', '/designmaterial/add/fromlib', name, None))
    def addDesMaterial(self, name, E, fk, ni=0, type=0):
        ''' Add a design material from scratch. Uniaxial type is required (e.g. rebar, FRP, etc.)
        
        Args:
            name: Name of the new design material
            E: Young's modulus
            fk: Characteristic strength
            ni (optional): Optional. Poisson's ratio
            type (optional): Optional. Integer to set materal type for checking: 1 steel, aluminium 2, concrete 3, timber 4, masonry 5, tensionFragile 6

        Returns:
            ID of the added material
        '''
        return int(self.nfrest('GET', '/material/add/des/'+qt(name)+'/'+str(E)+'/'+str(fk)+'/'+str(ni)+'/'+str(type)+'', None, None))
    def addDLSection(self, Lz, Ly, tw, tf1, gap):
        ''' Add a new beam double L section to the model.
        
        Args:
            Lz: Outer base
            Ly: Outer height
            tw: Wall thickness
            tf1: Bottom flange thickness
            gap: Gap between single profiles

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/doublelshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(gap)+'', None, None))
    def addDTSection(self, Lz, Ly, tw, tf1, tf2, Lz2=0):
        ''' Add a new beam double-T section to the model.
        
        Args:
            Lz: Outer base
            Ly: Outer height
            tw: Wall thickness
            tf1: Top flange thickness
            tf2: Bottom flange thickness
            Lz2 (optional): Outer bottom base, if different from top

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/dtshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(tf2)+'/'+str(Lz2)+'', None, None))
    def addEC8spectrum(self, ag, q, LS, damping=0.05, soilType='A', type1=True):
        ''' Add a EC8 spectrum function from given paramters.
        
        Args:
            ag: Spectral acceleration for T=0
            q: Behaviour factor
            LS: Limit State (OLS,DLS,LLS or CLS)
            damping (optional): Damping ratio for the spectrum. Eg. 0.05
            soilType (optional): Soil category, letters A,B,C,D,E
            type1 (optional): Flag. If true, Type 1 spectrum is returned, Type 2 otherwise.

        Returns:
            The ID of the added spectral function
        '''
        return int(self.nfrest('GET', '/function/ec8spectrum/'+str(ag)+'/'+str(q)+'/'+qt(LS)+'/'+str(damping)+'/'+qt(soilType)+'/'+str(type1)+'', None, None))
    def addEdgeLoad(self, elem, values:list, edge, direction, loadcase, local=False):
        ''' Add a uniform or linear distributed load on the specified edge of planar element.
        
        Args:
            elem: Planar element retaining the load
            values: Array of nodal values. Use one value if constant.
            edge: Index of the edge to be loaded. It starts from 1.
            direction: Direction of the load: 1=X, 2=Y, 3=Z, 4=RX, 5=RY, 6=RZ
            loadcase: Name of the loadcase
            local (optional): Optional. True if load has been defined locally. False by default

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/load/element/edgeadd/'+qt(elem)+'/'+str(edge)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', values, None))
    def addFillInSection(self, sectionID, x:list, y:list, material=0, doNotCenter=False):
        ''' Add a filled figure in an already defined beam section
        
        Args:
            sectionID: ID of the section
            x: Array of x coordinates
            y: Array of y coordinates
            material (optional): Optional, ID of the figure material
            doNotCenter (optional): Optional, avoid section centering

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/add/fill/'+str(sectionID)+'/'+str(material)+'/'+str(doNotCenter)+'', None, dict([("x",json.dumps(x)),("y",json.dumps(y))])))
    def addFloorPlane(self, name, type, n1, n2, n3, n4=''):
        ''' Add a floor plane load to the model
        
        Args:
            name: Name of the floor load to be used
            type: Distribution of the floor load: 1 triangular - 2 quadrangular-centroid - 3 oriented quadrangular - 4 two-way quadrangular
            n1: 1st node
            n2: 2nd node
            n3: 3rd node
            n4 (optional): 4th node required only if quadrangular distribution is set

        Returns:
            True if successful, False if not or if nodes don't form a plane or beam elements don't cover the entire perimeter
        '''
        return sbool(self.nfrest('GET', '/load/floor/planeadd/'+qt(name)+'/'+str(type)+'/'+qt(n1)+'/'+qt(n2)+'/'+qt(n3)+'/'+qt(n4)+'', None, None))
    def addGroup(self, name):
        ''' Add an empty group to the model
        
        Args:
            name: 

        Returns:
            False if already existing, True otherwise
        '''
        return sbool(self.nfrest('GET', '/group/add/'+qt(name)+'', None, None))
    def addHoleInSection(self, sectionID, x:list, y:list, material=0, doNotCenter=False):
        ''' Add and empty figure in an already defined beam section
        
        Args:
            sectionID: ID of the section
            x: Array of x coordinates
            y: Array of y coordinates
            material (optional): Optional, ID of the figure material
            doNotCenter (optional): Optional, avoid section centering

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/add/hole/'+str(sectionID)+'/'+str(material)+'/'+str(doNotCenter)+'', None, dict([("x",json.dumps(x)),("y",json.dumps(y))])))
    def addIsoMaterial(self, name, E, ni, Wden, fk=0, conductivity=0, specificHeat=0, type=0):
        ''' Add an isotropic material from scratch
        
        Args:
            name: Name of the new material
            E: Young's modulus
            ni: Poisson's ratio
            Wden: Weight density
            fk (optional): Characteristic strength
            conductivity (optional): Conductivity, for thermal analysis
            specificHeat (optional): Specific heat, for thermal analysis
            type (optional): Optional. Integer to set materal type for checking: 1 steel, aluminium 2, concrete 3, timber 4, masonry 5, tensionFragile 6

        Returns:
            ID of the added material
        '''
        return int(self.nfrest('GET', '/material/add/iso/'+qt(name)+'/'+str(E)+'/'+str(ni)+'/'+str(Wden)+'/'+str(fk)+'/'+str(conductivity)+'/'+str(specificHeat)+'/'+str(type)+'', None, None))
    def addLayeredPlanarSection(self, layerThicknesses:list, layerMaterials:list):
        ''' Add a new layered planar section to the model
        
        Args:
            layerThicknesses: Array of double with layer thicknesses
            layerMaterials: Array of integers with layer materials

        Returns:
            The ID assigned to the section
        '''
        return int(self.nfrest('GET', '/section/add/layeredplanar', None, dict([("layerThicknesses",json.dumps(layerThicknesses)),("layerMaterials",json.dumps(layerMaterials))])))
    def addLoadCase(self, name):
        ''' Add a loacase of a given name to the model
        
        Args:
            name: Name of the loadcase

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/add/'+qt(name)+'', None, None))
    def addLoadCaseToCombination(self, name, loadcase, factor):
        ''' Add a loadcase and a factor to an already existing combination, buckling or PDelta analysis
        
        Args:
            name: Name of the combination or buckling analysis
            loadcase: Name of the loadcase to add to the combination
            factor: Factor for the loadcase to add to the combination

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/add/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'', None, None))
    def addLoadCaseToTimeHistoryAnalysis(self, name, loadcase, factor, THid=-1):
        ''' Add a loadcase and a factor to an already existing time-history analysis (static or dynamic)
        
        Args:
            name: Name of the existing time-history analysis
            loadcase: Name of the loadcase to add
            factor: Factor for the loadcase to add
            THid (optional): Optional. The ID of the time series to associate with load, default is -1 for ramp

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/addth/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'/'+str(THid)+'', None, None))
    def addLongitRebar(self, elem, X, Y, area, matID, Linit, Lfin, rectBase=0, strandTens=0):
        ''' Add a longitudinal rebar to a member (beam, column or wall)
        
        Args:
            elem: ID of the element
            X: X coordinate in transversal section
            Y: Y coordinate in transversal section
            area: Area of the rebar
            matID: ID of the associated design material
            Linit: Initial abscissa from 0 to 1
            Lfin: Final abscissa from 0 to 1
            rectBase (optional): Optional. Rectangular width if layer is added instead of bar
            strandTens (optional): Optional. Tension for strand

        Returns:
            True is successful
        '''
        return sbool(self.nfrest('GET', '/element/rebar/long/'+qt(elem)+'/'+str(X)+'/'+str(Y)+'/'+str(area)+'/'+str(matID)+'/'+str(Linit)+'/'+str(Lfin)+'/'+str(rectBase)+'/'+str(strandTens)+'', None, None))
    def addLongitRebarInSection(self, sectionID, X, Y, area, matID, rectBase=0, strandTens=0):
        ''' Add a longitudinal bar to a section
        
        Args:
            sectionID: ID of the section
            X: X coordinate in transversal section
            Y: Y coordinate in transversal section
            area: Area of the rebar
            matID: ID of the associated design material
            rectBase (optional): Optional. Rectangular width if layer is added instead of bar
            strandTens (optional): Optional. Tension for strand

        Returns:
            Bar is added if area is bigger of the eventual bar in the same position. To avoid this, clear rebar prior to use this command
        '''
        return sbool(self.nfrest('GET', '/section/rebar/long/'+qt(sectionID)+'/'+str(X)+'/'+str(Y)+'/'+str(area)+'/'+str(matID)+'/'+str(rectBase)+'/'+str(strandTens)+'', None, None))
    def addLongitRebarInSection(self, sectionID, X, Y, area, matID, rectBase=0, strandTens=0):
        ''' Add a longitudinal bar to a section
        
        Args:
            sectionID: ID of the section
            X: X coordinate in transversal section
            Y: Y coordinate in transversal section
            area: Area of the rebar
            matID: ID of the associated design material
            rectBase (optional): Optional. Rectangular width if layer is added instead of bar
            strandTens (optional): Optional. Tension for strand

        Returns:
            Bar is added if area is bigger of the eventual bar in the same position. To avoid this, clear rebar prior to use this command
        '''
        return sbool(self.nfrest('GET', '/section/rebar/long/'+str(sectionID)+'/'+str(X)+'/'+str(Y)+'/'+str(area)+'/'+str(matID)+'/'+str(rectBase)+'/'+str(strandTens)+'', None, None))
    def addLSection(self, Lz, Ly, tw, tf1):
        ''' Add a new beam L section to the model.
        
        Args:
            Lz: Outer base
            Ly: Outer height
            tw: Wall thickness
            tf1: Bottom flange thickness

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/lshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'', None, None))
    def addMatFromLib(self, name):
        ''' Add a material from library
        
        Args:
            name: 

        Returns:
            ID of the added material, 0 if not found
        '''
        return int(self.nfrest('POST', '/material/add/fromlib', name, None))
    def addMember(self, elems:list):
        ''' Add a member in the model
        
        Args:
            elems: Array of beam IDs to be added. The first entry will be the member name

        Returns:
            True if successful, False otherwise. Beams are ordered
        '''
        return sbool(self.nfrest('GET', '/model/member/add', None, dict([("elems",json.dumps(elems))])))
    def addMeshedWall(self, ID, origX, origY, origZ, div1, div2, plan, leng, hei, angle=0, tilt='0', nodeOffset=10000, isHorizontal=False):
        ''' Add a wall to the model meshed with quad elements
        
        Args:
            ID: ID of the wall
            origX: X origin coordinate
            origY: Y origin coordinate
            origZ: Z origin coordinate
            div1: Number of division along 1st direction
            div2: Number of division along 2st direction
            plan: Plane of the wall, use "XY", "XZ" or "YZ"
            leng: Lenght of the wall
            hei: Height of the wall
            angle (optional): Optional. Angle with respect to the normal of XY plane, or angle with respect to the horizontal for YZ and YZ planes
            tilt (optional): Optional, default "0". Use "x" or "y" for YZ and YZ planes
            nodeOffset (optional): Optional, default 10000. Offset for node numbering
            isHorizontal (optional): Set to true to create vertical section cuts. If omitted or set to false, vertical wall is assumed.

        Returns:
            A list of nodes for the wall
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/addmeshedwall/'+str(ID)+'/'+str(origX)+'/'+str(origY)+'/'+str(origZ)+'/'+str(div1)+'/'+str(div2)+'/'+qt(plan)+'/'+str(leng)+'/'+str(hei)+'/'+str(angle)+'/'+qt(tilt)+'/'+str(nodeOffset)+'/'+str(isHorizontal)+'', None, None))
    def addNodalDisp(self, node, disp, direction, loadcase):
        ''' Add an imposed displacement to the selected node
        
        Args:
            node: Node retaining the load
            disp: Imposed displacement value
            direction: Direction of the load: 1=X, 2=Y, 3=Z, 4=RX, 5=RY, 6=RZ
            loadcase: Name of the loadcase

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/node/disp/'+qt(node)+'/'+str(disp)+'/'+str(direction)+'/'+qt(loadcase)+'', None, None))
    def addNodalLoad(self, node, value, direction, loadcase, local=False):
        ''' Add a nodal load to the model
        
        Args:
            node: Node retaining the load
            value: Load value
            direction: Direction of the load: 1=X, 2=Y, 3=Z, 4=RX, 5=RY, 6=RZ
            loadcase: Name of the loadcase
            local (optional): True if load has been defined locally

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/node/add/'+qt(node)+'/'+str(value)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', None, None))
    def addNodalMass(self, ID, tmx, tmy, tmz, rmx, rmy, rmz):
        ''' Add a nodal mass
        
        Args:
            ID: ID of the node hosting the mass
            tmx: Translational mass in X
            tmy: Translational mass in Y
            tmz: Translational mass in Z
            rmx: Rotational inertia around X
            rmy: Rotational inertia around Y
            rmz: Rotational inertia around Z

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/mass/add/'+qt(ID)+'/'+str(tmx)+'/'+str(tmy)+'/'+str(tmz)+'/'+str(rmx)+'/'+str(rmy)+'/'+str(rmz)+'', None, None))
    def addNodalSpring(self, n1, propName):
        ''' Add a spring connected to the ground. Existing results will be deleted.
        
        Args:
            n1: Selected node
            propName: Name of the property of the spring

        Returns:
            The ID of the added elem
        '''
        return self.nfrest('GET', '/element/add/nodalspring/'+qt(n1)+'/'+qt(propName)+'', None, None)
    def addNode(self, x, y, z, lcs1X=0, lcs1Y=0, lcs1Z=0, lcs2X=0, lcs2Y=0, lcs2Z=0):
        ''' Add a new node to the model. Existing results will be deleted.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
            lcs1X (optional): 1st vector of nodal local axis: component x
            lcs1Y (optional): 1st vector of nodal local axis: component y
            lcs1Z (optional): 1st vector of nodal local axis: component z
            lcs2X (optional): 2nd vector of nodal local axis: component x
            lcs2Y (optional): 2nd vector of nodal local axis: component y
            lcs2Z (optional): 2nd vector of nodal local axis: component z

        Returns:
            The ID of the added node, empty string in case of error
        '''
        return self.nfrest('GET', '/node/add/'+str(x)+'/'+str(y)+'/'+str(z)+'/'+str(lcs1X)+'/'+str(lcs1Y)+'/'+str(lcs1Z)+'/'+str(lcs2X)+'/'+str(lcs2Y)+'/'+str(lcs2Z)+'', None, None)
    def addNodeWithID(self, x, y, z, ID):
        ''' Add a new node with ID
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
            ID: ID of the node to be added to the model

        Returns:
            True if successful, False if node is already existing
        '''
        return sbool(self.nfrest('GET', '/node/add/'+str(x)+'/'+str(y)+'/'+str(z)+'/'+qt(ID)+'', None, None))
    def addNormalhinge(self, name, checkType, position, includeShear=False, includeTorsion=False, cKpl=0.001, FresRatio=0.2):
        ''' Add a beam hinge without NVM interaction, ready to be assigned to elements. To be used typically for beams part of rigid floors
        
        Args:
            name: Name of the hinge
            checkType: Name of the check to be applied - use "Concrete_EC" or "Concrete_NTC" for concrete beams, "Steel_Hinge_EC3" for steel, "Aluminium_Hinge_EC9" for aluminium alloy, or national/custom rules
            position: Position in percentage of beam length (0 or 100)
            includeShear (optional): True to include shear DoFs
            includeTorsion (optional): True to include torsion as hinge DoF
            cKpl (optional): Ratio for plastic branch stiffness over elastic stiffness
            FresRatio (optional): Residual force after failure, ratio with yielding

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/hinge/add/simple/'+qt(name)+'/'+qt(checkType)+'/'+str(position)+'/'+str(includeShear)+'/'+str(includeTorsion)+'/'+str(cKpl)+'/'+str(FresRatio)+'', None, None))
    def addNTCspectrum(self, lat, lon, LS, soil, Vr, St, hh=1, q0=1, isHregular=False, damping=0.05, customAg=0, VerticalComponent=False):
        ''' Add a NTC 2018 spectrum from given parameters.
        
        Args:
            lat: Latitude in WGS84. Location must be in Italy.
            lon: Longitude in WGS84. Location must be in Italy.
            LS: Limit State for spectrum: SLO, SLD, SLV or SLC
            soil: Soil category, letters A,B,C,D,E
            Vr: Reference life as per NTC 2018, in years
            St: Topographic coefficient for the site
            hh (optional): h/H ratio of building site, maximum is 1
            q0 (optional): Behaviour factor, default is 1.0 (elastic spectrum)
            isHregular (optional): True for regular shaped buildings over height
            damping (optional): Damping ratio for the spectrum. Eg. 0.05
            customAg (optional): Optional. Spectral acceleration for T=0
            VerticalComponent (optional): True if spectrum is for vertical component. Deafult is false.

        Returns:
            The ID of the added spectral function
        '''
        return int(self.nfrest('GET', '/function/ntcspectrum/'+str(lat)+'/'+str(lon)+'/'+qt(LS)+'/'+qt(soil)+'/'+str(Vr)+'/'+str(St)+'/'+str(hh)+'/'+str(q0)+'/'+str(isHregular)+'/'+str(damping)+'/'+str(customAg)+'/'+str(VerticalComponent)+'', None, None))
    def addNVMhinge(self, name, checkType, position, includeShear=False, includeTorsion=False, cKpl=0.001, FresRatio=0.2, stopResidualBranch=False):
        ''' Add a beam hinge with NVM interaction, ready to be assigned to elements. Typically, this is the hinge for columns.
        
        Args:
            name: Name of the hinge
            checkType: Name of the check to be applied - use "Concrete_EC" or "Concrete_NTC" for concrete beams, "Steel_Hinge_EC3" for steel, "Aluminium_Hinge_EC9" for aluminium alloy, or national/custom rules
            position: Position in percentage of beam length (0 or 100)
            includeShear (optional): True to include shear as interaction DoFs
            includeTorsion (optional): True to include torsion as hinge DoF
            cKpl (optional): Ratio for plastic branch stiffness over elastic stiffness
            FresRatio (optional): Residual force after failure, ratio with yielding
            stopResidualBranch (optional): Optional, default is false. If true, hinge exhibits a residual branch with its own ultimate deformation

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/hinge/add/nvm/'+qt(name)+'/'+qt(checkType)+'/'+str(position)+'/'+str(includeShear)+'/'+str(includeTorsion)+'/'+str(cKpl)+'/'+str(FresRatio)+'/'+str(stopResidualBranch)+'', None, None))
    def addObject(self, o, other=0):
        ''' Directly add object to model
        
        Args:
            o: Object to be added
            other (optional): Flag to distinguish object types

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/model/addobject/'+str(other)+'', o, None))
    def addOmegaSection(self, Lz, Ly, tw, d):
        ''' Add a new beam omega or cold-formed C section to the model.
        
        Args:
            Lz: Inner base
            Ly: Outer height
            tw: Wall thickness
            d: Outer flange length

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/omega/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(d)+'', None, None))
    def addOrChangeDesMaterialProperty(self, ID, name, value, units=''):
        ''' Add or modify a custom property of the selected design material
        
        Args:
            ID: ID of the design material
            name: Name of the property
            value: Value of the property as string. Value must use . as decimal separator
            units (optional): Optional. Units of measure for property value

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/designmaterial/prop/'+str(ID)+'/'+qt(name)+'/'+qt(value)+'/'+qt(units)+'', None, None))
    def addOrChangeMaterialProperty(self, ID, name, value, units=''):
        ''' Add or modify a custom property of the selected material
        
        Args:
            ID: ID of the material
            name: Name of the property
            value: Value of the property as a string (including name, code, etc.). Value must use . as decimal separator
            units (optional): Optional. Units of measure for property value

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/material/prop/'+str(ID)+'/'+qt(name)+'/'+qt(value)+'/'+qt(units)+'', None, None))
    def addOrModifyCustomData(self, key, value):
        ''' Add a data field into the model
        
        Args:
            key: Key, must be unique
            value: Value to store, in string format, or object already serialize in JSON

        Returns:
            True
        '''
        return sbool(self.nfrest('POST', '/model/customdata/'+qt(key)+'', value, None))
    def addPipeSection(self, D, t):
        ''' Add a new beam pipe section to the model.
        
        Args:
            D: Outer diameter D
            t: Thickness t

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/pipe/'+str(D)+'/'+str(t)+'', None, None))
    def addPlanarSection(self, t):
        ''' Add a new planar section to the model
        
        Args:
            t: Thickness

        Returns:
            The ID assigned to the section
        '''
        return int(self.nfrest('GET', '/section/add/planar/'+str(t)+'', None, None))
    def addQuad(self, n1, n2, n3, n4, sect=0, mat=0):
        ''' Add a quad planar element to the model
        
        Args:
            n1: Connected node 1
            n2: Connected node 2
            n3: Connected node 3
            n4: Connected node 4
            sect (optional): Optional section ID
            mat (optional): Optional material ID

        Returns:
            The ID of the added elem
        '''
        return self.nfrest('GET', '/element/add/quad/'+qt(n1)+'/'+qt(n2)+'/'+qt(n3)+'/'+qt(n4)+'/'+str(sect)+'/'+str(mat)+'', None, None)
    def addQuadWithID(self, n1, n2, n3, n4, ID, sect=0, mat=0):
        ''' Add a quad planar element to the model with the desired ID
        
        Args:
            n1: Connected node 1
            n2: Connected node 2
            n3: Connected node 3
            n4: Connected node 4
            ID: Element ID
            sect (optional): Optional section ID
            mat (optional): Optional material ID

        Returns:
            The ID of the added elem
        '''
        return sbool(self.nfrest('GET', '/element/add/quadwithid/'+qt(n1)+'/'+qt(n2)+'/'+qt(n3)+'/'+qt(n4)+'/'+qt(ID)+'/'+str(sect)+'/'+str(mat)+'', None, None))
    def addRebarPattern(self, elem, pattern, Linit, Lfin, numBars, rebCover, matID, area, netSpacing=0):
        ''' Adds rebars by pattern in the selected element.
        
        Args:
            elem: ID of the element
            pattern: Top=0, Bottom=1, Equal spacing=2, Wall=3, Lateral=4, Left=5, Right=6, Intermediate=7
            Linit: Initial abscissa in percentage of length
            Lfin: Final abscissa in percentage of length
            numBars: Number of bars to be placed
            rebCover: Rebar cover from the centre of the first bar to the border of the section. It applies in both directions
            matID: ID of the associated design material
            area: Area of each single rebar rebar
            netSpacing (optional): Spacing of net in walls. Effective only if pattern is 3.

        Returns:
            True is successful
        '''
        return sbool(self.nfrest('GET', '/element/rebar/pattern/'+qt(elem)+'/'+str(pattern)+'/'+str(Linit)+'/'+str(Lfin)+'/'+str(numBars)+'/'+str(rebCover)+'/'+str(matID)+'/'+str(area)+'/'+str(netSpacing)+'', None, None))
    def addRebarPatternInSection(self, pattern, sectionID, numBars, rebCover, matID, area, netSpacing=0):
        ''' Adds rebars by pattern in the selected section.
        
        Args:
            pattern: Top=0, Bottom=1, Equal spacing=2, Wall=3, Lateral=4, Left=5, Right=6
            sectionID: ID of the section
            numBars: Number of bars to be placed
            rebCover: Rebar cover from the centre of the first bar to the border of the section. It applies in both directions
            matID: ID of the associated design material
            area: Area of each single rebar rebar
            netSpacing (optional): Spacing of net in walls. Effective only if pattern is 3.

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/section/rebar/pattern/'+str(pattern)+'/'+str(sectionID)+'/'+str(numBars)+'/'+str(rebCover)+'/'+str(matID)+'/'+str(area)+'/'+str(netSpacing)+'', None, None))
    def addRectangleInSection(self, sectionID, b, h, centerX, centerY, isEmpty=False, material=0, doNotCenter=False):
        ''' Add a rectangular figure in the selected section
        
        Args:
            sectionID: ID of the section
            b: Base
            h: Height
            centerX: Center X
            centerY: Center Y
            isEmpty (optional): Optional, True if figure is a hole
            material (optional): Optional, ID of the figure material
            doNotCenter (optional): Optional, avoid section centering

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/add/addrect/'+str(sectionID)+'/'+str(b)+'/'+str(h)+'/'+str(centerX)+'/'+str(centerY)+'/'+str(isEmpty)+'/'+str(material)+'/'+str(doNotCenter)+'', None, None))
    def addRectSection(self, Lz, Ly):
        ''' Add a new beam rectangular section to the model.
        
        Args:
            Lz: Base Lz
            Ly: Height Ly

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/rect/'+str(Lz)+'/'+str(Ly)+'', None, None))
    def addSectFromLib(self, name):
        ''' Add a section from library
        
        Args:
            name: Name of the section

        Returns:
            ID of the added section, 0 if not found
        '''
        return int(self.nfrest('POST', '/section/add/fromlib', name, None))
    def addSectFromLib(self, name, doNotCenter=False):
        ''' Add a section from library
        
        Args:
            name: Name of the section
            doNotCenter (optional): Optional. Do not center the section, useful for sections by points

        Returns:
            ID of the added section, 0 if not found
        '''
        return int(self.nfrest('POST', '/section/add/fromlib/'+str(doNotCenter)+'', name, None))
    def addSectionByPoints(self, x:list, y:list, CF_tw=0, CF_rc=0, material=0, doNotCenter=False):
        ''' Add a section by points. x() and y() are the 1st series of points (filled figure). If a cold-formed section is added, specify optional parameters.
        
        Args:
            x: Array of x coordinates
            y: Array of y coordinates
            CF_tw (optional): Optional, thickness of a cold-formed section
            CF_rc (optional): Optional, radius of curvature of a cold-formed section
            material (optional): Optional, ID of the section material
            doNotCenter (optional): Optional, avoid section centering

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/bypoints/'+str(CF_tw)+'/'+str(CF_rc)+'/'+str(material)+'/'+str(doNotCenter)+'', None, dict([("x",json.dumps(x)),("y",json.dumps(y))])))
    def addSectionCover(self, sectionID, coverMat, coverThickness):
        ''' Add a section cover, e.g. for fire checking purposes
        
        Args:
            sectionID: ID of the original section
            coverMat: ID of the material for the cover layer
            coverThickness: Thickness of the cover layer

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/add/cover/'+str(sectionID)+'/'+str(coverMat)+'/'+str(coverThickness)+'', None, None))
    def addSectionFromDXF(self, path, CF_tw=0, CF_rc=0, material=0):
        ''' Add a section from a DXF file containing polylines. If a cold-formed section is added, specify optional parameters.
        
        Args:
            path: Full path of DXF file
            CF_tw (optional): Optional, thickness of a cold-formed section
            CF_rc (optional): Optional, radius of curvature of a cold-formed section
            material (optional): Optional, ID of the section material

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/fromdxf/'+str(CF_tw)+'/'+str(CF_rc)+'/'+str(material)+'', None, dict([("path",path)])))
    def addSeriesFunction(self, Xlist:list, Ylist:list, type, units=''):
        ''' Add a time series function to the model
        
        Args:
            Xlist: Array of times/periods
            Ylist: Array of values, same size of Xlist
            type: 0 displacement TH, 1 velocity TH, 2 acceleration TH, 3 acceleration spectrum, 4 displacement spectrum
            units (optional): Units of measure for data in ordinate (Y)

        Returns:
            The ID of the time series, -1 in case of errors
        '''
        return int(self.nfrest('GET', '/function/add/'+str(type)+'', None, dict([("x",json.dumps(Xlist)),("y",json.dumps(Ylist)),("units",units)])))
    def addSineFunction(self, frequency, phase, stp, duration, maxAmplitude, isGrowing=False, type=0, units=''):
        ''' Add a sine function to the model. It can be growing or not.
        
        Args:
            frequency: Frequency of sine function, in Hz
            phase: Phase angle, in radians
            stp: Number of step per cycle
            duration: Duration of the function
            maxAmplitude: Amplitude of the function
            isGrowing (optional): Optional: True if growing sine function. Default: false.
            type (optional): Optional: 0 displacement TH, 1 velocity TH, 2 acceleration TH, 3 acceleration spectrum, 4 displacement spectrum
            units (optional): Optional: Units of measure for data in ordinate (Y)

        Returns:
            The ID of the time series
        '''
        return int(self.nfrest('GET', '/function/sine/'+str(frequency)+'/'+str(phase)+'/'+str(stp)+'/'+str(duration)+'/'+str(maxAmplitude)+'/'+str(isGrowing)+'/'+str(type)+'', None, dict([("units",units)])))
    def addSolid(self, nodes:list, mat=0):
        ''' Add a solid element to the model. Element type is set on the size of the number of nodes
        
        Args:
            nodes: Array of nodes. 4 for tetra, 6 for wedge, 8 for hexa, 10 for tetra10, 15 for wedge15, 20 for hexa20.
            mat (optional): Optional material ID

        Returns:
            The ID of the added elem
        '''
        return self.nfrest('GET', '/element/add/solid/'+str(mat)+'', None, dict([("nodes",json.dumps(nodes))]))
    def addSpring(self, n1, n2, propName):
        ''' Add a new 2-node spring to the model. Existing results will be deleted.
        
        Args:
            n1: First node ID
            n2: Second node ID
            propName: Name of the property of the spring

        Returns:
            The ID of the added elem
        '''
        return self.nfrest('GET', '/element/add/spring/'+qt(n1)+'/'+qt(n2)+'/'+qt(propName)+'', None, None)
    def addSpringNLProperty(self, name, NLdofs:list, NLprops:list, local=False):
        ''' Add a non-linear spring property to the model
        
        Args:
            name: Name of the property, must be unique
            NLdofs: Array of integers from 0 to 15 to associate a non-linear behaviour to each DoF. Use -1 to leave the DoF inactive
            NLprops: Array containing 6 arrays of numerical properties for the each selected non-linear behaviour
            local (optional): True if properties are referred to local axes of the spring element

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/springproperty/nl/add/'+qt(name)+'/'+json.dumps(NLdofs)+'/'+str(local)+'', NLprops, None))
    def addSpringProperty(self, name, Kx, Ky, Kz, Krx, Kry, Krz, local=False):
        ''' Add a spring property to the model
        
        Args:
            name: Name of the property, must be unique
            Kx: Stiffness in X direction
            Ky: Stiffness in Y direction
            Kz: Stiffness in Z direction
            Krx: Stiffness in RX direction
            Kry: Stiffness in RY direction
            Krz: Stiffness in RZ direction
            local (optional): True if properties are referred to local axes of the spring element

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/springproperty/simple/add/'+qt(name)+'/'+str(Kx)+'/'+str(Ky)+'/'+str(Kz)+'/'+str(Krx)+'/'+str(Kry)+'/'+str(Krz)+'/'+str(local)+'', None, None))
    def addSpringsOnOverlappedNodes(self, n:list, propName):
        ''' Add springs on selected overlapped nodes.
        
        Args:
            n: Array of nodes
            propName: Name of the property of the springs

        Returns:
            
        '''
        return json.loads(self.nfrest('POST', '/element/add/springsonnodes/'+qt(propName)+'', n, None))
    def addSpringWithID(self, n1, n2, ID, propName):
        ''' Add a new 2-node spring to the model with the desired ID. Existing results will be deleted.
        
        Args:
            n1: First node ID
            n2: Second node ID
            ID: Element ID
            propName: Name of the property of the spring

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/element/add/springwithid/'+qt(n1)+'/'+qt(n2)+'/'+qt(ID)+'/'+qt(propName)+'', None, None))
    def addStirrupBars(self, elem, LnumY, LnumZ, area, spacing, matID, Linit, Lfin):
        ''' Add stirrup bars to a member (beam, column or wall)
        
        Args:
            elem: ID of the element
            LnumY: Legs in Y dir.
            LnumZ: Legs in Z dir.
            area: Area of the rebar
            spacing: Stirrups spacing
            matID: ID of the associated design material
            Linit: Initial abscissa from 0 to 1
            Lfin: Final abscissa from 0 to 1

        Returns:
            True is successful
        '''
        return sbool(self.nfrest('GET', '/element/rebar/stirrup/'+qt(elem)+'/'+str(LnumY)+'/'+str(LnumZ)+'/'+str(area)+'/'+str(spacing)+'/'+str(matID)+'/'+str(Linit)+'/'+str(Lfin)+'', None, None))
    def addStirrupBarsInSection(self, sectionID, LnumY, LnumZ, area, spacing, matID):
        ''' Add stirrup bars to a section
        
        Args:
            sectionID: ID of the section
            LnumY: Legs in Y dir.
            LnumZ: Legs in Z dir.
            area: Area of the rebar
            spacing: Stirrups spacing
            matID: ID of the associated design material

        Returns:
            True is successful
        '''
        return sbool(self.nfrest('GET', '/section/rebar/stirrup/'+str(sectionID)+'/'+str(LnumY)+'/'+str(LnumZ)+'/'+str(area)+'/'+str(spacing)+'/'+str(matID)+'', None, None))
    def addSubsoilNodalSpringsOnElements(self, n:list, propName):
        ''' Add nodal subsoil springs in nodes of chosen planar elements.
        
        Args:
            n: Array of planar element IDs
            propName: Name of the property of the springs

        Returns:
            True if successful, False if the reference property is defined in local coordinates
        '''
        return sbool(self.nfrest('POST', '/element/add/soilsprings/'+qt(propName)+'', n, None))
    def addSubsoilZProperty(self, width, Rmodulus):
        ''' Add a subsoil distributed spring in Z direction of the model
        
        Args:
            width: Width of the bottom side of element
            Rmodulus: Reaction modulus

        Returns:
            The name of the property added, empty string in case of error
        '''
        return self.nfrest('GET', '/springproperty/subsoil/add/'+str(width)+'/'+str(Rmodulus)+'', None, None)
    def addSurfaceLoad(self, elem, values:list, direction, loadcase, local=False):
        ''' Add a uniformly distributed or bi-linear load on the specified face of planar element.
        
        Args:
            elem: Planar element retaining the load
            values: Array of nodal values. Use one value if constant.
            direction: Direction of the load: 1=X, 2=Y, 3=Z, 4=RX, 5=RY, 6=RZ
            loadcase: Name of the loadcase
            local (optional): Optional. True if load has been defined locally. False by default

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/load/element/surfaceadd/'+qt(elem)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', values, None))
    def addThermalDistLoad(self, elem, values:list, loadcase):
        ''' Add thermal loads for strain-only loading in beams and shells
        
        Args:
            elem: ID of the element
            values: Array of double of length 3: 0 = uniform temperature, 1 = gradient in local z, 2 = gradient in local y
            loadcase: Name of the loadcase

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/load/element/tempdistadd/'+qt(elem)+'/'+qt(loadcase)+'', values, None))
    def addTria(self, n1, n2, n3, sect=0, mat=0):
        ''' Add a tria planar element to the model
        
        Args:
            n1: Connected node 1
            n2: Connected node 2
            n3: Connected node 3
            sect (optional): Optional section ID
            mat (optional): Optional material ID

        Returns:
            The ID of the added elem
        '''
        return self.nfrest('GET', '/element/add/tria/'+qt(n1)+'/'+qt(n2)+'/'+qt(n3)+'/'+str(sect)+'/'+str(mat)+'', None, None)
    def addTriaWithID(self, n1, n2, n3, ID, sect=0, mat=0):
        ''' Add a tria planar element to the model with the desired ID
        
        Args:
            n1: Connected node 1
            n2: Connected node 2
            n3: Connected node 3
            ID: Element ID
            sect (optional): Optional section ID
            mat (optional): Optional material ID

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/element/add/triawithid/'+qt(n1)+'/'+qt(n2)+'/'+qt(n3)+'/'+qt(ID)+'/'+str(sect)+'/'+str(mat)+'', None, None))
    def addTruss(self, n1, n2, sect=0, mat=0):
        ''' Add a new truss to the model. Existing results will be deleted.
        
        Args:
            n1: First node ID
            n2: Second node ID
            sect (optional): Optional section ID
            mat (optional): Optional material ID

        Returns:
            The ID of the added elem
        '''
        return self.nfrest('GET', '/element/add/truss/'+qt(n1)+'/'+qt(n2)+'/'+str(sect)+'/'+str(mat)+'', None, None)
    def addTrussWithID(self, n1, n2, ID, sect=0, mat=0):
        ''' Add a new truss to the model with the desired ID. Existing results will be deleted.
        
        Args:
            n1: First node ID
            n2: Second node ID
            ID: Element ID
            sect (optional): Optional section ID
            mat (optional): Optional material ID

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/element/add/trusswithid/'+qt(n1)+'/'+qt(n2)+'/'+qt(ID)+'/'+str(sect)+'/'+str(mat)+'', None, None))
    def addTSection(self, Lz, Ly, tw, tf1):
        ''' Add a new beam T section to the model.
        
        Args:
            Lz: Outer base
            Ly: Outer height
            tw: Wall thickness
            tf1: Top flange thickness

        Returns:
            The ID assigned to the section.
        '''
        return int(self.nfrest('GET', '/section/add/tshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'', None, None))
    def addVolumeLoad(self, elem, value, direction, loadcase):
        ''' Add volume loading for solids
        
        Args:
            elem: Selected solid element
            value: Value
            direction: Direction of load
            loadcase: Name of the loadcase

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/element/volumeadd/'+qt(elem)+'/'+str(value)+'/'+str(direction)+'/'+qt(loadcase)+'', None, None))
    def alignShellXaxis(self, num, x, y, z):
        ''' Align the x local axis of the selected shell element to the given vector
        
        Args:
            num: Number of the element
            x: x component of 1st local axis
            y: y component of 1st local axis
            z: z component of 1st local axis

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/element/shellxaxis/'+qt(num)+'/'+str(x)+'/'+str(y)+'/'+str(z)+'', None, None))
    def AnalyzeFireElement(self, elem, endTime, beamExposure=2, columnExposure=3, checkCombo='', selectForcesCrit=2, fireCurve=0, outOfProc=False, noWindow=False, customFireCurve=0):
        ''' Write and run a new model for non-linear thermal analysis of an element section.
        
        Args:
            elem: ID of the element
            endTime: Final time in minutes (e.g. 90)
            beamExposure (optional): Beam edges exposed to fire: 0 bottom, 1 lateral edges, 2 lateral edges+bottom, 3 all edges, 4 bottom+left, 5 bottom+right
            columnExposure (optional): Column edges exposed to fire: 0 single edge, 1 two edges, 2 three edges, 3 all edges
            checkCombo (optional): Optional. Input a loadcase name to check section against its forces
            selectForcesCrit (optional): Criterion for selecting forces in section: 0 max My, - 1 max Mz - 2 max for both My and Mz
            fireCurve (optional): Optional. Fire curve: 0 ISO 834, 1 external, 2 hydrocarbon
            outOfProc (optional): If true, run the model out of process
            noWindow (optional): If true, hide the solver window or its output lines from console. Applicable only if out of process is active
            customFireCurve (optional): Optional, ID of the custom fire curve to be used

        Returns:
            The path of the newly created model or, if checking is required, an array containing "Element-Station", "N", "Vy", "Vz", "Myy", "Mzz", "Ratio-NMM", "Ratio-V", path
        '''
        return json.loads(self.nfrest('GET', '/res/check/analyzefire/'+qt(elem)+'/'+str(endTime)+'/'+str(beamExposure)+'/'+str(columnExposure)+'/'+qt(checkCombo)+'/'+str(selectForcesCrit)+'/'+str(fireCurve)+'/'+str(outOfProc)+'/'+str(noWindow)+'/'+str(customFireCurve)+'', None, None))
    def appendDocXformula(self, formula, alignment=0):
        ''' Append and render a formula in Ascii syntax to an already opened DocX document. By default, this is aligned to center.
        
        Args:
            formula: Ascii formula text
            alignment (optional): Optional, default is 1. 0=left, 1=center, 2=right, 3=justified

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('POST', '/op/docx/appendformula/'+str(alignment)+'', formula, None))
    def appendDocXimage(self, imagePath, ratio=1, alignment=0):
        ''' Append image to an already opened DocX document. By default, this is aligned to center.
        
        Args:
            imagePath: Path of the picture
            ratio (optional): Size ratio of the picture
            alignment (optional): Optional, default is 1. 0=left, 1=center, 2=right, 3=justified

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/docx/appendimage/'+str(ratio)+'/'+str(alignment)+'', None, dict([("path",imagePath)])))
    def appendDocXtext(self, text:list, alignment=0, color=0, bold=False, italic=False, underline=False):
        ''' Append text to an already opened DocX document
        
        Args:
            text: 
            alignment (optional): Optional, default is 0. 0=left, 1=center, 2=right, 3=justified
            color (optional): Optional, default is 0. RGB integer value for color
            bold (optional): Optional, default is false. True for bold
            italic (optional): Optional, default is false. True for italic
            underline (optional): Optional, default is false. True for underlined text

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/op/docx/appendtext/'+str(alignment)+'/'+str(color)+'/'+str(bold)+'/'+str(italic)+'/'+str(underline)+'', text, None))
    def applyButterworthFilter(self, values:list, samplingF, cutF, order, lowPass):
        ''' Apply Butterworth filter to the 2-columns input data
        
        Args:
            values: 2-columns input data (eg. time vs. displacements)
            samplingF: Sampling frequency
            cutF: Cut-off frequency
            order: Order of the filter, an even number greater or equal to 2
            lowPass: True if low-pass, false if high-pass

        Returns:
            Array of double
        '''
        return json.loads(self.nfrest('POST', '/op/bwfilter/'+str(samplingF)+'/'+str(cutF)+'/'+str(order)+'/'+str(lowPass)+'', values, None))
    def applyEC8lateralForces(self, thID, loadCaseX, loadCaseY, propMasses=False, T1=0, ct=0.05, lam=1):
        ''' Apply lateral forces to the master nodes of the model. Rigid diaphragms and masses are required.
        
        Args:
            thID: ID of the spectrum function to be used as reference for total base shear
            loadCaseX: Loadcase name in X dir. in which lateral forces are stored.
            loadCaseY: Loadcase name in Y dir. in which lateral forces are stored.
            propMasses (optional): Flag (true or false). If true lateral forces follow height distribution, if false lateral forces are proportional to floor masses.
            T1 (optional): Fundamental period of the structure. If not estimated (0), specify ct and lam
            ct (optional): Optional, default 0.05. Coefficient for estimation of fundamental period from EC8 4.6: T1=ct*H^(3/4)
            lam (optional): Optional, default 1. Coefficient for estimation of base shear as per EC8 4.5: Fb=Sd(T1)*m*lam

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/lateralforces/'+str(thID)+'/'+qt(loadCaseX)+'/'+qt(loadCaseY)+'/'+str(propMasses)+'/'+str(T1)+'/'+str(ct)+'/'+str(lam)+'', None, None))
    def areRebarsInsideSection(self, ID):
        ''' Check if all rebars are inside the section. Only the first fill figure is considered.
        
        Args:
            ID: ID of the section

        Returns:
            Array of integers of the size of the rebars, with: 0 if rebar is outside figure, 1 if it's on a polygon vertex, 2 on border, 3 internal
        '''
        return json.loads(self.nfrest('GET', '/section/rebar/inside/'+qt(ID)+'', None, None))
    def assignHinge(self, beamID, hingeName):
        ''' Assign a plastic hinge to a beam
        
        Args:
            beamID: ID of the beam element hosting the hinge
            hingeName: Name of the hinge property to assign

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/hinge/assign/'+qt(beamID)+'/'+qt(hingeName)+'', None, None))
    def assignMaterialToElement(self, element, materialID):
        ''' Assign a selected material to the desired element
        
        Args:
            element: ID of the element
            materialID: ID of the material

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/material/assign/'+qt(element)+'/'+str(materialID)+'', None, None))
    def assignSectionToElement(self, element, sectionID):
        ''' Assign a selected section to the desired element
        
        Args:
            element: ID of the element
            sectionID: ID of the section

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/section/assign/'+qt(element)+'/'+str(sectionID)+'', None, None))
    def assignSubsoilProperty(self, element, prop):
        ''' Assign a subsoil property to the selected element
        
        Args:
            element: ID of the element
            prop: Name of the property to assign

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/springproperty/subsoil/assign/'+qt(element)+'/'+qt(prop)+'', None, None))
    def assignToGroup(self, name, nodes:list, elements:list, clear=False):
        ''' Assign nodes and/or elements to a previously defined group
        
        Args:
            name: Name of the group
            nodes: Array of nodes
            elements: Array of elements
            clear (optional): Optional. Clear assigned nodes and elements

        Returns:
            False if not existing, True otherwise
        '''
        return sbool(self.nfrest('GET', '/group/assign/'+qt(name)+'/'+str(clear)+'', None, dict([("nodes",json.dumps(nodes)),("elements",json.dumps(elements))])))
    def changeDefSolverType(self, type):
        ''' Change the system of equation type in standard solver
        
        Args:
            type: 0 for default (slow, lability detection), 1 for DSS (fast, less memory consumption), 2 for SPOOLES (fast)

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/opt/changedefsolvertype/'+str(type)+'', None, None))
    def changeElementProperty(self, ID, prop, value):
        ''' Change element property
        
        Args:
            ID: ID of the element
            prop: Name of the property to change
            value: New value of property

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('POST', '/element/prop/'+qt(ID)+'/'+qt(prop)+'/'+qt(value)+'', None, None))
    def changeLoadValue(self, i, loadValue):
        ''' Change the load value of i-th load entity
        
        Args:
            i: Number of the load, get via getLoadsForNode or getLoadsForElement
            loadValue: New loading value

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/change/'+str(i)+'/'+str(loadValue)+'', None, None))
    def changeOrAddSectionPoint(self, sectionID, seriesID, ptID, x, y):
        ''' Change or add a point in an already defined section
        
        Args:
            sectionID: ID of the section
            seriesID: ID of the series, starts at 1
            ptID: Point index in the series, starts at 1. Use 0 to add a point at the beginning of the series
            x: New z coordinate
            y: New y coordinate

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/add/changeaddpt/'+str(sectionID)+'/'+str(seriesID)+'/'+str(ptID)+'/'+str(x)+'/'+str(y)+'', None, None))
    def changeSolver(self, type, path=''):
        ''' Change the default solver
        
        Args:
            type: 0 for default solver, 1 for OpenSees, 2 for CalculiX
            path (optional): Optional. Full path to the solver assembly.

        Returns:
            True if successful, False if path is missing
        '''
        return sbool(self.nfrest('GET', '/op/opt/changesolver/'+str(type)+'', None, dict([("path",path)])))
    def changeSpringNLProperty(self, name, NLdofs:list, NLprops:list):
        ''' Change a non-linear spring property already defined in the model
        
        Args:
            name: Name of the property, must be unique
            NLdofs: Array of integers from 0 to 15 to associate a non-linear behaviour to each DoF. Use -1 to leave the DoF inactive
            NLprops: Array containing 6 arrays of numerical properties for the each selected non-linear behaviour

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/springproperty/nl/change/'+qt(name)+'/'+json.dumps(NLdofs)+'', NLprops, None))
    def changeSpringNLPropertyDof(self, name, DoF, NLtype, NLprops:list):
        ''' Change a non-linear spring property already defined in the model
        
        Args:
            name: Name of the property, must be unique
            DoF: Dof of the property from 1 to 6
            NLtype: Integer value from 0 to 15 to associate a non-linear behaviour to each DoF. Use -1 to leave the DoF inactive
            NLprops: Array of numerical properties for the selected non-linear behaviour

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/springproperty/nl/change/'+qt(name)+'/'+str(DoF)+'/'+str(NLtype)+'', NLprops, None))
    def changeSpringProperty(self, name, Kx, Ky, Kz, Krx, Kry, Krz):
        ''' Change a spring property in the model
        
        Args:
            name: Name of the property, must be unique
            Kx: Stiffness in X direction
            Ky: Stiffness in Y direction
            Kz: Stiffness in Z direction
            Krx: Stiffness in RX direction
            Kry: Stiffness in RY direction
            Krz: Stiffness in RZ direction

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/springproperty/simple/change/'+qt(name)+'/'+str(Kx)+'/'+str(Ky)+'/'+str(Kz)+'/'+str(Krx)+'/'+str(Kry)+'/'+str(Krz)+'', None, None))
    def checkConnectivity(self, notPassedElems=None, overlappedNodes=None):
        ''' Check overlapped beam nodes and anti-clockwise connectivity for all the other elements. The function always tries to correct incorrect elements, hence subsequent checks could be negative.
        
        Args:
            notPassedElems (optional): Optional. Empty array eventually filled with elements IDs that don't passed the check. Not available in REST API
            overlappedNodes (optional): Optional. Empty array eventually filled with detected overlapped nodes in Line elements. Not available in REST API

        Returns:
            True if check has been successful for all elements
        '''
        return sbool(self.nfrest('GET', '/op/mesh/connectivity'+str(notPassedElems)+'/'+str(overlappedNodes)+'', None, None))
    def checkElement(self, elem, lc, t, stationType, verName, savelog=False, messages=False, defaultParams:list=None, logPath=None):
        ''' Check a single element in a model against results.
        
        Args:
            elem: ID of the element to be checked
            lc: Loadcase containing results
            t: Reference time for results. For linear analyses, use "1".
            stationType: 0 for 5 stations, 1 for 3 stations, 2 for I and J, 3 for I only, 4 for J only, 5 for M only, 6 for 1/4, 7 for 3/4, 8 for M and 1/4 and 3/4, 9 for 1/4 and 3/4
            verName: Name of the checking to be used. E.g. "Steel EC3" or "EC2_Concrete". NVV files have underscore.
            savelog (optional): Optionally, log file is written
            messages (optional): Optionally, messages from checking engine are shown
            defaultParams (optional): Optionally, parameters for checking
            logPath (optional): Optionally, returns path of the checking log file

        Returns:
            True if checking is satisfied, False in any other case
        '''
        return sbool(self.nfrest('GET', '/res/check/element/'+qt(elem)+'/'+qt(lc)+'/'+qt(t)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("logPath",logPath)])))
    def checkElementRatio(self, elem, lc, t, stationType, verName, savelog=False, messages=False, defaultParams:list=None, logPath=None):
        ''' Check a single element in a model against results.
        
        Args:
            elem: ID of the element to be checked
            lc: Loadcase containing results
            t: Reference time for results. For linear analyses, use "1".
            stationType: 0 for 5 stations, 1 for 3 stations, 2 for I and J, 3 for I only, 4 for J only, 5 for M only, 6 for 1/4, 7 for 3/4, 8 for M and 1/4 and 3/4, 9 for 1/4 and 3/4
            verName: Name of the checking to be used. E.g. "Steel EC3" or "EC2_Concrete". NVV files have underscore.
            savelog (optional): Optionally, log file is written
            messages (optional): Optionally, messages from checking engine are shown
            defaultParams (optional): Optionally, parameters for checking
            logPath (optional): Optionally, returns path of the checking log file

        Returns:
            A value less than 1 if the element satisfies checking. 100 is returned in case of error
        '''
        return float(self.nfrest('GET', '/res/check/elementRatio/'+qt(elem)+'/'+qt(lc)+'/'+qt(t)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("logPath",logPath)])))
    def checkElements(self, elems:list, lc, ts, stationType, verName, savelog=False, messages=False, defaultParams:list=None):
        ''' Check the specified elements in a model against results.
        
        Args:
            elems: IDs of the elements to be checked
            lc: Loadcase containing results
            ts: Reference time for results. For linear analyses, use "1".
            stationType: 0 for 5 stations, 1 for 3 stations, 2 for I and J, 3 for I only, 4 for J only, 5 for M only, 6 for 1/4, 7 for 3/4, 8 for M and 1/4 and 3/4, 9 for 1/4 and 3/4
            verName: Name of the checking to be used. E.g. "Steel EC3" or "EC2_Concrete". NVV files have underscore.
            savelog (optional): Optionally, log file is written
            messages (optional): Optionally, messages from checking engine are shown
            defaultParams (optional): Optionally, parameters for checking

        Returns:
            True if all elements satisfy checking
        '''
        return sbool(self.nfrest('GET', '/res/check/elements/'+qt(lc)+'/'+qt(ts)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("elems",json.dumps(elems))])))
    def checkElementsRatio(self, elems:list, lc, ts, stationType, verName, savelog=False, messages=False, defaultParams:list=None):
        ''' Check the specified elements in a model against results.
        
        Args:
            elems: IDs of the elements to be checked
            lc: Loadcase containing results
            ts: Reference time for results. For linear analyses, use "1".
            stationType: 0 for 5 stations, 1 for 3 stations, 2 for I and J, 3 for I only, 4 for J only, 5 for M only, 6 for 1/4, 7 for 3/4, 8 for M and 1/4 and 3/4, 9 for 1/4 and 3/4
            verName: Name of the checking to be used. E.g. "Steel EC3" or "EC2_Concrete". NVV files have underscore.
            savelog (optional): Optionally, log file is written
            messages (optional): Optionally, messages from checking engine are shown
            defaultParams (optional): Optionally, parameters for checking

        Returns:
            A value less than 1 if all elements satisfy checking. 100 is returned in case of error
        '''
        return float(self.nfrest('GET', '/res/check/elementsRatio/'+qt(lc)+'/'+qt(ts)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("elems",json.dumps(elems))])))
    def checkElementStation(self, elem, lc, t, stationAbsissa, verName, defaultParams:list=None, logPath=None, messages=False):
        ''' Check a single station in a model against results.
        
        Args:
            elem: ID of the element to be checked
            lc: Loadcase containing results
            t: Reference time for results. For linear analyses, use "1".
            stationAbsissa: Absissa of the section to check for the element
            verName: Name of the checking to be used. E.g. "Steel EC3" or "EC2_Concrete". NVV files have underscore.
            defaultParams (optional): Optionally, parameters for checking
            logPath (optional): Path for logging. If empty (default), actual path is returned. If "no", no log is written
            messages (optional): Optional, default is false. If true, activates message dialogs from the checking engine

        Returns:
            A dictionary of string and decimal containing all the values used for checking and results
        '''
        return json.loads(self.nfrest('GET', '/res/check/station/'+qt(elem)+'/'+qt(lc)+'/'+qt(t)+'/'+str(stationAbsissa)+'/'+qt(verName)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("logPath",logPath)])))
    def checkFreeNodes(self):
        ''' Check free nodes in the model
        
        
        Returns:
            An array of the detected free nodes.
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/findfreenodes', None, None))
    def checkLineElements(self):
        ''' Check line elements and mesh if necessary.
        
        
        Returns:
            The number of meshed line elements
        '''
        return int(self.nfrest('GET', '/op/mesh/lineelems', None, None))
    def checkModel(self, lc, ts, stationType, verName, savelog=False, messages=False, defaultParams:list=None):
        ''' Check the entire model model with results.
        
        Args:
            lc: Loadcase containing results
            ts: Reference time for results. For linear analyses, use "1".
            stationType: 0 for 5 stations, 1 for 3 stations, 2 for I and J, 3 for I only, 4 for J only, 5 for M only, 6 for 1/4, 7 for 3/4, 8 for M and 1/4 and 3/4, 9 for 1/4 and 3/4
            verName: Name of the checking to be used. E.g. "Steel EC3" or "EC2_Concrete". NVV files have underscore, no file extension.
            savelog (optional): Optionally, log file is written
            messages (optional): Optionally, messages from checking engine are shown
            defaultParams (optional): Optionally, parameters for checking

        Returns:
            True if checking is satisfied, False in any other case
        '''
        return sbool(self.nfrest('GET', '/res/check/model/'+qt(lc)+'/'+qt(ts)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams))])))
    def checkNode(self, node, lc, ts, verName, savelog=False, messages=False, defaultParams:list=None, logPath=None):
        ''' Check a single node in a model against results.
        
        Args:
            node: ID of the node to be checked
            lc: Loadcase containing results
            ts: Reference time for results. For linear analyses, use "1".
            verName: Name of the checking to be used. E.g. "Steel EC3" or "EC2_Concrete". NVV files have underscore.
            savelog (optional): Optionally, log file is written
            messages (optional): Optionally, messages from checking engine are shown
            defaultParams (optional): Optionally, parameters for checking
            logPath (optional): Optionally, returns path of the checking log file

        Returns:
            True if node satisfies checking, False otherwise
        '''
        return sbool(self.nfrest('GET', '/res/check/node/'+qt(node)+'/'+qt(lc)+'/'+qt(ts)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("logPath",logPath)])))
    def checkNodes(self, nodes:list, lc, ts, stationType, verName, savelog=False, messages=False, defaultParams:list=None):
        ''' Check specified nodes in a model against results.
        
        Args:
            nodes: ID of the nodes to be checked
            lc: Loadcase containing results
            ts: Reference time for results. For linear analyses, use "1".
            stationType: Name of the checking to be used. E.g. "Steel EC3" or "EC2_Concrete". NVV files have underscore.
            verName: Optionally, log file is written
            savelog (optional): Optionally, messages from checking engine are shown
            messages (optional): Optional. Parameters for checking
            defaultParams (optional)

        Returns:
            True if nodes satisfy checking, False otherwise
        '''
        return sbool(self.nfrest('GET', '/res/check/nodes/'+qt(lc)+'/'+qt(ts)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("nodes",json.dumps(nodes))])))
    def checkOverlappedElements(self):
        ''' Check overlapped elements in the model
        
        
        Returns:
            A list of overlapped elements
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/findoverlappedelements', None, None))
    def clearElementCustomProperties(self, elem):
        ''' Clear element custom properties
        
        Args:
            elem: 

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/element/customprop/'+qt(elem)+'', None, None))
    def clearElementRebar(self, elem):
        ''' Clear all element rebar
        
        Args:
            elem: ID of the element or Wall group name

        Returns:
            True is successful
        '''
        return sbool(self.nfrest('GET', '/element/rebar/clear/'+qt(elem)+'', None, None))
    def clearSectionRebar(self, ID):
        ''' Clear all section rebar
        
        Args:
            ID: ID of the section

        Returns:
            True is successful
        '''
        return sbool(self.nfrest('GET', '/section/rebar/clear/'+qt(ID)+'', None, None))
    def clearSectionRebar(self, ID):
        ''' Clear all section rebar
        
        Args:
            ID: ID of the section

        Returns:
            True is successful
        '''
        return sbool(self.nfrest('GET', '/section/rebar/clear/'+str(ID)+'', None, None))
    def clearSelection(self):
        ''' Clear selected items. REST version only against local instance of NextFEM Designer
        
        
        Returns:
            
        '''
        return sbool(self.nfrest('GET', '/op/clearselection', None, None))
    def clearStoredDomains(self):
        ''' Clear stored resisting domains
        
        
        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/res/check/cleardomains', None, None))
    def colorizeModel(self, criterion, excl:list=None):
        ''' Colorize with random colors all the elements
        
        Args:
            criterion: 1 by section, 2 by material, 3 by group
            excl (optional): Array of integer color to be avoided (e.g. selection colors). Optional - if null, selection colors are used

        Returns:
            
        '''
        return self.nfrest('GET', '/model/colors/colorize/'+str(criterion)+'', None, dict([("excl",json.dumps(excl))]))
    def compileDocX(self, dict:list, tableDict:list=None, twoPasses=False):
        ''' Compile the open document for keyword substitution
        
        Args:
            dict: Dictionary of the keywords to be replaced by its values
            tableDict (optional): Dictionary of keywords to be replaced by a table, described by a list of string() - each item of the list represents the single row as an array of string
            twoPasses (optional): Enable double pass for the document

        Returns:
            True
        '''
        return sbool(self.nfrest('GET', '/op/docx/compile/'+str(twoPasses)+'', tableDict, dict([("dict",json.dumps(dict))])))
    def convertToMeshedSection(self, sectionID):
        ''' Convert an existing section to a new tria-meshed section. Remember to re-assign the new section to elements with assignSectionToElement
        
        Args:
            sectionID: ID of the original section

        Returns:
            The ID of the new meshed section, 0 if errors occur
        '''
        return int(self.nfrest('GET', '/op/mesh/meshedsection/'+str(sectionID)+'', None, None))
    def convertUnits(self, length, force):
        ''' Convert model and results to the specified new units.
        
        Args:
            length: Units for length (e.g. "m", "in", ...)
            force: Units for force (e.g. "N", "kipf", ...)

        Returns:
            
        '''
        return self.nfrest('GET', '/units/convertunits/'+qt(length)+'/'+qt(force)+'', None, None)
    def convertValue(self, value, OldUnits, NewUnits):
        ''' Convert units of a value.
        
        Args:
            value: Numerical value to convert
            OldUnits: Old units of the input value. Eg. kN/cm^2
            NewUnits: Target units for the input value. Eg. N/mm^2

        Returns:
            Converted value
        '''
        return float(self.nfrest('GET', '/units/convert/'+str(value)+'', None, dict([("OldUnits",OldUnits),("NewUnits",NewUnits)])))
    def createDocX(self, path, text:list, template=''):
        ''' Create a DocX file with the desired text
        
        Args:
            path: Path of the DocX document
            text: Text to be written in the document
            template (optional): Optional. Path of a DocX template to be used in document generation

        Returns:
            Always true
        '''
        return sbool(self.nfrest('GET', '/op/docx/create'+json.dumps(text)+'', None, dict([("path",path),("template",template)])))
    def customCheck(self, formulae:list):
        ''' Run checking on user formulae. No node or element quantities are given. See also getItemDataResults method.
        
        Args:
            formulae: Dictionary of string and decimal containing formulae (see NextFEM Scripting language reference)

        Returns:
            A dictionary of string and decimal containing all the checking results
        '''
        return json.loads(self.nfrest('POST', '/res/check/item', formulae, None))
    def CustomLicense(self, lic):
        ''' Check if a license key is available
        
        Args:
            lic

        Returns:
            True or False
        '''
        return sbool(self.nfrest('GET', '/op/lic', None, dict([("val",lic)])))
    def defaultColors(self):
        ''' Revert to default colors
        
        
        Returns:
            
        '''
        return self.nfrest('GET', '/model/colors/default', None, None)
    def deleteChecks(self):
        ''' Delete the stored checks.
        
        
        Returns:
            True if operations goes fine.
        '''
        return sbool(self.nfrest('GET', '/res/delchecks', None, None))
    def deleteDocXheadings(self, headingsIDtoDelete:list):
        ''' Remove the paragraphs contained in the specified titles
        
        Args:
            headingsIDtoDelete: Array of paragraph IDs to be deleted

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/docx/delheadings', headingsIDtoDelete, None))
    def deleteGroup(self, name):
        ''' Remove the specified group from model
        
        Args:
            name: Name of the group to be removed

        Returns:
            False if not existing, True otherwise
        '''
        return sbool(self.nfrest('GET', '/group/delete/'+qt(name)+'', None, None))
    def deleteResults(self):
        ''' Delete the stored results.
        
        
        Returns:
            True if operations goes fine.
        '''
        return sbool(self.nfrest('GET', '/res/delete', None, None))
    def divideHexa(self, hexaID, divX, divY, divZ):
        ''' Divide an existing Hexa element
        
        Args:
            hexaID: ID of the existing Hexa
            divX: Number of divisions in X direction
            divY: Number of divisions in Y direction
            divZ: Number of divisions in Z direction

        Returns:
            An array containing the IDs of newly created Hexa elements
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/dividehexa/'+qt(hexaID)+'/'+str(divX)+'/'+str(divY)+'/'+str(divZ)+'', None, None))
    def divideLine(self, lines:list, fractions:list):
        ''' Divide existing Line elements
        
        Args:
            lines: Array of Line elements to be divided
            fractions: Division pattern, normalized to 1

        Returns:
            An array containing the IDs of newly created Line elements
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/divideline', None, dict([("lines",json.dumps(lines)),("fractions",json.dumps(fractions))])))
    def divideLineByNodes(self, line, nodes:list):
        ''' Divide existing Line elements by nodes
        
        Args:
            line: Line element ID
            nodes: Array of nodes ID

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/mesh/dividelinebynodes/'+qt(line)+'', None, dict([("nodes",json.dumps(nodes))])))
    def divideQuad(self, quadID, divX, divY):
        ''' Divide an existing Quad element
        
        Args:
            quadID: ID of the existing Quad
            divX: Number of divisions in X direction
            divY: Number of divisions in Y direction

        Returns:
            An array containing the IDs of newly created Quad elements
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/dividequad/'+qt(quadID)+'/'+str(divX)+'/'+str(divY)+'', None, None))
    def divideWedge(self, wedgeID, div):
        ''' Divide an existing Wedge element along its extrusion direction
        
        Args:
            wedgeID: ID of the existing Wedge
            div: Number of divisions

        Returns:
            An array containing the IDs of newly created Wedge elements
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/dividewedge/'+qt(wedgeID)+'/'+str(div)+'', None, None))
    def duplicateSection(self, originalID):
        ''' Duplicate the selected section
        
        Args:
            originalID: Original ID of the section to be copied

        Returns:
            The ID of the newly created copy of the section
        '''
        return int(self.nfrest('GET', '/section/duplicate/'+str(originalID)+'', None, None))
    def exportGLTF(self, path, saveIFC=False):
        ''' Export the model to glTF format for web sharing.
        
        Args:
            path: Path of the file to be saved
            saveIFC (optional): Optional parameter to save IFC to the same folder. Default is false

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/export/gltf/'+str(saveIFC)+'', None, dict([("path",path)])))
    def exportIFC(self, path, saveAsXML=False):
        ''' Export IFC file
        
        Args:
            path: Path of the file to be saved
            saveAsXML (optional): False is default. True to save in XML format.

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/export/ifc/'+str(saveAsXML)+'', None, dict([("path",path)])))
    def exportIOM(self, filename):
        ''' Export model to IDEA StatiCa Open Model format. It generates filename.xml and filename.xmlR for results, if any.
        
        Args:
            filename: Full path for the output model in XML format.

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/export/idea', None, dict([("path",filename)])))
    def exportMidas(self, path):
        ''' Export model in MGT format for Midas GEN
        
        Args:
            path: Full path of saved file

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/export/midas', None, dict([("path",path)])))
    def exportOpenSees(self, path, loadcase):
        ''' Export model in OpenSees TCL format for a chosen loadcase
        
        Args:
            path: Full path of TCL file
            loadcase: Load case to be exported

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/export/opensees/'+qt(loadcase)+'', None, dict([("path",path)])))
    def exportRCbeamsDXF(self, path, elements:list):
        ''' Export the selected RC beam to DXF format. Rebars and hoops will be inserted in DXF, if present
        
        Args:
            path: Path of the resulting DXF file
            elements: Array of elements to include in DXF

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/element/exportdxf', None, dict([("path",path),("elements",json.dumps(elements))])))
    def exportRCmemberDXF(self, path, member):
        ''' Export the selected RC member to DXF format. Rebars and hoops will be inserted in DXF, if present
        
        Args:
            path: Path of the resulting DXF file
            member: Member name

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/model/member/exportdxf/'+qt(member)+'', None, dict([("path",path)])))
    def exportSAF(self, path):
        ''' Export structural model in SAF file
        
        Args:
            path: Full path of SAF .xlsx file

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/export/saf', None, dict([("path",path)])))
    def exportSAP2000(self, path):
        ''' Export model in S2K format for SAP2000
        
        Args:
            path: Full path of saved file

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/export/sap2000', None, dict([("path",path)])))
    def exportSectionDXF(self, path, sID):
        ''' Export the selected section to DXF format. Rebars and hoops are included, if present
        
        Args:
            path: Path of the resulting DXF file
            sID: ID of the section

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/section/exportdxf/'+str(sID)+'', None, dict([("path",path)])))
    def exportWexBIM(self, path, saveIFC=False, copyViewer=True):
        ''' Export the model to WexBIM format for web sharing.
        
        Args:
            path: Path of the file to be saved
            saveIFC (optional): Optional parameter to save IFC to the same folder. Default is false
            copyViewer (optional): Optional parameter to copy viewer engine files to the same folder. Default is true

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/export/wexbim/'+str(saveIFC)+'/'+str(copyViewer)+'', None, dict([("path",path)])))
    def exportXMLresults(self, filename):
        ''' Export results in XML format
        
        Args:
            filename: Path of the file to save

        Returns:
            
        '''
        return sbool(self.nfrest('GET', '/op/export/xmlres', None, dict([("path",filename)])))
    def functionFromFile(self, filename, type=9, units=''):
        ''' Load a function from text file.
        
        Args:
            filename: Path of the text file containing function to load
            type (optional): 0 displacement TH, 1 velocity TH, 2 acceleration TH, 3 acceleration spectrum, 4 displacement spectrum
            units (optional): Units of measure for data in ordinate (Y)

        Returns:
            The ID of the time series, -1 in case of errors
        '''
        return int(self.nfrest('GET', '/function/fromfile/'+str(type)+'', None, dict([("units",units),("path",filename)])))
    def generateFrame(self, baysX, baysY, sn, ddx, ddy, ddz, sx, sy, sz, matx, maty, matz, lc1='', lc2='', lc3='', Lval1=0, Lval2=0, Lval3=0, loadBeamX=False, rigidfloor=False):
        ''' Generate a spatial frame of desired characteristics
        
        Args:
            baysX: Bays in X direction
            baysY: Bays in Y direction
            sn: Number of storey
            ddx: Bay width along X dir.
            ddy: Bay width along Y dir.
            ddz: Storey height
            sx: Section ID for beams in X
            sy: Section ID for beams in Y
            sz: Section ID for columns
            matx: Material ID for beams in X
            maty: Material ID for beams in Y
            matz: Material ID for columns
            lc1 (optional): Loadcase in which storing loads
            lc2 (optional): Loadcase in which storing loads
            lc3 (optional): Loadcase in which storing loads
            Lval1 (optional): Load value for loadcase 1
            Lval2 (optional): Load value for loadcase 2
            Lval3 (optional): Load value for loadcase 3
            loadBeamX (optional): True for loading beams in X, false for loading beams in Y dir.
            rigidfloor (optional): True to force rigid floor contraints

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/mesh/generateframe/'+str(baysX)+'/'+str(baysY)+'/'+str(sn)+'/'+str(ddx)+'/'+str(ddy)+'/'+str(ddz)+'/'+str(sx)+'/'+str(sy)+'/'+str(sz)+'/'+str(matx)+'/'+str(maty)+'/'+str(matz)+'/'+qt(lc1)+'/'+qt(lc2)+'/'+qt(lc3)+'/'+str(Lval1)+'/'+str(Lval2)+'/'+str(Lval3)+'/'+str(loadBeamX)+'/'+str(rigidfloor)+'', None, None))
    def generateLoadCombinations(self, type, comboPrefix=''):
        ''' Generate load combinations as per EC1. General Design license is needed to run.
        
        Args:
            type: Combinations set type: Fundamental 0, Characteristic 1, Frequent 2, Quasi_permanent 3, Serviceability 4, Seismic 5, All 6
            comboPrefix (optional): Optional prefix for generated combinations

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/generate/'+str(type)+'/'+qt(comboPrefix)+'', None, None))
    def getAlignedNodes(self, n1, n2, tol=0):
        ''' Return nodes aligned with the given two as input
        
        Args:
            n1: 1st node as vert3 structure
            n2: 2nd node as vert3 structure
            tol (optional): Optional. Tolerance needed to check alignement. Consider to lower it if n1 and n2 are close.

        Returns:
            A list of nodal IDs
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/alignednodes/'+str(tol)+'', None, dict([("n1",n1),("n2",n2)])))
    def getAreaByNodes(self, nodes:list):
        ''' Get area from the selected nodes
        
        Args:
            nodes: Array of nodes ID

        Returns:
            Area inside the polygon described by nodes
        '''
        return float(self.nfrest('POST', '/node/area', nodes, None))
    def getBC(self, node):
        ''' Get restraints of a single node
        
        Args:
            node: ID of the node

        Returns:
            Boolean array containing True if DOF is restrained
        '''
        return json.loads(self.nfrest('GET', '/bc/get/'+qt(node)+'', None, None))
    def getBeamDeflection(self, num, loadcase, time, type, station):
        ''' Get beam deflection for the selected element, loadcase, time and station
        
        Args:
            num: element no.
            loadcase: 
            time: For linear analysis, set as 1
            type: 1=local x, 2=local y, 3=local z, 4=local rx, 5=local ry, 6=local rz
            station: Usually a beam has 5 stations (1, 2, 3, 4 or 5)

        Returns:
            The requested value. 0 if something went wrong.
        '''
        return float(self.nfrest('GET', '/res/beamdeflection/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(type)+'/'+str(station)+'', None, None))
    def getBeamDeflections(self, num, loadcase, type, offsetL=0, numStations=21, time='1'):
        ''' Get the beam deflections for the selected number of stations along beam
        
        Args:
            num: Element no.
            loadcase: Loadcase name
            type: 1=N, 2=Vy, 3=Vz, 4=Mt, 5=My, 6=Mz
            offsetL (optional): Optional. Offset to queue output to another beam (length of the preceding beam).
            numStations (optional): Optional. Number of stations, default is 21.
            time (optional): Optional. Time for non-linear analysis. Default is 1.

        Returns:
            A check structure with positions and values
        '''
        return self.nfrest('GET', '/res/beamdeflections/'+qt(num)+'/'+qt(loadcase)+'/'+str(type)+'/'+str(offsetL)+'/'+str(numStations)+'/'+qt(time)+'', None, None)
    def getBeamForce(self, num, loadcase, time, type, station):
        ''' Get beam force for the selected element, loadcase, time and station
        
        Args:
            num: element no.
            loadcase: loadcase name
            time: For linear analysis, set as 1
            type: 1=N, 2=Vy, 3=Vz, 4=Mt, 5=My, 6=Mz
            station: Usually a beam has 5 stations (1, 2, 3, 4 or 5)

        Returns:
            The requested value. 0 if something went wrong.
        '''
        return float(self.nfrest('GET', '/res/beamforce/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(type)+'/'+str(station)+'', None, None))
    def getBeamForce2(self, num, loadcase, time, type, absissa):
        ''' Get beam force for the selected element, loadcase, time and absissa
        
        Args:
            num: element no.
            loadcase: loadcase name
            time: For linear analysis, set as 1
            type: 1=N, 2=Vy, 3=Vz, 4=Mt, 5=My, 6=Mz
            absissa: Usually a beam has 5 stations (1, 2, 3, 4 or 5)

        Returns:
            The requested value. 0 if something went wrong.
        '''
        return float(self.nfrest('GET', '/res/beamforce2/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(type)+'/'+str(absissa)+'', None, None))
    def getBeamForces(self, num, loadcase, station, time='1'):
        ''' Get all the beam forces for the selected element, loadcase, time and station
        
        Args:
            num: Element no.
            loadcase: Loadcase name
            station: Usually a beam has 5 stations (1, 2, 3, 4 or 5)
            time (optional): Optional. Default is 1 = linear analysis

        Returns:
            A vector of size 6. Null vector if something went wrong
        '''
        return json.loads(self.nfrest('GET', '/res/beamforces/'+qt(num)+'/'+qt(loadcase)+'/'+str(station)+'/'+qt(time)+'', None, None))
    def getBeamForcesAtNode(self, elem, node, loadcase, time='1'):
        ''' Get all the forces for the selected element at the specified node (beam end), loadcase, time and station
        
        Args:
            elem: Element no.
            node: Reference node no.
            loadcase: Loadcase name
            time (optional): Optional. Default is 1 = linear analysis

        Returns:
            A vector of size 6. Null vector if something went wrong
        '''
        return json.loads(self.nfrest('GET', '/res/beamforcesatnode/'+qt(elem)+'/'+qt(node)+'/'+qt(loadcase)+'/'+qt(time)+'', None, None))
    def getBeamForcesDiagram(self, num, loadcase, type, offsetL=0, numStations=21, time='1'):
        ''' Get the beam diagrams values for the selected number of stations along beam
        
        Args:
            num: Element no.
            loadcase: Loadcase name
            type: 1=N, 2=Vy, 3=Vz, 4=Mt, 5=My, 6=Mz
            offsetL (optional): Optional. Offset to queue output to another beam (length of the preceding beam).
            numStations (optional): Optional. Number of stations, default is 21.
            time (optional): Optional. Time for non-linear analysis. Default is 1.

        Returns:
            A check structure with positions and values
        '''
        return self.nfrest('GET', '/res/beamdiagram/'+qt(num)+'/'+qt(loadcase)+'/'+str(type)+'/'+str(offsetL)+'/'+str(numStations)+'/'+qt(time)+'', None, None)
    def getBeamForcesEnvelopeTable(self, num, stationsMode, loadcases:list=None):
        ''' Get beam forces consistent envelope, as a table. Envelopes are made on specified loadcases, or on all result cases. Suitable for many combinations or for time-history analyses.
        
        Args:
            num: Element no.
            stationsMode: 0 for 5 stations, 1 for 3 stations, 2 for I and J, 3 for I only, 4 for J only, 5 for M only, 6 for 1/4, 7 for 3/4, 8 for M and 1/4 and 3/4, 9 for 1/4 and 3/4
            loadcases (optional): Array of reference loadcases.

        Returns:
            A table as a list of string arrays.
        '''
        return json.loads(self.nfrest('GET', '/res/beamforcesenvtable/'+qt(num)+'/'+str(stationsMode)+'', loadcases, None))
    def getBeamResMoments(self, elemID):
        ''' Get the beam resisting moments for each direction of a beam
        
        Args:
            elemID: ID of the selected element

        Returns:
            An array containing a list of {abscissa,Mrzmax,Mrzmin,Mrymax,Mrymin}
        '''
        return json.loads(self.nfrest('GET', '/res/check/beammoments/'+qt(elemID)+'', None, None))
    def getBeamResShear(self, elemID, loadcase='', time='1'):
        ''' Get the beam resisting shear for each direction of a beam.   WARNING: This is possible only against results of a given loadcase for the element, otherwise a set of zero forces are given and results would not be accurate
        
        Args:
            elemID: ID of the selected element
            loadcase (optional): Optional. Loadcase for results
            time (optional): Optional. Time for results

        Returns:
            An array containing a list of {abscissa,Vry,-Vry,Vrz,-Vrz}
        '''
        return json.loads(self.nfrest('GET', '/res/check/beamshearres/'+qt(elemID)+'/'+qt(loadcase)+'/'+qt(time)+'', None, None))
    def getBuiltInChecking(self):
        ''' Get available checking scripts.
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/res/check/sets', None, None))
    def getCheckNameByMaterial(self, ID):
        ''' Get checking-set name from the built-in list
        
        Args:
            ID: ID of the material

        Returns:
            String
        '''
        return self.nfrest('GET', '/res/check/checkbymat/'+qt(ID)+'', None, None)
    def getCombinationCoeffPsi(self, subscript, type):
        ''' Get the current psi combination coefficient
        
        Args:
            subscript: 0 for psi0, 1 for psi1, 2 for psi2
            type: 1 for variable loading, 2 for wind loads, 3 for snow loading

        Returns:
            Double value
        '''
        return float(self.nfrest('GET', '/loadcase/getpsi/'+str(subscript)+'/'+str(type)+'', None, None))
    def getCombinationDesignType(self, name):
        ''' Returns an integer representing the combination type
        
        Args:
            name: Name of the combination

        Returns:
            -1 if not defined, 0 Ultimate Limit State, 1 Seismic combination, 2 Serviceability, 3 Serviceability-Characteristic, 4 Serviceability-Frequent, 5 Serviceability-QuasiPermanent
        '''
        return int(self.nfrest('GET', '/loadcase/combo/designtype/'+qt(name)+'', None, None))
    def getCombinationsByDesignType(self, type, servType=0):
        ''' Get an array of linear add combinations of the selected design type
        
        Args:
            type: The combination type for checking: 0 (default) unknown, 1 ultimate, 2 serviceability, 3 seismic
            servType (optional): The serviceability combination type for checking: 0 (default) unknown, 1 characteristic, 2 frequent, 3 quasi-permanent

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/loadcases/descombos/designtype/'+str(type)+'/'+str(servType)+'', None, None))
    def getConnectedElements(self, node, onlyOfType=-1):
        ''' Get all the elements connected to the specified node
        
        Args:
            node: Node ID
            onlyOfType (optional): Optional. Select only elements of type: unk = 0,line = 1,tria = 2,quad = 3,hexa = 4,wedge = 5,tetra = 6,user = 10,line3 = 20,quad8 = 21,hexa16 = 22,hexa20 = 23,tetra10 = 24,tria6 = 25,wedge15 = 26,spring2nodes = 40

        Returns:
            An array of element IDs
        '''
        return json.loads(self.nfrest('GET', '/node/connectedelements/'+qt(node)+'/'+str(onlyOfType)+'', None, None))
    def getControlNode(self):
        ''' Return the ID of the higher central node.
        
        
        Returns:
            ID of node. -1 if not found
        '''
        return self.nfrest('GET', '/op/controlnode', None, None)
    def getCornerNodes(self, nodes:list, lcs:list):
        ''' Return the corner nodes in a list of nodes
        
        Args:
            nodes: List of node IDs
            lcs: vert3 structure for defining first and second spatial directions

        Returns:
            A list of corner nodes, max 4
        '''
        return json.loads(self.nfrest('GET', '/op/corners', None, dict([("nodes",json.dumps(nodes)),("lcs",json.dumps(lcs))])))
    def getCustomData(self, key):
        ''' Get custom data stored in the model.
        
        Args:
            key: Key, must be unique

        Returns:
            False if the key was not found
        '''
        return self.nfrest('GET', '/model/customdata/'+qt(key)+'', None, None)
    def getDataPlot(self, xseries:list, yseries:list, transparent, name='', Xunits='', Yunits='', color=0, useDots=True):
        ''' Get plot of the given user data as array of bytes
        
        Args:
            xseries: X series of user data
            yseries: Y series of user data
            transparent: If true, set transparent background
            name (optional): Optional. Title of the plot
            Xunits (optional): Optional. Units for x axis
            Yunits (optional): Optional. Units for y axis
            color (optional): Optional. Default is 0 (black)
            useDots (optional): Optional. Default is false

        Returns:
            Array of bytes
        '''
        return json.loads(self.nfrest('GET', '/function/plotdata/'+str(transparent)+'/'+qt(name)+'/'+str(color)+'/'+str(useDots)+'', None, dict([("xseries",json.dumps(xseries)),("yseries",json.dumps(yseries)),("Xunits",Xunits),("Yunits",Yunits)])))
    def getDefinedDesignMaterials(self):
        ''' Return a list of used design material IDs
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/designmaterials', None, None))
    def getDefinedMaterials(self):
        ''' Return a list of used material IDs
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/materials', None, None))
    def getDefinedSections(self):
        ''' Return a list of used section IDs
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/sections', None, None))
    def getDesignMaterialProperty(self, ID, name, units=None):
        ''' Return selected property from a design material
        
        Args:
            ID: Material ID
            name: Name of the property: alphaT, behaviour, code, E, G, fk, ni, Mden, Wden, type
            units (optional): String supplied to function to eventually convert units of returned value

        Returns:
            The requested value as string. Empty in case of error
        '''
        return self.nfrest('GET', '/designmaterial/prop/'+qt(ID)+'/'+qt(name)+'', None, dict([("units",units)]))
    def getDesignMaterialsLibrary(self, filter='', type=0):
        ''' Return an array of string containing design material names from built-in library.
        
        Args:
            filter (optional): Optional. String supporting wildcards for material name
            type (optional): Optional. Integer for material type: Steel = 1, Aluminium = 2, Concrete = 3, Timber = 4, Masonry = 5, TensionFragile = 6

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/designmaterials/library/'+qt(filter)+'/'+str(type)+'', None, None))
    def getDesignMaterialsLibrary(self, filename, filter='', type=0):
        ''' Return an array of string containing design material names from built-in library.
        
        Args:
            filename: Name of the nfm library, without extension
            filter (optional): Optional. String supporting wildcards for material name
            type (optional): Optional. Integer for material type: Steel = 1, Aluminium = 2, Concrete = 3, Timber = 4, Masonry = 5, TensionFragile = 6

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/designmaterials/libraryf/'+qt(filename)+'/'+qt(filter)+'/'+str(type)+'', None, None))
    def getDocXheadings(self):
        ''' Get a list of headings contained in the current DocX document.
        
        
        Returns:
            List of array of strings as (ID, level, title)
        '''
        return json.loads(self.nfrest('GET', '/op/docx/headings', None, None))
    def getElementArea(self, ID):
        ''' Get element area of planar elements or surface for solids
        
        Args:
            ID: 

        Returns:
            
        '''
        return float(self.nfrest('GET', '/element/area/'+qt(ID)+'', None, None))
    def getElementCentroid(self, ID):
        ''' Return the coordinates of the centroid of the selected element
        
        Args:
            ID: ID of the element

        Returns:
            A double array
        '''
        return json.loads(self.nfrest('GET', '/element/centroid/'+qt(ID)+'', None, None))
    def getElementChecks(self, ID, lc, time):
        ''' Get the checks stored in the model for the specified element
        
        Args:
            ID: ID of the element
            lc: Name of the loadcase
            time: Time

        Returns:
            Null if no checking are available
        '''
        return self.nfrest('GET', '/res/check/elementA/'+qt(ID)+'/'+qt(lc)+'/'+qt(time)+'', None, None)
    def getElementConnectivity(self, ID):
        ''' Return the connectivity of the specified element.
        
        Args:
            ID: ID of the element

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/element/conn/'+qt(ID)+'', None, None))
    def getElementCustomProperty(self, elem, propName):
        ''' Get an already defined element custom property
        
        Args:
            elem: ID of the element
            propName: Property name

        Returns:
            Null string if not set
        '''
        return self.nfrest('GET', '/element/customprop/'+qt(elem)+'/'+qt(propName)+'', None, None)
    def getElementInfo(self, element):
        ''' Get text with element properties
        
        Args:
            element: 

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/element/info/'+qt(element)+'', None, None))
    def getElementOffset(self, elem):
        ''' Get the element offset for selected beam element
        
        Args:
            elem: ID of the beam element

        Returns:
            An array of size 2 with offset in z and offset in y local directions. Return null array even if the element is not found
        '''
        return json.loads(self.nfrest('GET', '/element/beamoffset/'+qt(elem)+'', None, None))
    def getElementProperty(self, ID, name):
        ''' Return selected property of element
        
        Args:
            ID: ID of the element
            name: Name of the property: num, angle, groupE, isJoint, isTruss, isPlaneStress, lun, mat, member, offsetI, offsetJ, sect, set2, sprProp, type

        Returns:
            The requested value as string. Empty in case of error
        '''
        return self.nfrest('GET', '/element/prop/'+qt(ID)+'/'+qt(name)+'', None, None)
    def getElementRebarSegments(self, elem):
        ''' Get rebar segments with their initial and final position, in percentage of element length
        
        Args:
            elem: ID of the element or group name

        Returns:
            An array of double with {Linital, Lfinal} for each segment. The number of segment is the lenght of the array divided by 2
        '''
        return json.loads(self.nfrest('GET', '/section/rebar/segments/'+qt(elem)+'', None, None))
    def getElementsChecks(self, lc, time):
        ''' Get the checks stored in the model for elements
        
        Args:
            lc: Name of the loadcase
            time: Time

        Returns:
            Null if no checking are available
        '''
        return json.loads(self.nfrest('GET', '/res/check/elementsA/'+qt(lc)+'/'+qt(time)+'', None, None))
    def getElementsChecksByMat(self, mat):
        ''' Get the checks stored in the model for the selected material type
        
        Args:
            mat: Material type: Steel = 1, Aluminium = 2, Concrete = 3, Timber = 4, Masonry = 5, TensionFragile = 6, Fire Resistant = 7

        Returns:
            Null if no checking are available
        '''
        return json.loads(self.nfrest('GET', '/res/check/elementsM/'+str(mat)+'', None, None))
    def getElementsFromGroup(self, name):
        ''' Get elements from group
        
        Args:
            name: Group name

        Returns:
            
        '''
        return json.loads(self.nfrest('GET', '/group/elements/'+qt(name)+'', None, None))
    def getElementType(self, ID):
        ''' Get element type: unk = 0,line = 1,tria = 2,quad = 3,hexa = 4,wedge = 5,tetra = 6,user = 10,line3 = 20,quad8 = 21,hexa16 = 22,hexa20 = 23,tetra10 = 24,tria6 = 25,wedge15 = 26,spring2nodes = 40
        
        Args:
            ID: ID of the element

        Returns:
            A string describing the element type
        '''
        return self.nfrest('GET', '/element/type/'+qt(ID)+'', None, None)
    def getElementVolume(self, ID):
        ''' Get element volume for solids
        
        Args:
            ID: 

        Returns:
            
        '''
        return float(self.nfrest('GET', '/element/volume/'+qt(ID)+'', None, None))
    def getEndRelease(self, beamID):
        ''' Give beam releases ratios. If 0, the dof is completely released.
        
        Args:
            beamID: ID of the beam

        Returns:
            Matrix of double of size [2,6], 6 for end I and 6 for end J. -1 means the DoF is not released
        '''
        return json.loads(self.nfrest('GET', '/element/beamendrelease/'+qt(beamID)+'', None, None))
    def getEnvelopeCombination(self, name):
        ''' Return a check object with loadcases and corresponding factors for desired envelope load combination.
        
        Args:
            name: Name of load combination

        Returns:
            A check object
        '''
        return self.nfrest('GET', '/loadcase/combo/getenv/'+qt(name)+'', None, None)
    def getExtrudedBeamPoints(self, elemID):
        ''' Get points from the extruded beam section in 3D space
        
        Args:
            elemID: ID of the beam element

        Returns:
            Array of vert3 instances
        '''
        return json.loads(self.nfrest('GET', '/element/extrudedbeam/'+qt(elemID)+'', None, None))
    def getFireSectionImage(self, elemID, titleX='', titleY='', title='', quoteUnits='', quoteFormat='0.00', showAxes=True, showOrigin=0, transparent=False):
        ''' Get section plot into an array of Bytes of Png image
        
        Args:
            elemID: ID of the element with the desired section
            titleX (optional): Optional title for X axis
            titleY (optional): Optional title for Y axis
            title (optional): Optional graph title
            quoteUnits (optional): Optional. Units of quotes, if set display quotes
            quoteFormat (optional): Optional. Numeric format of quotes
            showAxes (optional): Optional, default true
            showOrigin (optional): Optional, default 0. 1 to show Z and Y arrows, 2 for X and Y arrows
            transparent (optional): Optional, default false. If true, set transparent background

        Returns:
            Array of bytes
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/fireimage/'+str(elemID)+'/'+qt(titleX)+'/'+qt(titleY)+'/'+qt(title)+'/'+qt(quoteUnits)+'/'+qt(quoteFormat)+'/'+str(showAxes)+'/'+str(showOrigin)+'/'+str(transparent)+'', None, None))
    def getFirstMode(self, ct=0.05):
        ''' Get from results or estimate the first period of the structure. If no results are available, relationship as per EC8 4.6 is used.
        
        Args:
            ct (optional): Optional, default 0.05. Coefficient for estimation of fundamental period from EC8 4.6: T1=ct*H^(3/4)

        Returns:
            The first period of the model
        '''
        return float(self.nfrest('GET', '/res/firstmode/'+str(ct)+'', None, None))
    def getFloorLoadType(self, name):
        ''' Get a string describing the selected floor load type
        
        Args:
            name: Name of the floor load type

        Returns:
            String
        '''
        return self.nfrest('GET', '/load/floor/planetype/'+qt(name)+'', None, None)
    def getFloorPlanes(self):
        ''' Return a list of defined floor planes
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/load/floor/planesget', None, None))
    def getForceUnit(self):
        ''' Get the unit for force in the model
        
        
        Returns:
            The unit for force in the model
        '''
        return self.nfrest('GET', '/units/f', None, None)
    def getFreeElementID(self):
        ''' Get the next free element ID
        
        
        Returns:
            Int64 value
        '''
        return self.nfrest('GET', '/op/freeelementid', None, None)
    def getFreeNodeID(self):
        ''' Get the next free node ID
        
        
        Returns:
            Int64 value
        '''
        return self.nfrest('GET', '/op/freenodeid', None, None)
    def getFunctionGeneralData(self, funcID):
        ''' Get custom data stored in the selected function
        
        Args:
            funcID: ID of the function

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/function/gendata/'+str(funcID)+'', None, None))
    def getFunctionName(self, funcID):
        ''' Get name of the selected function
        
        Args:
            funcID: ID of the function

        Returns:
            String
        '''
        return self.nfrest('GET', '/function/name/'+str(funcID)+'', None, None)
    def getFunctionPlot(self, funcID, imagePath):
        ''' Get plot of the selected function
        
        Args:
            funcID: ID of the function
            imagePath: Path of the PNG image to be written

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/function/plot/'+str(funcID)+'', None, dict([("path",imagePath)])))
    def getFunctions(self):
        ''' Get a list of IDs of already defined functions
        
        
        Returns:
            Array of Int32
        '''
        return json.loads(self.nfrest('GET', '/functions', None, None))
    def getFunctionUnits(self, funcID):
        ''' Get units of the selected function (Y values)
        
        Args:
            funcID: ID of the function

        Returns:
            String
        '''
        return self.nfrest('GET', '/function/units/'+str(funcID)+'', None, None)
    def getGreekLetter(self, input):
        ''' Return the corresponding letter from Greek alphabet
        
        Args:
            input: Latin letter to convert

        Returns:
            String
        '''
        return self.nfrest('GET', '/op/greek'+qt(input)+'', None, None)
    def getGroups(self):
        ''' Get all groups in the model
        
        
        Returns:
            An array with names of groups
        '''
        return json.loads(self.nfrest('GET', '/groups', None, None))
    def getItemDataResults(self, item, lc, t, station=0):
        ''' Get properties and results for the selected node or element
        
        Args:
            item: ID of the item (node or element) to be checked. If item is an element, specifiy a non-zero station
            lc: Loadcase containing results
            t: Reference time for results. For linear analyses, use "1".
            station (optional): Optional, default 0. Use: 1 fo I, 2 for 1/4, 3 for M, 4 for 3/4, 5 for J. For elements other than lines, use 1

        Returns:
            A dictionary of string and decimal containing all the values used for checking and results
        '''
        return json.loads(self.nfrest('GET', '/res/check/data/'+qt(item)+'/'+qt(lc)+'/'+qt(t)+'/'+str(station)+'', None, None))
    def getLanguage(self):
        ''' Get language code (eg. "en" for English)
        
        
        Returns:
            String
        '''
        return self.nfrest('GET', '/op/opt/lang', None, None)
    def getLastBilinearMomentCurvature(self):
        ''' Get bilinearized moment-curvature of the last section calculated in getSectMomentCurvature
        
        
        Returns:
            A list of arrays of double (size 2)
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/bilmomentcurvature', None, None))
    def getLastMomentCurvatureData(self):
        ''' Get last moment-curvature extended data for the last section calculated in getSectMomentCurvature
        
        
        Returns:
            List of array of strings
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/momentcurvaturedata', None, None))
    def getLastRunLog(self):
        ''' Get log for the last run analysis
        
        
        Returns:
            An array of string, empty if not available
        '''
        return json.loads(self.nfrest('GET', '/op/runlog', None, None))
    def getLastSectionRes3DDomainPoints(self, conn=None):
        ''' Get list of 3D points for plotting 3D resisting domain of the last computed section
        
        Args:
            conn (optional): Optional. Connectivity dictionary for 3D points passed by reference

        Returns:
            A list of vert3 containing 3D points of the domain boundary
        '''
        return json.loads(self.nfrest('GET', '/res/check/plot3dsectiondomain'+str(conn)+'', None, None))
    def getLastSectionResDomainPoints(self, domainType, cleanResponseTolerance=0):
        ''' Get list of points for plotting resisting domain of the last computed sections
        
        Args:
            domainType: 0 for Myy vs. Mzz, 1 for N vs. Myy, 2 for N vs. Mzz
            cleanResponseTolerance (optional): Optional, default is 0. Clean points given in N-Mxx domains, to be used only if wrong plot is obtained (e.g. set to 1e-8)

        Returns:
            A list of array of double values, each of size 2 (X,Y)
        '''
        return json.loads(self.nfrest('GET', '/res/check/lastplotsectiondomain/'+str(domainType)+'/'+str(cleanResponseTolerance)+'', None, None))
    def getLenUnit(self):
        ''' Get the unit for length in the model
        
        
        Returns:
            The unit for length in the model
        '''
        return self.nfrest('GET', '/units/l', None, None)
    def getLinearAddCombination(self, name):
        ''' Return a check object with loadcases and corresponding factors for desired load combination.
        
        Args:
            name: Name of load combination

        Returns:
            A check object
        '''
        return self.nfrest('GET', '/loadcase/combo/get/'+qt(name)+'', None, None)
    def getLoad(self, i):
        ''' Returns a string describing of the i-th load in the model.
        
        Args:
            i: ID of the load, starting from 0.

        Returns:
            Returns a description of the i-th load in the model. Empty string if not found
        '''
        return self.nfrest('GET', '/load/'+str(i)+'', None, None)
    def getLoadA(self, i):
        ''' Returns an array of strings describing of the i-th load in the model (ID,Node,Element,Direction,Load value,Load case)
        
        Args:
            i: ID of the load, starting from 0.

        Returns:
            Returns a description of the i-th load in the model. Empty string if not found
        '''
        return json.loads(self.nfrest('GET', '/load/getA/'+str(i)+'', None, None))
    def getLoadcaseFactor(self, loadcase):
        ''' Get load factor for the function associated to the selected loadcase
        
        Args:
            loadcase: Name of the loadcase

        Returns:
            Double value
        '''
        return float(self.nfrest('GET', '/loadcase/getfactor/'+qt(loadcase)+'', None, None))
    def getLoadCaseFunction(self, loadcase):
        ''' Get the function associated to the selected loadcase
        
        Args:
            loadcase: Name of the loadcase

        Returns:
            0 if not function is associates, the ID of the function otherwise
        '''
        return int(self.nfrest('GET', '/loadcase/getfunc/'+qt(loadcase)+'', None, None))
    def getLoadCases(self):
        ''' Get the names of loadcases set in the model.
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/loadcases', None, None))
    def getLoadCaseType(self, name):
        ''' Get loadcase type
        
        Args:
            name: Name of the loadcase

        Returns:
            Integer type: 0 Dead, 1 Live, 2 Wind, 3 Snow, 4 User, 5 Quake, 6 unknown, 7 Thermal, 8 Prestress
        '''
        return int(self.nfrest('GET', '/loadcase/gettype/'+qt(name)+'', None, None))
    def getLoadCombinations(self, includeEnvelopes=True):
        ''' Get the names of load combinations set in the model.
        
        Args:
            includeEnvelopes (optional): Optional. False to exclude envelopes

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/loadcase/combos/'+str(includeEnvelopes)+'', None, None))
    def getLoadDurationClass(self, loadcase):
        ''' Returns the load duration class for the requested loadcase
        
        Args:
            loadcase: Name of the loadcase

        Returns:
            0 Permanent, 1 Long term, 2 Medium term, 3 Short term, 4 Istantaneous. If not defined yet, return 0 (permanent)
        '''
        return int(self.nfrest('GET', '/load/getduration/'+qt(loadcase)+'', None, None))
    def getLoadingData(self):
        ''' Retrieve custom data about wind, snow and other custom loading
        
        
        Returns:
            String
        '''
        return self.nfrest('GET', '/model/loadingdata', None, None)
    def getLoadsForElement(self, element):
        ''' Produces a list of load IDs for a single element.
        
        Args:
            element: ID of the element

        Returns:
            Produces as list of load IDs for a single element.
        '''
        return json.loads(self.nfrest('GET', '/load/element/get/'+qt(element)+'', None, None))
    def getLoadsForNode(self, node):
        ''' Produces a list of load IDs for a single node.
        
        Args:
            node: ID of the node

        Returns:
            Produces as list of load IDs for a single node.
        '''
        return json.loads(self.nfrest('GET', '/load/node/get/'+qt(node)+'', None, None))
    def getLoadsInLoadcase(self, loadcase):
        ''' Produces a list of load IDs for a single loadcase.
        
        Args:
            loadcase: Loadcase name

        Returns:
            Array of Int32
        '''
        return json.loads(self.nfrest('GET', '/load/inloadcase/'+qt(loadcase)+'', None, None))
    def getLocalAxes(self, ID):
        ''' Return local axes of an element as API.vert3
        
        Args:
            ID: 

        Returns:
            
        '''
        return json.loads(self.nfrest('GET', '/element/lcs/'+qt(ID)+'', None, None))
    def getLocalAxesArray(self, ID):
        ''' Return local axes of an element as array of double {x1,x2,x3,y1,y2,y3,z1,z2,z3}
        
        Args:
            ID: 

        Returns:
            Array of double
        '''
        return json.loads(self.nfrest('GET', '/element/lcsA/'+qt(ID)+'', None, None))
    def getMacroelement(self, elemID):
        ''' Get the macroelement type assigned to the selected element
        
        Args:
            elemID: Selected element ID

        Returns:
            Line=0, Line3=1, Quad1=2, Quad2=3, Quad3=4, masonryWall=5, rigidWall=6, -1 if not assigned
        '''
        return int(self.nfrest('GET', '/element/macro/'+qt(elemID)+'', None, None))
    def getMaterialProperty(self, ID, name, units=None):
        ''' Return selected property from a material
        
        Args:
            ID: Material ID
            name: Name of the property: alphaT, behaviour, code, E, G, fk, ni, Mden, Wden, type
            units (optional): String supplied to function to eventually convert units of returned value

        Returns:
            The requested value as string. Empty in case of error
        '''
        return self.nfrest('GET', '/material/prop/'+qt(ID)+'/'+qt(name)+'', None, dict([("units",units)]))
    def getMaterialsLibrary(self, filter='', type=0):
        ''' Return an array of string containing material names from built-in library.
        
        Args:
            filter (optional): Optional. String supporting wildcards for material name
            type (optional): Optional. Integer for material type: Steel = 1, Aluminium = 2, Concrete = 3, Timber = 4, Masonry = 5, TensionFragile = 6

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/materials/library/'+qt(filter)+'/'+str(type)+'', None, None))
    def getMaterialsLibrary(self, filename, filter='', type=0):
        ''' Return an array of string containing material names from built-in library.
        
        Args:
            filename: Name of the nfm library, without extension
            filter (optional): Optional. String supporting wildcards for material name
            type (optional): Optional. Integer for material type: Steel = 1, Aluminium = 2, Concrete = 3, Timber = 4, Masonry = 5, TensionFragile = 6

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/materials/libraryf/'+qt(filename)+'/'+qt(filter)+'/'+str(type)+'', None, None))
    def getMaxMinBeamForces(self, sectionID, type):
        ''' Get maximum and minimum beam forces from elements having the same section, in all loadcases and all stations
        
        Args:
            sectionID: Section ID
            type: 1=N, 2=Vy, 3=Vz, 4=Mt, 5=My, 6=Mz

        Returns:
            An array of length 2 containing max and min force for the desired type
        '''
        return json.loads(self.nfrest('GET', '/res/maxminbeamforces/'+str(sectionID)+'/'+str(type)+'', None, None))
    def getMaxMinNodeDispl(self, dir, nodes:list=None):
        ''' Get maximum and minimum nodal displacement from all nodal results.
        
        Args:
            dir: Direction: 1 xyz, 2 x, 3 y, 4 z, 5 xy, 6 yz, 7 xz, 8 rxyz (rotations)
            nodes (optional): 

        Returns:
            
        '''
        return json.loads(self.nfrest('POST', '/res/maxmindispl/'+str(dir)+'', nodes, None))
    def getMaxMinWoodArmerMoments(self, elementID):
        ''' Get maximum and minimun Wood-Armer moments from elements in the same group of the selected element
        
        Args:
            elementID: One element in wall or slab group

        Returns:
            An array of length 2 containing max and min moments in this order: bottom dir.x, botton dir.y, top dir.x, top dir.y
        '''
        return json.loads(self.nfrest('GET', '/res/maxminwoodarmer/'+str(elementID)+'', None, None))
    def getMaxMinWoodArmerMoments(self, groupName):
        ''' Get maximum and minimun Wood-Armer moments from elements in the same group of the selected element
        
        Args:
            groupName: Wall or slab group name

        Returns:
            An array of length 2 containing max and min moments in this order: bottom dir.x, botton dir.y, top dir.x, top dir.y
        '''
        return json.loads(self.nfrest('GET', '/res/maxminwoodarmerg/'+qt(groupName)+'', None, None))
    def getMemberElements(self, member):
        ''' Get the IDs of beam elements grouped in a member.
        
        Args:
            member: Member ID

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/model/member/elems/'+qt(member)+'', None, None))
    def getMemberLength(self, member):
        ''' Get member length
        
        Args:
            member: Member ID

        Returns:
            Double
        '''
        return float(self.nfrest('GET', '/model/member/leng/'+qt(member)+'', None, None))
    def getMembers(self):
        ''' Get a list of members defined in the model
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/model/member/all', None, None))
    def getModalPeriod(self, num, loadcase):
        ''' Get a modal period of the structure or the buckling factor
        
        Args:
            num: Number of the mode
            loadcase: Name of the loadcase

        Returns:
            0 if not found or error
        '''
        return float(self.nfrest('GET', '/res/period/'+str(num)+'/'+qt(loadcase)+'', None, None))
    def getModes(self, loadcase=None):
        ''' Get the number of available modes in results
        
        Args:
            loadcase (optional): Optional. Name of the loadcase, if empty the first avaialble modal o response spectrum data is used

        Returns:
            loadcase parameters is passed by reference, hence the selected loadcase is returned if loadcase is empty
        '''
        return int(self.nfrest('GET', '/res/modes/'+str(loadcase)+'', None, None))
    def getMultiplePlots(self, plotList:list, transparent=False, names:list=None, Xunits='', Yunits='', colors:list=None, useDots:list=None, showLegend=False):
        ''' Get plots of multiple series in a single image
        
        Args:
            plotList: List of list of double[2] arrays
            transparent (optional): If true, set transparent background
            names (optional): Optional. Titles of the plots
            Xunits (optional): Optional. Units for x axis
            Yunits (optional): Optional. Units for y axis
            colors (optional): Optional. Array of plot colors
            useDots (optional): Optional. Array of boolean values for using dots in each plot
            showLegend (optional): Optional. True to enable graph legend

        Returns:
            List of arrays of bytes
        '''
        return json.loads(self.nfrest('GET', '/function/plotmultipledata/'+str(transparent)+'/'+json.dumps(names)+'/'+qt(Xunits)+'/'+qt(Yunits)+'/'+json.dumps(colors)+'/'+json.dumps(useDots)+'/'+str(showLegend)+'', plotList, dict([("colors",xseries),("useDots",yseries)])))
    def getNodalDisp(self, num, loadcase, time, direction):
        ''' Get nodal displacement from the selected loadcase and time
        
        Args:
            num: node no.
            loadcase: loadcase name
            time: time
            direction: Global direction: 1=X, 2=Y, 3=Z, 4=RX, 5=RY, 6=RZ

        Returns:
            The requested value. 0 if something went wrong.
        '''
        return float(self.nfrest('GET', '/res/displacement/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(direction)+'', None, None))
    def getNodalReact(self, num, loadcase, time, direction):
        ''' Get nodal reaction from the selected loadcase and time
        
        Args:
            num: node no.
            loadcase: loadcase name
            time: time
            direction: Global direction: 1=X, 2=Y, 3=Z, 4=RX, 5=RY, 6=RZ

        Returns:
            The requested value. 0 if something went wrong.
        '''
        return float(self.nfrest('GET', '/res/reaction/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(direction)+'', None, None))
    def getNodalShellForce(self, num, loadcase, time, type):
        ''' Get nodal shell forces from nodes connected to shell elements
        
        Args:
            num: Node number
            loadcase: Loadcase name
            time: Time value in results, for linear analyses is 1
            type: Name of the property to get

        Returns:
            The requested value. 0 if something went wrong.
        '''
        return float(self.nfrest('GET', '/res/nodalshellforce/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+qt(type)+'', None, None))
    def getNodalStress(self, num, loadcase, time, type):
        ''' Get stress from node
        
        Args:
            num: Node number
            loadcase: Loadcase name
            time: Time value in results, for linear analyses is 1
            type: Name of the property to get

        Returns:
            The requested value. 0 if something went wrong.
        '''
        return float(self.nfrest('GET', '/res/nodalstress/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+qt(type)+'', None, None))
    def getNodeChecks(self, ID, lc, time):
        ''' Get the checks stored in the model for the specified node
        
        Args:
            ID: ID of the element
            lc: Name of the loadcase
            time: Time

        Returns:
            Null if no checking are available
        '''
        return self.nfrest('GET', '/res/check/nodsA/'+qt(ID)+'/'+qt(lc)+'/'+qt(time)+'', None, None)
    def getNodeCoordinates(self, ID):
        ''' Returns node coordinates as double array
        
        Args:
            ID: ID of the node

        Returns:
            Array of doubles
        '''
        return json.loads(self.nfrest('GET', '/node/ID'+qt(ID)+'', None, None))
    def getNodeInfo(self, node):
        ''' Get text with node properties
        
        Args:
            node: ID of the node

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/node/info/'+qt(node)+'', None, None))
    def getNodePosition(self, ID):
        ''' Returns node position as vert3 object
        
        Args:
            ID: ID of the node

        Returns:
            A vert3 object
        '''
        return self.nfrest('GET', '/node/ID'+qt(ID)+'', None, None)
    def getNodeProperty(self, ID, name):
        ''' Return selected property of node
        
        Args:
            ID: ID of the node
            name: Name of the property: num, nonStr, isJoint

        Returns:
            The requested value as string. Empty in case of error
        '''
        return self.nfrest('GET', '/node/prop/'+qt(ID)+'/'+qt(name)+'', None, None)
    def getNodesChecks(self, lc, time):
        ''' Get the checks stored in the model for nodes
        
        Args:
            lc: Name of the loadcase
            time: Time

        Returns:
            Null if no checking are available
        '''
        return json.loads(self.nfrest('GET', '/res/check/nodesA/'+qt(lc)+'/'+qt(time)+'', None, None))
    def getNodesFromCoords(self, dir, coord, tol=1E-06):
        ''' Get nodes having the specified coordinates
        
        Args:
            dir: 1 for X, 2 for Y and 3 for Z
            coord: Values of the selected coordinate
            tol (optional): Optional. Tolerance, default values is 1.e-6

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/nodesbycoords/'+str(dir)+'/'+str(coord)+'/'+str(tol)+'', None, None))
    def getNodesFromGroup(self, name):
        ''' Get nodes from group
        
        Args:
            name: Group name

        Returns:
            
        '''
        return json.loads(self.nfrest('GET', '/group/nodes/'+qt(name)+'', None, None))
    def getNodesOnSides(self, nodes:list, tol=4.94065645841247E-324):
        ''' Get nodes on borders of the selected rectangular shell region
        
        Args:
            nodes: Array of nodes
            tol (optional): Optional. Tolerance

        Returns:
            Array of size 4 with bottom, right, top and left nodes
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/borders/'+str(tol)+'', None, dict([("nodes",json.dumps(nodes))])))
    def getOSprocedureName(self):
        ''' Return the NextFEM procedure file for OpenSees, without .tcl extension
        
        
        Returns:
            String
        '''
        return self.nfrest('GET', '/op/export/osproc', None, None)
    def getParticipatingMassesRatios(self, mode, loadcase):
        ''' Get ratios of participating masses from modal or response spectrum analysis
        
        Args:
            mode: Mode number
            loadcase: Name of the loadcase

        Returns:
            Array of double
        '''
        return json.loads(self.nfrest('GET', '/res/partmasses/'+str(mode)+'/'+qt(loadcase)+'', None, None))
    def getParticipationFactors(self, mode, loadcase):
        ''' Get participation factors from modal or response spectrum analysis
        
        Args:
            mode: Mode number
            loadcase: Name of the loadcase

        Returns:
            Array of double
        '''
        return json.loads(self.nfrest('GET', '/res/partfactors/'+str(mode)+'/'+qt(loadcase)+'', None, None))
    def getReinfPropertiesNTC(self, matID, secID, CF, betaAng, Hshear, Bshear, outInMPa=False):
        ''' Get design data for FRP/FRCM strips as per CNR DT 200 Italian code
        
        Args:
            matID: ID of the FRP/FRCM design material
            secID: ID of the associated section. Must have a material already assigned
            CF: Confidence factor
            betaAng: Angle of FRP strips for shear resistance, in degrees
            Hshear: Height of FRP strips for shear resistance
            Bshear: Width of FRP strips for shear resistance in section z direction
            outInMPa (optional): Optional, default is false. Set as true if you want output in MPa

        Returns:
            A dictionary of string, double values
        '''
        return json.loads(self.nfrest('GET', '/material/frpdata/'+str(matID)+'/'+str(secID)+'/'+str(CF)+'/'+str(betaAng)+'/'+str(Hshear)+'/'+str(Bshear)+'/'+str(outInMPa)+'', None, None))
    def getResultHistory(self, loadcase, itemID, resultType, resultID1=0, resultID2=0):
        ''' Get result history for the selected quantity
        
        Args:
            loadcase: Name of the loadcase
            itemID: Node or element ID
            resultType: Time=0, nodal displ.=1, nodal velocity=2, nodal acceleration=3, nodal reaction=4, nodal force=5, nodal stress=6, nodal strain=7,
 beam force=8, beam deflection=9, spring state variable=10, nodal temperture=11
            resultID1 (optional): Required for all types of data except time and temperature, starts at 1
            resultID2 (optional): Required for beam data, 1=N/x, 2=Vy/y, 3=Vz/z, 4=Mt/rx, 5=My/ry, 6=Mz/rz

        Returns:
            Array of double
        '''
        return json.loads(self.nfrest('GET', '/res/hist/'+qt(loadcase)+'/'+qt(itemID)+'/'+str(resultType)+'/'+str(resultID1)+'/'+str(resultID2)+'', None, None))
    def getRigidDiaphragms(self):
        ''' Gives the list of master nodes in rigid diaphragms
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/rigiddiaph', None, None))
    def getRigidOffsets(self, beamID):
        ''' Get beam end offset length ratios, or and array of 0 if no end offset is present
        
        Args:
            beamID: ID of the beam element

        Returns:
            Return an array of size 2 with the relative length of the rigid offset for ends I and J, respectively
        '''
        return json.loads(self.nfrest('GET', '/element/beamendoffset/'+qt(beamID)+'', None, None))
    def getSectionColor(self, ID):
        ''' Get the color of the selected section in RGB format
        
        Args:
            ID: ID of the section

        Returns:
            Integer
        '''
        return int(self.nfrest('GET', '/section/set/color/'+qt(ID)+'', None, None))
    def getSectionCutForce(self, groupName, loadcase, time, type):
        ''' Get section cut force for the selected section cut, loadcase, time and DoF
        
        Args:
            groupName: Name of section cut group
            loadcase: Loadcase name
            time: For linear analysis, set as 1
            type: 1=N, 2=Vy, 3=Vz, 4=Mt, 5=My, 6=Mz

        Returns:
            The requested value. 0 if something went wrong.
        '''
        return float(self.nfrest('GET', '/res/sectioncutforce/'+qt(groupName)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(type)+'', None, None))
    def getSectionFigure(self, sectionID, figureID, isHole=False):
        ''' Get points in Z-Y plane from a section figure. Typically, index 1 contains the first (filled) figure.
        
        Args:
            sectionID: ID of the section
            figureID: 1-based index of the figure
            isHole (optional): Default false. True if requested figure is a hole

        Returns:
            A 2-dimensional array of double
        '''
        return json.loads(self.nfrest('GET', '/section/figure/'+str(sectionID)+'/'+str(figureID)+'/'+str(isHole)+'', None, None))
    def getSectionImage(self, sectionID, titleX='', titleY='', title='', quoteUnits='', quoteFormat='0.00', showAxes=True, showOrigin=0, transparent=False, selectedBar=0):
        ''' Get section plot into an array of Bytes of Png image
        
        Args:
            sectionID: ID of the section
            titleX (optional): Optional title for X axis
            titleY (optional): Optional title for Y axis
            title (optional): Optional graph title
            quoteUnits (optional): Optional. Units of quotes, if set display quotes
            quoteFormat (optional): Optional. Numeric format of quotes
            showAxes (optional): Optional, default true
            showOrigin (optional): Optional, default 0. 1 to show Z and Y arrows, 2 for X and Y arrows
            transparent (optional): Optional, default false. If true, set transparent background
            selectedBar (optional): Optional, default 0. Index of rebar to highlight, 0 to remove highlightning. Set to -1 to remove bars and show section center

        Returns:
            Array of bytes
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/imageB/'+str(sectionID)+'/'+qt(titleX)+'/'+qt(titleY)+'/'+qt(title)+'/'+qt(quoteUnits)+'/'+qt(quoteFormat)+'/'+str(showAxes)+'/'+str(showOrigin)+'/'+str(transparent)+'/'+str(selectedBar)+'', None, None))
    def getSectionOffset(self, ID):
        ''' Get the section offset for selected beam element
        
        Args:
            ID: ID of the beam element

        Returns:
            An array of size 2 with offset in z and offset in y local directions. Return null array even if the element is not found
        '''
        return json.loads(self.nfrest('GET', '/section/set/offset/'+qt(ID)+'', None, None))
    def getSectionProperties(self, ID):
        ''' Get all properties of a section
        
        Args:
            ID: ID of the section

        Returns:
            A string array with all properties
        '''
        return json.loads(self.nfrest('GET', '/section/props/'+qt(ID)+'', None, None))
    def getSectionProperty(self, ID, name):
        ''' Get selected property of a section
        
        Args:
            ID: ID of the section
            name: Name of the property: name, code, type, Lx, Ly, b, h, t, etc.

        Returns:
            A string with the desired property
        '''
        return self.nfrest('GET', '/section/prop/'+qt(ID)+'/'+qt(name)+'', None, None)
    def getSectionRebarCoords(self, ID):
        ''' Get rebar coordinates from selected section
        
        Args:
            ID: ID of the section

        Returns:
            Array of X,Y coordinates of size (rebarNumber,2). Coordinates are always referred to the center of reinforcement
        '''
        return json.loads(self.nfrest('GET', '/section/rebar/coords/'+qt(ID)+'', None, None))
    def getSectionRebarSize(self, ID):
        ''' Get rebar dimensions from selected section
        
        Args:
            ID: ID of the section

        Returns:
            Array of dimensions of size (rebarNumber,2). All values in mm. Each item starts with Dd with d the diameter for bars, base x height @ rotation for rectangular reinforcements
        '''
        return json.loads(self.nfrest('GET', '/section/rebar/size/'+qt(ID)+'', None, None))
    def getSectionResDomainPoints(self, domainIndex, domainType, cleanResponseTolerance=0):
        ''' Get list of points for plotting resisting domain of already computed sections
        
        Args:
            domainIndex: Index of the domain, base 0, returned by getSectionResMoments2, getSectionResMoments3, getSectionResMoments4
            domainType: 0 for Myy vs. Mzz, 1 for N vs. Myy, 2 for N vs. Mzz
            cleanResponseTolerance (optional): Optional, default is 0. Clean points given in N-Mxx domains, to be used only if wrong plot is obtained (e.g. set to 1e-8)

        Returns:
            A list of array of double values, each of size 2 (X,Y)
        '''
        return json.loads(self.nfrest('GET', '/res/check/plotsectiondomain/'+str(domainIndex)+'/'+str(domainType)+'/'+str(cleanResponseTolerance)+'', None, None))
    def getSectionResMoments(self, ID, station, calcType, N, Myy, Mzz):
        ''' Get flexural strength of a beam station by calculating neutral axis
        
        Args:
            ID: ID of the element
            station: ID of station, from 1 to 5
            calcType: 0 plastic, 1 elastic, 2 thermal-plastic, 3 thermal-elastic, 4 elastic limit, 5 thermal-elastic limit
            N: Axial force. Positive for tension
            Myy: Moment around vertical section axis
            Mzz: Moment around horizontal section axis

        Returns:
            A string with serialized results in JSON format
        '''
        return self.nfrest('GET', '/op/sectioncalc/a/'+qt(ID)+'/'+str(station)+'/'+str(calcType)+'/'+str(N)+'/'+str(Myy)+'/'+str(Mzz)+'', None, None)
    def getSectionResMoments(self, sectionID, materialID, calcType, N, Myy, Mzz):
        ''' Get flexural strength of a section by calculating neutral axis
        
        Args:
            sectionID: ID of the section
            materialID: ID of material
            calcType: 0 plastic, 1 elastic, 2 thermal-plastic, 3 thermal-elastic, 4 elastic limit, 5 thermal-elastic limit
            N: Axial force. Positive for tension
            Myy: Moment around vertical section axis
            Mzz: Moment around horizontal section axis

        Returns:
            A string in JSON format
        '''
        return self.nfrest('GET', '/op/sectioncalc/b/'+qt(sectionID)+'/'+qt(materialID)+'/'+str(calcType)+'/'+str(N)+'/'+str(Myy)+'/'+str(Mzz)+'', None, None)
    def getSectionResMoments2(self, sectionID, calcType, N, Mzz, Myy, saveImages='', domainTp=0, options=None, Nserv=0, Mzzserv=0, Myyserv=0):
        ''' Get flexural strength of a section by calculating neutral axis. Material must be set as section property, see setSectionMaterial.
        
        Args:
            sectionID: ID of the section
            calcType: 0 plastic, 1 elastic, 2 thermal-plastic, 3 thermal-elastic, 4 elastic limit, 5 thermal-elastic limit
            N: Axial force. Positive for tension
            Mzz: Moment around vertical section axis
            Myy: Moment around horizontal section axis
            saveImages (optional): Path for saving images of calculated section and domain, in PNG format. Only path a filename is required, no extension.
            domainTp (optional): Optional. Domain type for image: 0 for Myy_Mzz, 1 for N_Myy, 2 for N_Mzz
            options (optional): Optional. Calculation options
            Nserv (optional): Optional. Serviceability axial force. Positive for tension
            Mzzserv (optional): Optional. Serviceability Mzz
            Myyserv (optional): Optional. Serviceability Myy

        Returns:
            An array of strings containing calculation results
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/c/'+str(sectionID)+'/'+str(calcType)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(domainTp)+'/'+str(Nserv)+'/'+str(Mzzserv)+'/'+str(Myyserv)+'', None, dict([("saveImages",saveImages),("options",options)])))
    def getSectionResMoments3(self, sectionID, calcType, N, Mzz, Myy, saveImages='', domainTp=0, options=None, Nserv=0, Mzzserv=0, Myyserv=0):
        ''' Get flexural strength of a section by calculating neutral axis. Material must be set as section property, see setSectionMaterial.
        
        Args:
            sectionID: ID of the section
            calcType: 0 plastic, 1 elastic, 2 thermal-plastic, 3 thermal-elastic, 4 elastic limit, 5 thermal-elastic limit
            N: Axial force. Positive for tension
            Mzz: Moment around vertical section axis
            Myy: Moment around horizontal section axis
            saveImages (optional): Path for saving images of calculated section and domain, in PNG format. Only path a filename is required, no extension.
            domainTp (optional): Optional. Domain type for image: 0 for Myy_Mzz, 1 for N_Myy, 2 for N_Mzz
            options (optional): Optional. Calculation options
            Nserv (optional): Optional. Serviceability axial force. Positive for tension
            Mzzserv (optional): Optional. Serviceability Mzz
            Myyserv (optional): Optional. Serviceability Myy

        Returns:
            A check structure with results
        '''
        return self.nfrest('GET', '/op/sectioncalc/d/'+str(sectionID)+'/'+str(calcType)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(domainTp)+'/'+str(Nserv)+'/'+str(Mzzserv)+'/'+str(Myyserv)+'', None, dict([("saveImages",saveImages),("options",options)]))
    def getSectionResShear(self, sectionID, N=0, Mzz=0, Myy=0, Vy=0, Vz=0):
        ''' Get section shear resistance by automatically selecting checking rules for section material
        
        Args:
            sectionID: ID of the section
            N (optional): Optional. Axial force. Positive for tension
            Mzz (optional): Optional. Moment around vertical section axis
            Myy (optional): Optional. Moment around horizontal section axis
            Vy (optional): Optional. Shear force in y direction
            Vz (optional): Optional. Shear force in z direction

        Returns:
            An array of size 2 with VrdY and VrdZ
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/shear/'+str(sectionID)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(Vy)+'/'+str(Vz)+'', None, None))
    def getSectionResShear(self, sectionID, verName, N=0, Mzz=0, Myy=0, Vy=0, Vz=0):
        ''' Get section shear resistance
        
        Args:
            sectionID: ID of the section
            verName: Name of the checking to be used
            N (optional): Optional. Axial force. Positive for tension
            Mzz (optional): Optional. Moment around vertical section axis
            Myy (optional): Optional. Moment around horizontal section axis
            Vy (optional): Optional. Shear force in y direction
            Vz (optional): Optional. Shear force in z direction

        Returns:
            An array of size 2 with VrdY and VrdZ
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/shear/'+str(sectionID)+'/'+qt(verName)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(Vy)+'/'+str(Vz)+'', None, None))
    def getSectionResShearDict(self, sectionID, verName, N=0, Mzz=0, Myy=0, Vy=0, Vz=0, overrideValues:list=None):
        ''' Get section shear resistance
        
        Args:
            sectionID: ID of the section
            verName: Name of the checking to be used
            N (optional): Optional. Axial force. Positive for tension
            Mzz (optional): Optional. Moment around vertical section axis
            Myy (optional): Optional. Moment around horizontal section axis
            Vy (optional): Optional. Shear force in y direction
            Vz (optional): Optional. Shear force in z direction
            overrideValues (optional): Optional dictionary of {string, double} containing overrides for checking (e.g. ctgtheta = 1 for concrete)

        Returns:
            A dictionary of {string, double} containing all the results from calculation
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/shear2/'+str(sectionID)+'/'+qt(verName)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(Vy)+'/'+str(Vz)+'', overrideValues, None))
    def getSectionsLibrary(self, filter=''):
        ''' Return an array of string containing section names from built-in library.
        
        Args:
            filter (optional): Optional. String supporting wildcards for material name

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/sections/library/'+qt(filter)+'', None, None))
    def getSectionsLibrary(self, filename, filter=''):
        ''' Return an array of string containing section names from built-in library.
        
        Args:
            filename: Name of the nfs library, without extension
            filter (optional): Optional. String supporting wildcards for material name

        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/sections/libraryf/'+qt(filename)+'/'+qt(filter)+'', None, None))
    def getSectMomentCurvature(self, sectionID, N, Mzz, Myy, npts=20, Nserv=0, Mzzserv=0, Myyserv=0):
        ''' Get moment-curvature diagram for the selected section
        
        Args:
            sectionID: ID of the section
            N: Axial force. Positive for tension
            Mzz: Moment around vertical section axis
            Myy: Moment around horizontal section axis
            npts (optional): Optional. Number of curve points. Default 20
            Nserv (optional): Optional. Serviceability axial force. Positive for tension
            Mzzserv (optional): Optional. Serviceability Mzz
            Myyserv (optional): Optional. Serviceability Myy

        Returns:
            A list of arrays of double (size 2) with resisting moment vs. curvature (1/units of length)
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/momentcurvature/'+str(sectionID)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(npts)+'/'+str(Nserv)+'/'+str(Mzzserv)+'/'+str(Myyserv)+'', None, None))
    def getSeparator(self):
        ''' Returns separator used by the program
        
        
        Returns:
            String value
        '''
        return self.nfrest('GET', '/op/sep', None, None)
    def getShearResFromDict(self, dict:list):
        ''' Get section shear resistance from an already performed checking given in a dictionary of string, double
        
        Args:
            dict: Dictionary of string, double of an already performed checking

        Returns:
            An array of size 2 with VrdY and VrdZ
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/shearres', dict, None))
    def getShearResFromDict(self, dict:list):
        ''' Get section shear resistance from an already performed checking given in a dictionary of string, double
        
        Args:
            dict: Dictionary of string, double of an already performed checking

        Returns:
            An array of size 2 with VrdY and VrdZ
        '''
        return json.loads(self.nfrest('GET', '/op/sectioncalc/shearres', dict, None))
    def getShellEndRelease(self, ID):
        ''' Give shell releases
        
        Args:
            ID: ID of the shell. Tria and Quad only

        Returns:
            Matrix of boolean of size [n,6], where n is the number of nodes. 6 boolean values for each node (fx, fy, fz, mx, my, drilling)
        '''
        return json.loads(self.nfrest('GET', '/element/shellendrelease/'+qt(ID)+'', None, None))
    def getSoilPressureAtNode(self, node, loadcase, time='1'):
        ''' Return the soil pressure (positive if compression on soil) in Z global direction
        
        Args:
            node: Reference node
            loadcase: Name of the loadcase
            time (optional): Optional, time of result, default is 1

        Returns:
            Double value
        '''
        return float(self.nfrest('GET', '/res/soilpressureatnode/'+qt(node)+'/'+qt(loadcase)+'/'+qt(time)+'', None, None))
    def getSpringLocalAxes(self, elem):
        ''' Get local axes of a spring element
        
        Args:
            elem: Spring element number

        Returns:
            Array of double of size 9, empty if error occurs
        '''
        return json.loads(self.nfrest('GET', '/springproperty/axes/'+qt(elem)+'', None, None))
    def getStaticLoadCases(self):
        ''' Get the names of static analysis loadcases set in the model.
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/loadcases/static', None, None))
    def getSubsoilElements(self):
        ''' Get a list of elements having subsoil springs
        
        
        Returns:
            An array of element IDs
        '''
        return json.loads(self.nfrest('GET', '/element/add/subsoil', None, None))
    def getTimePeriods(self, lc):
        ''' Returns time/period values in results for the desired loadcase
        
        Args:
            lc: The desired loadcase

        Returns:
            Return nothing if empty results
        '''
        return json.loads(self.nfrest('GET', '/res/periods/'+qt(lc)+'', None, None))
    def getUserViews(self):
        ''' Get a list of names of user-defined model views
        
        
        Returns:
            An array of strings
        '''
        return json.loads(self.nfrest('GET', '/model/userviews', None, None))
    def getVersion(self):
        ''' Get API version
        
        
        Returns:
            A decimal containing the version. Eg. 1.52 stands for v1.5, patch 2
        '''
        return float(self.nfrest('GET', '/version', None, None))
    def getWallGroups(self):
        ''' Return all the groups than can be associated to a wall
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/element/walls/list', None, None))
    def getWallHeight(self, grpName):
        ''' Gives the height of a specified wall
        
        Args:
            grpName: Name of wall group

        Returns:
            Double value
        '''
        return float(self.nfrest('GET', '/element/walls/height/'+qt(grpName)+'', None, None))
    def getWalls(self):
        ''' Return all the wall elements by their number
        
        
        Returns:
            Array of strings
        '''
        return json.loads(self.nfrest('GET', '/element/walls/elems', None, None))
    def getWallSection(self, grpName):
        ''' Gives the dimensions (thickness and width) of a specified wall
        
        Args:
            grpName: Name of wall group

        Returns:
            Array of float with thickness and width
        '''
        return json.loads(self.nfrest('GET', '/element/walls/section/'+qt(grpName)+'', None, None))
    def hasResults(self, loadcase=''):
        ''' Flag indicating if model has results
        
        Args:
            loadcase (optional): Optional. Loadcase for results

        Returns:
            A boolean flag, True if any kind of result is present
        '''
        return sbool(self.nfrest('GET', '/res', None, dict([("lc",loadcase)])))
    def importAbaqusCalculix(self, path):
        ''' Import ABAQUS/CalculiX model
        
        Args:
            path: Full path of INP file

        Returns:
            Always true
        '''
        return sbool(self.nfrest('GET', '/op/import/abaqus', None, dict([("path",path)])))
    def importDolmen(self, path):
        ''' Import a CDM Dolmen model
        
        Args:
            path: Full path of STR file

        Returns:
            True if results have been read, only if .bin results are in the same folder
        '''
        return sbool(self.nfrest('GET', '/op/import/dolmen', None, dict([("path",path)])))
    def importDXF(self, path):
        ''' Import DXF file
        
        Args:
            path: Path of DXF file to be imported

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/import/dxf', None, dict([("path",path)])))
    def importDXF(self, stream):
        ''' Import DXF from stream
        
        Args:
            stream: Stream to be imported

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('POST', '/op/import/dxfstream', stream, None))
    def importGMesh(self, path):
        ''' Import a text GMesh v2 file
        
        Args:
            path: Full path of GMesh file

        Returns:
            False in case of error or GeneralDesign license missing
        '''
        return sbool(self.nfrest('GET', '/op/import/gmesh', None, dict([("path",path)])))
    def importIFC(self, path, includeRigidLinks=False):
        ''' Import IFC file
        
        Args:
            path: Full path of the IFC file
            includeRigidLinks (optional): False is default. True to read rigid links from structural models

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/import/ifc/'+str(includeRigidLinks)+'', None, dict([("path",path)])))
    def importMesh(self, path):
        ''' Import a text Mesh file from off2msh format (MeshVersionFormatted 1) or neutral
        
        Args:
            path: Full path of Mesh file

        Returns:
            False in case of error or GeneralDesign license missing
        '''
        return sbool(self.nfrest('GET', '/op/import/mesh', None, dict([("path",path)])))
    def importMidas(self, path):
        ''' Import a Midas GEN/Civil model in text format
        
        Args:
            path: Full path of MGT/MCT file

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/import/midasfile', None, dict([("path",path)])))
    def importMidas(self, model:list):
        ''' Import a Midas GEN/Civil model in text format
        
        Args:
            model: Array of model lines

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('POST', '/op/import/midastext', model, None))
    def importMidasResults(self, path):
        ''' Read results from Midas GEN/Civil tables, copied to a text file
        
        Args:
            path: Full path of results file

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/import/midasresult', None, dict([("path",path)])))
    def importMidasResults(self, text:list):
        ''' Read results from Midas GEN/Civil tables, copied to a text file
        
        Args:
            text: Array of strings

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('POST', '/op/import/midasresulttext', text, None))
    def importNodeElemFiles(self, path):
        ''' Import a node/elem set of file
        
        Args:
            path: Path of .node or .elem file

        Returns:
            
        '''
        return sbool(self.nfrest('GET', '/op/import/nodeelem', None, dict([("path",path)])))
    def importOBJ(self, path):
        ''' Import text OBJ file
        
        Args:
            path: Full path of OBJ file

        Returns:
            
        '''
        return sbool(self.nfrest('GET', '/op/import/obj', None, dict([("path",path)])))
    def importOpenSees(self, path):
        ''' Import OpenSees model in TCL format
        
        Args:
            path: Full path of TCL file

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/import/opensees', None, dict([("path",path)])))
    def importOpenSeesRecorder(self, path, type, useTimeFlag=True):
        ''' Import an OpenSees recorder text file. XML is also supported.
        
        Args:
            path: Full path of results file
            type: Type of result: 1-displacements 2-reactions 3-eigenvectors 4-accelerations 5-forces
            useTimeFlag (optional): Set to true if -time flag has been used in the recorder setting

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/import/recorder/'+str(type)+'/'+str(useTimeFlag)+'', None, dict([("path",path)])))
    def importSAF(self, path):
        ''' Import structural model in SAF file
        
        Args:
            path: Full path of SAF .xlsx file

        Returns:
            True if results have been read
        '''
        return sbool(self.nfrest('GET', '/op/import/saf', None, dict([("path",path)])))
    def importSAP2000(self, path):
        ''' Import a SAP2000 model in text format
        
        Args:
            path: Full path of S2K file

        Returns:
            True if results are present
        '''
        return sbool(self.nfrest('GET', '/op/import/sap2000', None, dict([("path",path)])))
    def importSeismoStruct(self, path):
        ''' Import a SeismoStruct XML model
        
        Args:
            path: Full path of XML file

        Returns:
            True if results have been read, only if .out file is in the same folder
        '''
        return sbool(self.nfrest('GET', '/op/import/seismostruct', None, dict([("path",path)])))
    def importSismicad(self, path, lenUnit='cm', forceUnit='daN'):
        ''' Import a Sismicad model. Consider to call importSismicadSects_Combo to read sections and combinations before calling this function.
        
        Args:
            path: Full path of Sismicad 90static.F3F/F2F file
            lenUnit (optional): Optional length units to be provided, default is cm
            forceUnit (optional): Optional force unit to be provided, default is daN

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/import/sismicad'+qt(lenUnit)+'/'+qt(forceUnit)+'', None, dict([("path",path)])))
    def importSismicadSects_Combo(self, path):
        ''' Read section definitions and combinations from Sismicad tables, in TXT format
        
        Args:
            path: Full path of TXT file

        Returns:
            Always true
        '''
        return sbool(self.nfrest('GET', '/op/import/sismicadset', None, dict([("path",path)])))
    def importSismicadSects_Combo(self, text:list):
        ''' Read section definitions and combinations from Sismicad tables, in TXT format
        
        Args:
            text: Array of strings

        Returns:
            True if at least one loadcase or combination is read
        '''
        return sbool(self.nfrest('POST', '/op/import/sismicadsettext', text, None))
    def importSofistik(self, path):
        ''' Import a Sofistik model from database
        
        Args:
            path: Full path of CDB file

        Returns:
            True if results have been read
        '''
        return sbool(self.nfrest('GET', '/op/import/sofistik', None, dict([("path",path)])))
    def importSR3(self, path):
        ''' Import a OpenSargon model in binary format
        
        Args:
            path: Full path of OpenSargon SR3 file

        Returns:
            True if results have been read, only if .sdb file is in the same folder
        '''
        return sbool(self.nfrest('GET', '/op/import/sr3', None, dict([("path",path)])))
    def importSR4(self, path):
        ''' Import a OpenSargon model in text format
        
        Args:
            path: Full path of OpenSargon SR4 file

        Returns:
            True if results have been read
        '''
        return sbool(self.nfrest('GET', '/op/import/sr4', None, dict([("path",path)])))
    def importSTL(self, path):
        ''' Import text or binary STL file
        
        Args:
            path: Full path of STL file

        Returns:
            
        '''
        return sbool(self.nfrest('GET', '/op/import/stl', None, dict([("path",path)])))
    def importStraus7(self, path):
        ''' Import a Straus7 model in text format
        
        Args:
            path: Full path of Straus7 TXT file

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/import/straus7', None, dict([("path",path)])))
    def importStrausResults(self, path):
        ''' Read results from Straus7 tables, copied to a text file
        
        Args:
            path: Full path of results file

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/import/straus7result', None, dict([("path",path)])))
    def importStrausResults(self, text:list):
        ''' Read results from Straus7 tables, copied to a text file
        
        Args:
            text: Array of strings

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('POST', '/op/import/straus7resulttext', text, None))
    def importWinStrand(self, path):
        ''' Import a EnExSys WinStrand model in XML format
        
        Args:
            path: Full path of XML file

        Returns:
            True if results have been read
        '''
        return sbool(self.nfrest('GET', '/op/import/winstrand', None, dict([("path",path)])))
    def importZeusNL(self, path):
        ''' Import a Zeus-NL/ADAPTIC model
        
        Args:
            path: Full path of Zeus-NL/ADAPTIC model file

        Returns:
            
        '''
        return sbool(self.nfrest('GET', '/op/import/zeusnl', None, dict([("path",path)])))
    def importZeusNLresults(self, path):
        ''' Import results from Zeus-NL/ADAPTIC .num file
        
        Args:
            path: Full path of Zeus-NL/ADAPTIC .num file

        Returns:
            
        '''
        return sbool(self.nfrest('GET', '/op/import/zeusnlres', None, dict([("path",path)])))
    def is64bit(self):
        ''' Check if running program is at 64bit
        
        
        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/is64bit', None, None))
    def isColumn(self, beamID):
        ''' Check if a beam element is vertical or not
        
        Args:
            beamID: ID of the beam element to check

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/element/iscolumn/'+qt(beamID)+'', None, None))
    def isNodeLoaded(self, node):
        ''' Tell if the node is loaded or not
        
        Args:
            node: ID of the node

        Returns:
            True if almost one nodal load has been found
        '''
        return sbool(self.nfrest('GET', '/load/node/isloaded/'+qt(node)+'', None, None))
    def isRestrained(self, node):
        ''' Tell if the node is restrained or not
        
        Args:
            node: ID of the node

        Returns:
            True if almost one dof is restrained
        '''
        return sbool(self.nfrest('GET', '/bc/node/'+qt(node)+'', None, None))
    def LangTrasl(self, input):
        ''' Return a translation of the input string depending on the current locale.
        
        Args:
            input: 

        Returns:
            
        '''
        return self.nfrest('POST', '/op/trasl', input, None)
    def LaunchLoadCase(self, loadcase, outOfProc=False, noWindow=False):
        ''' Launch a single loadcase calculation, not waiting for finishing
        
        Args:
            loadcase: The loadcase name to run
            outOfProc (optional): If true, run the model out of process
            noWindow (optional): If true, hide the solver window or its output lines from console. Applicable only if out of process is active

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/op/launchlc/'+qt(loadcase)+'/'+str(outOfProc)+'/'+str(noWindow)+'', None, None))
    def LaunchModel(self, outOfProc=False, noWindow=False):
        ''' Launch entire model calculation, not waiting for finishing
        
        Args:
            outOfProc (optional): If true, run the model out of process
            noWindow (optional): If true, hide the solver window or its output lines from console. Applicable only if out of process is active

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/op/launchmodel/'+str(outOfProc)+'/'+str(noWindow)+'', None, None))
    def listDesignMaterialCustomProperty(self, ID):
        ''' Get a list of the custom properties stored in the selected design material
        
        Args:
            ID: ID of the material

        Returns:
            Array of string with custom properties names. Use getDesignMaterialProperty method to get values.
        '''
        return json.loads(self.nfrest('GET', '/designmaterial/proplist/'+str(ID)+'', None, None))
    def listMaterialCustomProperty(self, ID):
        ''' Get a list of the custom properties stored in the selected material
        
        Args:
            ID: ID of the material

        Returns:
            Array of string with custom properties names. Use getMaterialProperty method to get values.
        '''
        return json.loads(self.nfrest('GET', '/material/proplist/'+str(ID)+'', None, None))
    def LoadCaseFromCombo(self, comboName):
        ''' Generates a load-case from a linear add combination.
        
        Args:
            comboName: 

        Returns:
            The name of the new loadcase created
        '''
        return self.nfrest('GET', '/loadcase/fromcombo/'+qt(comboName)+'', None, None)
    def mergeImportedLines(self, lineIDs:list):
        ''' Merge selected Line elements with imported results
        
        Args:
            lineIDs: Array of Lines to be merged

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/mesh/mergeimportedlines', None, dict([("lines",json.dumps(lineIDs))])))
    def mergeLines(self, lineIDs:list):
        ''' Merge selected Line elements
        
        Args:
            lineIDs: Array of Lines to be merged

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/mesh/mergelines', None, dict([("lines",json.dumps(lineIDs))])))
    def mergeModelData(self, modeldata):
        ''' Merge a new model to the existing one
        
        Args:
            modeldata: Model in JSON format

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('PUT', '/model/data'+qt(modeldata)+'', None, None))
    def mergeModelResults(self, modelresults):
        ''' Merge a new set of results to the existing ones
        
        Args:
            modelresults: Results in JSON format

        Returns:
            
        '''
        return sbool(self.nfrest('PUT', '/model/results'+qt(modelresults)+'', None, None))
    def mergeOverlappedNodes(self):
        ''' Merge overlapped nodes in the model
        
        
        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/mesh/mergenodes', None, None))
    def meshAreaTria(self, filledContour:list, emptyContour:list, maxTriaArea, useAllNodes=False, belt=0, useQuad=False, minAngle=20):
        ''' Mesh a planar area with triangular or quadrilateral elements
        
        Args:
            filledContour: List of nodes defining the filled part
            emptyContour: List of nodes defining holes
            maxTriaArea: Maximum area for each triangular element
            useAllNodes (optional): Optional. Include internal nodes in mesh - only for convex regions
            belt (optional): Optional. Size of the optional belt, external to the convex polygon
            useQuad (optional): Optional. Use Quad where possible
            minAngle (optional): Optional. Mininum angle in degrees for triangles generation, default is 20°

        Returns:
            An array containing the IDs of newly created Tria elements
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/tria/'+str(maxTriaArea)+'/'+str(useAllNodes)+'/'+str(belt)+'/'+str(useQuad)+'/'+str(minAngle)+'', None, dict([("filled",json.dumps(filledContour)),("empty",json.dumps(emptyContour))])))
    def meshAreaTriaMulti(self, filledContour:list, emptyContour:list, maxTriaArea, useAllNodes=False, belt=0, useQuad=False, minAngle=20):
        ''' Mesh planar areas with triangular or quadrilateral elements. This function has to be used when defined more than one hole per meshed region.
        
        Args:
            filledContour: List of array of nodes defining the filled part
            emptyContour: List of array of nodes defining holes
            maxTriaArea: Maximum area for each triangular element
            useAllNodes (optional): Optional. Include internal nodes in mesh - only for convex regions
            belt (optional): Optional. Size of the optional belt, external to the convex polygon
            useQuad (optional): Optional. Use Quad where possible
            minAngle (optional): Optional. Mininum angle in degrees for triangles generation, default is 20°

        Returns:
            An array containing the IDs of newly created Tria elements
        '''
        return json.loads(self.nfrest('GET', '/op/mesh/triamulti/'+str(maxTriaArea)+'/'+str(useAllNodes)+'/'+str(belt)+'/'+str(useQuad)+'/'+str(minAngle)+'', None, dict([("filled",json.dumps(filledContour)),("empty",json.dumps(emptyContour))])))
    def meshQuad2Wall(self, quadIDs:list, isHorizontal=False):
        ''' Mesh and group into wall a single quad element.
        
        Args:
            quadIDs: List of ID of the quads to mesh.
            isHorizontal (optional): Set to true to create vertical section cuts. If omitted or set to false, vertical wall is assumed.

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/mesh/quad2wall/'+str(isHorizontal)+'', None, dict([("quadIDs",json.dumps(quadIDs))])))
    def ModelToSection(self, openModelPath=''):
        ''' Write a section from a thermal model made with planar elements
        
        Args:
            openModelPath (optional): Optional. Path of the model to read, otherwise the current model is used

        Returns:
            ID of the newly added section
        '''
        return self.nfrest('GET', '/model/model2section', None, dict([("path",openModelPath)]))
    def moveNodes(self, nodes:list, displX, displY, displZ, absolutePosition=False):
        ''' Move nodes
        
        Args:
            nodes: Array of nodes ID to be rotated
            displX: Displacement in X direction
            displY: Displacement in Y direction
            displZ: Displacement in Z direction
            absolutePosition (optional): Optional. True if previous parameters indicate absolute position in space

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/mesh/movenodes/'+str(displX)+'/'+str(displY)+'/'+str(displZ)+'/'+str(absolutePosition)+'', None, dict([("nodes",json.dumps(nodes))])))
    def newModel(self):
        ''' Clear model
        
        
        Returns:
            
        '''
        return self.nfrest('GET', '/op/new', None, None)
    def openIDEAcodeCheck(self):
        ''' Open IDEA CheckBot, if installed. Only for local instances of NextFEM Designer
        
        
        Returns:
            
        '''
        return self.nfrest('GET', '/op/export/ccm', None, None)
    def openModel(self, filename):
        ''' Open the specified NXF or XML model
        
        Args:
            filename: Path to the model

        Returns:
            True if opening has been successful
        '''
        return sbool(self.nfrest('GET', '/op/open', None, dict([("path",filename)])))
    def quad2tria(self, elem):
        ''' Transform a quad element into 2 tria elements
        
        Args:
            elem: ID of the quad element

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/op/mesh/quad2tria/'+qt(elem)+'', None, None))
    def readBeamForces(self, num, loadcase, time, N, Vy, Vz, Mt, Myy, Mzz, pos):
        ''' Add a beam forces set to results.
        
        Args:
            num: ID of the beam element
            loadcase: Loadcase to filled
            time: Time. For linear analyses, use 1.
            N: Axial force
            Vy: Shear force in y local axis
            Vz: Shear force in z local axis
            Mt: Twisting moment
            Myy: Bending moment around y axis
            Mzz: Bending moment around z axis
            pos: Distance from the beginning of the beam to the station specified

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/res/import/beamforces/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(N)+'/'+str(Vy)+'/'+str(Vz)+'/'+str(Mt)+'/'+str(Myy)+'/'+str(Mzz)+'/'+str(pos)+'', None, None))
    def recalculateSection(self, ID):
        ''' Recalculate section properties, if needed
        
        Args:
            ID: ID of the section

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/recalc/'+str(ID)+'', None, None))
    def refreshDesignerView(self, vstate=0, resize=False):
        ''' Refresh view of the remote connected instance of NextFEM Designer. Valid only after connect() command.
        
        Args:
            vstate (optional): Optional. Int value from ViewState enumerator, default is Reset (0). (1) NoOperation, (2) NodesVisible, (3) NodesNumber, (4) ElementsNumber, etc.
            resize (optional): Optional, default to false (no view resize)

        Returns:
            
        '''
        return self.nfrest('GET', '/op/view/'+str(vstate)+'/'+str(resize)+'', None, None)
    def refreshHinges(self):
        ''' Recalculate all hinges assigned in the model. Useful after modification of material or section.
        
        
        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/hinge/refresh', None, None))
    def removeAllLoads(self):
        ''' Removes all the loads in the model
        
        
        Returns:
            True if successful, False otherwise
        '''
        return sbool(self.nfrest('DELETE', '/load/all', None, None))
    def removeAllLoadsForLoadcase(self, lc):
        ''' Removes all the loads in the model for the selected loadcase
        
        Args:
            lc: Name of the loadcase

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('DELETE', '/load/alllc/'+qt(lc)+'', None, None))
    def removeBC(self, node):
        ''' Remove boundary condition for a node
        
        Args:
            node: Node ID

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('DELETE', '/bc/'+qt(node)+'', None, None))
    def removeCompositeFlags(self, ID):
        ''' Remove flags for composite section
        
        Args:
            ID: ID of the section

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/set/removecomposite/'+str(ID)+'', None, None))
    def removeCustomData(self, key):
        ''' Remove a custom data field from the model
        
        Args:
            key: Key, must be unique

        Returns:
            True if successful, False is the key was not present
        '''
        return sbool(self.nfrest('DELETE', '/model/customdata/'+qt(key)+'', None, None))
    def removeDesMaterialProperty(self, ID, name):
        ''' Remove a custom property from the selected design material
        
        Args:
            ID: ID of the design material
            name: Name of the property

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/designmaterial/prop/'+str(ID)+'/'+qt(name)+'', None, None))
    def removeElement(self, ID):
        ''' Remove the specified element from the model
        
        Args:
            ID: ID of the element to be removed

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/element/'+qt(ID)+'', None, None))
    def removeElementsFromMember(self, member, elems:list):
        ''' Remove the specified elements from a member
        
        Args:
            member: Member ID
            elems: IDs of elements to be removed

        Returns:
            True if successful, False otherwise
        '''
        return sbool(self.nfrest('DELETE', '/model/member/elems/'+qt(member)+'', None, dict([("elems",json.dumps(elems))])))
    def removeFloorLoad(self, name):
        ''' Remove the specified floor load type
        
        Args:
            name: 

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/load/floor/remove/'+qt(name)+'', None, None))
    def removeFloorPlane(self, name):
        ''' Remove a floor plane specified by its name
        
        Args:
            name: 

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/load/floor/planeremove/'+qt(name)+'', None, None))
    def removeFreeNodes(self):
        ''' Find and remove free nodes in the model
        
        
        Returns:
            True
        '''
        return sbool(self.nfrest('GET', '/op/mesh/removefreenodes', None, None))
    def removeHinges(self, beamID):
        ''' Remove all hinges from a beam element
        
        Args:
            beamID: ID of the beam element

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/hinge/remove/'+qt(beamID)+'', None, None))
    def removeLink(self, node):
        ''' Removes a rigid link from the model.
        
        Args:
            node: ID of the slave node.

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/op/mesh/constraint/'+qt(node)+'', None, None))
    def removeLoad(self, ID):
        ''' Removes the specified load.
        
        Args:
            ID: ID of the load to be removed, starting from 0.

        Returns:
            True if successful, False otherwise
        '''
        return sbool(self.nfrest('DELETE', '/load/'+str(ID)+'', None, None))
    def removeLoadCase(self, name):
        ''' Remove the specified loacase
        
        Args:
            name: Name of the loadcase

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/loadcase/'+qt(name)+'', None, None))
    def removeLoadCaseFromCombination(self, name, loadcase):
        ''' Remove loadcase and factor from an already existing combination, buckling or PDelta analysis
        
        Args:
            name: Name of the combination or buckling analysis
            loadcase: Name of the loadcase to be removed

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/remove/'+qt(name)+'/'+qt(loadcase)+'', None, None))
    def removeLoadCaseToTimeHistoryAnalysis(self, name, loadcase):
        ''' Remove loadcase and factor to an already existing time-history analysis
        
        Args:
            name: Name of the time-history analysis
            loadcase: Name of the loadcase to be removed

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/removeth/'+qt(name)+'/'+qt(loadcase)+'', None, None))
    def removeMaterial(self, materialID):
        ''' Remove the selected material
        
        Args:
            materialID: ID of the material

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/material/remove/'+str(materialID)+'', None, None))
    def removeMaterialProperty(self, ID, name):
        ''' Remove a custom property from the selected material
        
        Args:
            ID: ID of the material
            name: Name of the property

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/material/prop/'+str(ID)+'/'+qt(name)+'', None, None))
    def removeMember(self, member):
        ''' Remove a member from the model
        
        Args:
            member: Member ID

        Returns:
            True if successful, False otherwise
        '''
        return sbool(self.nfrest('GET', '/model/member/remove/'+qt(member)+'', None, None))
    def removeNodalMass(self, ID):
        ''' Remove all masses defined in a node
        
        Args:
            ID: ID of the node hosting the masses

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/mass/remove/'+qt(ID)+'', None, None))
    def removeNode(self, ID):
        ''' Remove the node with the specified ID from the model
        
        Args:
            ID: ID of the node to be removed

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/node/ID'+qt(ID)+'', None, None))
    def removeNodeCS(self, num):
        ''' Remove a previously defined Local Coordinate System from a node.
        
        Args:
            num: Node number

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/node/cs/'+qt(num)+'', None, None))
    def removeOverlappedElements(self, tol=-1):
        ''' Find and remove overlapped elements in the model, handling members and groups
        
        Args:
            tol (optional): Optional parameter for tolerance

        Returns:
            True
        '''
        return sbool(self.nfrest('GET', '/op/mesh/removeoverlappedelements'+str(tol)+'', None, None))
    def removeRigidDiaphragms(self):
        ''' Remove all the rigid floor constraints in the model.
        
        
        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/op/mesh/rigiddiaph', None, None))
    def removeSection(self, sectionID):
        ''' Remove the selected section
        
        Args:
            sectionID: ID of the section

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/remove/'+str(sectionID)+'', None, None))
    def removeSectionCover(self, sectionID):
        ''' Remove section cover
        
        Args:
            sectionID: ID of the section

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('DELETE', '/section/add/cover/'+str(sectionID)+'', None, None))
    def removeSectionFigure(self, sectionID, figureID, isEmpty=False):
        ''' Remove a figure from the selected section
        
        Args:
            sectionID: ID of the section
            figureID: 1-based index of the figure to remove
            isEmpty (optional): Optional, True if the figure is a hole

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/add/removefigure/'+str(sectionID)+'/'+str(figureID)+'/'+str(isEmpty)+'', None, None))
    def removeSectionProperty(self, ID, name):
        ''' Revert a previously custom section property to automatic evaluation
        
        Args:
            ID: ID of the section
            name: Name of the native property: Area, Jxc, Jyc, Jxyc, Jt, Iw, shAreaX, shAreaY, or custom value to be removed

        Returns:
            True if property has been reverted to automatic evaluation or custom prop. has been removed
        '''
        return sbool(self.nfrest('DELETE', '/section/prop/'+qt(ID)+'/'+qt(name)+'', None, None))
    def removeSpringProperty(self, name):
        ''' Remove a linear or non-linear spring property
        
        Args:
            name: Name of the property set

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('DELETE', '/springproperty/'+qt(name)+'', None, None))
    def renameSection(self, sectionID, name, code=''):
        ''' Assign name to an already defined section
        
        Args:
            sectionID: ID of the section
            name: Name of the section
            code (optional): Reference code

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/section/rename/'+str(sectionID)+'/'+qt(name)+'/'+qt(code)+'', None, None))
    def renumberElements(self, initialID, step):
        ''' Renumber elements in the model
        
        Args:
            initialID: ID for 1st element, must be > 0
            step: Increment in numbering

        Returns:
            True if renumbering has been applied, false otherwise
        '''
        return sbool(self.nfrest('GET', '/op/mesh/renumber/elements/'+str(initialID)+'/'+str(step)+'', None, None))
    def renumberElementsByCoordinates(self, dir1, dir2):
        ''' Renumber elements in the model with spatial criteria, using element centroid
        
        Args:
            dir1: Index of first criterium: 1 by X, 2 by Y, 3 by Z
            dir2: Index of second criterium: 1 by X, 2 by Y, 3 by Z

        Returns:
            True if renumbering has been applied, false otherwise
        '''
        return sbool(self.nfrest('GET', '/op/mesh/renumber/elementsbycoords/'+str(dir1)+'/'+str(dir2)+'', None, None))
    def renumberNodes(self, initialID, step):
        ''' Renumber nodes in the model
        
        Args:
            initialID: ID for 1st node, must be > 0
            step: Increment in numbering

        Returns:
            True if renumbering has been applied, false otherwise
        '''
        return sbool(self.nfrest('GET', '/op/mesh/renumber/nodes/'+str(initialID)+'/'+str(step)+'', None, None))
    def renumberNodesByCoordinates(self, dir1, dir2):
        ''' Renumber nodes in the model with spatial criteria
        
        Args:
            dir1: Index of first criterium: 1 by X, 2 by Y, 3 by Z
            dir2: Index of second criterium: 1 by X, 2 by Y, 3 by Z

        Returns:
            True if renumbering has been applied, false otherwise
        '''
        return sbool(self.nfrest('GET', '/op/mesh/renumber/nodesbycoords/'+str(dir1)+'/'+str(dir2)+'', None, None))
    def requestDesignerUndo(self, ustate=0):
        ''' Request undo to remote connected instance of NextFEM Designer. Valid only after connect() command.
        
        Args:
            ustate (optional): Optional. Int value from UndoOps enumerator, default is Normal (0). NormalDontAsk (1), NoUndo (2).

        Returns:
            
        '''
        return self.nfrest('GET', '/op/undo/'+str(ustate)+'', None, None)
    def rotateNodes(self, nodes:list, axisX, axisY, axisZ, angle):
        ''' Rotate nodes by moving them
        
        Args:
            nodes: Array of nodes ID to be rotated
            axisX: X component of rotation axis
            axisY: Y component of rotation axis
            axisZ: Z component of rotation axis
            angle: Angle of rotation, in degrees

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/mesh/rotatenodes/'+str(axisX)+'/'+str(axisY)+'/'+str(axisZ)+'/'+str(angle)+'', None, dict([("nodes",json.dumps(nodes))])))
    def RunLoadCase(self, loadcase, outOfProc=False, noWindow=False):
        ''' Run a single loadcase
        
        Args:
            loadcase: 
            outOfProc (optional): If true, run the loadcase out of process
            noWindow (optional): If true, hide the solver window or its output lines from console. Applicable only if out of process is active

        Returns:
            The first error encountered in analysis. If successful returns empty string.
        '''
        return self.nfrest('GET', '/op/runlc/'+qt(loadcase)+'/'+str(outOfProc)+'/'+str(noWindow)+'', None, None)
    def RunModel(self, outOfProc=False, noWindow=False):
        ''' Run entire model
        
        Args:
            outOfProc (optional): If true, run the model out of process
            noWindow (optional): If true, hide the solver window or its output lines from console. Applicable only if out of process is active

        Returns:
            The first error encountered in analysis. If successful returns empty string.
        '''
        return self.nfrest('GET', '/op/run/'+str(outOfProc)+'/'+str(noWindow)+'', None, None)
    def saveDocX(self):
        ''' Save the current DocX document to a file. After saving, the document cannot be modified.
        
        
        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/docx/save', None, None))
    def saveDocXbytes(self, readOnlyPassword=''):
        ''' Save the current DocX document to an array of bytes. After saving, the document cannot be modified.
        
        Args:
            readOnlyPassword (optional): Set a read-only password for the document. If the password start with 'u_', unlocking is not possible

        Returns:
            Array of bytes
        '''
        return json.loads(self.nfrest('GET', '/op/docx/bytes', readOnlyPassword, None))
    def saveModel(self, filename):
        ''' Save the model and results with desired name
        
        Args:
            filename: 

        Returns:
            True if the model has been loaded correctly, False otherwise
        '''
        return sbool(self.nfrest('GET', '/op/save', None, dict([("path",filename)])))
    def saveOptions(self):
        ''' Save program options, including solver preferences, tolerances, etc.
        
        
        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/opt/saveopts', None, None))
    def saveSectionImage(self, sectionID, path):
        ''' Save section plot into a Png image
        
        Args:
            sectionID: ID of the section
            path: Path for saving image, in PNG format. Only path and filename are required, no extension.

        Returns:
            True if successed
        '''
        return sbool(self.nfrest('GET', '/op/sectioncalc/image/'+str(sectionID)+'', None, dict([("path",path)])))
    def saveSectionImageWithBars(self, elemID, progr, path):
        ''' Save a plot of an element section with rebar, if any, into a Png image
        
        Args:
            elemID: ID of the element
            progr: Progressive on element, from 0 to 100
            path: Path for saving image, in PNG format. Only path and filename are required, no extension.

        Returns:
            True if successed
        '''
        return sbool(self.nfrest('GET', '/op/sectioncalc/imagewithbars/'+qt(elemID)+'/'+str(progr)+'', None, dict([("path",path)])))
    def scaleNodes(self, nodes:list, scaleX, scaleY, scaleZ, scaleCenterX=0, scaleCenterY=0, scaleCenterZ=0):
        ''' Scale nodes
        
        Args:
            nodes: Array of nodes ID to be scaled
            scaleX: Scale factor in X direction
            scaleY: Scale factor in Y direction
            scaleZ: Scale factor in Z direction
            scaleCenterX (optional): Scale center - X coordinate, optional, default 0
            scaleCenterY (optional): Scale center - Y coordinate, optional, default 0
            scaleCenterZ (optional): Scale center - Z coordinate, optional, default 0

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('GET', '/op/mesh/scalenodes/'+str(scaleX)+'/'+str(scaleY)+'/'+str(scaleZ)+'/'+str(scaleCenterX)+'/'+str(scaleCenterY)+'/'+str(scaleCenterZ)+'', None, dict([("nodes",json.dumps(nodes))])))
    def SectionToModel(self, sectionID, saveModelPath=''):
        ''' Write model of a section, meshed with Tria elements, typically for thermal analysis
        
        Args:
            sectionID: ID of the section
            saveModelPath (optional): Optional. Path to the model to write, otherwise current is used

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/model/section2model/'+qt(sectionID)+'', None, dict([("path",saveModelPath)])))
    def seriesFromFunction(self, funcID):
        ''' Get the series of the selected function
        
        Args:
            funcID: ID of the function

        Returns:
            An array of double (2 columns)
        '''
        return json.loads(self.nfrest('GET', '/function/series/'+str(funcID)+'', None, None))
    def setAluSection(self, ID, SectionClass=3, Jw=0):
        ''' Set aluminium checking parameters for section
        
        Args:
            ID: ID of the section
            SectionClass (optional): Steel class section
            Jw (optional): Warping constant

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/set/alu/'+str(ID)+'/'+str(SectionClass)+'/'+str(Jw)+'', None, None))
    def setAnalysisSequence(self, name, previousCase):
        ''' Set the loadcases calculation order by specifying the preceding case.
        
        Args:
            name: Name of the present loadcase to modify.
            previousCase: Name of the loadcase to be calculated before the present loadcase.

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/sequence/'+qt(name)+'/'+qt(previousCase)+'', None, None))
    def setBC(self, node, x, y, z, rx, ry, rz):
        ''' Set the boundary conditions (restraints) for a node
        
        Args:
            node: Node to be restrained
            x: True if restrained
            y: True if restrained
            z: True if restrained
            rx: True if restrained
            ry: True if restrained
            rz: True if restrained

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/bc/set/'+qt(node)+'/'+str(x)+'/'+str(y)+'/'+str(z)+'/'+str(rx)+'/'+str(ry)+'/'+str(rz)+'', None, None))
    def setBeamAngle(self, num, angle):
        ''' Set the rotation angle of the specified beam.
        
        Args:
            num: Number of the element
            angle: Angle in degrees

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/element/beamangle/'+qt(num)+'/'+str(angle)+'', None, None))
    def setBucklingAnalysis(self, name, Nmodes, tol=0.0001):
        ''' Set a buckling analysis from an existing loadcase, if it doesn't contain loads, use addLoadCaseToCombination to add the load contained in other loadcases.
        
        Args:
            name: Name of the loadcase
            Nmodes: Number of requested buckling modes
            tol (optional): Tolerance

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/setbuck/'+qt(name)+'/'+str(Nmodes)+'/'+str(tol)+'', None, None))
    def setCombination(self, name, loadcase, factor, type=0, servType=0):
        ''' Set a linear add combination from an existing loadcase. It can be called multiple times.
        
        Args:
            name: Name of the loadcase to transform into a combination, or target combination
            loadcase: Name of the loadcase to add to the combination
            factor: Factor for the loadcase to add to the combination
            type (optional): Set the combination type for checking: 0 (default) unknown, 1 ultimate, 2 serviceability, 3 seismic
            servType (optional): Set the combination type for checking: 0 (default) unknown, 1 characteristic, 2 frequent, 3 quasi-permanent

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/set/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'/'+str(type)+'/'+str(servType)+'', None, None))
    def setCombinationCoeffPsi(self, subscript, type, value):
        ''' Set the psi combination coefficient to the desired value
        
        Args:
            subscript: 0 for psi0, 1 for psi1, 2 for psi2
            type: 1 for variable loading, 2 for wind loads, 3 for snow loading
            value: Desired psi value

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/setpsi/'+str(subscript)+'/'+str(type)+'/'+str(value)+'', None, None))
    def setCombinationFactors(self, gG, gQ, psiVar:list=None, psiWind:list=None, psiSnow:list=None, gSW=0):
        ''' Set or change combination factors
        
        Args:
            gG: Combination factor for permanent loading (default 1.4)
            gQ: Combination factor for variable loading (default 1.5)
            psiVar (optional): Optional array of size 3. Partial factors for variable loading (0.7,0.5,0.3)
            psiWind (optional): Optional array of size 3. Partial factors for wind loading (0.6,0.2,0.0)
            psiSnow (optional): Optional array of size 3. Partial factors for snow loading (0.5,0.2,0.0)
            gSW (optional): Optional override factor for self-weight (e.g. use 1.3 is as per NTC and set gG to 1.5)

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/loadcase/setcfactors/'+str(gG)+'/'+str(gQ)+'/'+str(gSW)+'', None, dict([("psiVar",json.dumps(psiVar)),("psiWind",json.dumps(psiWind)),("psiSnow",json.dumps(psiSnow))])))
    def setCompositeBeam(self, ID, MposFactor=-1, MnegFactor=-1):
        ''' Set composite section beam properties
        
        Args:
            ID: ID of the section
            MposFactor (optional): Inertia weight factor for positive moment, default is 0.6
            MnegFactor (optional): Inertia weight factor for negative moment, default is 0.4

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/set/compositebeam/'+str(ID)+'/'+str(MposFactor)+'/'+str(MnegFactor)+'', None, None))
    def setCompositeColumn(self, ID, EcFactor=-1, ReductionFactor=-1):
        ''' Set composite section column properties
        
        Args:
            ID: ID of the section
            EcFactor (optional): Reduction factor for concrete modulus, default is 0.5
            ReductionFactor (optional): Reduction factor for column inertia, default is 0.9

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/set/compositecolumn/'+str(ID)+'/'+str(EcFactor)+'/'+str(ReductionFactor)+'', None, None))
    def setConcretePropertiesNTC(self, matID, fc, isCharacteristic=True, unitsIn='MPa'):
        ''' Assign a custom compressive strength to a concrete material, recalculating E and ftk as per NTC code
        
        Args:
            matID: ID of the selected material
            fc: Compressive strength in MPa. If different units are used, specify them in unitsIn
            isCharacteristic (optional): Optional, default is true. fc is assumed to be a characteristic value. If set to false, it is assumed as an average value
            unitsIn (optional): Optional, default MPa. String specifying the units of fc

        Returns:
            The value of the calculated Young's modulus
        '''
        return float(self.nfrest('GET', '/material/concretentc/'+str(matID)+'/'+str(fc)+'/'+str(isCharacteristic)+'', None, dict([("unitsIn",unitsIn)])))
    def setConstraint(self, n, master, x, y, z, rx, ry, rz):
        ''' Set a general constraint between 2 nodes
        
        Args:
            n: ID of slave node
            master: ID of master node
            x: True to apply constraint to this DoF
            y: True to apply constraint to this DoF
            z: True to apply constraint to this DoF
            rx: True to apply constraint to this DoF
            ry: True to apply constraint to this DoF
            rz: True to apply constraint to this DoF

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/op/mesh/constraint/'+qt(n)+'/'+qt(master)+'/'+str(x)+'/'+str(y)+'/'+str(z)+'/'+str(rx)+'/'+str(ry)+'/'+str(rz)+'', None, None))
    def setElemAsJoint(self, num, status):
        ''' Set the Joint property of the specified element.
        
        Args:
            num: Number of the element
            status: True or False to activate or deactivate the IsJoint flag

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/element/setjoint/'+qt(num)+'/'+str(status)+'', None, None))
    def setElementChecks(self, ID, lc, time, data, setContour=False):
        ''' Import a set of checks for the specified element. If already existing, the set is overwritten.
        
        Args:
            ID: ID of the element
            lc: Loadcase name
            time: Time
            data: A "API.check" instance containing check names and values
            setContour (optional): Optional. Activate contour in view instead of default capacity/demand ratios. Default is false

        Returns:
            True if imported successfully
        '''
        return sbool(self.nfrest('GET', '/res/import/elementcheck/'+qt(ID)+'/'+qt(lc)+'/'+qt(time)+'/'+str(setContour)+'', None, dict([("data",data)])))
    def setElementCustomProperty(self, elem, propName, propValue):
        ''' Set or change an element custom property
        
        Args:
            elem: ID of the element
            propName: Property name
            propValue: Property value

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/element/customprop/'+qt(elem)+'/'+qt(propName)+'/'+qt(propValue)+'', None, None))
    def setElementOffset(self, elem, offsetZ, offsetY):
        ''' Set element line offset for the selected beam element
        
        Args:
            elem: ID of the beam element
            offsetZ: Offset in local z direction
            offsetY: Offset in local y direction

        Returns:
            True if successful, False otherwise
        '''
        return sbool(self.nfrest('POST', '/element/beamoffset/'+qt(elem)+'/'+str(offsetZ)+'/'+str(offsetY)+'', None, None))
    def setElementSection(self, elem, sectID):
        ''' Assign a section to an element. An alternative to assignSectionToElement
        
        Args:
            elem: Beam or planar element ID
            sectID: ID of the section

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/section/'+qt(elem)+'/'+str(sectID)+'', None, None))
    def setEndRelease(self, beamID, node, DOFmask:list, useStiffness=False):
        ''' Assign an end release to a beam element by specifying its force percentage or joint stiffness.
        
        Args:
            beamID: ID of the beam element
            node: Node of the beam element to which assign release
            DOFmask: Array of 6 percentages (0=free, 1=fully connected) or stiffnesses if useStiffness is True
            useStiffness (optional): Set to true to specify stiffnesses into DOFmask

        Returns:
            True if successful, False if the cannot be assigned. End releases cannot be assigned to beams with flexural hinges.
        '''
        return sbool(self.nfrest('POST', '/element/beamendrelease/'+qt(beamID)+'/'+qt(node)+'/'+str(useStiffness)+'', None, dict([("DOFmask",json.dumps(DOFmask))])))
    def setEnvelope(self, name, loadcase, factor, type=0, servType=0):
        ''' Set an envelope combination from an existing loadcase. It can be called multiple times.
        
        Args:
            name: Name of the loadcase to transform into a combination, or target combination
            loadcase: Name of the loadcase to add to the combination
            factor: Factor for the loadcase to add to the combination
            type (optional): Set the combination type for checking: 0 (default) unknown, 1 ultimate, 2 serviceability, 3 seismic
            servType (optional): Set the serviceability combination type for checking: 0 (default) unknown, 1 characteristic, 2 frequent, 3 quasi-permanent

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/setenv/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'/'+str(type)+'/'+str(servType)+'', None, None))
    def setFiberSection(self, ID, divZ=0, divY=0):
        ''' Make the selected section a fiber section. Suitable only for OpenSees solver.
        
        Args:
            ID: ID of the section
            divZ (optional): Division in Z direction
            divY (optional): Division in Y direction

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/set/fibers/'+str(ID)+'/'+str(divZ)+'/'+str(divY)+'', None, None))
    def setFirePoint(self, loadcase, fireNode, targetTemp, gradientY=0, gradientZ=0, tempAtten=20, dontLoadUnder=50):
        ''' Set the point of fire used to set temperatures of all the elements in the model
        
        Args:
            loadcase: Loadcase
            fireNode: ID of the node setting the fire position
            targetTemp: Final target temperature, in °C
            gradientY (optional): Fixed gradient (local y) to be applied. Optional, default is 0
            gradientZ (optional): Fixed gradient (local z) to be applied. Optional, default is 0
            tempAtten (optional): Temperature attenuation. Optional, default is 20°C/m
            dontLoadUnder (optional): Don't apply load under this temperature. Optional, default is 50°C

        Returns:
            A list of loaded elements
        '''
        return json.loads(self.nfrest('GET', '/load/firepoint/'+qt(loadcase)+'/'+qt(fireNode)+'/'+str(targetTemp)+'/'+str(gradientY)+'/'+str(gradientZ)+'/'+str(tempAtten)+'/'+str(dontLoadUnder)+'', None, None))
    def setFloorLoad(self, name, loadcase, loadvalue, dirX, dirY, dirZ):
        ''' Add or modify floor load type
        
        Args:
            name: Name of the floor load type
            loadcase: Name of one of the loadcases composing the floor load
            loadvalue: Corresponding load value for the loadcase composing the floor load
            dirX: Vector for loading direction: x component
            dirY: Vector for loading direction: y component
            dirZ: Vector for loading direction: z component

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/floor/set/'+qt(name)+'/'+qt(loadcase)+'/'+str(loadvalue)+'/'+str(dirX)+'/'+str(dirY)+'/'+str(dirZ)+'', None, None))
    def setFunctionGeneralData(self, funcID, data:list):
        ''' Set custom data stored in the selected function
        
        Args:
            funcID: 
            data: 

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('POST', '/function/gendata/'+str(funcID)+'', None, dict([("data",json.dumps(data))])))
    def setLanguage(self, code):
        ''' Set language code
        
        Args:
            code: Supported codes: "en", "it", "es".

        Returns:
            
        '''
        return self.nfrest('POST', '/op/opt/lang/'+qt(code)+'', None, None)
    def setLoadA(self, load:list):
        ''' Modify an existing load through an array, conforming to the one got via getLoadA
        
        Args:
            load: Array of strings with: ID,Node,Element,Direction,Load value,Load case

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/load/setA', load, None))
    def setLoadcaseFactor(self, loadcase, factor):
        ''' Change load factor for the function associated to the selected loadcase
        
        Args:
            loadcase: Name of the loadcase
            factor: Factor, cannot be 0

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/setfactor/'+qt(loadcase)+'/'+str(factor)+'', None, None))
    def setLoadCasePhaseInCombination(self, name, loadcase, phase):
        ''' Set the phase to a loadcase in an already existing combination, for analysis
        
        Args:
            name: Name of the combination or buckling analysis
            loadcase: Name of the loadcase to add to the combination
            phase: Set phase as integer for the selected loadcase in the combination. 0 for variable load, 1 for constant load

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/setphase/'+qt(name)+'/'+qt(loadcase)+'/'+str(phase)+'', None, None))
    def setLoadCaseType(self, name, type):
        ''' Set loadcase type
        
        Args:
            name: Name of the loadcase
            type: Integer type: 0 Dead, 1 Live, 2 Wind, 3 Snow, 4 User, 5 Quake, 6 unknown, 7 Thermal, 8 Prestress

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/settype/'+qt(name)+'/'+str(type)+'', None, None))
    def setLoadDurationClass(self, loadcase, durationClass):
        ''' Set the load duration class for the selected loadcase
        
        Args:
            loadcase: Name of the loadcase
            durationClass: 0 Permanent, 1 Long term, 2 Medium term, 3 Short term, 4 Istantaneous

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/setduration/'+qt(loadcase)+'/'+str(durationClass)+'', None, None))
    def setLoadsToMass(self, loadcase, factor=1, remove=False):
        ''' Add, modify or remove a load-to-mass setting.
        
        Args:
            loadcase: Name of the loadcase containing loads
            factor (optional): Factor for conversion in mass
            remove (optional): Flag for removing the selected loadcase from setting

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/mass/load2mass/'+qt(loadcase)+'/'+str(factor)+'/'+str(remove)+'', None, None))
    def setMacroelement(self, elemID, macroType):
        ''' Assign macroelement type to the selected element
        
        Args:
            elemID: Selected element ID
            macroType: Line=0, Line3=1, Quad1=2, Quad2=3, Quad3=4, masonryWall=5, rigidWall=6. Use -1 to remove assignation

        Returns:
            Boolean
        '''
        return sbool(self.nfrest('POST', '/element/macro/'+qt(elemID)+'/'+str(macroType)+'', None, None))
    def setModalAnalysis(self, name, Nmodes, tol=0.0001):
        ''' Set a modal analysis upon an existing load case
        
        Args:
            name: Name of the loadcase
            Nmodes: Number of requested modes
            tol (optional): Tolerance

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/setmodal/'+qt(name)+'/'+str(Nmodes)+'/'+str(tol)+'', None, None))
    def setNLDanalysis(self, name, tStep, nSteps, tol, iters, seriesID, Xfactor, Yfactor, Zfactor, RXfactor, RYfactor, RZfactor, seriesFactor=1, Mdamp=0, NlGeo=False):
        ''' Set a non linear dynamic analysis upon an existing load case
        
        Args:
            name: Name of the loadcase
            tStep: Time step
            nSteps: Number of steps
            tol: Tolerance
            iters: Maximum iterations for each increment
            seriesID: ID of the series
            Xfactor: Factor for time series in X direction
            Yfactor: Factor for time series in Y direction
            Zfactor: Factor for time series in Z direction
            RXfactor: Factor for time series in RX direction
            RYfactor: Factor for time series in RY direction
            RZfactor: Factor for time series in RZ direction
            seriesFactor (optional): Factor for the series
            Mdamp (optional): Mass damping factor
            NlGeo (optional): Flag for accounting second-order effects

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/setnldyn/'+qt(name)+'/'+str(tStep)+'/'+str(nSteps)+'/'+str(tol)+'/'+str(iters)+'/'+str(seriesID)+'/'+str(Xfactor)+'/'+str(Yfactor)+'/'+str(Zfactor)+'/'+str(RXfactor)+'/'+str(RYfactor)+'/'+str(RZfactor)+'/'+str(seriesFactor)+'/'+str(Mdamp)+'/'+str(NlGeo)+'', None, None))
    def setNLSanalysis(self, name, tStep, nSteps, tol, iters=10, seriesID=-1, dispControlNode='', dispControlDOF=0, NlGeo=False):
        ''' Set a non linear static analysis upon an existing load case
        
        Args:
            name: Name of the loadcase
            tStep: Time step
            nSteps: Number of steps
            tol: Tolerance
            iters (optional): Maximum iterations for each increment
            seriesID (optional): ID of the series
            dispControlNode (optional): ID of the node for displacement control
            dispControlDOF (optional): DOF of the control node for displ. control
            NlGeo (optional): Flag for accounting second-order effects

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/setnlstatic/'+qt(name)+'/'+str(tStep)+'/'+str(nSteps)+'/'+str(tol)+'/'+str(iters)+'/'+str(seriesID)+'/'+qt(dispControlNode)+'/'+str(dispControlDOF)+'/'+str(NlGeo)+'', None, None))
    def setNodeAsJoint(self, num, status):
        ''' Set the Joint property of the specified node.
        
        Args:
            num: Number of the node
            status: True or False to activate or deactivate the IsJoint flag

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/node/setjoint/'+qt(num)+'/'+str(status)+'', None, None))
    def setNodeChecks(self, ID, lc, time, data, setContour=False):
        ''' Import a set of checks for the specified node. If already existing, the set is overwritten.
        
        Args:
            ID: ID of the node
            lc: Loadcase name
            time: Time
            data: A "API.check" instance containing check names and values
            setContour (optional): Optional. Activate contour in view instead of default capacity/demand ratios. Default is false

        Returns:
            True if imported successfully
        '''
        return sbool(self.nfrest('GET', '/res/import/nodecheck/'+qt(ID)+'/'+qt(lc)+'/'+qt(time)+'/'+str(setContour)+'', None, dict([("data",data)])))
    def setNodeCoordinates(self, ID, coords:list):
        ''' Set node coordinates as double array
        
        Args:
            ID: ID of the node
            coords: Array of size 3 containing nodal coordinates

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('POST', '/node/ID'+qt(ID)+'', coords, None))
    def setNodeCS(self, num, x1, y1, z1, x2, y2, z2):
        ''' Set the Local Coordinate System of a node by specifying the first 2 vectors.
        
        Args:
            num: Number of the node
            x1: x coord. of 1st vector
            y1: y coord. of 1st vector
            z1: z coord. of 1st vector
            x2: x coord. of 2st vector
            y2: y coord. of 2st vector
            z2: z coord. of 2st vector

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/node/cs/'+qt(num)+'/'+str(x1)+'/'+str(y1)+'/'+str(z1)+'/'+str(x2)+'/'+str(y2)+'/'+str(z2)+'', None, None))
    def setNodePosition(self, node):
        ''' Set or change node position as vert3 object
        
        Args:
            node: vert3 structure of the node

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('POST', '/node/ID', node, None))
    def setPDeltaAnalysis(self, name, tol=0.0001):
        ''' Set a PDelta analysis from an existing loadcase, if it doesn't contain loads, use addLoadCaseToCombination to add the load contained in other loadcases.
        
        Args:
            name: Name of the loadcase
            tol (optional): Tolerance

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/setpdelta/'+qt(name)+'/'+str(tol)+'', None, None))
    def setResponseSpectrumAnalysis(self, direction, loadcase, modesNumber, spectrumFuncID, modalDamping=0.05, factor=1):
        ''' Set a Response Spectrum analysis on an existing loadcase
        
        Args:
            direction: 1 X, 2 Y, 3 Z
            loadcase: Name of the seismic loadcase
            modesNumber: NUmber of modes to be considered
            spectrumFuncID: ID of the spectral acceleration or displacement function
            modalDamping (optional): Optional. Modal damping to be assumed. Default is 0.05
            factor (optional): Optional. Amplification factor. Default is 1

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/setrs/'+str(direction)+'/'+qt(loadcase)+'/'+str(modesNumber)+'/'+str(spectrumFuncID)+'/'+str(modalDamping)+'/'+str(factor)+'', None, None))
    def setRigidDiaphragms(self, constraintType=0, nodesList:list=None, masterNode='', restrainZMaster=False):
        ''' Set rigid diaphragms for all model. Floors heigths are taken automatically, restrained floors are skipped.
        
        Args:
            constraintType (optional): 0 for automatic master node, 1 to add a master node, 2 to manually specify master node for a selected group of nodes
            nodesList (optional): Optional list containing nodes ID for the rigid floor. If not specified, all nodes are taken
            masterNode (optional): ID of master node, only if constraintType = 2
            restrainZMaster (optional): Restrain the master node in Z direction, only if constraintType is 1 or 2

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('PUT', '/op/mesh/rigiddiaph/'+str(constraintType)+'/'+qt(masterNode)+'/'+str(restrainZMaster)+'', None, dict([("nodesList",json.dumps(nodesList))])))
    def setRigidLink(self, n1, n2):
        ''' Set a rigid link between two nodes.
        
        Args:
            n1: ID of first node (master)
            n2: ID of second node (slave)

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('PUT', '/op/mesh/rigidlink/'+qt(n1)+'/'+qt(n2)+'', None, None))
    def setRigidOffsets(self, beamID, values:list, isAbsLength=False):
        ''' Assign rigid offsets to beam.
        
        Args:
            beamID: ID of the beam element
            values: Array of size 2 containing length ratio for each end (I, J)
            isAbsLength (optional): True to use absolute length instead of ratio

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/element/beamendoffset/'+qt(beamID)+'/'+str(isAbsLength)+'', None, dict([("values",json.dumps(values))])))
    def setSectionAngle(self, ID, a):
        ''' Set the rotation angle for a beam section.
        
        Args:
            ID: ID of the section
            a: Angle in degrees

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/set/angle/'+str(ID)+'/'+str(a)+'', None, None))
    def setSectionColor(self, ID, Red, Green, Blue):
        ''' Set the color of the selected section in RGB format
        
        Args:
            ID: ID of the section
            Red: Red [0,255]
            Green: Green [0,255]
            Blue: Blue [0,255]

        Returns:
            True if successful, False otherwise
        '''
        return sbool(self.nfrest('POST', '/section/set/color/'+qt(ID)+'/'+str(Red)+'/'+str(Green)+'/'+str(Blue)+'', None, None))
    def setSectionMaterial(self, ID, materialID):
        ''' Set the material as section property
        
        Args:
            ID: ID of the section
            materialID: ID of the material to associate

        Returns:
            True
        '''
        return sbool(self.nfrest('GET', '/section/set/material/'+str(ID)+'/'+str(materialID)+'', None, None))
    def setSectionOffset(self, ID, offsetZ, offsetY):
        ''' Set a section offset for the selected beam section
        
        Args:
            ID: ID of the beam section
            offsetZ: Offset in local z direction
            offsetY: Offset in local y direction

        Returns:
            True if successful, False otherwise
        '''
        return sbool(self.nfrest('POST', '/section/set/offset/'+qt(ID)+'/'+str(offsetZ)+'/'+str(offsetY)+'', None, None))
    def setSectionProperty(self, ID, name, value):
        ''' Set selected property of a section. To change name or code properties, use renameSection method.
        
        Args:
            ID: ID of the section
            name: Name of the property: Area, Jxc, Jyc, Jxyc, Jt, Iw, shAreaX, shAreaY, or custom value to be added
            value: Value to be stored

        Returns:
            1 if native propery has changes, 2 if custom property is added, 0 in case of error
        '''
        return int(self.nfrest('POST', '/section/prop/'+qt(ID)+'/'+qt(name)+'/'+str(value)+'', None, None))
    def setSectionRebarsToElements(self, ID):
        ''' Assign section rebars and stirrups in elements having the same section
        
        Args:
            ID: ID of the section

        Returns:
            True is successful
        '''
        return sbool(self.nfrest('GET', '/section/rebar/toelems/'+qt(ID)+'', None, None))
    def setSectionRebarsToElements(self, ID):
        ''' Assign section rebars and stirrups in elements having the same section
        
        Args:
            ID: ID of the section

        Returns:
            True is successful
        '''
        return sbool(self.nfrest('GET', '/section/rebar/toelems/'+str(ID)+'', None, None))
    def setSeismicFloorEccentricity(self, thID, ct=0.05, lam=1):
        ''' Compute floor torque moments for accounting 5% eccentricity for center of mass of each rigid floor. Rigid diaphragms and masses are required.
        
        Args:
            thID: ID of the spectrum function to be used as reference for total base shear
            ct (optional): Optional, default 0.05. Coefficient for estimation of fundamental period from EC8 4.6: T1=ct*H^(3/4)
            lam (optional): Optional, default 1. Coefficient for estimation of base shear as per EC8 4.5: Fb=Sd(T1)*m*lam

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/setseismicecc/'+str(thID)+'/'+str(ct)+'/'+str(lam)+'', None, None))
    def setSeismicLoadcaseForCombos(self, direction, loadcase, enableFloorEccentricity5=False, seismicCombinationType=0):
        ''' Set the seismic loadcase for directional combinations (e.g. response spectrum). Repeat the command for other directions.
        
        Args:
            direction: 1 X, 2 Y, 3 Z
            loadcase: Name of the seismic loadcase
            enableFloorEccentricity5 (optional): Optional. False as default
            seismicCombinationType (optional): Optional. 100,30 rule is default (0), use (1) for SRSS rule

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/setseismiclc/'+str(direction)+'/'+qt(loadcase)+'/'+str(enableFloorEccentricity5)+'/'+str(seismicCombinationType)+'', None, None))
    def setSelfWeight(self, loadcase):
        ''' Set the loadcase hosting the automatic self-weight
        
        Args:
            loadcase: Name of the loadcase hosting the automatic self-weight

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/setsw/'+qt(loadcase)+'', None, None))
    def setSelfWeightDirection(self, direction):
        ''' Set the self-weight direction in space
        
        Args:
            direction: Default is -Z=-3. X=1, Y=2, Z=3, -X=-1, -Y=-2, -Z=-3

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/load/setswdir/'+str(direction)+'', None, None))
    def setShearReinfRCdata(self, ID, data:list):
        ''' Set or overwrite material data for shear reinforcement with tension-fragile design material in RC section. Set Shear strip width less than or equal to 0 to remove data
        
        Args:
            ID: ID of the section
            data: Array containing: Shear strip width, Shear strip spacing, Shear strip angle [°], Shear strip material ID, Shear strip thickness [mm], Shear strip height, Confinement strip spacing (-1 for continuous), Shear strip height along base

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/set/shearreinfrc/'+str(ID)+'', None, dict([("data",json.dumps(data))])))
    def setShellEndRelease(self, ID, node, DOFmask:list):
        ''' Set end release for shell element
        
        Args:
            ID: ID of the shell element. Must be Tria or Quad
            node: ID of the shell node to release
            DOFmask: Array of 6 boolean values (fx, fy, fz, mx, my, drilling)

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/element/shellendrelease/'+qt(ID)+'/'+qt(node)+'', None, dict([("DOFmask",json.dumps(DOFmask))])))
    def setSpringLocalAxes(self, name, x1, y1, z1, x2, y2, z2):
        ''' Set local axes in the selected spring property
        
        Args:
            name: Name of the spring property
            x1: Local axis 1 - x
            y1: Local axis 1 - y
            z1: Local axis 1 - z
            x2: Local axis 2 - x
            y2: Local axis 2 - y
            z2: Local axis 2 - z

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('POST', '/springproperty/axes/'+qt(name)+'/'+str(x1)+'/'+str(y1)+'/'+str(z1)+'/'+str(x2)+'/'+str(y2)+'/'+str(z2)+'', None, None))
    def setSRSScombination(self, name, loadcase, factor, type=0, servType=0):
        ''' Set a linear add combination from an existing loadcase. It can be called multiple times.
        
        Args:
            name: Name of the loadcase to transform into a combination, or target combination
            loadcase: Name of the loadcase to add to the combination
            factor: Factor for the loadcase to add to the combination
            type (optional): Set the combination type for checking: 0 (default) unknown, 1 ultimate, 2 serviceability, 3 seismic
            servType (optional): Set the combination type for checking: 0 (default) unknown, 1 characteristic, 2 frequent, 3 quasi-permanent

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/loadcase/combo/setsrss/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'/'+str(type)+'/'+str(servType)+'', None, None))
    def setSteelSection(self, ID, SectionClass=3, alphaLT=0.76, alphay=0.76, alphaz=0.76, Jw=0):
        ''' Set steel checking parameters for section
        
        Args:
            ID: ID of the section
            SectionClass (optional): Steel class section
            alphaLT (optional): Stability curve factor for lateral-torsional buckling
            alphay (optional): Stability factor for flexural buckling around y axis
            alphaz (optional): Stability factor for flexural buckling around z axis
            Jw (optional): Warping constant

        Returns:
            True if successful
        '''
        return sbool(self.nfrest('GET', '/section/set/steel/'+str(ID)+'/'+str(SectionClass)+'/'+str(alphaLT)+'/'+str(alphay)+'/'+str(alphaz)+'/'+str(Jw)+'', None, None))
    def setUnits(self, length, force):
        ''' Set units in the model
        
        Args:
            length: String with desider unit, eg. "m"
            force: String with desider unit, eg. "kN"

        Returns:
            Boolean value
        '''
        return sbool(self.nfrest('GET', '/units/set/'+qt(length)+'/'+qt(force)+'', None, None))
    def setWall(self, elems:list, rotate90=False, isSlab=False):
        ''' Create a wall for design, including 3 section cuts, from the selected planar elements
        
        Args:
            elems: Array of elements forming the wall
            rotate90 (optional): Optional. To create vertical section cuts, set to true
            isSlab (optional): Optional. If set to true, no section cuts are created

        Returns:
            Name of the newly created wall group
        '''
        return self.nfrest('GET', '/element/walls/set/'+str(rotate90)+'/'+str(isSlab)+'', None, dict([("elems",json.dumps(elems))]))
    def showViewport(self, path, width=600, height=400):
        ''' Open the viewport showing the model in path. REST version only against local instance of NextFEM Designer
        
        Args:
            path: 
            width (optional): 
            height (optional): 

        Returns:
            
        '''
        return sbool(self.nfrest('GET', '/op/showvieport/'+qt(path)+'/'+str(width)+'/'+str(height)+'', None, None))
    def userCheck(self, verName, overrideValues:list=None):
        ''' Run checking on user script. No node or element quantities are given. See also getItemDataResults method.
        
        Args:
            verName: Name of the checking to be used
            overrideValues (optional): Optional dictionary of {string, double} containing overrides for checking

        Returns:
            
        '''
        return json.loads(self.nfrest('POST', '/res/check/user'+qt(verName)+'', overrideValues, None))
    def valueFromFunction(self, Xval, funcID):
        ''' Get the value of the selected function corresponding to the desired abscissa
        
        Args:
            Xval: Abscissa
            funcID: ID of the function

        Returns:
            The ordinate for the desired abscissa and function.
        '''
        return float(self.nfrest('GET', '/function/value/'+str(Xval)+'/'+str(funcID)+'', None, None))
    def valueFromString(self, text, valueName):
        ''' Get value from a string containing key=value
        
        Args:
            text: String to be processed
            valueName: Key name

        Returns:
            
        '''
        return self.nfrest('GET', '/op/import/valfromstring/'+qt(text)+'/'+qt(valueName)+'', None, None)
    def vertexFromNode(self, node):
        ''' Get vertex from node for calculation with vert3 class.
        
        Args:
            node: ID of the node

        Returns:
            A vert3 object
        '''
        return self.nfrest('GET', '/node/vertex/'+qt(node)+'', None, None)
    @property
    def areaColor(self):
        '''   Change color for areas   '''
        return int(self.nfrest('GET','/model/colors/area'))
    @areaColor.setter
    def areaColor(self,value):
        '''   Change color for areas   '''
        self.nfrest('POST','/model/colors/area', heads={'val':str(value)})
    @property
    def autoMassInX(self):
        '''   Set the auto-mass in X direction.   '''
        return sbool(self.nfrest('GET','/mass/autoX'))
    @autoMassInX.setter
    def autoMassInX(self,value):
        '''   Set the auto-mass in X direction.   '''
        self.nfrest('POST','/mass/autoX', heads={'val':str(value)})
    @property
    def autoMassInY(self):
        '''   Set the auto-mass in Y direction.   '''
        return sbool(self.nfrest('GET','/mass/autoY'))
    @autoMassInY.setter
    def autoMassInY(self,value):
        '''   Set the auto-mass in Y direction.   '''
        self.nfrest('POST','/mass/autoY', heads={'val':str(value)})
    @property
    def autoMassInZ(self):
        '''   Set the auto-mass in Z direction.   '''
        return sbool(self.nfrest('GET','/mass/autoZ'))
    @autoMassInZ.setter
    def autoMassInZ(self,value):
        '''   Set the auto-mass in Z direction.   '''
        self.nfrest('POST','/mass/autoZ', heads={'val':str(value)})
    @property
    def backgroundColor(self):
        '''   Get or set the background color   '''
        return int(self.nfrest('GET','/model/colors/back'))
    @backgroundColor.setter
    def backgroundColor(self,value):
        '''   Get or set the background color   '''
        self.nfrest('POST','/model/colors/back', heads={'val':str(value)})
    @property
    def baselineGrade(self):
        '''   Get or set the degree of the baseline correction function for dynamic analyses. Set to -1 to disable baseline correction, or use 0, 1, 2 or 3.   '''
        return int(self.nfrest('GET','/op/opt/baseline'))
    @baselineGrade.setter
    def baselineGrade(self,value):
        '''   Get or set the degree of the baseline correction function for dynamic analyses. Set to -1 to disable baseline correction, or use 0, 1, 2 or 3.   '''
        self.nfrest('POST','/op/opt/baseline', heads={'val':str(value)})
    @property
    def binFolder(self):
        '''   Get or set binary folder for NextFEM API - this will affect only design data (materials, translations, etc.)   '''
        return self.nfrest('GET','/op/opt/binfolder')
    @binFolder.setter
    def binFolder(self,value):
        '''   Get or set binary folder for NextFEM API - this will affect only design data (materials, translations, etc.)   '''
        self.nfrest('POST','/op/opt/binfolder', heads={'val':str(value)})
    @property
    def bordersColor(self):
        '''   Change color for borders in extruded view   '''
        return int(self.nfrest('GET','/model/colors/border'))
    @bordersColor.setter
    def bordersColor(self,value):
        '''   Change color for borders in extruded view   '''
        self.nfrest('POST','/model/colors/border', heads={'val':str(value)})
    @property
    def constraintsColor(self):
        '''   Change color for constraints   '''
        return int(self.nfrest('GET','/model/colors/constraint'))
    @constraintsColor.setter
    def constraintsColor(self,value):
        '''   Change color for constraints   '''
        self.nfrest('POST','/model/colors/constraint', heads={'val':str(value)})
    @property
    def defSolverType(self):
        '''   Get the system of equation type in standard solver. The property is read-only, use changeDefSolverType to modify it   '''
        return int(self.nfrest('GET','/op/opt/defsolvertype'))
    @property
    def designMaterialsID(self)->list:
        '''   Get the list of design material IDs   '''
        return json.loads(self.nfrest('GET','/designmaterials'))
    @property
    def DocXfontSize(self):
        '''   Change font size for DocX reporting tool. Default is 8   '''
        return int(self.nfrest('GET','/op/docx/fontsize'))
    @DocXfontSize.setter
    def DocXfontSize(self,value):
        '''   Change font size for DocX reporting tool. Default is 8   '''
        self.nfrest('POST','/op/docx/fontsize', heads={'val':str(value)})
    @property
    def DocXtableAlignment(self):
        '''   Change table aligment: 0=left, 1=center, 2=right, 3=justified. Default is 1   '''
        return int(self.nfrest('GET','/op/docx/tablealign'))
    @DocXtableAlignment.setter
    def DocXtableAlignment(self,value):
        '''   Change table aligment: 0=left, 1=center, 2=right, 3=justified. Default is 1   '''
        self.nfrest('POST','/op/docx/tablealign', heads={'val':str(value)})
    @property
    def DocXtableBorders(self)->list:
        '''   Change table borders: True=border present, False=no border. Default is True for all sides.   '''
        return json.loads(self.nfrest('GET','/op/docx/tableborders'))
    @DocXtableBorders.setter
    def DocXtableBorders(self,value:list):
        '''   Change table borders: True=border present, False=no border. Default is True for all sides.   '''
        self.nfrest('POST','/op/docx/tableborders', heads={'val':str(value)})
    @property
    def DocXtableFitting(self):
        '''   Change table fitting: True=Page, False=Content. Default is False.   '''
        return sbool(self.nfrest('GET','/op/docx/tablefit'))
    @DocXtableFitting.setter
    def DocXtableFitting(self,value):
        '''   Change table fitting: True=Page, False=Content. Default is False.   '''
        self.nfrest('POST','/op/docx/tablefit', heads={'val':str(value)})
    @property
    def DocXtableFontSize(self):
        '''   Change table font size for DocX reporting tool. Default is 6   '''
        return int(self.nfrest('GET','/op/docx/tablefontsize'))
    @DocXtableFontSize.setter
    def DocXtableFontSize(self,value):
        '''   Change table font size for DocX reporting tool. Default is 6   '''
        self.nfrest('POST','/op/docx/tablefontsize', heads={'val':str(value)})
    @property
    def dontDeleteChecks(self):
        '''   Set if checking results can be deleted or not.   '''
        return sbool(self.nfrest('GET','/res/donotdeletechecks'))
    @dontDeleteChecks.setter
    def dontDeleteChecks(self,value):
        '''   Set if checking results can be deleted or not.   '''
        self.nfrest('POST','/res/donotdeletechecks', heads={'val':str(value)})
    @property
    def dontDeleteResults(self):
        '''   Set if results can be deleted or not.   '''
        return sbool(self.nfrest('GET','/res/donotdelete'))
    @dontDeleteResults.setter
    def dontDeleteResults(self,value):
        '''   Set if results can be deleted or not.   '''
        self.nfrest('POST','/res/donotdelete', heads={'val':str(value)})
    @property
    def DXFoptions(self):
        '''   Get or set a JSON string containing options for DXF export of RC beams and members   '''
        return self.nfrest('GET','/op/opt/dxfoptions')
    @DXFoptions.setter
    def DXFoptions(self,value):
        '''   Get or set a JSON string containing options for DXF export of RC beams and members   '''
        self.nfrest('POST','/op/opt/dxfoptions', heads={'val':str(value)})
    @property
    def elemsList(self)->list:
        '''   Get the list of element numbers   '''
        return json.loads(self.nfrest('GET','/elements'))
    @property
    def elemsNumber(self):
        '''   Get the number of elements in the model   '''
        return self.nfrest('GET','/elements/number')
    @property
    def elemTextColor(self):
        '''   Change color for element text   '''
        return int(self.nfrest('GET','/model/colors/elemtext'))
    @elemTextColor.setter
    def elemTextColor(self,value):
        '''   Change color for element text   '''
        self.nfrest('POST','/model/colors/elemtext', heads={'val':str(value)})
    @property
    def envName(self):
        '''   Return the name of checking envelope   '''
        return self.nfrest('GET','/model/env')
    @property
    def hingesColor(self):
        '''   Change color for hinges   '''
        return int(self.nfrest('GET','/model/colors/hinge'))
    @hingesColor.setter
    def hingesColor(self,value):
        '''   Change color for hinges   '''
        self.nfrest('POST','/model/colors/hinge', heads={'val':str(value)})
    @property
    def IFC_format(self):
        '''   Set 0 for IFC4, 1 for IFC2x3   '''
        return int(self.nfrest('GET','/op/opt/ifcformat'))
    @IFC_format.setter
    def IFC_format(self,value):
        '''   Set 0 for IFC4, 1 for IFC2x3   '''
        self.nfrest('POST','/op/opt/ifcformat', heads={'val':str(value)})
    @property
    def IFC_includeAnalyticalModel(self):
        '''   Set whether or not to include analytical model in IFC export   '''
        return sbool(self.nfrest('GET','/op/opt/ifcanalytical'))
    @IFC_includeAnalyticalModel.setter
    def IFC_includeAnalyticalModel(self,value):
        '''   Set whether or not to include analytical model in IFC export   '''
        self.nfrest('POST','/op/opt/ifcanalytical', heads={'val':str(value)})
    @property
    def IFC_WallMeshSize(self):
        '''   Set or get mesh size for meshing walls in IFC import, in millimeters   '''
        return float(self.nfrest('GET','/op/opt/ifcwallmeshsize'))
    @IFC_WallMeshSize.setter
    def IFC_WallMeshSize(self,value):
        '''   Set or get mesh size for meshing walls in IFC import, in millimeters   '''
        self.nfrest('POST','/op/opt/ifcwallmeshsize', heads={'val':str(value)})
    @property
    def isRemote(self):
        '''   True if this API instance is redirected to a remote server   '''
        return sbool(self.nfrest('GET','na'))
    @property
    def lineColor(self):
        '''   Change color for lines   '''
        return int(self.nfrest('GET','/model/colors/line'))
    @lineColor.setter
    def lineColor(self,value):
        '''   Change color for lines   '''
        self.nfrest('POST','/model/colors/line', heads={'val':str(value)})
    @property
    def loading(self):
        '''   Readonly property for API loading   '''
        return sbool(self.nfrest('GET',''))
    @property
    def massColor(self):
        '''   Change color for mass   '''
        return int(self.nfrest('GET','/model/colors/mass'))
    @massColor.setter
    def massColor(self,value):
        '''   Change color for mass   '''
        self.nfrest('POST','/model/colors/mass', heads={'val':str(value)})
    @property
    def materialsID(self)->list:
        '''   Get the list of material IDs   '''
        return json.loads(self.nfrest('GET','/materials'))
    @property
    def modeldata(self):
        '''   Model in JSON format   '''
        return self.nfrest('GET','/model/data')
    @modeldata.setter
    def modeldata(self,value):
        '''   Model in JSON format   '''
        self.nfrest('POST','/model/data',value)
    @property
    def modelName(self):
        '''   Name of the model. To be set prior to launch to have properly-named temporary files.   '''
        return self.nfrest('GET','/model')
    @modelName.setter
    def modelName(self,value):
        '''   Name of the model. To be set prior to launch to have properly-named temporary files.   '''
        self.nfrest('POST','/model', heads={'val':str(value)})
    @property
    def modelPath(self):
        '''   Return the full path of the currently opened file   '''
        return self.nfrest('GET','/model/path')
    @property
    def modelresults(self):
        '''   Results in JSON format   '''
        return self.nfrest('GET','/model/results')
    @modelresults.setter
    def modelresults(self,value):
        '''   Results in JSON format   '''
        self.nfrest('POST','/model/results',value)
    @property
    def nodeColor(self):
        '''   Change color for nodes   '''
        return int(self.nfrest('GET','/model/colors/node'))
    @nodeColor.setter
    def nodeColor(self,value):
        '''   Change color for nodes   '''
        self.nfrest('POST','/model/colors/node', heads={'val':str(value)})
    @property
    def nodesList(self)->list:
        '''   Get the list of node numbers   '''
        return json.loads(self.nfrest('GET','/nodes'))
    @property
    def nodesNumber(self):
        '''   Get the number of nodes in the model   '''
        return self.nfrest('GET','/nodes/number')
    @property
    def nodeTextColor(self):
        '''   Change color for node text   '''
        return int(self.nfrest('GET','/model/colors/nodetext'))
    @nodeTextColor.setter
    def nodeTextColor(self,value):
        '''   Change color for node text   '''
        self.nfrest('POST','/model/colors/nodetext', heads={'val':str(value)})
    @property
    def numberFormat(self):
        '''   Get or set the format for printing numbers in output of some functions (e.g. getNodeInfo, getElementInfo)   '''
        return self.nfrest('GET','/op/opt/numberformat')
    @numberFormat.setter
    def numberFormat(self,value):
        '''   Get or set the format for printing numbers in output of some functions (e.g. getNodeInfo, getElementInfo)   '''
        self.nfrest('POST','/op/opt/numberformat', heads={'val':str(value)})
    @property
    def OS_beamWithHingesOption(self):
        '''   Get or set flag for using beamWithHinges instead of forceBeamColumn in OpenSees fiber models   '''
        return sbool(self.nfrest('GET','/op/opt/os/beamwithhinges'))
    @OS_beamWithHingesOption.setter
    def OS_beamWithHingesOption(self,value):
        '''   Get or set flag for using beamWithHinges instead of forceBeamColumn in OpenSees fiber models   '''
        self.nfrest('POST','/op/opt/os/beamwithhinges', heads={'val':str(value)})
    @property
    def OS_concreteTensileStrength(self):
        '''   Get or set flag for using or not the tensile strength in concrete for fiber sections   '''
        return sbool(self.nfrest('GET','/op/opt/os/tensilesrc'))
    @OS_concreteTensileStrength.setter
    def OS_concreteTensileStrength(self,value):
        '''   Get or set flag for using or not the tensile strength in concrete for fiber sections   '''
        self.nfrest('POST','/op/opt/os/tensilesrc', heads={'val':str(value)})
    @property
    def OS_IntegrationPointsOption(self):
        '''   Get or set number of integration points in OpenSees fiber models   '''
        return int(self.nfrest('GET','/op/opt/os/intpoints'))
    @OS_IntegrationPointsOption.setter
    def OS_IntegrationPointsOption(self,value):
        '''   Get or set number of integration points in OpenSees fiber models   '''
        self.nfrest('POST','/op/opt/os/intpoints', heads={'val':str(value)})
    @property
    def OS_NDfiberSectionsOption(self):
        '''   Get or set flag for using NDFiber sections in OpenSees fiber models   '''
        return sbool(self.nfrest('GET','/op/opt/os/ndfibersects'))
    @OS_NDfiberSectionsOption.setter
    def OS_NDfiberSectionsOption(self,value):
        '''   Get or set flag for using NDFiber sections in OpenSees fiber models   '''
        self.nfrest('POST','/op/opt/os/ndfibersects', heads={'val':str(value)})
    @property
    def OS_saveStateVariables(self):
        '''   Get or set flag for saving state variables in OpenSees analysis   '''
        return sbool(self.nfrest('GET','/op/opt/os/statevars'))
    @OS_saveStateVariables.setter
    def OS_saveStateVariables(self,value):
        '''   Get or set flag for saving state variables in OpenSees analysis   '''
        self.nfrest('POST','/op/opt/os/statevars', heads={'val':str(value)})
    @property
    def releasesColor(self):
        '''   Change color for releases   '''
        return int(self.nfrest('GET','/model/colors/release'))
    @releasesColor.setter
    def releasesColor(self,value):
        '''   Change color for releases   '''
        self.nfrest('POST','/model/colors/release', heads={'val':str(value)})
    @property
    def resCalc_accuracy(self):
        '''   Get or set section calculation accuracy in Section Analyzer (from 10 to 1000)   '''
        return int(self.nfrest('GET','/op/opt/calcaccuracy'))
    @resCalc_accuracy.setter
    def resCalc_accuracy(self,value):
        '''   Get or set section calculation accuracy in Section Analyzer (from 10 to 1000)   '''
        self.nfrest('POST','/op/opt/calcaccuracy', heads={'val':str(value)})
    @property
    def resCalc_cacheEnabled(self):
        '''   Enable or disable section calculation cache. Enabled by default.   '''
        return sbool(self.nfrest('GET','/op/opt/rescalc/cacheenabled'))
    @resCalc_cacheEnabled.setter
    def resCalc_cacheEnabled(self,value):
        '''   Enable or disable section calculation cache. Enabled by default.   '''
        self.nfrest('POST','/op/opt/rescalc/cacheenabled', heads={'val':str(value)})
    @property
    def resCalc_cacheSize(self):
        '''   Get or set the cache size for storing section calculations   '''
        return int(self.nfrest('GET','/op/opt/calcusefibers'))
    @resCalc_cacheSize.setter
    def resCalc_cacheSize(self,value):
        '''   Get or set the cache size for storing section calculations   '''
        self.nfrest('POST','/op/opt/calcusefibers', heads={'val':str(value)})
    @property
    def resCalc_concreteBehaviour(self):
        '''   Set concrete law for strength calculation: 0 parabola-rectangle, 1 bilinear, 2 confined   '''
        return int(self.nfrest('GET','/op/opt/rescalc/concbeh'))
    @resCalc_concreteBehaviour.setter
    def resCalc_concreteBehaviour(self,value):
        '''   Set concrete law for strength calculation: 0 parabola-rectangle, 1 bilinear, 2 confined   '''
        self.nfrest('POST','/op/opt/rescalc/concbeh', heads={'val':str(value)})
    @property
    def resCalc_domainCorrectionType(self):
        '''   Set the type of resisting domain correction (0,1,2,3) - contact NextFEM Support to change this   '''
        return int(self.nfrest('GET','/op/opt/rescalc/domcorr'))
    @resCalc_domainCorrectionType.setter
    def resCalc_domainCorrectionType(self,value):
        '''   Set the type of resisting domain correction (0,1,2,3) - contact NextFEM Support to change this   '''
        self.nfrest('POST','/op/opt/rescalc/domcorr', heads={'val':str(value)})
    @property
    def resCalc_elasticTolerance(self):
        '''   Tolerance for elastic strength calculation of a section   '''
        return float(self.nfrest('GET','/op/opt/rescalc/eltoll'))
    @resCalc_elasticTolerance.setter
    def resCalc_elasticTolerance(self,value):
        '''   Tolerance for elastic strength calculation of a section   '''
        self.nfrest('POST','/op/opt/rescalc/eltoll', heads={'val':str(value)})
    @property
    def resCalc_getAllJSONresults(self):
        '''   Get or set a flag to get all results in JSON from getSectionResMoments method   '''
        return sbool(self.nfrest('GET','/op/opt/rescalc/allresjson'))
    @resCalc_getAllJSONresults.setter
    def resCalc_getAllJSONresults(self,value):
        '''   Get or set a flag to get all results in JSON from getSectionResMoments method   '''
        self.nfrest('POST','/op/opt/rescalc/allresjson', heads={'val':str(value)})
    @property
    def resCalc_homogBarsFactor(self):
        '''   Set custom homogenization factor for bars in concrete sections   '''
        return int(self.nfrest('GET','/op/opt/rescalc/homog'))
    @resCalc_homogBarsFactor.setter
    def resCalc_homogBarsFactor(self,value):
        '''   Set custom homogenization factor for bars in concrete sections   '''
        self.nfrest('POST','/op/opt/rescalc/homog', heads={'val':str(value)})
    @property
    def resCalc_kMod(self):
        '''   Set kmod factor for strength calculation of timber sections   '''
        return float(self.nfrest('GET','/op/opt/rescalc/kmod'))
    @resCalc_kMod.setter
    def resCalc_kMod(self,value):
        '''   Set kmod factor for strength calculation of timber sections   '''
        self.nfrest('POST','/op/opt/rescalc/kmod', heads={'val':str(value)})
    @property
    def resCalc_rebarHardeningRatio(self):
        '''   Hardening ratio for rebar bilinear behaviour   '''
        return float(self.nfrest('GET','/op/opt/rescalc/rebhard'))
    @resCalc_rebarHardeningRatio.setter
    def resCalc_rebarHardeningRatio(self,value):
        '''   Hardening ratio for rebar bilinear behaviour   '''
        self.nfrest('POST','/op/opt/rescalc/rebhard', heads={'val':str(value)})
    @property
    def resCalc_refinement(self):
        '''   Get or set the refinement in resistance calculation domain (e.g. more domain points in the zone of interest)   '''
        return sbool(self.nfrest('GET','/op/opt/calcrefinement'))
    @resCalc_refinement.setter
    def resCalc_refinement(self,value):
        '''   Get or set the refinement in resistance calculation domain (e.g. more domain points in the zone of interest)   '''
        self.nfrest('POST','/op/opt/calcrefinement', heads={'val':str(value)})
    @property
    def resCalc_resDomainSlices(self):
        '''   Set number of domain slices in sectional strength calculation   '''
        return int(self.nfrest('GET','/op/opt/rescalc/domainslices'))
    @resCalc_resDomainSlices.setter
    def resCalc_resDomainSlices(self,value):
        '''   Set number of domain slices in sectional strength calculation   '''
        self.nfrest('POST','/op/opt/rescalc/domainslices', heads={'val':str(value)})
    @property
    def resCalc_responseInTension(self):
        '''   Set response in tension for concrete sections in strength calculation   '''
        return sbool(self.nfrest('GET','/op/opt/rescalc/tensresp'))
    @resCalc_responseInTension.setter
    def resCalc_responseInTension(self,value):
        '''   Set response in tension for concrete sections in strength calculation   '''
        self.nfrest('POST','/op/opt/rescalc/tensresp', heads={'val':str(value)})
    @property
    def resCalc_steelClass(self):
        '''   Set the class for steel section in strength calculation (1, 2, 3, 4)   '''
        return int(self.nfrest('GET','/op/opt/rescalc/steelclass'))
    @resCalc_steelClass.setter
    def resCalc_steelClass(self,value):
        '''   Set the class for steel section in strength calculation (1, 2, 3, 4)   '''
        self.nfrest('POST','/op/opt/rescalc/steelclass', heads={'val':str(value)})
    @property
    def resCalc_strandHardeningRatio(self):
        '''   Hardening ratio for strand bilinear behaviour   '''
        return float(self.nfrest('GET','/op/opt/rescalc/strhard'))
    @resCalc_strandHardeningRatio.setter
    def resCalc_strandHardeningRatio(self,value):
        '''   Hardening ratio for strand bilinear behaviour   '''
        self.nfrest('POST','/op/opt/rescalc/strhard', heads={'val':str(value)})
    @property
    def resCalc_useFibers(self):
        '''   Get or set if fibers are used in section calculation (True or False)   '''
        return sbool(self.nfrest('GET','/op/opt/calcusefibers'))
    @resCalc_useFibers.setter
    def resCalc_useFibers(self,value):
        '''   Get or set if fibers are used in section calculation (True or False)   '''
        self.nfrest('POST','/op/opt/calcusefibers', heads={'val':str(value)})
    @property
    def restraintsColor(self):
        '''   Change color for restraints   '''
        return int(self.nfrest('GET','/model/colors/restraint'))
    @restraintsColor.setter
    def restraintsColor(self,value):
        '''   Change color for restraints   '''
        self.nfrest('POST','/model/colors/restraint', heads={'val':str(value)})
    @property
    def saveStateVariables(self):
        '''   Get or set flag for saving state variables in NXF file   '''
        return sbool(self.nfrest('GET','/op/opt/os/statevars'))
    @saveStateVariables.setter
    def saveStateVariables(self,value):
        '''   Get or set flag for saving state variables in NXF file   '''
        self.nfrest('POST','/op/opt/os/statevars', heads={'val':str(value)})
    @property
    def sectionsID(self)->list:
        '''   Get the list of section IDs   '''
        return json.loads(self.nfrest('GET','/sections'))
    @property
    def selAreaColor(self):
        '''   Change color for selected areas   '''
        return int(self.nfrest('GET','/model/colors/selarea'))
    @selAreaColor.setter
    def selAreaColor(self,value):
        '''   Change color for selected areas   '''
        self.nfrest('POST','/model/colors/selarea', heads={'val':str(value)})
    @property
    def selectedElements(self)->list:
        '''   Get or set selected elements in viewport. REST version only against local instance of NextFEM Designer   '''
        return json.loads(self.nfrest('GET','/op/selectedelements'))
    @selectedElements.setter
    def selectedElements(self,value:list):
        '''   Get or set selected elements in viewport. REST version only against local instance of NextFEM Designer   '''
        self.nfrest('POST','/op/selectedelements', heads={'val':str(value)})
    @property
    def selectedNodes(self)->list:
        '''   Get or set selected nodes in viewport. REST version only against local instance of NextFEM Designer   '''
        return json.loads(self.nfrest('GET','/op/selectednodes'))
    @selectedNodes.setter
    def selectedNodes(self,value:list):
        '''   Get or set selected nodes in viewport. REST version only against local instance of NextFEM Designer   '''
        self.nfrest('POST','/op/selectednodes', heads={'val':str(value)})
    @property
    def selLineColor(self):
        '''   Change color for selected lines   '''
        return int(self.nfrest('GET','/model/colors/selline'))
    @selLineColor.setter
    def selLineColor(self,value):
        '''   Change color for selected lines   '''
        self.nfrest('POST','/model/colors/selline', heads={'val':str(value)})
    @property
    def selNodeColor(self):
        '''   Change color for selected nodes   '''
        return int(self.nfrest('GET','/model/colors/selnode'))
    @selNodeColor.setter
    def selNodeColor(self,value):
        '''   Change color for selected nodes   '''
        self.nfrest('POST','/model/colors/selnode', heads={'val':str(value)})
    @property
    def selSolidColor(self):
        '''   Change color for selected solids   '''
        return int(self.nfrest('GET','/model/colors/selsolid'))
    @selSolidColor.setter
    def selSolidColor(self,value):
        '''   Change color for selected solids   '''
        self.nfrest('POST','/model/colors/selsolid', heads={'val':str(value)})
    @property
    def selSpringColor(self):
        '''   Change color for selected springs   '''
        return int(self.nfrest('GET','/model/colors/node'))
    @selSpringColor.setter
    def selSpringColor(self,value):
        '''   Change color for selected springs   '''
        self.nfrest('POST','/model/colors/node', heads={'val':str(value)})
    @property
    def solidColor(self):
        '''   Change color for solids   '''
        return int(self.nfrest('GET','/model/colors/solid'))
    @solidColor.setter
    def solidColor(self,value):
        '''   Change color for solids   '''
        self.nfrest('POST','/model/colors/solid', heads={'val':str(value)})
    @property
    def solverType(self):
        '''   Get current solver type. The property is read-only, use changeSolver to modify it   '''
        return int(self.nfrest('GET','/op/opt/solvertype'))
    @property
    def springColor(self):
        '''   Change color for springs   '''
        return int(self.nfrest('GET','/model/colors/spring'))
    @springColor.setter
    def springColor(self,value):
        '''   Change color for springs   '''
        self.nfrest('POST','/model/colors/spring', heads={'val':str(value)})
    @property
    def tempFolder(self):
        '''   Get or set the temporary folder.   '''
        return self.nfrest('GET','/op/opt/tempfolder')
    @tempFolder.setter
    def tempFolder(self,value):
        '''   Get or set the temporary folder.   '''
        self.nfrest('POST','/op/opt/tempfolder', heads={'val':str(value)})
    @property
    def textColor(self):
        '''   Change color for text   '''
        return int(self.nfrest('GET','/model/colors/text'))
    @textColor.setter
    def textColor(self,value):
        '''   Change color for text   '''
        self.nfrest('POST','/model/colors/text', heads={'val':str(value)})
    @property
    def useFastEigensolver(self):
        '''   Get or set flag for using fast eigensolver   '''
        return sbool(self.nfrest('GET','/op/opt/os/fasteigen'))
    @useFastEigensolver.setter
    def useFastEigensolver(self,value):
        '''   Get or set flag for using fast eigensolver   '''
        self.nfrest('POST','/op/opt/os/fasteigen', heads={'val':str(value)})
    @property
    def WallMeshSize(self):
        '''   Set or get mesh size for meshing areas in the model, in millimeters   '''
        return float(self.nfrest('GET','/op/opt/wallmeshsize'))
    @WallMeshSize.setter
    def WallMeshSize(self,value):
        '''   Set or get mesh size for meshing areas in the model, in millimeters   '''
        self.nfrest('POST','/op/opt/wallmeshsize', heads={'val':str(value)})
