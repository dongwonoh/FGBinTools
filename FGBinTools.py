# Functions to read and write data from binary FaceGen files - Ron Dotsch (rdotsch@gmail.com)

# VERSION 0.6

# Changelog 0.6:
# - added writeFG and _pack

# Changelog 0.5:
# - added printControlLabels and findControlByLabel functions

# Changelog 0.4:
# - seemed a problem with little vs. big endian introduced by Python 2.7 with pack/unpack. Added < to unpack of ctl file in InsertSlider which seems to have solved the problem.

# Changelog 0.3:
# - added insertSlider 
# - added readEGM
# - replaced readCtl (still half implemented), programs using old version will break, change readCtl reference into readCtlOld in older programs for backwards compatibility
# - added getSliderVector
# - added sliderExists
# - added insertOrthogonalSlider
# - added insertSliderFromFG

# Changelog 0.2:
# - added readFG (works except for texture image at the end)

# Changelog 0.1:
# - added readTri (gives errors at the end, does not work properly)
# - added readCtl (works, but the second half has not been implemented yet)

from struct import *
from numpy import array
from LinAlgTools import orthogonalize, normalize
import ctypes

def _unpack(fmt, binFilePointer):
    return list(unpack_from(fmt, binFilePointer.read(calcsize(fmt))))

def _pack(fmt, binFilePointer, values=[], offset=0):
    binFilePointer.write(pack(fmt, *values))

def readFG(FGFileName):
    with open(FGFileName, 'rb') as fg:
        fgData = {}
        (dummy, geomBasisVersion, texBasisVersion, SS, SA, TS, TA, zero, detailTexFlag) = _unpack('<8s8L', fg)

        if not dummy == b'FRFG0001':
            print("Not a valid .FG file.")
            return False

        fgData['SS'] = [i for i in _unpack('<%ih' % SS, fg)]
        fgData['SA'] = [i for i in _unpack('<%ih' % SA, fg)]
        fgData['TS'] = [i for i in _unpack('<%ih' % TS, fg)]
        fgData['TA'] = [i for i in _unpack('<%ih' % TA, fg)]
        return fgData

def writeFG(FGFileName, SymShape = [], ASymShape = [], SymTexture = []):
    with open(FGFileName, 'wb') as fg:
        
        # preamble
        fmt = '<8s8L130h'
        values = [b'FRFG0001', 2001060901, 81, 50, 30, 50, 0, 0, 0]

        # fix coordinate values
        if len(SymShape) == 0:
            SymShape = 50 * [0]
        elif len(SymShape) < 50:
            print("Warning: SymShape should have 50 values, padding with zeros")
            SymShape.append((50 - len(SymShape)) * [0])
        elif len(SymShape) > 50:
            print("Warning: SymShape should have 50 values, cutting values")
            SymShape = SymShape[:50]
        
        if len(ASymShape) == 0:
            ASymShape = 30 * [0]
        elif len(ASymShape) < 30:
            print("Warning: ASymShape should have 30 values, padding with zeros")
            ASymShape.append((30 - len(ASymShape)) * [0])
        elif len(ASymShape) > 30:
            print("Warning: ASymShape should have 30 values, cutting values")
            ASymShape = ASymShape[:30]
        
        if len(SymTexture) == 0:
            SymShape = 50 * [0]
        elif len(SymTexture) < 50:
            print("Warning: SymTexture should have 50 values, padding with zeros")
            SymTexture.append((50 - len(SymTexture)) * [0])
        elif len(SymTexture) > 50:
            print("Warning: SymTexture should have 50 values, cutting values")
            SymTexture = SymTexture[:50]

        # append coordinate
        values.extend(SymShape + ASymShape + SymTexture)    

        # write to file
        _pack(fmt, fg, values)


def readEGM(egmFileName):
    with open(egmFileName, 'rb') as egm:
        egmData = {'S':[], 'A':[]}
        (dummy, V, S, A, geomBasisVersion, reserved) = _unpack('<8s4L40s', egm)
        if not dummy == 'FREGM002':
            print("Not a valid .EGM file.")
            return False

        for mode in range(S):
            (scale, ) = _unpack('<f', egm)
            egmData['S'].append([])
            for vertex in range(V):
                egmData['S'][mode].append([scale * i for i in _unpack('<3h', egm)])

        

        for mode in range(A):
            (scale, ) = _unpack('<f', egm)
            egmData['A'].append([])
            for vertex in range(V):
                egmData['A'][mode].append([scale * i for i in _unpack('<3h', egm)])

    return egmData
    
def readTri(triFileName):
    with open(triFileName, 'rb') as tri:
        triData = {'vert':[], 'tri':[], 'quad':[], 'vlabels':[], 'slabels':[], 'tex':[], 'ttInd':[], 'qtInd':[], 'morphs':[]}
        
        (dummy, V, T, Q, LV, LS, X, ext, Md, Ms, K, reserved) = _unpack('<8s10I16s', tri)
        for i in range(V + K):
            triData['vert'].append(_unpack('3f', tri))
        for i in range(T):
            triData['tri'].append(_unpack('<3i', tri))
        for i in range(Q):
            triData['quad'].append(_unpack('<4i', tri))
        for i in range(LV):
            (vlabels, S) = _unpack('<2i', tri)
            string  = _unpack('<%is' % S, tri)
            triData['vlabels'].append((vlabels, string))
        for i in range(LS):
            slabels = _unpack('<i3fi', tri)
            S = slabels.pop()
            string = _unpack('<%is' % S, tri)
            triData['slabels'].append((slabels, string))
        
        if X == 0 and (ext & 0x01):
            for i in range(V):
                triData['tex'].append(_unpack('2f', tri))
        elif X > 0 and (ext & 0x01):
            for i in range(X):
                triData['tex'].append(_unpack('2f', tri))
            for i in range(T):
                triData['ttInd'].append(_unpack('<3i', tri))
            for i in range(Q):
                triData['qtInd'].append(_unpack('<4i', tri))
        
        for i in range(Md):
            N = _unpack('<i', tri)[0]
            (label) = _unpack('%is' % N, tri)
            print(label)
            #print (label, scale)
            deltas = []
            for j in range(V):
                deltas.append(_unpack('<f3h' , tri))
            triData['morphs'].append((label, deltas))
    
    return triData


def insertSlider(sliderLabel, vectorAsList, sliderType, ctlFile):
    # read and remember until appropriate sliderType
    print("Writing slider {} to .ctl file {}".format(sliderLabel, ctlFile))
    with open(ctlFile, 'rb') as ctl:
        ctlData = {}
        
        out = ""
        
        (dummy, geometryBasisVersion, textureBasisVersion, nGS, nGA, nTS, nTA, nLGS) = _unpack('<8s7L', ctl)

        if dummy != b'FRCTL001':
            print("File is not a FaceGen binary .ctl file.")
            return False

        out = pack('<8s6L', dummy, geometryBasisVersion, textureBasisVersion, nGS, nGA, nTS, nTA)

        if sliderType == 'SS':
            if len(vectorAsList) != nGS:
                print("Number of weights incorrect for slider type.")
                return False
            out += pack('<L', nLGS + 1)
            for weight in vectorAsList:
                out += pack('<f', weight)
            out += pack('<L%is' % len(sliderLabel), len(sliderLabel), bytes(sliderLabel, 'utf-8'))
        else:
            out += pack('<L', nLGS)

        for _ in range(nLGS):
            out += ctl.read(calcsize('%if' % nGS))  # weights
            (labelLength, ) = _unpack('<L', ctl)
            out += pack('<L', labelLength)
            out += ctl.read(calcsize('%is' % labelLength))

        (nLGA, ) = _unpack('<I', ctl)

        if sliderType == 'SA':
            if len(vectorAsList) != nGA:
                print("Number of weights incorrect for slider type.")
                return False
            out += pack('<L', nLGA + 1)
            for weight in vectorAsList:
                out += pack('<f', weight)
            out += pack('<L%is' % len(sliderLabel), len(sliderLabel), bytes(sliderLabel, 'utf-8'))
        else:
            out += pack('<L', nLGA)

        for _ in range(nLGA):
            out += ctl.read(calcsize('%if' % nGA))  # weights
            (labelLength, ) = _unpack('<L', ctl)
            out += pack('<L', labelLength)
            out += ctl.read(calcsize('%is' % labelLength))  # label string

        (nLTS, ) = _unpack('<I', ctl)

        if sliderType == 'TS':
            if len(vectorAsList) != nTS:
                print("Number of weights incorrect for slider type.")
                return False
            out += pack('<L', nLTS + 1)
            for weight in vectorAsList:
                out += pack('<f', weight)
            out += pack('<L%is' % len(sliderLabel), len(sliderLabel), bytes(sliderLabel, 'utf-8'))
        else:
            out += pack('<L', nLTS)

        for _ in range(nLTS):
            out += ctl.read(calcsize('%if' % nTS))  # weights
            (labelLength, ) = _unpack('<L', ctl)
            out += pack('<L', labelLength)
            out += ctl.read(calcsize('%is' % labelLength))  # label string

        (nLTA, ) = _unpack('<I', ctl)

        if sliderType == 'TA':
            if len(vectorAsList) != nTA:
                print("Number of weights incorrect for slider type.")
                return False
            out += pack('<L', nLTA + 1)
            for weight in vectorAsList:
                out += pack('<f', weight)
            out += pack('<L%is' % len(sliderLabel), len(sliderLabel), bytes(sliderLabel, 'utf-8'))
        else:
            out += pack('<L', nLTA)

        for _ in range(nLTA):
            out += ctl.read(calcsize('%if' % nTA))  # weights
            (labelLength, ) = _unpack('<L', ctl)
            out += pack('<L', labelLength)
            out += ctl.read(calcsize('%is' % labelLength))  # label string

        out += ctl.read()

    with open(ctlFile, 'wb') as ctl:
        ctl.write(out)

    return True

    
def readCtl(ctlFile):
    # read and remember until appropriate sliderType
    with open(ctlFile, 'rb') as ctl:
        data = {'GS':[], 'GA':[], 'TS':[], 'TA':[]}

        (dummy, geometryBasisVersion, textureBasisVersion, nGS, nGA, nTS, nTA, nLGS) = _unpack ('<8s7L', ctl)

        if not dummy == 'FRCTL001':
            print("File is not a FaceGen binary .ctl file.")
            return False

        for i in range(nLGS):
            weights = _unpack('%if' % (nGS), ctl) 
            (labelLength, ) = _unpack('<L', ctl)
            (label, ) = _unpack('%is' % (labelLength), ctl)
            data['GS'].append((label, weights))

        (nLGA, ) = _unpack('<I', ctl)
        for i in range(nLGA):
            weights = _unpack('%if' % (nGA), ctl) 
            (labelLength, ) = _unpack('<L', ctl)
            (label, ) = _unpack('%is' % (labelLength), ctl)
            data['GA'].append((label, weights))

        (nLTS, ) = _unpack('<I', ctl)
        for i in range(nLTS):
            weights = _unpack('%if' % (nTS), ctl) 
            (labelLength, ) = _unpack('<L', ctl)
            (label, ) = _unpack('%is' % (labelLength), ctl)
            data['TS'].append((label, weights))

        (nLTA, ) = _unpack('<I', ctl)
        for i in range(nLTA):
            weights = _unpack('%if' % (nTA), ctl) 
            (labelLength, ) = _unpack('<L', ctl)
            (label, ) = _unpack('%is' % (labelLength), ctl)
            data['TA'].append((label, weights))

    return data

def getSliderVector(ctlFileName, label, sliderType = 'SS'):
    if sliderType[0] == "S":
        sliderType = "G" + sliderType[1]
    ctl = readCtl(ctlFileName)[sliderType]
    for ctlLabel, weights in ctl:
        if ctlLabel == label:
            return array(weights)

def sliderExists(ctlFileName, label, sliderType = 'SS'):
    if getSliderVector(ctlFileName, label , sliderType) == None:
        return False
    else:
        return True


def readCtlOld(ctlFileName):
    with open(ctlFileName, 'rb') as ctl:
        ctlData = {}

        fmt = '<8s7L'
        (dummy, geometryBasisVersion, textureBasisVersion, nGS, nGA, nTS, nTA, nLGS) = unpack_from(fmt, ctl.read(calcsize(fmt)))

        if dummy != b'FRCTL001':
            print("File is not a FaceGen binary .ctl file.")
            return False

        ctlData['LGS'] = {'labels':[], 'weights':[]}
        for _ in range(nLGS):
            fmt = '%ifL' % (nGS)
            ctlData['LGS']['weights'].append(list(unpack_from(fmt, ctl.read(calcsize(fmt)))))
            nLabels = ctlData['LGS']['weights'][-1].pop()
            if _ < nLGS - 1:
                fmt = '%is' % (nLabels)
            else:
                fmt = '<%isI' % (nLabels)
            ctlData['LGS']['labels'].extend(unpack_from(fmt, ctl.read(calcsize(fmt))))

        nLGA = ctlData['LGS']['labels'].pop()
        ctlData['LGA'] = {'labels':[], 'weights':[]}
        for _ in range(nLGA):
            fmt = '<%ifI' % (nGA)
            ctlData['LGA']['weights'].append(list(unpack_from(fmt, ctl.read(calcsize(fmt)))))
            nLabels = ctlData['LGA']['weights'][-1].pop()
            if _ < nLGA - 1:
                fmt = '%is' % (nLabels)
            else:
                fmt = '<%isI' % (nLabels)
            ctlData['LGA']['labels'].extend(unpack_from(fmt, ctl.read(calcsize(fmt))))

        nLTS = ctlData['LGA']['labels'].pop()
        ctlData['LTS'] = {'labels':[], 'weights':[]}
        for _ in range(nLTS):
            fmt = '<%ifI' % (nTS)
            ctlData['LTS']['weights'].append(list(unpack_from(fmt, ctl.read(calcsize(fmt)))))
            nLabels = ctlData['LTS']['weights'][-1].pop()
            if _ < nLTS - 1:
                fmt = '%is' % (nLabels)
            else:
                fmt = '<%isI' % (nLabels)
            ctlData['LTS']['labels'].extend(unpack_from(fmt, ctl.read(calcsize(fmt))))

        nLTA = ctlData['LTS']['labels'].pop()
        ctlData['LTA'] = {'labels':[], 'weights':[]}
        for _ in range(nLTA):
            fmt = '<%ifI' % (nTA)
            ctlData['LTA']['weights'].append(list(unpack_from(fmt, ctl.read(calcsize(fmt)))))
            nLabels = ctlData['LTA']['weights'][-1].pop()
            if _ < nLTA - 1:
                fmt = '%is' % (nLabels)
            else:
                fmt = '<%isI' % (nLabels)
            ctlData['LTA']['labels'].extend(unpack_from(fmt, ctl.read(calcsize(fmt))))

        # Second half of control file not yet implemented, was not needed until you were looking here.:)

        return ctlData

def insertSliderFromFG (ctlfile, fgfile, label = False, sliderType = 'SS' ):
    weights = normalize(array(readFG(fgfile)['SS']))
    if not label:
        label = "Vector based on %s" % fgfile

    if not sliderExists(ctlfile, label):
        insertSlider(label, weights.tolist(), 'SS', ctlfile)
    else:
        return False
    return True
    
def insertOrthogonalSlider (ctlfile, vec1label, vec2label, newlabel = False):
    vec1 = getSliderVector(ctlfile, vec1label)
    vec2 = getSliderVector(ctlfile, vec2label)

    (orthovec, weights) = orthogonalize(vec1, vec2)
    print("%s orthogonal to %s (%.4f * %s + %.4f * %s)" % (vec2label, vec1label, weights[0], vec1label, weights[1], vec2label))
    
    if newlabel:
        label = newlabel
    else:
        label = "%s orthogonal to %s (%.4f * %s + %.4f * %s)" % (vec2label, vec1label, weights[0], vec1label, weights[1], vec2label)
        
    if not getSliderVector(ctlfile, label) == None:
        print("Slider %s already exists in control file (%s)." % (label, ctlfile))
    else:
        if insertSlider(label, orthovec.tolist(), 'SS', ctlfile):
            print (label, "added to control file:", ctlfile)
        else:
            print (label, "NOT added to control file:", ctlfile)

def printControlLabels(ctl):
    for ctltype in ctl:
        for control in ctl[ctltype]:
            print(ctltype, control[0])

def findControlByLabel(ctl, label, ctltype = 'GS'):
    for control in ctl[ctltype]:
        if control[0] == label:
            return control[1]


if __name__ == "__main__":
    writeFG('test1.fg', range(50), range(30), range(50))
    print(readFG('test1.fg'))