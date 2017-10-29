from music21 import *
import random

mf = midi.MidiFile()

mf.open("Midis/bach-invention-08.mid")
mf.read()
mf.close()

bachinv8 = midi.translate.midiFileToStream(mf)

sequence = []
matrix = [[0 for i in range(7)] for j in range(7)]

for n in bachinv8[0]:
    try:
        if(n.name == 'F'):
            sequence.append(0)
        elif(n.name == 'G'):
            sequence.append(1)
        elif(n.name == 'A'):
            sequence.append(2)
        elif(n.name == 'B-'):
            sequence.append(3)
        elif(n.name == 'C'):
            sequence.append(4)
        elif(n.name == 'D'):
            sequence.append(5)
        elif(n.name == 'E'):
            sequence.append(6)
    except:
        print(n,"produced an error")

d = 0
while(True):
    try:
        matrix[sequence[d]][sequence[d+1]] += 1
        d += 1
    except:
        break
    
matrix2 = [[(matrix[i][j])**2 for j in range(7)] for i in range(7)]

print(matrix)

print(matrix2)

matrixNorm = [[matrix2[i][j]/sum(matrix2[i]) for j in range(7)] for i in range(7)]


fakeBach = stream.Stream()

k = note.Note("F4")
k.duration = duration.Duration("eighth")

fakeBach.append(k)
last = 0

for i in range(119):
    r = random.random()
    k = note.Note("F4")
    k.duration = duration.Duration("eighth")
    a = 0
    for a in range(7):
        r -= matrixNorm[last][a]
        if(r < 0.0001):
            break
    if(a == 0):
        fakeBach.append(k)
    elif(a == 3):
        fakeBach.append(k.transpose("P4"))
    elif(a == 4):
        fakeBach.append(k.transpose("P5"))
    else:
        fakeBach.append(k.transpose("M" + str(a+1)))
    last = a

fakeBach.show('midi', fp= r"Generated\sample1.mid")


        
    
