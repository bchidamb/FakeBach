import music21 as m
from math import floor
from markov import autoGenerate

filelist = ["Midis/bach-invention-01.mid", \
            "Midis/bach-invention-03.mid", \
            "Midis/bach-invention-05.mid", \
            "Midis/bach-invention-06.mid", \
            "Midis/bach-invention-08.mid", \
            "Midis/bach-invention-10.mid", \
            "Midis/bach-invention-12.mid", \
            "Midis/bach-invention-14.mid"]

def filesToStreams(filelist):
    streamlist = []
    for file in filelist:
        mf = m.midi.MidiFile()
        mf.open(file)
        mf.read()
        s = m.midi.translate.midiFileToStream(mf)
        try:
            k = s[0].getElementsByClass("Key")[0]
        except:
            k = s.analyze('key')
        i = m.interval.Interval(k.tonic, m.pitch.Pitch('C'))
        sNew = s.transpose(i)
        mf.close()
        streamlist.append(sNew)

    return streamlist

midilist = filesToStreams(filelist)

def splitBeat(part):
    partB = m.stream.Stream()
    partB.append(m.meter.TimeSignature('1/4'))
    for e in part.getElementsByClass(["Note", "Rest"]):
        partB.append(e)
    return partB.makeMeasures()

def readBeat(M):
    seq = []
    Mn = M.getElementsByClass("Note")
    for o in M:
        if o.duration.quarterLength > 0.0:
            if(o in Mn):
                seq.append([0, o.duration])
            else:
                seq.append([1, o.duration])
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


beats = []
notes = []

for song in midilist:
    part = song[0]
    for e in splitBeat(part):
        beats.append(readBeat(e))
    for nt in part.getElementsByClass(["Note"]):
        notes.append(nt.pitch)

bIt, bSeq = getSeq(beats)
nIt, nSeq = getSeq(notes)

B, N = (2, 3) #These settings are ideal.
'''
Report b = 2
Sequence length: 844
Markov entries: 228
Report n = 3
Sequence length: 2306
Markov entries: 912
'''

#print("Report b = %d" % B)
bSeqNew = autoGenerate(bSeq, 120, B)
bNew = [bIt[i] for i in bSeqNew]

for b in bIt:
    if len(b) > 10:
        print(b)

c = 0
for b in bNew:
    for e in b:
        if e[0] == 0:
            c += 1

#print("Report n = %d" % N)
nSeqNew = autoGenerate(nSeq, c, N)

part1 = m.stream.Part()


j = 0
for b in bNew:
    for e in b:
        if e[0] == 0:
            part1.append(m.note.Note(nIt[nSeqNew[j]], duration = e[1]))
            j += 1
        else:
            part1.append(m.note.Rest(duration = e[1]))

part2 = m.stream.Part()

bSeqNew = autoGenerate(bSeq, 120, B) #this is a new generated sequence
bNew = [bIt[i] for i in bSeqNew]

j = 0
index = 0
for i, b in enumerate(bNew):
    index = len(part1.getElementsByOffset(0, i+3.99).getElementsByClass("Note"))
    j = 0
    for e in b:
        if e[0] == 0:
            nt = m.note.Note(nIt[nSeqNew[(index+j)%len(nSeqNew)]], duration = e[1])
            part2.append(nt.transpose("P-8"))
            j += 1
        else:
            rs = m.note.Rest(duration = e[1])
            part2.append(rs)

for e in part2:
    e.offset += 4.0


fakeBach = m.stream.Stream([part1, part2])

fakeBach.show('midi')

#fakeBach.show('midi', fp = "Generated\song.midi")
