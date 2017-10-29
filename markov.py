import random

def intMarkov1(seq):
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

    return matrix

def intMarkovN(seq, n, wrap):
    m = max(seq)
    matrix = {-1:{n:m}}

    if(wrap):
        seq += seq[:n]

    for i in range(len(seq)-n):
        p = intEncode([seq[i+j] for j in range(n)], m)
        q = seq[i+n]

        if(p in matrix):
            if(q in matrix[p]):
                matrix[p][q] += 1
            else:
                matrix[p][q] = 1
        else:
            matrix[p] = {q: 1}

    return matrix

#g = list of ints to be encoded, m = largest int
def intEncode(g, m):
    return sum([g[i]*(m+1)**i for i in range(len(g))])

#e = encoded int, n = number of ints in list
def intDecode(e, m, n):
    out = []
    for i in range(n):
        out.append(e % (m+1))
        e = e//(m+1)
    return out

def nextRandom(p):
    if(len(p) == 0):
        return None
    r = random.uniform(0, sum(p.values()))
    for k in p:
        r -= p[k]
        if(r < 0.0001):
            break
    return k

def generate(start, matrix, l, report=False):
    if report:
        print("Markov entries: %d" % len(matrix))
    
    out = start
    n = [k for k in matrix[-1]][0]
    m = matrix[-1][n]

    if(len(start) != n):
        return None
    
    for i in range(l-n):
        out += [nextRandom(matrix[intEncode(out[-n:],m)])]

    return out

def autoGenerate(seq, l, n, report=False):
    if report:
        print("Sequence length: %d" % len(seq))
    return generate(seq[:n], intMarkovN(seq, n, True), l, report)
