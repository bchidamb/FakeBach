from music21 import *
import random
from math import floor

mf = midi.MidiFile()

mf.open("Midis/bach-invention-08.mid")
mf.read()
mf.close()

bachinv8 = midi.translate.midiFileToStream(mf)

part0 = bachinv8[0].getElementsByClass(["Note","Rest"])

part0M = stream.Stream()

for i in range(int(floor(part0[-1].offset))):
    part0M.append([])

for e in part0:
    if len(part0M)-1 < int(floor(e.offset)):
        s = stream.Stream()
        s.append(e)
        part0M.append(s)
    else:
        part0M[int(floor(e.offset))].append(e)


#-1 = start, 0 = down, 1 = same, 2 = up, 3 = rest

def readMeasure(M):
    seq = []
    nC = 0
    Mn = M.getElementsByClass("Note")
    for o in M:
        if(o in Mn):
            if(nC == 0):
                seq.append([-1, o.duration])
            elif(Mn[nC] < Mn[nC - 1]):
                seq.append([0, o.duration])
            elif(Mn[nC] == Mn[nC - 1]):
                seq.append([1, o.duration])
            else:
                seq.append([2, o.duration])
            nC += 1
        else:
            seq.append([3, o.duration])
    return seq

def intMarkov(seq):
    start = None
    matrix = dict()

    for i in range(len(seq)-1):
        n1 = seq[i]
        n2 = seq[i+1]

        if(n1 in matrix):
            if(n2 in matrix[n1]):
                matrix[n1][n2] += 1
            else:
                matrix[n1][n2] = 1
        else:
            matrix[n1] = {n2: 1}
        if(start == None):
            start = n1

    return {k0: {k1: matrix[k0][k1]/sum(matrix[k0].values()) for k1 in matrix[k0]} for k0 in matrix}

def nextRandom(p):
    if(len(p) == 0):
        return None
    r = random.uniform(0, sum(p.values()))
    for k in p:
        r -= p[k]
        if(r < 0.0001):
            break
    return k
    

measures = []
mSeq = []

for measure in part0M:
    rM = readMeasure(measure)
    if(rM not in measures):
        measures.append(rM)
    mSeq.append(measures.index(rM))

matrix = intMarkov(mSeq)

notes = []
nSeq = []

for nt in part0.getElementsByClass("Note"):
    if(nt.pitch not in notes):
        notes.append(nt.pitch)
    nSeq.append(notes.index(nt.pitch))

mTrix = intMarkov(mSeq)
nTrix = intMarkov(nSeq)

mOut = [0]
nOut = [0]

fakeBach = stream.Stream()

nextM = 0
lastN = 0

for i in range(120):
    for o in measures[nextM]:
        if(o[0] == 3):
            fakeBach.append(note.Rest(duration = o[1]))
        else:
            if(o[0] == -1):
                lastN = nextRandom({x:nTrix[lastN][x] for x in nTrix[lastN]})
            elif(o[0] == 0):
                lastN = nextRandom({x:nTrix[lastN][x] for x in nTrix[lastN] if x < lastN})
            elif(o[0] == 2):
                lastN = nextRandom({x:nTrix[lastN][x] for x in nTrix[lastN] if x > lastN})
            if(lastN == None):
                lastN = nOut[-2] #(-2): this helps prevent repeat notes
            nOut.append(lastN)
            fakeBach.append(note.Note(notes[lastN], duration = o[1]))
    nextM = nextRandom(mTrix[nextM])
    mOut.append(measures[nextM])

fakeBach.show('midi', fp= r"Generated\sample2.mid")



    
