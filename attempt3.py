import music21 as m
import random
from math import floor
from markov import intMarkovN, nextRandom

filelist = ["Midis/bach-invention-08.mid", \
            "Midis/bach-invention-09.mid"]

def filesToStreams(filelist):
    streamlist = []
    for file in filelist:
        mf = m.midi.MidiFile()
        mf.open(file)
        mf.read()
        s = m.midi.translate.midiFileToStream(mf)
        k = s[0].getElementsByClass("Key")[0]
        i = m.interval.Interval(k.tonic, m.pitch.Pitch('C'))
        sNew = s.transpose(i)
        mf.close()
        streamlist.append(sNew)

    return streamlist

midilist = filesToStreams(filelist)

'''
chords = midilist[0].chordify()
for c in chords.getElementsByClass("Chord"):
    c.closedPosition(inPlace = True)
'''

def splitMeasure(part):
    partM = m.stream.Stream()

    for e in part:
        if len(partM) - 1 < int(floor(e.offset)):
            s = m.stream.Stream()
            s.append(e)
            partM.append(s)
        else:
            partM[int(floor(e.offset))].append(e)

    return partM

def analyzeMeasure(M):
    n = M.getElementsByClass("Note")
    p = list(set([nt.pitch for nt in n]))
    if(len(p) == 0):
        return
    elif len(p) > 4 or len(p) < 3:
        return m.chord.Chord([p[0], p[0].transpose('M3'), p[0].transpose('P5')])
    else:
        return m.chord.Chord(p).closedPosition()

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


def getSeq(List):
    items = []
    sequence = []
    for e in List:
        if e not in items:
            items.append(e)
            sequence.append(len(items) - 1)
        else:
            sequence.append(items.index(e))
    return [items, sequence]

measures = []
chords = []

for song in midilist:
    part = song[0]
    for e in splitMeasure(part):
        measures.append(readMeasure(e))
        c = analyzeMeasure(e)
        if c != None:
            chords.append(c)

mIt, mSeq = getSeq(measures)
cIt, cSeq = getSeq(chords)

output = m.stream.Stream()

for c in cIt:
    output.append(c)

output.show('midi', fp= r"Generated\sample3.mid")


