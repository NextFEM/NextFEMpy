import requests,json,urllib

def sbool(arg):
    if arg=="True":
        return True
    else:
        return False

def qt(s):
    return urllib.parse.quote(s, safe='')

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
        if not(headersDict is None):
            for dd in headersDict:
                self.headers[dd]=headersDict[dd]

    def nfrest(self, method, command, body=None, heads=None):
        url = self.baseUrl + command
        if method == "POST":
            response = requests.post(url=url, headers=self.headers, json=body)
        elif method == "PUT":
            response = requests.put(url=url, headers=self.headers, json=body)
        elif method == "GET":
            response = requests.get(url=url, headers=self.headers)
        elif method == "DELETE":
            response = requests.delete(url=url, headers=self.headers)
        # print request and return response
        if self.msg: print("*** " + self.user + " :: " + method, command, response.status_code)
        return response.text

    def nfrestB(self, method, command, body=None, heads=None):
        # return bytes
        url = self.baseUrl + command
        if method == "POST":
            response = requests.post(url=url, headers=self.headers, json=body)
        elif method == "PUT":
            response = requests.put(url=url, headers=self.headers, json=body)
        elif method == "GET":
            response = requests.get(url=url, headers=self.headers)
        elif method == "DELETE":
            response = requests.delete(url=url, headers=self.headers)
        return response.content

    # methods and properties for Server
    def saveUser(self): return bool(self.nfrest('GET', '/op/saveuser')); # save model on server
    def userFile(self, filename, localPath):
        # get file from server, return bytes
        bts=self.nfrestB('GET', '/op/userfile', None, dict([("path",filename)]))
        if bts==b'False': 
            return False
        with open(localPath, "wb") as binary_file:
            binary_file.write(bts)
        return True

    # methods and properties
    def activeBarsDiameters(self): return json.loads(self.nfrest('GET', '/element/rebar/barsdiam', None, None))
    def activeHoopsDiameters(self): return json.loads(self.nfrest('GET', '/element/rebar/hoopsdiam', None, None))
    def addBeam(self, n1, n2, sect=0, mat=0, sect2=0): return self.nfrest('GET', '/element/add/beam/'+qt(n1)+'/'+qt(n2)+'/'+str(sect)+'/'+str(mat)+'/'+str(sect2)+'', None, None)
    def addBeamLoad(self, elem, value1, value2, position1, position2, direction, loadcase, local=False): return sbool(self.nfrest('GET', '/load/element/beamadd/'+qt(elem)+'/'+str(value1)+'/'+str(value2)+'/'+str(position1)+'/'+str(position2)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', None, None))
    def addBeamLoad(self, elem, values, positions, direction, loadcase, local=False): return sbool(self.nfrest('GET', '/load/element/beamaddA/'+qt(elem)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', None, dict([("values",json.dumps(values)),("positions",json.dumps(positions))])))
    def addBeamLoadU(self, elem, value, direction, loadcase, local=False): return sbool(self.nfrest('GET', '/load/element/beamaddU/'+qt(elem)+'/'+str(value)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', None, None))
    def addBoxSection(self, Lz, Ly, tw, tf1, tf2): return int(self.nfrest('GET', '/section/add/box/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(tf2)+'', None, None))
    def addCircleInSection(self, sectionID, diameter, centerX, centerY, isEmpty=False, material=0, doNotCenter=False): return sbool(self.nfrest('GET', '/section/add/addcirc/'+str(sectionID)+'/'+str(diameter)+'/'+str(centerX)+'/'+str(centerY)+'/'+str(isEmpty)+'/'+str(material)+'/'+str(doNotCenter)+'', None, None))
    def addCircSection(self, D): return int(self.nfrest('GET', '/section/add/circ/'+str(D)+'', None, None))
    def addCSection(self, Lz, Ly, tw, tf1, tf2, Lz2=0): return int(self.nfrest('GET', '/section/add/cshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(tf2)+'/'+str(Lz2)+'', None, None))
    def addDCSection(self, Lz, Ly, tw, tf1, tf2, gap, Lz2=0): return int(self.nfrest('GET', '/section/add/doublecshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(tf2)+'/'+str(gap)+'/'+str(Lz2)+'', None, None))
    def addDesignMatFromLib(self, name): return int(self.nfrest('POST', '/designmaterial/add/fromlib', name, None))
    def addDesMaterial(self, name, E, fk, ni=0, type=0): return int(self.nfrest('GET', '/material/add/des/'+qt(name)+'/'+str(E)+'/'+str(fk)+'/'+str(ni)+'/'+str(type)+'', None, None))
    def addDLSection(self, Lz, Ly, tw, tf1, gap): return int(self.nfrest('GET', '/section/add/doublelshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(gap)+'', None, None))
    def addDTSection(self, Lz, Ly, tw, tf1, tf2, Lz2=0): return int(self.nfrest('GET', '/section/add/dtshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'/'+str(tf2)+'/'+str(Lz2)+'', None, None))
    def addEC8spectrum(self, ag, q, LS, damping=0.05, soilType='A', type1=True): return int(self.nfrest('GET', '/function/ec8spectrum/'+str(ag)+'/'+str(q)+'/'+qt(LS)+'/'+str(damping)+'/'+qt(soilType)+'/'+str(type1)+'', None, None))
    def addEdgeLoad(self, elem, values, edge, direction, loadcase, local=False): return sbool(self.nfrest('POST', '/load/element/edgeadd/'+qt(elem)+'/'+str(edge)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', values, None))
    def addFillInSection(self, sectionID, x, y, material=0, doNotCenter=False): return sbool(self.nfrest('GET', '/section/add/fill/'+str(sectionID)+'/'+str(material)+'/'+str(doNotCenter)+'', None, dict([("x",json.dumps(x)),("y",json.dumps(y))])))
    def addFloorPlane(self, name, type, n1, n2, n3, n4=''): return sbool(self.nfrest('GET', '/load/floor/planeadd/'+qt(name)+'/'+str(type)+'/'+qt(n1)+'/'+qt(n2)+'/'+qt(n3)+'/'+qt(n4)+'', None, None))
    def addGroup(self, name): return sbool(self.nfrest('GET', '/group/add/'+qt(name)+'', None, None))
    def addHoleInSection(self, sectionID, x, y, material=0, doNotCenter=False): return sbool(self.nfrest('GET', '/section/add/hole/'+str(sectionID)+'/'+str(material)+'/'+str(doNotCenter)+'', None, dict([("x",json.dumps(x)),("y",json.dumps(y))])))
    def addIsoMaterial(self, name, E, ni, Wden, fk=0, conductivity=0, specificHeat=0, type=0): return int(self.nfrest('GET', '/material/add/iso/'+qt(name)+'/'+str(E)+'/'+str(ni)+'/'+str(Wden)+'/'+str(fk)+'/'+str(conductivity)+'/'+str(specificHeat)+'/'+str(type)+'', None, None))
    def addLayeredPlanarSection(self, layerThicknesses, layerMaterials): return int(self.nfrest('GET', '/section/add/layeredplanar', None, dict([("layerThicknesses",json.dumps(layerThicknesses)),("layerMaterials",json.dumps(layerMaterials))])))
    def addLoadCase(self, name): return sbool(self.nfrest('GET', '/loadcase/add/'+qt(name)+'', None, None))
    def addLoadCaseToCombination(self, name, loadcase, factor): return sbool(self.nfrest('GET', '/loadcase/combo/add/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'', None, None))
    def addLoadCaseToTimeHistoryAnalysis(self, name, loadcase, factor, THid=-1): return sbool(self.nfrest('GET', '/loadcase/combo/addth/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'/'+str(THid)+'', None, None))
    def addLongitRebar(self, elem, X, Y, area, matID, Linit, Lfin, rectBase=0, strandTens=0): return sbool(self.nfrest('GET', '/element/rebar/long/'+qt(elem)+'/'+str(X)+'/'+str(Y)+'/'+str(area)+'/'+str(matID)+'/'+str(Linit)+'/'+str(Lfin)+'/'+str(rectBase)+'/'+str(strandTens)+'', None, None))
    def addLongitRebarInSection(self, sectionID, X, Y, area, matID, rectBase=0, strandTens=0): return sbool(self.nfrest('GET', '/section/rebar/long/'+qt(sectionID)+'/'+str(X)+'/'+str(Y)+'/'+str(area)+'/'+str(matID)+'/'+str(rectBase)+'/'+str(strandTens)+'', None, None))
    def addLongitRebarInSection(self, sectionID, X, Y, area, matID, rectBase=0, strandTens=0): return sbool(self.nfrest('GET', '/section/rebar/long/'+str(sectionID)+'/'+str(X)+'/'+str(Y)+'/'+str(area)+'/'+str(matID)+'/'+str(rectBase)+'/'+str(strandTens)+'', None, None))
    def addLSection(self, Lz, Ly, tw, tf1): return int(self.nfrest('GET', '/section/add/lshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'', None, None))
    def addMatFromLib(self, name): return int(self.nfrest('POST', '/material/add/fromlib', name, None))
    def addMember(self, elems): return sbool(self.nfrest('GET', '/model/member/add', None, dict([("elems",json.dumps(elems))])))
    def addMeshedWall(self, ID, origX, origY, origZ, div1, div2, plan, leng, hei, angle=0, tilt='0', nodeOffset=10000, isHorizontal=False): return json.loads(self.nfrest('GET', '/op/mesh/addmeshedwall/'+str(ID)+'/'+str(origX)+'/'+str(origY)+'/'+str(origZ)+'/'+str(div1)+'/'+str(div2)+'/'+qt(plan)+'/'+str(leng)+'/'+str(hei)+'/'+str(angle)+'/'+qt(tilt)+'/'+str(nodeOffset)+'/'+str(isHorizontal)+'', None, None))
    def addNodalDisp(self, node, disp, direction, loadcase): return sbool(self.nfrest('GET', '/load/node/disp/'+qt(node)+'/'+str(disp)+'/'+str(direction)+'/'+qt(loadcase)+'', None, None))
    def addNodalLoad(self, node, value, direction, loadcase, local=False): return sbool(self.nfrest('GET', '/load/node/add/'+qt(node)+'/'+str(value)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', None, None))
    def addNodalMass(self, ID, tmx, tmy, tmz, rmx, rmy, rmz): return sbool(self.nfrest('GET', '/mass/add/'+qt(ID)+'/'+str(tmx)+'/'+str(tmy)+'/'+str(tmz)+'/'+str(rmx)+'/'+str(rmy)+'/'+str(rmz)+'', None, None))
    def addNodalSpring(self, n1, propName): return self.nfrest('GET', '/element/add/nodalspring/'+qt(n1)+'/'+qt(propName)+'', None, None)
    def addNode(self, x, y, z, lcs1X=0, lcs1Y=0, lcs1Z=0, lcs2X=0, lcs2Y=0, lcs2Z=0): return self.nfrest('GET', '/node/add/'+str(x)+'/'+str(y)+'/'+str(z)+'/'+str(lcs1X)+'/'+str(lcs1Y)+'/'+str(lcs1Z)+'/'+str(lcs2X)+'/'+str(lcs2Y)+'/'+str(lcs2Z)+'', None, None)
    def addNodeWithID(self, x, y, z, ID): return sbool(self.nfrest('GET', '/node/add/'+str(x)+'/'+str(y)+'/'+str(z)+'/'+qt(ID)+'', None, None))
    def addNormalhinge(self, name, checkType, position, includeShear=False, includeTorsion=False, cKpl=0.001, FresRatio=0.2): return sbool(self.nfrest('GET', '/hinge/add/simple/'+qt(name)+'/'+qt(checkType)+'/'+str(position)+'/'+str(includeShear)+'/'+str(includeTorsion)+'/'+str(cKpl)+'/'+str(FresRatio)+'', None, None))
    def addNTCspectrum(self, lat, lon, LS, soil, Vr, St, hh=1, q0=1, isHregular=False, damping=0.05, customAg=0, VerticalComponent=False): return int(self.nfrest('GET', '/function/ntcspectrum/'+str(lat)+'/'+str(lon)+'/'+qt(LS)+'/'+qt(soil)+'/'+str(Vr)+'/'+str(St)+'/'+str(hh)+'/'+str(q0)+'/'+str(isHregular)+'/'+str(damping)+'/'+str(customAg)+'/'+str(VerticalComponent)+'', None, None))
    def addNVMhinge(self, name, checkType, position, includeShear=False, includeTorsion=False, cKpl=0.001, FresRatio=0.2, stopResidualBranch=False): return sbool(self.nfrest('GET', '/hinge/add/nvm/'+qt(name)+'/'+qt(checkType)+'/'+str(position)+'/'+str(includeShear)+'/'+str(includeTorsion)+'/'+str(cKpl)+'/'+str(FresRatio)+'/'+str(stopResidualBranch)+'', None, None))
    def addObject(self, o, other=0): return sbool(self.nfrest('POST', '/model/addobject/'+str(other)+'', o, None))
    def addOmegaSection(self, Lz, Ly, tw, d): return int(self.nfrest('GET', '/section/add/omega/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(d)+'', None, None))
    def addOrChangeDesMaterialProperty(self, ID, name, value, units=''): return sbool(self.nfrest('POST', '/designmaterial/prop/'+str(ID)+'/'+qt(name)+'/'+qt(value)+'/'+qt(units)+'', None, None))
    def addOrChangeMaterialProperty(self, ID, name, value, units=''): return sbool(self.nfrest('POST', '/material/prop/'+str(ID)+'/'+qt(name)+'/'+qt(value)+'/'+qt(units)+'', None, None))
    def addOrModifyCustomData(self, key, value): return sbool(self.nfrest('POST', '/model/customdata/'+qt(key)+'', value, None))
    def addPipeSection(self, D, t): return int(self.nfrest('GET', '/section/add/pipe/'+str(D)+'/'+str(t)+'', None, None))
    def addPlanarSection(self, t): return int(self.nfrest('GET', '/section/add/planar/'+str(t)+'', None, None))
    def addQuad(self, n1, n2, n3, n4, sect=0, mat=0): return self.nfrest('GET', '/element/add/quad/'+qt(n1)+'/'+qt(n2)+'/'+qt(n3)+'/'+qt(n4)+'/'+str(sect)+'/'+str(mat)+'', None, None)
    def addRebarPattern(self, elem, pattern, Linit, Lfin, numBars, rebCover, matID, area, netSpacing=0): return sbool(self.nfrest('GET', '/element/rebar/pattern/'+qt(elem)+'/'+str(pattern)+'/'+str(Linit)+'/'+str(Lfin)+'/'+str(numBars)+'/'+str(rebCover)+'/'+str(matID)+'/'+str(area)+'/'+str(netSpacing)+'', None, None))
    def addRebarPatternInSection(self, pattern, sectionID, numBars, rebCover, matID, area, netSpacing=0): return sbool(self.nfrest('GET', '/section/rebar/pattern/'+str(pattern)+'/'+str(sectionID)+'/'+str(numBars)+'/'+str(rebCover)+'/'+str(matID)+'/'+str(area)+'/'+str(netSpacing)+'', None, None))
    def addRectangleInSection(self, sectionID, b, h, centerX, centerY, isEmpty=False, material=0, doNotCenter=False): return sbool(self.nfrest('GET', '/section/add/addrect/'+str(sectionID)+'/'+str(b)+'/'+str(h)+'/'+str(centerX)+'/'+str(centerY)+'/'+str(isEmpty)+'/'+str(material)+'/'+str(doNotCenter)+'', None, None))
    def addRectSection(self, Lz, Ly): return int(self.nfrest('GET', '/section/add/rect/'+str(Lz)+'/'+str(Ly)+'', None, None))
    def addSectFromLib(self, name): return int(self.nfrest('POST', '/section/add/fromlib', name, None))
    def addSectFromLib(self, name, doNotCenter=False): return int(self.nfrest('POST', '/section/add/fromlib/'+str(doNotCenter)+'', name, None))
    def addSectionByPoints(self, x, y, CF_tw=0, CF_rc=0, material=0, doNotCenter=False): return int(self.nfrest('GET', '/section/add/bypoints/'+str(CF_tw)+'/'+str(CF_rc)+'/'+str(material)+'/'+str(doNotCenter)+'', None, dict([("x",json.dumps(x)),("y",json.dumps(y))])))
    def addSectionCover(self, sectionID, coverMat, coverThickness): return sbool(self.nfrest('GET', '/section/add/cover/'+str(sectionID)+'/'+str(coverMat)+'/'+str(coverThickness)+'', None, None))
    def addSectionFromDXF(self, path, CF_tw=0, CF_rc=0, material=0): return int(self.nfrest('GET', '/section/add/fromdxf/'+str(CF_tw)+'/'+str(CF_rc)+'/'+str(material)+'', None, dict([("path",path)])))
    def addSeriesFunction(self, Xlist, Ylist, type, units=''): return int(self.nfrest('GET', '/function/add/'+str(type)+'', None, dict([("x",json.dumps(Xlist)),("y",json.dumps(Ylist)),("units",units)])))
    def addSineFunction(self, frequency, phase, stp, duration, maxAmplitude, isGrowing=False, type=0, units=''): return int(self.nfrest('GET', '/function/sine/'+str(frequency)+'/'+str(phase)+'/'+str(stp)+'/'+str(duration)+'/'+str(maxAmplitude)+'/'+str(isGrowing)+'/'+str(type)+'', None, dict([("units",units)])))
    def addSolid(self, nodes, mat=0): return self.nfrest('GET', '/element/add/solid/'+str(mat)+'', None, dict([("nodes",json.dumps(nodes))]))
    def addSpring(self, n1, n2, propName): return self.nfrest('GET', '/element/add/beam/'+qt(n1)+'/'+qt(n2)+'/'+qt(propName)+'', None, None)
    def addSpringNLProperty(self, name, NLdofs, NLprops, local=False): return sbool(self.nfrest('POST', '/springproperty/nl/add/'+qt(name)+'/'+json.dumps(NLdofs)+'/'+str(local)+'', NLprops, None))
    def addSpringProperty(self, name, Kx, Ky, Kz, Krx, Kry, Krz, local=False): return sbool(self.nfrest('GET', '/springproperty/simple/add/'+qt(name)+'/'+str(Kx)+'/'+str(Ky)+'/'+str(Kz)+'/'+str(Krx)+'/'+str(Kry)+'/'+str(Krz)+'/'+str(local)+'', None, None))
    def addSpringsOnOverlappedNodes(self, n, propName): return json.loads(self.nfrest('POST', '/element/add/springsonnodes/'+qt(propName)+'', n, None))
    def addStirrupBars(self, elem, LnumY, LnumZ, area, spacing, matID, Linit, Lfin): return sbool(self.nfrest('GET', '/element/rebar/stirrup/'+qt(elem)+'/'+str(LnumY)+'/'+str(LnumZ)+'/'+str(area)+'/'+str(spacing)+'/'+str(matID)+'/'+str(Linit)+'/'+str(Lfin)+'', None, None))
    def addStirrupBarsInSection(self, sectionID, LnumY, LnumZ, area, spacing, matID): return sbool(self.nfrest('GET', '/section/rebar/stirrup/'+str(sectionID)+'/'+str(LnumY)+'/'+str(LnumZ)+'/'+str(area)+'/'+str(spacing)+'/'+str(matID)+'', None, None))
    def addSubsoilNodalSpringsOnElements(self, n, propName): return sbool(self.nfrest('POST', '/element/add/soilsprings/'+qt(propName)+'', n, None))
    def addSubsoilZProperty(self, width, Rmodulus): return self.nfrest('GET', '/springproperty/subsoil/add/'+str(width)+'/'+str(Rmodulus)+'', None, None)
    def addSurfaceLoad(self, elem, values, direction, loadcase, local=False): return sbool(self.nfrest('POST', '/load/element/surfaceadd/'+qt(elem)+'/'+str(direction)+'/'+qt(loadcase)+'/'+str(local)+'', values, None))
    def addThermalDistLoad(self, elem, values, loadcase): return sbool(self.nfrest('POST', '/load/element/tempdistadd/'+qt(elem)+'/'+qt(loadcase)+'', values, None))
    def addTria(self, n1, n2, n3, sect=0, mat=0): return self.nfrest('GET', '/element/add/tria/'+qt(n1)+'/'+qt(n2)+'/'+qt(n3)+'/'+str(sect)+'/'+str(mat)+'', None, None)
    def addTruss(self, n1, n2, sect=0, mat=0): return self.nfrest('GET', '/element/add/truss/'+qt(n1)+'/'+qt(n2)+'/'+str(sect)+'/'+str(mat)+'', None, None)
    def addTSection(self, Lz, Ly, tw, tf1): return int(self.nfrest('GET', '/section/add/tshape/'+str(Lz)+'/'+str(Ly)+'/'+str(tw)+'/'+str(tf1)+'', None, None))
    def addVolumeLoad(self, elem, value, direction, loadcase): return sbool(self.nfrest('GET', '/load/element/volumeadd/'+qt(elem)+'/'+str(value)+'/'+str(direction)+'/'+qt(loadcase)+'', None, None))
    def alignShellXaxis(self, num, x, y, z): return sbool(self.nfrest('GET', '/element/shellxaxis/'+qt(num)+'/'+str(x)+'/'+str(y)+'/'+str(z)+'', None, None))
    def AnalyzeFireElement(self, elem, endTime, beamExposure=2, columnExposure=3, checkCombo='', selectForcesCrit=2, fireCurve=0, outOfProc=False, noWindow=False, customFireCurve=0): return json.loads(self.nfrest('GET', '/res/check/analyzefire/'+qt(elem)+'/'+str(endTime)+'/'+str(beamExposure)+'/'+str(columnExposure)+'/'+qt(checkCombo)+'/'+str(selectForcesCrit)+'/'+str(fireCurve)+'/'+str(outOfProc)+'/'+str(noWindow)+'/'+str(customFireCurve)+'', None, None))
    def appendDocXformula(self, TeXcode, alignment=0): return sbool(self.nfrest('POST', '/op/docx/appendformula/'+str(alignment)+'', TeXcode, None))
    def appendDocXimage(self, imagePath, ratio=1, alignment=0): return sbool(self.nfrest('GET', '/op/docx/appendimage/'+str(ratio)+'/'+str(alignment)+'', None, dict([("path",imagePath)])))
    def appendDocXtext(self, text, alignment=0, color=0, bold=False, italic=False, underline=False): return sbool(self.nfrest('POST', '/op/docx/appendtext/'+str(alignment)+'/'+str(color)+'/'+str(bold)+'/'+str(italic)+'/'+str(underline)+'', text, None))
    def applyButterworthFilter(self, values, samplingF, cutF, order, lowPass): return json.loads(self.nfrest('POST', '/op/bwfilter/'+str(samplingF)+'/'+str(cutF)+'/'+str(order)+'/'+str(lowPass)+'', values, None))
    def applyEC8lateralForces(self, thID, loadCaseX, loadCaseY, propMasses=False, T1=0, ct=0.05, lam=1): return sbool(self.nfrest('GET', '/load/lateralforces/'+str(thID)+'/'+qt(loadCaseX)+'/'+qt(loadCaseY)+'/'+str(propMasses)+'/'+str(T1)+'/'+str(ct)+'/'+str(lam)+'', None, None))
    def assignHinge(self, beamID, hingeName): return sbool(self.nfrest('GET', '/hinge/assign/'+qt(beamID)+'/'+qt(hingeName)+'', None, None))
    def assignMaterialToElement(self, element, materialID): return sbool(self.nfrest('GET', '/material/assign/'+qt(element)+'/'+str(materialID)+'', None, None))
    def assignSectionToElement(self, element, sectionID): return sbool(self.nfrest('GET', '/section/assign/'+qt(element)+'/'+str(sectionID)+'', None, None))
    def assignSubsoilProperty(self, element, prop): return sbool(self.nfrest('GET', '/springproperty/subsoil/assign/'+qt(element)+'/'+qt(prop)+'', None, None))
    def assignToGroup(self, name, nodes, elements, clear=False): return sbool(self.nfrest('GET', '/group/assign/'+qt(name)+'/'+str(clear)+'', None, dict([("nodes",json.dumps(nodes)),("elements",json.dumps(elements))])))
    def changeDefSolverType(self, type): return sbool(self.nfrest('GET', '/op/opt/changedefsolvertype/'+str(type)+'', None, None))
    def changeElementProperty(self, ID, prop, value): return sbool(self.nfrest('POST', '/element/prop/'+qt(ID)+'/'+qt(prop)+'/'+qt(value)+'', None, None))
    def changeLoadValue(self, i, loadValue): return sbool(self.nfrest('GET', '/load/change/'+str(i)+'/'+str(loadValue)+'', None, None))
    def changeOrAddSectionPoint(self, sectionID, seriesID, ptID, x, y): return sbool(self.nfrest('GET', '/section/add/changeaddpt/'+str(sectionID)+'/'+str(seriesID)+'/'+str(ptID)+'/'+str(x)+'/'+str(y)+'', None, None))
    def changeSolver(self, type, path=''): return sbool(self.nfrest('GET', '/op/opt/changesolver/'+str(type)+'', None, dict([("path",path)])))
    def changeSpringNLProperty(self, name, NLdofs, NLprops): return sbool(self.nfrest('POST', '/springproperty/nl/change/'+qt(name)+'/'+json.dumps(NLdofs)+'', NLprops, None))
    def changeSpringNLPropertyDof(self, name, DoF, NLtype, NLprops): return sbool(self.nfrest('POST', '/springproperty/nl/change/'+qt(name)+'/'+str(DoF)+'/'+str(NLtype)+'', NLprops, None))
    def changeSpringProperty(self, name, Kx, Ky, Kz, Krx, Kry, Krz): return sbool(self.nfrest('GET', '/springproperty/simple/change/'+qt(name)+'/'+str(Kx)+'/'+str(Ky)+'/'+str(Kz)+'/'+str(Krx)+'/'+str(Kry)+'/'+str(Krz)+'', None, None))
    def checkConnectivity(self, notPassedElems=None, overlappedNodes=None): return sbool(self.nfrest('GET', '/op/mesh/connectivity'+str(notPassedElems)+'/'+str(overlappedNodes)+'', None, None))
    def checkElement(self, elem, lc, t, stationType, verName, savelog=False, messages=False, defaultParams=None, logPath=None): return sbool(self.nfrest('GET', '/res/check/element/'+qt(elem)+'/'+qt(lc)+'/'+qt(t)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("logPath",logPath)])))
    def checkElementRatio(self, elem, lc, t, stationType, verName, savelog=False, messages=False, defaultParams=None, logPath=None): return float(self.nfrest('GET', '/res/check/elementRatio/'+qt(elem)+'/'+qt(lc)+'/'+qt(t)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("logPath",logPath)])))
    def checkElements(self, elems, lc, ts, stationType, verName, savelog=False, messages=False, defaultParams=None): return sbool(self.nfrest('GET', '/res/check/elements/'+qt(lc)+'/'+qt(ts)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("elems",json.dumps(elems))])))
    def checkElementsRatio(self, elems, lc, ts, stationType, verName, savelog=False, messages=False, defaultParams=None): return float(self.nfrest('GET', '/res/check/elementsRatio/'+qt(lc)+'/'+qt(ts)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("elems",json.dumps(elems))])))
    def checkElementStation(self, elem, lc, t, stationAbsissa, verName, defaultParams=None, logPath=None, messages=False): return json.loads(self.nfrest('GET', '/res/check/station/'+qt(elem)+'/'+qt(lc)+'/'+qt(t)+'/'+str(stationAbsissa)+'/'+qt(verName)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("logPath",logPath)])))
    def checkFreeNodes(self): return json.loads(self.nfrest('GET', '/op/mesh/findfreenodes', None, None))
    def checkLineElements(self): return int(self.nfrest('GET', '/op/mesh/lineelems', None, None))
    def checkModel(self, lc, ts, stationType, verName, savelog=False, messages=False, defaultParams=None): return sbool(self.nfrest('GET', '/res/check/model/'+qt(lc)+'/'+qt(ts)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams))])))
    def checkNode(self, node, lc, ts, verName, savelog=False, messages=False, defaultParams=None, logPath=None): return sbool(self.nfrest('GET', '/res/check/node/'+qt(node)+'/'+qt(lc)+'/'+qt(ts)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("logPath",logPath)])))
    def checkNodes(self, nodes, lc, ts, stationType, verName, savelog=False, messages=False, defaultParams=None): return sbool(self.nfrest('GET', '/res/check/nodes/'+qt(lc)+'/'+qt(ts)+'/'+str(stationType)+'/'+qt(verName)+'/'+str(savelog)+'/'+str(messages)+'', None, dict([("defaultParams",json.dumps(defaultParams)),("nodes",json.dumps(nodes))])))
    def checkOverlappedElements(self): return json.loads(self.nfrest('GET', '/op/mesh/findoverlappedelements', None, None))
    def clearElementCustomProperties(self, elem): return sbool(self.nfrest('DELETE', '/element/customprop/'+qt(elem)+'', None, None))
    def clearElementRebar(self, elem): return sbool(self.nfrest('GET', '/element/rebar/clear/'+qt(elem)+'', None, None))
    def clearSectionRebar(self, ID): return sbool(self.nfrest('GET', '/section/rebar/clear/'+qt(ID)+'', None, None))
    def clearSectionRebar(self, ID): return sbool(self.nfrest('GET', '/section/rebar/clear/'+str(ID)+'', None, None))
    def clearSelection(self): return sbool(self.nfrest('GET', '/op/clearselection', None, None))
    def clearStoredDomains(self): return sbool(self.nfrest('GET', '/res/check/cleardomains', None, None))
    def colorizeModel(self, criterion, excl=None): return self.nfrest('GET', '/model/colors/colorize/'+str(criterion)+'', None, dict([("excl",json.dumps(excl))]))
    def compileDocX(self, dict, tableDict=None, twoPasses=False): return sbool(self.nfrest('GET', '/op/docx/compile/'+str(twoPasses)+'', tableDict, dict([("dict",json.dumps(dict))])))
    def convertToMeshedSection(self, sectionID): return int(self.nfrest('GET', '/op/mesh/meshedsection/'+str(sectionID)+'', None, None))
    def convertUnits(self, length, force): return self.nfrest('GET', '/units/convertunits/'+qt(length)+'/'+qt(force)+'', None, None)
    def convertValue(self, value, OldUnits, NewUnits): return float(self.nfrest('GET', '/units/convert/'+str(value)+'', None, dict([("OldUnits",OldUnits),("NewUnits",NewUnits)])))
    def createDocX(self, path, text, template=''): return sbool(self.nfrest('GET', '/op/docx/create'+json.dumps(text)+'', None, dict([("path",path),("template",template)])))
    def CustomLicense(self, lic): return sbool(self.nfrest('GET', '/op/lic', None, dict([("val",lic)])))
    def defaultColors(self): return self.nfrest('GET', '/model/colors/default', None, None)
    def deleteChecks(self): return sbool(self.nfrest('GET', '/res/delchecks', None, None))
    def deleteGroup(self, name): return sbool(self.nfrest('GET', '/group/delete/'+qt(name)+'', None, None))
    def deleteResults(self): return sbool(self.nfrest('GET', '/res/delete', None, None))
    def divideHexa(self, hexaID, divX, divY, divZ): return json.loads(self.nfrest('GET', '/op/mesh/dividehexa/'+qt(hexaID)+'/'+str(divX)+'/'+str(divY)+'/'+str(divZ)+'', None, None))
    def divideLine(self, lines, fractions): return json.loads(self.nfrest('GET', '/op/mesh/divideline', None, dict([("lines",json.dumps(lines)),("fractions",json.dumps(fractions))])))
    def divideLineByNodes(self, line, nodes): return sbool(self.nfrest('GET', '/op/mesh/dividelinebynodes/'+qt(line)+'', None, dict([("nodes",json.dumps(nodes))])))
    def divideQuad(self, quadID, divX, divY): return json.loads(self.nfrest('GET', '/op/mesh/dividequad/'+qt(quadID)+'/'+str(divX)+'/'+str(divY)+'', None, None))
    def divideWedge(self, wedgeID, div): return json.loads(self.nfrest('GET', '/op/mesh/dividewedge/'+qt(wedgeID)+'/'+str(div)+'', None, None))
    def duplicateSection(self, originalID): return int(self.nfrest('GET', '/section/duplicate/'+str(originalID)+'', None, None))
    def exportGLTF(self, path, saveIFC=False): return sbool(self.nfrest('GET', '/op/export/gltf/'+str(saveIFC)+'', None, dict([("path",path)])))
    def exportIFC(self, path, saveAsXML=False): return sbool(self.nfrest('GET', '/op/export/ifc/'+str(saveAsXML)+'', None, dict([("path",path)])))
    def exportIOM(self, filename): return sbool(self.nfrest('GET', '/op/export/idea', None, dict([("path",filename)])))
    def exportMidas(self, path): return sbool(self.nfrest('GET', '/op/export/midas', None, dict([("path",path)])))
    def exportOpenSees(self, path, loadcase): return sbool(self.nfrest('GET', '/op/export/opensees/'+qt(loadcase)+'', None, dict([("path",path)])))
    def exportRCbeamsDXF(self, path, elements): return sbool(self.nfrest('GET', '/element/exportdxf', None, dict([("path",path),("elements",json.dumps(elements))])))
    def exportRCmemberDXF(self, path, member): return sbool(self.nfrest('GET', '/model/member/exportdxf/'+qt(member)+'', None, dict([("path",path)])))
    def exportSAP2000(self, path): return sbool(self.nfrest('GET', '/op/export/sap2000', None, dict([("path",path)])))
    def exportSectionDXF(self, path, sID): return sbool(self.nfrest('GET', '/section/exportdxf/'+str(sID)+'', None, dict([("path",path)])))
    def exportWexBIM(self, path, saveIFC=False, copyViewer=True): return sbool(self.nfrest('GET', '/op/export/wexbim/'+str(saveIFC)+'/'+str(copyViewer)+'', None, dict([("path",path)])))
    def exportXMLresults(self, filename): return sbool(self.nfrest('GET', '/op/export/xmlres', None, dict([("path",filename)])))
    def functionFromFile(self, filename, type=9, units=''): return int(self.nfrest('GET', '/function/fromfile/'+str(type)+'', None, dict([("units",units),("path",filename)])))
    def generateFrame(self, baysX, baysY, sn, ddx, ddy, ddz, sx, sy, sz, matx, maty, matz, lc1='', lc2='', lc3='', Lval1=0, Lval2=0, Lval3=0, loadBeamX=False, rigidfloor=False): return sbool(self.nfrest('GET', '/op/mesh/generateframe/'+str(baysX)+'/'+str(baysY)+'/'+str(sn)+'/'+str(ddx)+'/'+str(ddy)+'/'+str(ddz)+'/'+str(sx)+'/'+str(sy)+'/'+str(sz)+'/'+str(matx)+'/'+str(maty)+'/'+str(matz)+'/'+qt(lc1)+'/'+qt(lc2)+'/'+qt(lc3)+'/'+str(Lval1)+'/'+str(Lval2)+'/'+str(Lval3)+'/'+str(loadBeamX)+'/'+str(rigidfloor)+'', None, None))
    def generateLoadCombinations(self, type, comboPrefix=''): return sbool(self.nfrest('GET', '/loadcase/generate/'+str(type)+'/'+qt(comboPrefix)+'', None, None))
    def getAlignedNodes(self, n1, n2, tol=0): return json.loads(self.nfrest('GET', '/op/mesh/alignednodes/'+str(tol)+'', None, dict([("n1",n1),("n2",n2)])))
    def getAnalysisTimeSteps(self, lc): return json.loads(self.nfrest('GET', '/res/steps/'+qt(lc)+'', None, None))
    def getAreaByNodes(self, nodes): return float(self.nfrest('POST', '/node/area', nodes, None))
    def getBC(self, node): return json.loads(self.nfrest('GET', '/bc/get/'+qt(node)+'', None, None))
    def getBeamDeflection(self, num, loadcase, time, type, station): return float(self.nfrest('GET', '/res/beamdeflection/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(type)+'/'+str(station)+'', None, None))
    def getBeamDeflections(self, num, loadcase, type, offsetL=0, numStations=21, time='1'): return self.nfrest('GET', '/res/beamdeflections/'+qt(num)+'/'+qt(loadcase)+'/'+str(type)+'/'+str(offsetL)+'/'+str(numStations)+'/'+qt(time)+'', None, None)
    def getBeamForce(self, num, loadcase, time, type, station): return float(self.nfrest('GET', '/res/beamforce/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(type)+'/'+str(station)+'', None, None))
    def getBeamForce2(self, num, loadcase, time, type, absissa): return float(self.nfrest('GET', '/res/beamforce2/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(type)+'/'+str(absissa)+'', None, None))
    def getBeamForces(self, num, loadcase, station, time='1'): return json.loads(self.nfrest('GET', '/res/beamforces/'+qt(num)+'/'+qt(loadcase)+'/'+str(station)+'/'+qt(time)+'', None, None))
    def getBeamForcesAtNode(self, elem, node, loadcase, time='1'): return json.loads(self.nfrest('GET', '/res/beamforcesatnode/'+qt(elem)+'/'+qt(node)+'/'+qt(loadcase)+'/'+qt(time)+'', None, None))
    def getBeamForcesDiagram(self, num, loadcase, type, offsetL=0, numStations=21, time='1'): return self.nfrest('GET', '/res/beamdiagram/'+qt(num)+'/'+qt(loadcase)+'/'+str(type)+'/'+str(offsetL)+'/'+str(numStations)+'/'+qt(time)+'', None, None)
    def getBeamResMoments(self, elemID): return json.loads(self.nfrest('GET', '/res/check/beammoments/'+qt(elemID)+'', None, None))
    def getBeamResShear(self, elemID, loadcase='', time='1'): return json.loads(self.nfrest('GET', '/res/check/beamshearres/'+qt(elemID)+'/'+qt(loadcase)+'/'+qt(time)+'', None, None))
    def getBuiltInChecking(self): return json.loads(self.nfrest('GET', '/res/check/sets', None, None))
    def getCheckNameByMaterial(self, ID): return self.nfrest('GET', '/res/check/checkbymat/'+qt(ID)+'', None, None)
    def getCombinationCoeffPsi(self, subscript, type): return float(self.nfrest('GET', '/loadcase/getpsi/'+str(subscript)+'/'+str(type)+'', None, None))
    def getCombinationDesignType(self, name): return int(self.nfrest('GET', '/loadcase/combo/designtype/'+qt(name)+'', None, None))
    def getCombinationsByDesignType(self, type, servType=0): return json.loads(self.nfrest('GET', '/loadcases/descombos/designtype/'+str(type)+'/'+str(servType)+'', None, None))
    def getConnectedElements(self, node, onlyOfType=-1): return json.loads(self.nfrest('GET', '/node/connectedelements/'+qt(node)+'/'+str(onlyOfType)+'', None, None))
    def getControlNode(self): return self.nfrest('GET', '/op/controlnode', None, None)
    def getCornerNodes(self, nodes, lcs): return json.loads(self.nfrest('GET', '/op/corners', None, dict([("nodes",json.dumps(nodes)),("lcs",json.dumps(lcs))])))
    def getCustomData(self, key): return self.nfrest('GET', '/model/customdata/'+qt(key)+'', None, None)
    def getDataPlot(self, xseries, yseries, imagePath, name='', Xunits='', Yunits=''): return sbool(self.nfrest('GET', '/function/plotdata/'+qt(name)+'', None, dict([("path",imagePath),("xseries",json.dumps(xseries)),("yseries",json.dumps(yseries)),("Xunits",Xunits),("Yunits",Yunits)])))
    def getDefinedDesignMaterials(self): return json.loads(self.nfrest('GET', '/designmaterials', None, None))
    def getDefinedMaterials(self): return json.loads(self.nfrest('GET', '/materials', None, None))
    def getDefinedSections(self): return json.loads(self.nfrest('GET', '/sections', None, None))
    def getDesignMaterialProperty(self, ID, name, units=None): return self.nfrest('GET', '/designmaterial/prop/'+qt(ID)+'/'+qt(name)+'', None, dict([("units",units)]))
    def getDesignMaterialsLibrary(self, filter='', type=0): return json.loads(self.nfrest('GET', '/designmaterials/library/'+qt(filter)+'/'+str(type)+'', None, None))
    def getDesignMaterialsLibrary(self, filename, filter='', type=0): return json.loads(self.nfrest('GET', '/designmaterials/libraryf/'+qt(filename)+'/'+qt(filter)+'/'+str(type)+'', None, None))
    def getElementArea(self, ID): return float(self.nfrest('GET', '/element/area/'+qt(ID)+'', None, None))
    def getElementCentroid(self, ID): return json.loads(self.nfrest('GET', '/element/centroid/'+qt(ID)+'', None, None))
    def getElementChecks(self, ID, lc, time): return self.nfrest('GET', '/res/check/elementA/'+qt(ID)+'/'+qt(lc)+'/'+qt(time)+'', None, None)
    def getElementConnectivity(self, ID): return json.loads(self.nfrest('GET', '/element/conn/'+qt(ID)+'', None, None))
    def getElementCustomProperty(self, elem, propName): return self.nfrest('GET', '/element/customprop/'+qt(elem)+'/'+qt(propName)+'', None, None)
    def getElementInfo(self, element): return json.loads(self.nfrest('GET', '/element/info/'+qt(element)+'', None, None))
    def getElementOffset(self, elem): return json.loads(self.nfrest('GET', '/element/beamoffset/'+qt(elem)+'', None, None))
    def getElementProperty(self, ID, name): return self.nfrest('GET', '/element/prop/'+qt(ID)+'/'+qt(name)+'', None, None)
    def getElementRebarSegments(self, elem): return json.loads(self.nfrest('GET', '/section/rebar/segments/'+qt(elem)+'', None, None))
    def getElementsChecks(self, lc, time): return json.loads(self.nfrest('GET', '/res/check/elementsA/'+qt(lc)+'/'+qt(time)+'', None, None))
    def getElementsChecksByMat(self, mat): return json.loads(self.nfrest('GET', '/res/check/elementsM/'+str(mat)+'', None, None))
    def getElementsFromGroup(self, name): return json.loads(self.nfrest('GET', '/group/elements/'+qt(name)+'', None, None))
    def getElementType(self, ID): return self.nfrest('GET', '/element/type/'+qt(ID)+'', None, None)
    def getElementVolume(self, ID): return float(self.nfrest('GET', '/element/volume/'+qt(ID)+'', None, None))
    def getEndRelease(self, beamID): return json.loads(self.nfrest('GET', '/element/beamendrelease/'+qt(beamID)+'', None, None))
    def getEnvelopeCombination(self, name): return self.nfrest('GET', '/loadcase/combo/getenv/'+qt(name)+'', None, None)
    def getExtrudedBeamPoints(self, elemID): return json.loads(self.nfrest('GET', '/element/extrudedbeam/'+qt(elemID)+'', None, None))
    def getFirstMode(self, ct=0.05): return float(self.nfrest('GET', '/res/firstmode/'+str(ct)+'', None, None))
    def getFloorLoadType(self, name): return self.nfrest('GET', '/load/floor/planetype/'+qt(name)+'', None, None)
    def getFloorPlanes(self): return json.loads(self.nfrest('GET', '/load/floor/planesget', None, None))
    def getForceUnit(self): return self.nfrest('GET', '/units/f', None, None)
    def getFreeElementID(self): return self.nfrest('GET', '/op/freeelementid', None, None)
    def getFreeNodeID(self): return self.nfrest('GET', '/op/freenodeid', None, None)
    def getFunctionGeneralData(self, funcID): return json.loads(self.nfrest('GET', '/function/gendata/'+str(funcID)+'', None, None))
    def getFunctionName(self, funcID): return self.nfrest('GET', '/function/name/'+str(funcID)+'', None, None)
    def getFunctionPlot(self, funcID, imagePath): return sbool(self.nfrest('GET', '/function/plot/'+str(funcID)+'', None, dict([("path",imagePath)])))
    def getFunctions(self): return json.loads(self.nfrest('GET', '/functions', None, None))
    def getFunctionUnits(self, funcID): return self.nfrest('GET', '/function/units/'+str(funcID)+'', None, None)
    def getGreekLetter(self, input): return self.nfrest('GET', '/op/greek'+qt(input)+'', None, None)
    def getGroups(self): return json.loads(self.nfrest('GET', '/groups', None, None))
    def getLanguage(self): return self.nfrest('GET', '/op/opt/lang', None, None)
    def getLastBilinearMomentCurvature(self): return json.loads(self.nfrest('GET', '/op/sectioncalc/bilmomentcurvature', None, None))
    def getLastMomentCurvatureData(self): return json.loads(self.nfrest('GET', '/op/sectioncalc/momentcurvaturedata', None, None))
    def getLastRunLog(self): return json.loads(self.nfrest('GET', '/op/runlog', None, None))
    def getLastSectionRes3DDomainPoints(self, conn=None): return json.loads(self.nfrest('GET', '/res/check/plot3dsectiondomain'+str(conn)+'', None, None))
    def getLenUnit(self): return self.nfrest('GET', '/units/l', None, None)
    def getLinearAddCombination(self, name): return self.nfrest('GET', '/loadcase/combo/get/'+qt(name)+'', None, None)
    def getLoad(self, i): return self.nfrest('GET', '/load/'+str(i)+'', None, None)
    def getLoadA(self, i): return json.loads(self.nfrest('GET', '/load/getA/'+str(i)+'', None, None))
    def getLoadcaseFactor(self, loadcase): return float(self.nfrest('GET', '/loadcase/getfactor/'+qt(loadcase)+'', None, None))
    def getLoadCases(self): return json.loads(self.nfrest('GET', '/loadcases', None, None))
    def getLoadCombinations(self, includeEnvelopes=True): return json.loads(self.nfrest('GET', '/loadcase/combos/'+str(includeEnvelopes)+'', None, None))
    def getLoadDurationClass(self, loadcase): return int(self.nfrest('GET', '/load/getduration/'+qt(loadcase)+'', None, None))
    def getLoadingData(self): return self.nfrest('GET', '/model/loadingdata', None, None)
    def getLoadsForElement(self, element): return json.loads(self.nfrest('GET', '/load/element/get/'+qt(element)+'', None, None))
    def getLoadsForNode(self, node): return json.loads(self.nfrest('GET', '/load/node/get/'+qt(node)+'', None, None))
    def getLoadsInLoadcase(self, loadcase): return json.loads(self.nfrest('GET', '/load/inloadcase/'+qt(loadcase)+'', None, None))
    def getLocalAxes(self, ID): return json.loads(self.nfrest('GET', '/element/lcs/'+qt(ID)+'', None, None))
    def getLocalAxesArray(self, ID): return json.loads(self.nfrest('GET', '/element/lcsA/'+qt(ID)+'', None, None))
    def getMacroelement(self, elemID): return int(self.nfrest('GET', '/element/macro/'+qt(elemID)+'', None, None))
    def getMaterialProperty(self, ID, name, units=None): return self.nfrest('GET', '/material/prop/'+qt(ID)+'/'+qt(name)+'', None, dict([("units",units)]))
    def getMaterialsLibrary(self, filter='', type=0): return json.loads(self.nfrest('GET', '/materials/library/'+qt(filter)+'/'+str(type)+'', None, None))
    def getMaterialsLibrary(self, filename, filter='', type=0): return json.loads(self.nfrest('GET', '/materials/libraryf/'+qt(filename)+'/'+qt(filter)+'/'+str(type)+'', None, None))
    def getMaxMinBeamForces(self, sectionID, type): return json.loads(self.nfrest('GET', '/res/maxminbeamforces/'+str(sectionID)+'/'+str(type)+'', None, None))
    def getMaxMinNodeDispl(self, dir, nodes=None): return json.loads(self.nfrest('POST', '/res/maxmindispl/'+str(dir)+'', nodes, None))
    def getMaxMinWoodArmerMoments(self, elementID): return json.loads(self.nfrest('GET', '/res/maxminwoodarmer/'+str(elementID)+'', None, None))
    def getMaxMinWoodArmerMoments(self, groupName): return json.loads(self.nfrest('GET', '/res/maxminwoodarmerg/'+qt(groupName)+'', None, None))
    def getMemberElements(self, member): return json.loads(self.nfrest('GET', '/model/member/elems/'+qt(member)+'', None, None))
    def getMemberLength(self, member): return float(self.nfrest('GET', '/model/member/leng/'+qt(member)+'', None, None))
    def getMembers(self): return json.loads(self.nfrest('GET', '/model/member/all', None, None))
    def getModalPeriod(self, num, loadcase): return float(self.nfrest('GET', '/res/period/'+str(num)+'/'+qt(loadcase)+'', None, None))
    def getModes(self, loadcase=None): return int(self.nfrest('GET', '/res/modes/'+str(loadcase)+'', None, None))
    def getNodalDisp(self, num, loadcase, time, direction): return float(self.nfrest('GET', '/res/displacement/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(direction)+'', None, None))
    def getNodalReact(self, num, loadcase, time, direction): return float(self.nfrest('GET', '/res/reaction/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(direction)+'', None, None))
    def getNodalShellForce(self, num, loadcase, time, type): return float(self.nfrest('GET', '/res/nodalshellforce/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+qt(type)+'', None, None))
    def getNodalStress(self, num, loadcase, time, type): return float(self.nfrest('GET', '/res/nodalstress/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+qt(type)+'', None, None))
    def getNodeChecks(self, ID, lc, time): return self.nfrest('GET', '/res/check/nodsA/'+qt(ID)+'/'+qt(lc)+'/'+qt(time)+'', None, None)
    def getNodeCoordinates(self, ID): return json.loads(self.nfrest('GET', '/node/ID'+qt(ID)+'', None, None))
    def getNodeInfo(self, node): return json.loads(self.nfrest('GET', '/node/info/'+qt(node)+'', None, None))
    def getNodePosition(self, ID): return self.nfrest('GET', '/node/ID'+qt(ID)+'', None, None)
    def getNodeProperty(self, ID, name): return self.nfrest('GET', '/node/prop/'+qt(ID)+'/'+qt(name)+'', None, None)
    def getNodesChecks(self, lc, time): return json.loads(self.nfrest('GET', '/res/check/nodesA/'+qt(lc)+'/'+qt(time)+'', None, None))
    def getNodesFromCoords(self, dir, coord, tol=1E-06): return json.loads(self.nfrest('GET', '/op/mesh/nodesbycoords/'+str(dir)+'/'+str(coord)+'/'+str(tol)+'', None, None))
    def getNodesFromGroup(self, name): return json.loads(self.nfrest('GET', '/group/nodes/'+qt(name)+'', None, None))
    def getNodesOnSides(self, nodes, tol=4.94065645841247E-324): return json.loads(self.nfrest('GET', '/op/mesh/borders/'+str(tol)+'', None, dict([("nodes",json.dumps(nodes))])))
    def getOSprocedureName(self): return self.nfrest('GET', '/op/export/osproc', None, None)
    def getParticipatingMassesRatios(self, mode, loadcase): return json.loads(self.nfrest('GET', '/res/partmasses/'+str(mode)+'/'+qt(loadcase)+'', None, None))
    def getParticipationFactors(self, mode, loadcase): return json.loads(self.nfrest('GET', '/res/partfactors/'+str(mode)+'/'+qt(loadcase)+'', None, None))
    def getReinfPropertiesNTC(self, matID, secID, CF, betaAng, Hshear, Bshear, outInMPa=False): return json.loads(self.nfrest('GET', '/material/frpdata/'+str(matID)+'/'+str(secID)+'/'+str(CF)+'/'+str(betaAng)+'/'+str(Hshear)+'/'+str(Bshear)+'/'+str(outInMPa)+'', None, None))
    def getResultHistory(self, loadcase, itemID, resultType, resultID1=0, resultID2=0): return json.loads(self.nfrest('GET', '/res/hist/'+qt(loadcase)+'/'+qt(itemID)+'/'+str(resultType)+'/'+str(resultID1)+'/'+str(resultID2)+'', None, None))
    def getRigidDiaphragms(self): return json.loads(self.nfrest('GET', '/op/mesh/rigiddiaph', None, None))
    def getRigidOffsets(self, beamID): return json.loads(self.nfrest('GET', '/element/beamendoffset/'+qt(beamID)+'', None, None))
    def getSectionColor(self, ID): return int(self.nfrest('GET', '/section/set/color/'+qt(ID)+'', None, None))
    def getSectionCutForce(self, groupName, loadcase, time, type): return float(self.nfrest('GET', '/res/sectioncutforce/'+qt(groupName)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(type)+'', None, None))
    def getSectionFigure(self, sectionID, figureID, isHole=False): return json.loads(self.nfrest('GET', '/section/figure/'+str(sectionID)+'/'+str(figureID)+'/'+str(isHole)+'', None, None))
    def getSectionOffset(self, ID): return json.loads(self.nfrest('GET', '/section/set/offset/'+qt(ID)+'', None, None))
    def getSectionProperties(self, ID): return json.loads(self.nfrest('GET', '/section/props/'+qt(ID)+'', None, None))
    def getSectionProperty(self, ID, name): return self.nfrest('GET', '/section/prop/'+qt(ID)+'/'+qt(name)+'', None, None)
    def getSectionRebarCoords(self, ID): return json.loads(self.nfrest('GET', '/section/rebar/coords/'+qt(ID)+'', None, None))
    def getSectionResDomainPoints(self, domainIndex, domainType, cleanResponseTolerance=0): return json.loads(self.nfrest('GET', '/res/check/plotsectiondomain/'+str(domainIndex)+'/'+str(domainType)+'/'+str(cleanResponseTolerance)+'', None, None))
    def getSectionResMoments(self, ID, station, calcType, N, Myy, Mzz): return self.nfrest('GET', '/op/sectioncalc/a/'+qt(ID)+'/'+str(station)+'/'+str(calcType)+'/'+str(N)+'/'+str(Myy)+'/'+str(Mzz)+'', None, None)
    def getSectionResMoments(self, sectionID, materialID, calcType, N, Myy, Mzz): return self.nfrest('GET', '/op/sectioncalc/b/'+qt(sectionID)+'/'+qt(materialID)+'/'+str(calcType)+'/'+str(N)+'/'+str(Myy)+'/'+str(Mzz)+'', None, None)
    def getSectionResMoments2(self, sectionID, calcType, N, Mzz, Myy, saveImages='', domainTp=0, options=None, Nserv=0, Mzzserv=0, Myyserv=0): return json.loads(self.nfrest('GET', '/op/sectioncalc/c/'+str(sectionID)+'/'+str(calcType)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(domainTp)+'/'+str(Nserv)+'/'+str(Mzzserv)+'/'+str(Myyserv)+'', None, dict([("saveImages",saveImages),("options",options)])))
    def getSectionResMoments3(self, sectionID, calcType, N, Mzz, Myy, saveImages='', domainTp=0, options=None, Nserv=0, Mzzserv=0, Myyserv=0): return self.nfrest('GET', '/op/sectioncalc/d/'+str(sectionID)+'/'+str(calcType)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(domainTp)+'/'+str(Nserv)+'/'+str(Mzzserv)+'/'+str(Myyserv)+'', None, dict([("saveImages",saveImages),("options",options)]))
    def getSectionResShear(self, sectionID, N=0, Mzz=0, Myy=0, Vy=0, Vz=0): return json.loads(self.nfrest('GET', '/op/sectioncalc/shear/'+str(sectionID)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(Vy)+'/'+str(Vz)+'', None, None))
    def getSectionResShear(self, sectionID, verName, N=0, Mzz=0, Myy=0, Vy=0, Vz=0): return json.loads(self.nfrest('GET', '/op/sectioncalc/shear/'+str(sectionID)+'/'+qt(verName)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(Vy)+'/'+str(Vz)+'', None, None))
    def getSectionResShearDict(self, sectionID, verName, N=0, Mzz=0, Myy=0, Vy=0, Vz=0, overrideValues=None): return json.loads(self.nfrest('GET', '/op/sectioncalc/shear2/'+str(sectionID)+'/'+qt(verName)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(Vy)+'/'+str(Vz)+'', overrideValues, None))
    def getSectionsLibrary(self, filter=''): return json.loads(self.nfrest('GET', '/sections/library/'+qt(filter)+'', None, None))
    def getSectionsLibrary(self, filename, filter=''): return json.loads(self.nfrest('GET', '/sections/libraryf/'+qt(filename)+'/'+qt(filter)+'', None, None))
    def getSectMomentCurvature(self, sectionID, N, Mzz, Myy, npts=20, Nserv=0, Mzzserv=0, Myyserv=0): return json.loads(self.nfrest('GET', '/op/sectioncalc/momentcurvature/'+str(sectionID)+'/'+str(N)+'/'+str(Mzz)+'/'+str(Myy)+'/'+str(npts)+'/'+str(Nserv)+'/'+str(Mzzserv)+'/'+str(Myyserv)+'', None, None))
    def getSeparator(self): return self.nfrest('GET', '/op/sep', None, None)
    def getShearResFromDict(self, dict): return json.loads(self.nfrest('GET', '/op/sectioncalc/shearres', dict, None))
    def getShearResFromDict(self, dict): return json.loads(self.nfrest('GET', '/op/sectioncalc/shearres', dict, None))
    def getShellEndRelease(self, ID): return json.loads(self.nfrest('GET', '/element/shellendrelease/'+qt(ID)+'', None, None))
    def getSoilPressureAtNode(self, node, loadcase, time='1'): return float(self.nfrest('GET', '/res/soilpressureatnode/'+qt(node)+'/'+qt(loadcase)+'/'+qt(time)+'', None, None))
    def getSpringLocalAxes(self, elem): return json.loads(self.nfrest('GET', '/springproperty/axes/'+qt(elem)+'', None, None))
    def getSubsoilElements(self): return json.loads(self.nfrest('GET', '/element/add/subsoil', None, None))
    def getTimePeriods(self, lc): return json.loads(self.nfrest('GET', '/res/periods/'+qt(lc)+'', None, None))
    def getVersion(self): return float(self.nfrest('GET', '/version', None, None))
    def getWallGroups(self): return json.loads(self.nfrest('GET', '/element/walls/list', None, None))
    def getWallHeight(self, grpName): return float(self.nfrest('GET', '/element/walls/height/'+qt(grpName)+'', None, None))
    def getWalls(self): return json.loads(self.nfrest('GET', '/element/walls/elems', None, None))
    def getWallSection(self, grpName): return json.loads(self.nfrest('GET', '/element/walls/section/'+qt(grpName)+'', None, None))
    def hasResults(self, loadcase=''): return sbool(self.nfrest('GET', '/res', None, dict([("lc",loadcase)])))
    def importAbaqusCalculix(self, path): return sbool(self.nfrest('GET', '/op/import/abaqus', None, dict([("path",path)])))
    def importDolmen(self, path): return sbool(self.nfrest('GET', '/op/import/dolmen', None, dict([("path",path)])))
    def importDXF(self, path): return sbool(self.nfrest('GET', '/op/import/dxf', None, dict([("path",path)])))
    def importDXF(self, stream): return sbool(self.nfrest('POST', '/op/import/dxfstream', stream, None))
    def importIFC(self, path, includeRigidLinks=False): return sbool(self.nfrest('GET', '/op/import/ifc/'+str(includeRigidLinks)+'', None, dict([("path",path)])))
    def importMidas(self, path): return sbool(self.nfrest('GET', '/op/import/midasfile', None, dict([("path",path)])))
    def importMidas(self, model): return sbool(self.nfrest('POST', '/op/import/midastext', model, None))
    def importMidasResults(self, path): return sbool(self.nfrest('GET', '/op/import/midasresult', None, dict([("path",path)])))
    def importMidasResults(self, text): return sbool(self.nfrest('POST', '/op/import/midasresulttext', text, None))
    def importOpenSees(self, path): return sbool(self.nfrest('GET', '/op/import/opensees', None, dict([("path",path)])))
    def importOpenSeesRecorder(self, path, type, useTimeFlag=True): return sbool(self.nfrest('GET', '/op/import/recorder/'+str(type)+'/'+str(useTimeFlag)+'', None, dict([("path",path)])))
    def importSAF(self, path): return sbool(self.nfrest('GET', '/op/import/saf', None, dict([("path",path)])))
    def importSAP2000(self, path): return sbool(self.nfrest('GET', '/op/import/sap2000', None, dict([("path",path)])))
    def importSeismoStruct(self, path): return sbool(self.nfrest('GET', '/op/import/seismostruct', None, dict([("path",path)])))
    def importSismicad(self, path, lenUnit='cm', forceUnit='daN'): return sbool(self.nfrest('GET', '/op/import/sismicad'+qt(lenUnit)+'/'+qt(forceUnit)+'', None, dict([("path",path)])))
    def importSismicadSects_Combo(self, path): return sbool(self.nfrest('GET', '/op/import/sismicadset', None, dict([("path",path)])))
    def importSismicadSects_Combo(self, text): return sbool(self.nfrest('POST', '/op/import/sismicadsettext', text, None))
    def importSofistik(self, path): return sbool(self.nfrest('GET', '/op/import/sofistik', None, dict([("path",path)])))
    def importSR3(self, path): return sbool(self.nfrest('GET', '/op/import/sr3', None, dict([("path",path)])))
    def importSR4(self, path): return sbool(self.nfrest('GET', '/op/import/sr4', None, dict([("path",path)])))
    def importStraus7(self, path): return sbool(self.nfrest('GET', '/op/import/straus7', None, dict([("path",path)])))
    def importStrausResults(self, path): return sbool(self.nfrest('GET', '/op/import/straus7result', None, dict([("path",path)])))
    def importStrausResults(self, text): return sbool(self.nfrest('POST', '/op/import/straus7resulttext', text, None))
    def importWinStrand(self, path): return sbool(self.nfrest('GET', '/op/import/winstrand', None, dict([("path",path)])))
    def is64bit(self): return sbool(self.nfrest('GET', '/op/is64bit', None, None))
    def isColumn(self, beamID): return sbool(self.nfrest('GET', '/element/iscolumn/'+qt(beamID)+'', None, None))
    def isNodeLoaded(self, node): return sbool(self.nfrest('GET', '/load/node/isloaded/'+qt(node)+'', None, None))
    def isRestrained(self, node): return sbool(self.nfrest('GET', '/bc/node/'+qt(node)+'', None, None))
    def LangTrasl(self, input): return self.nfrest('POST', '/op/trasl', input, None)
    def LaunchLoadCase(self, loadcase, outOfProc=False, noWindow=False): return sbool(self.nfrest('GET', '/op/launchlc/'+qt(loadcase)+'/'+str(outOfProc)+'/'+str(noWindow)+'', None, None))
    def LaunchModel(self, outOfProc=False, noWindow=False): return sbool(self.nfrest('GET', '/op/launchmodel/'+str(outOfProc)+'/'+str(noWindow)+'', None, None))
    def listDesignMaterialCustomProperty(self, ID): return json.loads(self.nfrest('GET', '/designmaterial/proplist/'+str(ID)+'', None, None))
    def listMaterialCustomProperty(self, ID): return json.loads(self.nfrest('GET', '/material/proplist/'+str(ID)+'', None, None))
    def LoadCaseFromCombo(self, comboName): return self.nfrest('GET', '/loadcase/fromcombo/'+qt(comboName)+'', None, None)
    def mergeImportedLines(self, lineIDs): return sbool(self.nfrest('GET', '/op/mesh/mergeimportedlines', None, dict([("lines",json.dumps(lineIDs))])))
    def mergeLines(self, lineIDs): return sbool(self.nfrest('GET', '/op/mesh/mergelines', None, dict([("lines",json.dumps(lineIDs))])))
    def mergeModelData(self, modeldata): return sbool(self.nfrest('PUT', '/model/data'+qt(modeldata)+'', None, None))
    def mergeModelResults(self, modelresults): return sbool(self.nfrest('PUT', '/model/results'+qt(modelresults)+'', None, None))
    def mergeOverlappedNodes(self): return sbool(self.nfrest('GET', '/op/mesh/mergenodes', None, None))
    def meshAreaTria(self, filledContour, emptyContour, maxTriaArea, useAllNodes=False, belt=0, useQuad=False, minAngle=20): return json.loads(self.nfrest('GET', '/op/mesh/tria/'+str(maxTriaArea)+'/'+str(useAllNodes)+'/'+str(belt)+'/'+str(useQuad)+'/'+str(minAngle)+'', None, dict([("filled",json.dumps(filledContour)),("empty",json.dumps(emptyContour))])))
    def meshAreaTriaMulti(self, filledContour, emptyContour, maxTriaArea, useAllNodes=False, belt=0, useQuad=False, minAngle=20): return json.loads(self.nfrest('GET', '/op/mesh/triamulti/'+str(maxTriaArea)+'/'+str(useAllNodes)+'/'+str(belt)+'/'+str(useQuad)+'/'+str(minAngle)+'', None, dict([("filled",json.dumps(filledContour)),("empty",json.dumps(emptyContour))])))
    def meshQuad2Wall(self, quadIDs, isHorizontal=False): return sbool(self.nfrest('GET', '/op/mesh/quad2wall/'+str(isHorizontal)+'', None, dict([("quadIDs",json.dumps(quadIDs))])))
    def ModelToSection(self, openModelPath=''): return self.nfrest('GET', '/model/model2section', None, dict([("path",openModelPath)]))
    def moveNodes(self, nodes, displX, displY, displZ, absolutePosition=False): return sbool(self.nfrest('GET', '/op/mesh/movenodes/'+str(displX)+'/'+str(displY)+'/'+str(displZ)+'/'+str(absolutePosition)+'', None, dict([("nodes",json.dumps(nodes))])))
    def newModel(self): return self.nfrest('GET', '/op/new', None, None)
    def openIDEAcodeCheck(self): return self.nfrest('GET', '/op/export/ccm', None, None)
    def openModel(self, filename): return sbool(self.nfrest('GET', '/op/open', None, dict([("path",filename)])))
    def quad2tria(self, elem): return sbool(self.nfrest('GET', '/op/mesh/quad2tria/'+qt(elem)+'', None, None))
    def readBeamForces(self, num, loadcase, time, N, Vy, Vz, Mt, Myy, Mzz, pos): return sbool(self.nfrest('GET', '/res/import/beamforces/'+qt(num)+'/'+qt(loadcase)+'/'+qt(time)+'/'+str(N)+'/'+str(Vy)+'/'+str(Vz)+'/'+str(Mt)+'/'+str(Myy)+'/'+str(Mzz)+'/'+str(pos)+'', None, None))
    def recalculateSection(self, ID): return sbool(self.nfrest('GET', '/section/recalc/'+str(ID)+'', None, None))
    def refreshDesignerView(self, vstate=0, resize=False): return self.nfrest('GET', '/op/view/'+str(vstate)+'/'+str(resize)+'', None, None)
    def refreshHinges(self): return sbool(self.nfrest('GET', '/hinge/refresh', None, None))
    def removeAllLoads(self): return sbool(self.nfrest('DELETE', '/load/all', None, None))
    def removeAllLoadsForLoadcase(self, lc): return sbool(self.nfrest('DELETE', '/load/alllc/'+qt(lc)+'', None, None))
    def removeBC(self, node): return sbool(self.nfrest('DELETE', '/bc/'+qt(node)+'', None, None))
    def removeCompositeFlags(self, ID): return sbool(self.nfrest('GET', '/section/set/removecomposite/'+str(ID)+'', None, None))
    def removeCustomData(self, key): return sbool(self.nfrest('DELETE', '/model/customdata/'+qt(key)+'', None, None))
    def removeDesMaterialProperty(self, ID, name): return sbool(self.nfrest('DELETE', '/designmaterial/prop/'+str(ID)+'/'+qt(name)+'', None, None))
    def removeElement(self, ID): return sbool(self.nfrest('DELETE', '/element/'+qt(ID)+'', None, None))
    def removeElementsFromMember(self, member, elems): return sbool(self.nfrest('DELETE', '/model/member/elems/'+qt(member)+'', None, dict([("elems",json.dumps(elems))])))
    def removeFloorLoad(self, name): return sbool(self.nfrest('GET', '/load/floor/remove/'+qt(name)+'', None, None))
    def removeFloorPlane(self, name): return sbool(self.nfrest('GET', '/load/floor/planeremove/'+qt(name)+'', None, None))
    def removeFreeNodes(self): return sbool(self.nfrest('GET', '/op/mesh/removefreenodes', None, None))
    def removeHinges(self, beamID): return sbool(self.nfrest('GET', '/hinge/remove/'+qt(beamID)+'', None, None))
    def removeLink(self, node): return sbool(self.nfrest('DELETE', '/op/mesh/constraint/'+qt(node)+'', None, None))
    def removeLoad(self, ID): return sbool(self.nfrest('DELETE', '/load/'+str(ID)+'', None, None))
    def removeLoadCase(self, name): return sbool(self.nfrest('DELETE', '/loadcase/'+qt(name)+'', None, None))
    def removeLoadCaseFromCombination(self, name, loadcase): return sbool(self.nfrest('GET', '/loadcase/combo/remove/'+qt(name)+'/'+qt(loadcase)+'', None, None))
    def removeLoadCaseToTimeHistoryAnalysis(self, name, loadcase): return sbool(self.nfrest('GET', '/loadcase/combo/removeth/'+qt(name)+'/'+qt(loadcase)+'', None, None))
    def removeMaterial(self, materialID): return sbool(self.nfrest('GET', '/material/remove/'+str(materialID)+'', None, None))
    def removeMaterialProperty(self, ID, name): return sbool(self.nfrest('DELETE', '/material/prop/'+str(ID)+'/'+qt(name)+'', None, None))
    def removeMember(self, member): return sbool(self.nfrest('GET', '/model/member/remove/'+qt(member)+'', None, None))
    def removeNodalMass(self, ID): return sbool(self.nfrest('GET', '/mass/remove/'+qt(ID)+'', None, None))
    def removeNode(self, ID): return sbool(self.nfrest('DELETE', '/node/ID'+qt(ID)+'', None, None))
    def removeNodeCS(self, num): return sbool(self.nfrest('DELETE', '/node/cs/'+qt(num)+'', None, None))
    def removeOverlappedElements(self, tol=-1): return sbool(self.nfrest('GET', '/op/mesh/removeoverlappedelements'+str(tol)+'', None, None))
    def removeRigidDiaphragms(self): return sbool(self.nfrest('DELETE', '/op/mesh/rigiddiaph', None, None))
    def removeSection(self, sectionID): return sbool(self.nfrest('GET', '/section/remove/'+str(sectionID)+'', None, None))
    def removeSectionCover(self, sectionID): return sbool(self.nfrest('DELETE', '/section/add/cover/'+str(sectionID)+'', None, None))
    def removeSectionFigure(self, sectionID, figureID, isEmpty=False): return sbool(self.nfrest('GET', '/section/add/removefigure/'+str(sectionID)+'/'+str(figureID)+'/'+str(isEmpty)+'', None, None))
    def removeSectionProperty(self, ID, name): return sbool(self.nfrest('DELETE', '/section/prop/'+qt(ID)+'/'+qt(name)+'', None, None))
    def removeSpringProperty(self, name): return sbool(self.nfrest('DELETE', '/springproperty/'+qt(name)+'', None, None))
    def renameSection(self, sectionID, name, code=''): return sbool(self.nfrest('GET', '/section/rename/'+str(sectionID)+'/'+qt(name)+'/'+qt(code)+'', None, None))
    def renumberElements(self, initialID, step): return sbool(self.nfrest('GET', '/op/mesh/renumber/elements/'+str(initialID)+'/'+str(step)+'', None, None))
    def renumberElementsByCoordinates(self, dir1, dir2): return sbool(self.nfrest('GET', '/op/mesh/renumber/elementsbycoords/'+str(dir1)+'/'+str(dir2)+'', None, None))
    def renumberNodes(self, initialID, step): return sbool(self.nfrest('GET', '/op/mesh/renumber/nodes/'+str(initialID)+'/'+str(step)+'', None, None))
    def renumberNodesByCoordinates(self, dir1, dir2): return sbool(self.nfrest('GET', '/op/mesh/renumber/nodesbycoords/'+str(dir1)+'/'+str(dir2)+'', None, None))
    def requestDesignerUndo(self, ustate=0): return self.nfrest('GET', '/op/undo/'+str(ustate)+'', None, None)
    def rotateNodes(self, nodes, axisX, axisY, axisZ, angle): return sbool(self.nfrest('GET', '/op/mesh/rotatenodes/'+str(axisX)+'/'+str(axisY)+'/'+str(axisZ)+'/'+str(angle)+'', None, dict([("nodes",json.dumps(nodes))])))
    def RunLoadCase(self, loadcase, outOfProc=False, noWindow=False): return self.nfrest('GET', '/op/runlc/'+qt(loadcase)+'/'+str(outOfProc)+'/'+str(noWindow)+'', None, None)
    def RunModel(self, outOfProc=False, noWindow=False): return self.nfrest('GET', '/op/run/'+str(outOfProc)+'/'+str(noWindow)+'', None, None)
    def saveDocX(self): return sbool(self.nfrest('GET', '/op/docx/save', None, None))
    def saveModel(self, filename): return sbool(self.nfrest('GET', '/op/save', None, dict([("path",filename)])))
    def saveOptions(self): return sbool(self.nfrest('GET', '/op/opt/saveopts', None, None))
    def saveSectionImage(self, sectionID, path): return sbool(self.nfrest('GET', '/op/sectioncalc/image/'+str(sectionID)+'', None, dict([("path",path)])))
    def saveSectionImageWithBars(self, elemID, progr, path): return sbool(self.nfrest('GET', '/op/sectioncalc/imagewithbars/'+qt(elemID)+'/'+str(progr)+'', None, dict([("path",path)])))
    def scaleNodes(self, nodes, scaleX, scaleY, scaleZ, scaleCenterX=0, scaleCenterY=0, scaleCenterZ=0): return sbool(self.nfrest('GET', '/op/mesh/scalenodes/'+str(scaleX)+'/'+str(scaleY)+'/'+str(scaleZ)+'/'+str(scaleCenterX)+'/'+str(scaleCenterY)+'/'+str(scaleCenterZ)+'', None, dict([("nodes",json.dumps(nodes))])))
    def SectionToModel(self, sectionID, saveModelPath=''): return sbool(self.nfrest('GET', '/model/section2model/'+qt(sectionID)+'', None, dict([("path",saveModelPath)])))
    def seriesFromFunction(self, funcID): return json.loads(self.nfrest('GET', '/function/series/'+str(funcID)+'', None, None))
    def setAluSection(self, ID, SectionClass=3, Jw=0): return sbool(self.nfrest('GET', '/section/set/alu/'+str(ID)+'/'+str(SectionClass)+'/'+str(Jw)+'', None, None))
    def setAnalysisSequence(self, name, previousCase): return sbool(self.nfrest('GET', '/loadcase/sequence/'+qt(name)+'/'+qt(previousCase)+'', None, None))
    def setBC(self, node, x, y, z, rx, ry, rz): return sbool(self.nfrest('GET', '/bc/set/'+qt(node)+'/'+str(x)+'/'+str(y)+'/'+str(z)+'/'+str(rx)+'/'+str(ry)+'/'+str(rz)+'', None, None))
    def setBeamAngle(self, num, angle): return sbool(self.nfrest('GET', '/element/beamangle/'+qt(num)+'/'+str(angle)+'', None, None))
    def setBucklingAnalysis(self, name, Nmodes, tol=0.0001): return sbool(self.nfrest('GET', '/loadcase/setbuck/'+qt(name)+'/'+str(Nmodes)+'/'+str(tol)+'', None, None))
    def setCombination(self, name, loadcase, factor, type=0, servType=0): return sbool(self.nfrest('GET', '/loadcase/combo/set/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'/'+str(type)+'/'+str(servType)+'', None, None))
    def setCombinationCoeffPsi(self, subscript, type, value): return sbool(self.nfrest('GET', '/loadcase/setpsi/'+str(subscript)+'/'+str(type)+'/'+str(value)+'', None, None))
    def setCombinationFactors(self, gG, gQ, psiVar=None, psiWind=None, psiSnow=None, gSW=0): return sbool(self.nfrest('GET', '/loadcase/setcfactors/'+str(gG)+'/'+str(gQ)+'/'+str(gSW)+'', None, dict([("psiVar",json.dumps(psiVar)),("psiWind",json.dumps(psiWind)),("psiSnow",json.dumps(psiSnow))])))
    def setCompositeBeam(self, ID, MposFactor=-1, MnegFactor=-1): return sbool(self.nfrest('GET', '/section/set/compositebeam/'+str(ID)+'/'+str(MposFactor)+'/'+str(MnegFactor)+'', None, None))
    def setCompositeColumn(self, ID, EcFactor=-1, ReductionFactor=-1): return sbool(self.nfrest('GET', '/section/set/compositecolumn/'+str(ID)+'/'+str(EcFactor)+'/'+str(ReductionFactor)+'', None, None))
    def setConcretePropertiesNTC(self, matID, fc, isCharacteristic=True, unitsIn='MPa'): return float(self.nfrest('GET', '/material/concretentc/'+str(matID)+'/'+str(fc)+'/'+str(isCharacteristic)+'', None, dict([("unitsIn",unitsIn)])))
    def setConstraint(self, n, master, x, y, z, rx, ry, rz): return sbool(self.nfrest('GET', '/op/mesh/constraint/'+qt(n)+'/'+qt(master)+'/'+str(x)+'/'+str(y)+'/'+str(z)+'/'+str(rx)+'/'+str(ry)+'/'+str(rz)+'', None, None))
    def setElemAsJoint(self, num, status): return sbool(self.nfrest('GET', '/element/setjoint/'+qt(num)+'/'+str(status)+'', None, None))
    def setElementChecks(self, ID, lc, time, data, setContour=False): return sbool(self.nfrest('GET', '/res/import/elementcheck/'+qt(ID)+'/'+qt(lc)+'/'+qt(time)+'/'+str(setContour)+'', None, dict([("data",data)])))
    def setElementCustomProperty(self, elem, propName, propValue): return sbool(self.nfrest('POST', '/element/customprop/'+qt(elem)+'/'+qt(propName)+'/'+qt(propValue)+'', None, None))
    def setElementOffset(self, elem, offsetZ, offsetY): return sbool(self.nfrest('POST', '/element/beamoffset/'+qt(elem)+'/'+str(offsetZ)+'/'+str(offsetY)+'', None, None))
    def setElementSection(self, elem, sectID): return sbool(self.nfrest('GET', '/section/'+qt(elem)+'/'+str(sectID)+'', None, None))
    def setEndRelease(self, beamID, node, DOFmask, useStiffness=False): return sbool(self.nfrest('POST', '/element/beamendrelease/'+qt(beamID)+'/'+qt(node)+'/'+str(useStiffness)+'', None, dict([("DOFmask",json.dumps(DOFmask))])))
    def setEnvelope(self, name, loadcase, factor, type=0, servType=0): return sbool(self.nfrest('GET', '/loadcase/combo/setenv/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'/'+str(type)+'/'+str(servType)+'', None, None))
    def setFiberSection(self, ID, divZ=0, divY=0): return sbool(self.nfrest('GET', '/section/set/fibers/'+str(ID)+'/'+str(divZ)+'/'+str(divY)+'', None, None))
    def setFirePoint(self, loadcase, fireNode, targetTemp, gradientY=0, gradientZ=0, tempAtten=20, dontLoadUnder=50): return json.loads(self.nfrest('GET', '/load/firepoint/'+qt(loadcase)+'/'+qt(fireNode)+'/'+str(targetTemp)+'/'+str(gradientY)+'/'+str(gradientZ)+'/'+str(tempAtten)+'/'+str(dontLoadUnder)+'', None, None))
    def setFloorLoad(self, name, loadcase, loadvalue, dirX, dirY, dirZ): return sbool(self.nfrest('GET', '/load/floor/set/'+qt(name)+'/'+qt(loadcase)+'/'+str(loadvalue)+'/'+str(dirX)+'/'+str(dirY)+'/'+str(dirZ)+'', None, None))
    def setFunctionGeneralData(self, funcID, data): return sbool(self.nfrest('POST', '/function/gendata/'+str(funcID)+'', None, dict([("data",json.dumps(data))])))
    def setLanguage(self, code): return self.nfrest('POST', '/op/opt/lang/'+qt(code)+'', None, None)
    def setLoadA(self, load): return sbool(self.nfrest('POST', '/load/setA', load, None))
    def setLoadcaseFactor(self, loadcase, factor): return sbool(self.nfrest('GET', '/loadcase/setfactor/'+qt(loadcase)+'/'+str(factor)+'', None, None))
    def setLoadCasePhaseInCombination(self, name, loadcase, phase): return sbool(self.nfrest('GET', '/loadcase/combo/setphase/'+qt(name)+'/'+qt(loadcase)+'/'+str(phase)+'', None, None))
    def setLoadCaseType(self, name, type): return sbool(self.nfrest('GET', '/loadcase/settype/'+qt(name)+'/'+str(type)+'', None, None))
    def setLoadDurationClass(self, loadcase, durationClass): return sbool(self.nfrest('GET', '/load/setduration/'+qt(loadcase)+'/'+str(durationClass)+'', None, None))
    def setLoadsToMass(self, loadcase, factor=1, remove=False): return sbool(self.nfrest('GET', '/mass/load2mass/'+qt(loadcase)+'/'+str(factor)+'/'+str(remove)+'', None, None))
    def setMacroelement(self, elemID, macroType): return sbool(self.nfrest('POST', '/element/macro/'+qt(elemID)+'/'+str(macroType)+'', None, None))
    def setModalAnalysis(self, name, Nmodes, tol=0.0001): return sbool(self.nfrest('GET', '/loadcase/setmodal/'+qt(name)+'/'+str(Nmodes)+'/'+str(tol)+'', None, None))
    def setNLDanalysis(self, name, tStep, nSteps, tol, iters, seriesID, Xfactor, Yfactor, Zfactor, RXfactor, RYfactor, RZfactor, seriesFactor=1, Mdamp=0, NlGeo=False): return sbool(self.nfrest('GET', '/loadcase/setnldyn/'+qt(name)+'/'+str(tStep)+'/'+str(nSteps)+'/'+str(tol)+'/'+str(iters)+'/'+str(seriesID)+'/'+str(Xfactor)+'/'+str(Yfactor)+'/'+str(Zfactor)+'/'+str(RXfactor)+'/'+str(RYfactor)+'/'+str(RZfactor)+'/'+str(seriesFactor)+'/'+str(Mdamp)+'/'+str(NlGeo)+'', None, None))
    def setNLSanalysis(self, name, tStep, nSteps, tol, iters=10, seriesID=-1, dispControlNode='', dispControlDOF=0, NlGeo=False): return sbool(self.nfrest('GET', '/loadcase/setnlstatic/'+qt(name)+'/'+str(tStep)+'/'+str(nSteps)+'/'+str(tol)+'/'+str(iters)+'/'+str(seriesID)+'/'+qt(dispControlNode)+'/'+str(dispControlDOF)+'/'+str(NlGeo)+'', None, None))
    def setNodeAsJoint(self, num, status): return sbool(self.nfrest('GET', '/node/setjoint/'+qt(num)+'/'+str(status)+'', None, None))
    def setNodeChecks(self, ID, lc, time, data, setContour=False): return sbool(self.nfrest('GET', '/res/import/nodecheck/'+qt(ID)+'/'+qt(lc)+'/'+qt(time)+'/'+str(setContour)+'', None, dict([("data",data)])))
    def setNodeCoordinates(self, ID, coords): return sbool(self.nfrest('POST', '/node/ID'+qt(ID)+'', coords, None))
    def setNodeCS(self, num, x1, y1, z1, x2, y2, z2): return sbool(self.nfrest('GET', '/node/cs/'+qt(num)+'/'+str(x1)+'/'+str(y1)+'/'+str(z1)+'/'+str(x2)+'/'+str(y2)+'/'+str(z2)+'', None, None))
    def setNodePosition(self, node): return sbool(self.nfrest('POST', '/node/ID', node, None))
    def setPDeltaAnalysis(self, name, tol=0.0001): return sbool(self.nfrest('GET', '/loadcase/setpdelta/'+qt(name)+'/'+str(tol)+'', None, None))
    def setResponseSpectrumAnalysis(self, direction, loadcase, modesNumber, spectrumFuncID, modalDamping=0.05, factor=1): return sbool(self.nfrest('GET', '/loadcase/setrs/'+str(direction)+'/'+qt(loadcase)+'/'+str(modesNumber)+'/'+str(spectrumFuncID)+'/'+str(modalDamping)+'/'+str(factor)+'', None, None))
    def setRigidDiaphragms(self, constraintType=0, nodesList=None, masterNode='', restrainZMaster=False): return sbool(self.nfrest('PUT', '/op/mesh/rigiddiaph/'+str(constraintType)+'/'+qt(masterNode)+'/'+str(restrainZMaster)+'', None, dict([("nodesList",json.dumps(nodesList))])))
    def setRigidLink(self, n1, n2): return sbool(self.nfrest('PUT', '/op/mesh/rigidlink/'+qt(n1)+'/'+qt(n2)+'', None, None))
    def setRigidOffsets(self, beamID, values, isAbsLength=False): return sbool(self.nfrest('POST', '/element/beamendoffset/'+qt(beamID)+'/'+str(isAbsLength)+'', None, dict([("values",json.dumps(values))])))
    def setSectionAngle(self, ID, a): return sbool(self.nfrest('GET', '/section/set/angle/'+str(ID)+'/'+str(a)+'', None, None))
    def setSectionColor(self, ID, Red, Green, Blue): return sbool(self.nfrest('POST', '/section/set/color/'+qt(ID)+'/'+str(Red)+'/'+str(Green)+'/'+str(Blue)+'', None, None))
    def setSectionMaterial(self, ID, materialID): return sbool(self.nfrest('GET', '/section/set/material/'+str(ID)+'/'+str(materialID)+'', None, None))
    def setSectionOffset(self, ID, offsetZ, offsetY): return sbool(self.nfrest('POST', '/section/set/offset/'+qt(ID)+'/'+str(offsetZ)+'/'+str(offsetY)+'', None, None))
    def setSectionProperty(self, ID, name, value): return int(self.nfrest('POST', '/section/prop/'+qt(ID)+'/'+qt(name)+'/'+str(value)+'', None, None))
    def setSectionRebarsToElements(self, ID): return sbool(self.nfrest('GET', '/section/rebar/toelems/'+qt(ID)+'', None, None))
    def setSectionRebarsToElements(self, ID): return sbool(self.nfrest('GET', '/section/rebar/toelems/'+str(ID)+'', None, None))
    def setSeismicFloorEccentricity(self, thID, ct=0.05, lam=1): return sbool(self.nfrest('GET', '/loadcase/combo/setseismicecc/'+str(thID)+'/'+str(ct)+'/'+str(lam)+'', None, None))
    def setSeismicLoadcaseForCombos(self, direction, loadcase, enableFloorEccentricity5=False, seismicCombinationType=0): return sbool(self.nfrest('GET', '/loadcase/combo/setseismiclc/'+str(direction)+'/'+qt(loadcase)+'/'+str(enableFloorEccentricity5)+'/'+str(seismicCombinationType)+'', None, None))
    def setSelfWeight(self, loadcase): return sbool(self.nfrest('GET', '/load/setsw/'+qt(loadcase)+'', None, None))
    def setSelfWeightDirection(self, direction): return sbool(self.nfrest('GET', '/load/setswdir/'+str(direction)+'', None, None))
    def setShearReinfRCdata(self, ID, data): return sbool(self.nfrest('GET', '/section/set/shearreinfrc/'+str(ID)+'', None, dict([("data",json.dumps(data))])))
    def setShellEndRelease(self, ID, node, DOFmask): return sbool(self.nfrest('POST', '/element/shellendrelease/'+qt(ID)+'/'+qt(node)+'', None, dict([("DOFmask",json.dumps(DOFmask))])))
    def setSpringLocalAxes(self, name, x1, y1, z1, x2, y2, z2): return sbool(self.nfrest('POST', '/springproperty/axes/'+qt(name)+'/'+str(x1)+'/'+str(y1)+'/'+str(z1)+'/'+str(x2)+'/'+str(y2)+'/'+str(z2)+'', None, None))
    def setSRSScombination(self, name, loadcase, factor, type=0, servType=0): return sbool(self.nfrest('GET', '/loadcase/combo/setsrss/'+qt(name)+'/'+qt(loadcase)+'/'+str(factor)+'/'+str(type)+'/'+str(servType)+'', None, None))
    def setSteelSection(self, ID, SectionClass=3, alphaLT=0.76, alphay=0.76, alphaz=0.76, Jw=0): return sbool(self.nfrest('GET', '/section/set/steel/'+str(ID)+'/'+str(SectionClass)+'/'+str(alphaLT)+'/'+str(alphay)+'/'+str(alphaz)+'/'+str(Jw)+'', None, None))
    def setUnits(self, length, force): return sbool(self.nfrest('GET', '/units/set/'+qt(length)+'/'+qt(force)+'', None, None))
    def setWall(self, elems, rotate90=False, isSlab=False): return self.nfrest('GET', '/element/walls/set/'+str(rotate90)+'/'+str(isSlab)+'', None, dict([("elems",json.dumps(elems))]))
    def showViewport(self, path, width=600, height=400): return sbool(self.nfrest('GET', '/op/showvieport/'+qt(path)+'/'+str(width)+'/'+str(height)+'', None, None))
    def valueFromFunction(self, Xval, funcID): return float(self.nfrest('GET', '/function/value/'+str(Xval)+'/'+str(funcID)+'', None, None))
    def valueFromString(self, text, valueName): return self.nfrest('GET', '/op/import/valfromstring/'+qt(text)+'/'+qt(valueName)+'', None, None)
    def vertexFromNode(self, node): return self.nfrest('GET', '/node/vertex/'+qt(node)+'', None, None)
    @property
    def areaColor(self): return int(self.nfrest('GET','/model/colors/area'))
    @areaColor.setter
    def areaColor(self,value): self.nfrest('POST','/model/colors/area', heads={'val':str(value)})
    @property
    def autoMassInX(self): return sbool(self.nfrest('GET','/mass/autoX'))
    @autoMassInX.setter
    def autoMassInX(self,value): self.nfrest('POST','/mass/autoX', heads={'val':str(value)})
    @property
    def autoMassInY(self): return sbool(self.nfrest('GET','/mass/autoY'))
    @autoMassInY.setter
    def autoMassInY(self,value): self.nfrest('POST','/mass/autoY', heads={'val':str(value)})
    @property
    def autoMassInZ(self): return sbool(self.nfrest('GET','/mass/autoZ'))
    @autoMassInZ.setter
    def autoMassInZ(self,value): self.nfrest('POST','/mass/autoZ', heads={'val':str(value)})
    @property
    def backgroundColor(self): return int(self.nfrest('GET','/model/colors/back'))
    @backgroundColor.setter
    def backgroundColor(self,value): self.nfrest('POST','/model/colors/back', heads={'val':str(value)})
    @property
    def baselineGrade(self): return int(self.nfrest('GET','/op/opt/baseline'))
    @baselineGrade.setter
    def baselineGrade(self,value): self.nfrest('POST','/op/opt/baseline', heads={'val':str(value)})
    @property
    def binFolder(self): return self.nfrest('GET','/op/opt/binfolder')
    @binFolder.setter
    def binFolder(self,value): self.nfrest('POST','/op/opt/binfolder', heads={'val':str(value)})
    @property
    def bordersColor(self): return int(self.nfrest('GET','/model/colors/border'))
    @bordersColor.setter
    def bordersColor(self,value): self.nfrest('POST','/model/colors/border', heads={'val':str(value)})
    @property
    def constraintsColor(self): return int(self.nfrest('GET','/model/colors/constraint'))
    @constraintsColor.setter
    def constraintsColor(self,value): self.nfrest('POST','/model/colors/constraint', heads={'val':str(value)})
    @property
    def defSolverType(self): return int(self.nfrest('GET','/op/opt/defsolvertype'))
    @property
    def designMaterialsID(self): return json.loads(self.nfrest('GET','/designmaterials'))
    @property
    def DocXfontSize(self): return int(self.nfrest('GET','/op/docx/fontsize'))
    @DocXfontSize.setter
    def DocXfontSize(self,value): self.nfrest('POST','/op/docx/fontsize', heads={'val':str(value)})
    @property
    def DocXformulaResolution(self): return int(self.nfrest('GET','/op/docx/formularesol'))
    @DocXformulaResolution.setter
    def DocXformulaResolution(self,value): self.nfrest('POST','/op/docx/formularesol', heads={'val':str(value)})
    @property
    def DocXtableAlignment(self): return int(self.nfrest('GET','/op/docx/tablealign'))
    @DocXtableAlignment.setter
    def DocXtableAlignment(self,value): self.nfrest('POST','/op/docx/tablealign', heads={'val':str(value)})
    @property
    def DocXtableFitting(self): return sbool(self.nfrest('GET','/op/docx/tablefit'))
    @DocXtableFitting.setter
    def DocXtableFitting(self,value): self.nfrest('POST','/op/docx/tablefit', heads={'val':str(value)})
    @property
    def DocXtableFontSize(self): return int(self.nfrest('GET','/op/docx/tablefontsize'))
    @DocXtableFontSize.setter
    def DocXtableFontSize(self,value): self.nfrest('POST','/op/docx/tablefontsize', heads={'val':str(value)})
    @property
    def dontDeleteResults(self): return sbool(self.nfrest('GET','/res/donotdelete'))
    @dontDeleteResults.setter
    def dontDeleteResults(self,value): self.nfrest('POST','/res/donotdelete', heads={'val':str(value)})
    @property
    def DXFoptions(self): return self.nfrest('GET','/op/opt/dxfoptions')
    @DXFoptions.setter
    def DXFoptions(self,value): self.nfrest('POST','/op/opt/dxfoptions', heads={'val':str(value)})
    @property
    def elemsList(self): return json.loads(self.nfrest('GET','/elements'))
    @property
    def elemsNumber(self): return self.nfrest('GET','/elements/number')
    @property
    def elemTextColor(self): return int(self.nfrest('GET','/model/colors/elemtext'))
    @elemTextColor.setter
    def elemTextColor(self,value): self.nfrest('POST','/model/colors/elemtext', heads={'val':str(value)})
    @property
    def envName(self): return self.nfrest('GET','/model/env')
    @property
    def hingesColor(self): return int(self.nfrest('GET','/model/colors/hinge'))
    @hingesColor.setter
    def hingesColor(self,value): self.nfrest('POST','/model/colors/hinge', heads={'val':str(value)})
    @property
    def IFC_format(self): return int(self.nfrest('GET','/op/opt/ifcformat'))
    @IFC_format.setter
    def IFC_format(self,value): self.nfrest('POST','/op/opt/ifcformat', heads={'val':str(value)})
    @property
    def IFC_includeAnalyticalModel(self): return sbool(self.nfrest('GET','/op/opt/ifcanalytical'))
    @IFC_includeAnalyticalModel.setter
    def IFC_includeAnalyticalModel(self,value): self.nfrest('POST','/op/opt/ifcanalytical', heads={'val':str(value)})
    @property
    def IFC_WallMeshSize(self): return float(self.nfrest('GET','/op/opt/ifcwallmeshsize'))
    @IFC_WallMeshSize.setter
    def IFC_WallMeshSize(self,value): self.nfrest('POST','/op/opt/ifcwallmeshsize', heads={'val':str(value)})
    @property
    def isRemote(self): return sbool(self.nfrest('GET','na'))
    @property
    def lineColor(self): return int(self.nfrest('GET','/model/colors/line'))
    @lineColor.setter
    def lineColor(self,value): self.nfrest('POST','/model/colors/line', heads={'val':str(value)})
    @property
    def loading(self): return sbool(self.nfrest('GET',''))
    @property
    def massColor(self): return int(self.nfrest('GET','/model/colors/mass'))
    @massColor.setter
    def massColor(self,value): self.nfrest('POST','/model/colors/mass', heads={'val':str(value)})
    @property
    def materialsID(self): return json.loads(self.nfrest('GET','/materials'))
    @property
    def modeldata(self): return self.nfrest('GET','/model/data')
    @modeldata.setter
    def modeldata(self,value): self.nfrest('POST','/model/data',value)
    @property
    def modelName(self): return self.nfrest('GET','/model')
    @modelName.setter
    def modelName(self,value): self.nfrest('POST','/model', heads={'val':str(value)})
    @property
    def modelPath(self): return self.nfrest('GET','/model/path')
    @property
    def modelresults(self): return self.nfrest('GET','/model/results')
    @modelresults.setter
    def modelresults(self,value): self.nfrest('POST','/model/results',value)
    @property
    def nodeColor(self): return int(self.nfrest('GET','/model/colors/node'))
    @nodeColor.setter
    def nodeColor(self,value): self.nfrest('POST','/model/colors/node', heads={'val':str(value)})
    @property
    def nodesList(self): return json.loads(self.nfrest('GET','/nodes'))
    @property
    def nodesNumber(self): return self.nfrest('GET','/nodes/number')
    @property
    def nodeTextColor(self): return int(self.nfrest('GET','/model/colors/nodetext'))
    @nodeTextColor.setter
    def nodeTextColor(self,value): self.nfrest('POST','/model/colors/nodetext', heads={'val':str(value)})
    @property
    def numberFormat(self): return self.nfrest('GET','/op/opt/numberformat')
    @numberFormat.setter
    def numberFormat(self,value): self.nfrest('POST','/op/opt/numberformat', heads={'val':str(value)})
    @property
    def OS_beamWithHingesOption(self): return sbool(self.nfrest('GET','/op/opt/os/beamwithhinges'))
    @OS_beamWithHingesOption.setter
    def OS_beamWithHingesOption(self,value): self.nfrest('POST','/op/opt/os/beamwithhinges', heads={'val':str(value)})
    @property
    def OS_concreteTensileStrength(self): return sbool(self.nfrest('GET','/op/opt/os/tensilesrc'))
    @OS_concreteTensileStrength.setter
    def OS_concreteTensileStrength(self,value): self.nfrest('POST','/op/opt/os/tensilesrc', heads={'val':str(value)})
    @property
    def OS_IntegrationPointsOption(self): return int(self.nfrest('GET','/op/opt/os/intpoints'))
    @OS_IntegrationPointsOption.setter
    def OS_IntegrationPointsOption(self,value): self.nfrest('POST','/op/opt/os/intpoints', heads={'val':str(value)})
    @property
    def OS_NDfiberSectionsOption(self): return sbool(self.nfrest('GET','/op/opt/os/ndfibersects'))
    @OS_NDfiberSectionsOption.setter
    def OS_NDfiberSectionsOption(self,value): self.nfrest('POST','/op/opt/os/ndfibersects', heads={'val':str(value)})
    @property
    def OS_saveStateVariables(self): return sbool(self.nfrest('GET','/op/opt/os/statevars'))
    @OS_saveStateVariables.setter
    def OS_saveStateVariables(self,value): self.nfrest('POST','/op/opt/os/statevars', heads={'val':str(value)})
    @property
    def releasesColor(self): return int(self.nfrest('GET','/model/colors/release'))
    @releasesColor.setter
    def releasesColor(self,value): self.nfrest('POST','/model/colors/release', heads={'val':str(value)})
    @property
    def resCalc_cacheEnabled(self): return sbool(self.nfrest('GET','/op/opt/rescalc/cacheenabled'))
    @resCalc_cacheEnabled.setter
    def resCalc_cacheEnabled(self,value): self.nfrest('POST','/op/opt/rescalc/cacheenabled', heads={'val':str(value)})
    @property
    def resCalc_concreteBehaviour(self): return int(self.nfrest('GET','/op/opt/rescalc/concbeh'))
    @resCalc_concreteBehaviour.setter
    def resCalc_concreteBehaviour(self,value): self.nfrest('POST','/op/opt/rescalc/concbeh', heads={'val':str(value)})
    @property
    def resCalc_domainCorrectionType(self): return int(self.nfrest('GET','/op/opt/rescalc/domcorr'))
    @resCalc_domainCorrectionType.setter
    def resCalc_domainCorrectionType(self,value): self.nfrest('POST','/op/opt/rescalc/domcorr', heads={'val':str(value)})
    @property
    def resCalc_elasticTolerance(self): return float(self.nfrest('GET','/op/opt/rescalc/eltoll'))
    @resCalc_elasticTolerance.setter
    def resCalc_elasticTolerance(self,value): self.nfrest('POST','/op/opt/rescalc/eltoll', heads={'val':str(value)})
    @property
    def resCalc_homogBarsFactor(self): return int(self.nfrest('GET','/op/opt/rescalc/homog'))
    @resCalc_homogBarsFactor.setter
    def resCalc_homogBarsFactor(self,value): self.nfrest('POST','/op/opt/rescalc/homog', heads={'val':str(value)})
    @property
    def resCalc_kMod(self): return float(self.nfrest('GET','/op/opt/rescalc/kmod'))
    @resCalc_kMod.setter
    def resCalc_kMod(self,value): self.nfrest('POST','/op/opt/rescalc/kmod', heads={'val':str(value)})
    @property
    def resCalc_rebarHardeningRatio(self): return float(self.nfrest('GET','/op/opt/rescalc/rebhard'))
    @resCalc_rebarHardeningRatio.setter
    def resCalc_rebarHardeningRatio(self,value): self.nfrest('POST','/op/opt/rescalc/rebhard', heads={'val':str(value)})
    @property
    def resCalc_resDomainSlices(self): return int(self.nfrest('GET','/op/opt/rescalc/domainslices'))
    @resCalc_resDomainSlices.setter
    def resCalc_resDomainSlices(self,value): self.nfrest('POST','/op/opt/rescalc/domainslices', heads={'val':str(value)})
    @property
    def resCalc_responseInTension(self): return sbool(self.nfrest('GET','/op/opt/rescalc/tensresp'))
    @resCalc_responseInTension.setter
    def resCalc_responseInTension(self,value): self.nfrest('POST','/op/opt/rescalc/tensresp', heads={'val':str(value)})
    @property
    def resCalc_steelClass(self): return int(self.nfrest('GET','/op/opt/rescalc/steelclass'))
    @resCalc_steelClass.setter
    def resCalc_steelClass(self,value): self.nfrest('POST','/op/opt/rescalc/steelclass', heads={'val':str(value)})
    @property
    def resCalc_strandHardeningRatio(self): return float(self.nfrest('GET','/op/opt/rescalc/strhard'))
    @resCalc_strandHardeningRatio.setter
    def resCalc_strandHardeningRatio(self,value): self.nfrest('POST','/op/opt/rescalc/strhard', heads={'val':str(value)})
    @property
    def restraintsColor(self): return int(self.nfrest('GET','/model/colors/restraint'))
    @restraintsColor.setter
    def restraintsColor(self,value): self.nfrest('POST','/model/colors/restraint', heads={'val':str(value)})
    @property
    def saveStateVariables(self): return sbool(self.nfrest('GET','/op/opt/os/statevars'))
    @saveStateVariables.setter
    def saveStateVariables(self,value): self.nfrest('POST','/op/opt/os/statevars', heads={'val':str(value)})
    @property
    def sectCalcAccuracy(self): return int(self.nfrest('GET','/op/opt/calcaccuracy'))
    @sectCalcAccuracy.setter
    def sectCalcAccuracy(self,value): self.nfrest('POST','/op/opt/calcaccuracy', heads={'val':str(value)})
    @property
    def sectCalcUseFibers(self): return sbool(self.nfrest('GET','/op/opt/calcusefibers'))
    @sectCalcUseFibers.setter
    def sectCalcUseFibers(self,value): self.nfrest('POST','/op/opt/calcusefibers', heads={'val':str(value)})
    @property
    def sectionsID(self): return json.loads(self.nfrest('GET','/sections'))
    @property
    def selAreaColor(self): return int(self.nfrest('GET','/model/colors/selarea'))
    @selAreaColor.setter
    def selAreaColor(self,value): self.nfrest('POST','/model/colors/selarea', heads={'val':str(value)})
    @property
    def selectedElements(self): return json.loads(self.nfrest('GET','/op/selectedelements'))
    @selectedElements.setter
    def selectedElements(self,value): self.nfrest('POST','/op/selectedelements', heads={'val':str(value)})
    @property
    def selectedNodes(self): return json.loads(self.nfrest('GET','/op/selectednodes'))
    @selectedNodes.setter
    def selectedNodes(self,value): self.nfrest('POST','/op/selectednodes', heads={'val':str(value)})
    @property
    def selLineColor(self): return int(self.nfrest('GET','/model/colors/selline'))
    @selLineColor.setter
    def selLineColor(self,value): self.nfrest('POST','/model/colors/selline', heads={'val':str(value)})
    @property
    def selNodeColor(self): return int(self.nfrest('GET','/model/colors/selnode'))
    @selNodeColor.setter
    def selNodeColor(self,value): self.nfrest('POST','/model/colors/selnode', heads={'val':str(value)})
    @property
    def selSolidColor(self): return int(self.nfrest('GET','/model/colors/selsolid'))
    @selSolidColor.setter
    def selSolidColor(self,value): self.nfrest('POST','/model/colors/selsolid', heads={'val':str(value)})
    @property
    def selSpringColor(self): return int(self.nfrest('GET','/model/colors/node'))
    @selSpringColor.setter
    def selSpringColor(self,value): self.nfrest('POST','/model/colors/node', heads={'val':str(value)})
    @property
    def solidColor(self): return int(self.nfrest('GET','/model/colors/solid'))
    @solidColor.setter
    def solidColor(self,value): self.nfrest('POST','/model/colors/solid', heads={'val':str(value)})
    @property
    def solverType(self): return int(self.nfrest('GET','/op/opt/solvertype'))
    @property
    def springColor(self): return int(self.nfrest('GET','/model/colors/spring'))
    @springColor.setter
    def springColor(self,value): self.nfrest('POST','/model/colors/spring', heads={'val':str(value)})
    @property
    def tempFolder(self): return self.nfrest('GET','/op/opt/tempfolder')
    @tempFolder.setter
    def tempFolder(self,value): self.nfrest('POST','/op/opt/tempfolder', heads={'val':str(value)})
    @property
    def textColor(self): return int(self.nfrest('GET','/model/colors/text'))
    @textColor.setter
    def textColor(self,value): self.nfrest('POST','/model/colors/text', heads={'val':str(value)})
    @property
    def useFastEigensolver(self): return sbool(self.nfrest('GET','/op/opt/os/fasteigen'))
    @useFastEigensolver.setter
    def useFastEigensolver(self,value): self.nfrest('POST','/op/opt/os/fasteigen', heads={'val':str(value)})
    @property
    def WallMeshSize(self): return float(self.nfrest('GET','/op/opt/wallmeshsize'))
    @WallMeshSize.setter
    def WallMeshSize(self,value): self.nfrest('POST','/op/opt/wallmeshsize', heads={'val':str(value)})
