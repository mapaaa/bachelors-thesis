#!/usr/bin/python3

import argparse
import itertools
import numpy as np
import os
import sys

import threading

from copy import deepcopy
from munkres import Munkres, DISALLOWED, print_matrix


CNT_BEST_PRODUCTIONS = 5 

# Calculeaza o matrice de dimensiune (n, m) unde
# n = numarul de cuvinte din univers
# m = numarul de clasamente
# _ord[i][j] = pozitia cuvantului i in clasamentul j
def make_ord(u, rankings):
    _ord = np.zeros((len(u), len(rankings)), dtype=int)  
    for i, word_u in enumerate(u):
        for j in range(len(rankings)):
            _ord[i][j] = 0
            for k, word_r in enumerate(rankings[j]):
                if word_u == word_r:
                    _ord[i][j] += CNT_BEST_PRODUCTIONS - k
                    break
    return _ord


# GAP = General Assignment Problem
def solveGAP(M, t):
    w = deepcopy(M)
    m = w.tolist()
    # for i in range(len(m)):
        # for j in range(len(m[i])):
            # if m[i][j] == 1e9:
                # m[i][j] = DISALLOWED

    #print_matrix(m)
    algo = Munkres()
    indexes = []
    try:
        indexes = algo.compute(m)
    except:
        print('Error in solveGAP')
        return []
    return indexes


# Doua solutii sunt diferite daca difera prin cel putin o muchie. Astfel,
# pornim de la o solutie, fixam o muchie pe care nu vrem sa o folosim si
# verificam daca exista o a doua solutie (ce nu foloseste muchia fixata).
def P(M, t, S, s, sink):
    for (x, y) in S:
        if y < sink:
            temp = M[x][y]
            M[x][y] = 1e9
        else:
            copie_linie = deepcopy(M[x,:])
            for j in range(sink, M.shape[1]):
                M[x][j] = 1e9

        S_prim = solveGAP(M, t)
        if len(S_prim) != 0:
            s1 = 0
            for (x1, y1) in S_prim:
                s1 = s1 + M[x1][y1]
            if s1 == s:
                if y < sink:
                    M[x][y] = temp
                else:
                    M[x,:] = deepcopy(copie_linie)
                return S_prim

        if y < sink:
            M[x][y] = temp
        else:
            M[x,:] = deepcopy(copie_linie)
    return []


def solve(M1, t1, S1, E, sink, i_x, i_y, level):
   # print('S1=', [(i_x[x], i_y[y]) for (x, y) in S1])
    s1 = 0
    for (x, y) in S1:
        s1 = s1 + M1[x][y]

    S1_prim = P(M1, t1, S1, s1, sink)
    for i in range(len(S1_prim)):
        if S1_prim[i][1] > sink:
            S1_prim[i] = (S1_prim[i][0], sink)
    if len(S1_prim) == 0:
        return
    #print('S1_prim=', [(i_x[x], i_y[y]) for (x, y) in S1_prim])

    # adaug la solutie etichetele reale
    S1_c = S1_prim.copy()
    for i in range(len(S1_c)):
        (x, y) = S1_c[i]
        S1_c[i] = (i_x[x], i_y[y])
    newsol = list(set().union(S1_c, E))
    newsol.sort()
    if newsol not in Sol:
        Sol.append(newsol)

    (x, y) = (0, 0)
    for (x1, y1) in S1: 
        if (x1, y1) not in S1_prim:
            x = x1
            y = y1
            break

    # subproblema 1: nu avem voie sa folosim muchia (x, y)
    M1[x][y] = 1e9
    if y >= sink:
        # cuvantul x nu mai poate fi asignat niciunei alte poziti
        for i in range(sink, M1.shape[1]):
            M1[x][i] = 1e9

    args1 = (np.copy(M1), t1, S1_prim.copy(),  E.copy(), sink, i_x.copy(), i_y.copy(), level+1)
    #solve(np.copy(M1), t1, S1_prim.copy(), E.copy(), sink, i_x.copy(), i_y.copy())

    # subproblema 2: folosim muchia (x, y)
    if (i_x[x], i_y[y]) not in E:
        E.append((i_x[x], i_y[y]))

    S1.remove((x, y))
    # stergem linia x
    M1 = np.delete(M1, (x), axis=0)
    # actualizam etichetele
    i_x.pop(x)
    for i in range(len(S1)):
        if S1[i][0] >= x:
            S1[i] = (S1[i][0] - 1, S1[i][1])
        
    if y < sink: 
        M1 = np.delete(M1, (y), axis=1)
        i_y.pop(y)
        for i in range(len(S1)):
            if S1[i][1] >= y:
                S1[i] = (S1[i][0], S1[i][1] - 1)
        sink -= 1

    else:
        j = M1.shape[1] - 1
        M1 = np.delete(M1, (j), axis=1)
        i_y.pop(j)
        for i in range(len(S1)):
            if S1[i][1] >= j:
                S1[i] = (S1[i][0], S1[i][1] - 1)
    args2 = (np.copy(M1), t1-1, S1.copy(), E.copy(), sink, i_x.copy(), i_y.copy(), level+1)
    if level <= 15:
        thread2 = threading.Thread(target=solve, args=args2)
        thread2.start()
        solve(args1[0], args1[1], args1[2], args1[3], args1[4], args1[5], args1[6], args1[7])
        thread2.join()
    else:
        solve(args1[0], args1[1], args1[2], args1[3], args1[4], args1[5], args1[6], args1[7])
        solve(args2[0], args2[1], args2[2], args2[3], args2[4], args2[5], args2[6], args2[7])
        #pool.map(solve, [args1, args2])
    #solve(np.copy(M1), t1-1, S1.copy(), E.copy(), sink, i_x.copy(), i_y.copy())


# w = matricea de costuri
# t = marimea cuplajului dorit
# AAP = All Assignments Problem
# Adapted from F. Manea and C.Ploscaru / A Generalization of the Assignment
# Problem and its Application to the Rank Aggregation Problem
def AAP(M, t):
    global Sol
    Sol = []
    S = solveGAP(M, t)
    if len(S) == 0:
        return Sol

    u = M.shape[0]
    # etichetele liniilor din matricea de costuri (cuvintelor)
    i_x = list(range(u)) 
    # etichetele coloanelor din matricea de costuri (pozitiilor)
    i_y = list(range(u)) 

    # Presupunem ca toate cuvintele care apar in agregare dupa lungimea finala 
    # dorita se afla de fapt pe aceeasi pozitie
    sink = CNT_BEST_PRODUCTIONS
    for i in range(len(S)):
        if S[i][1] > sink:
            S[i] = (S[i][0], sink)

    S.sort()
    Sol = [S]
    thread1 = threading.Thread(target=solve, args=(np.copy(M), t, S.copy(), [], sink, i_x.copy(), i_y.copy(), 1))
    thread1.start()
    thread1.join()
    #args = (np.copy(M), t, S.copy(), [], sink, i_x.copy(), i_y.copy(), 1)
    #result = pool.map(solve, args)
    return Sol


# rda = Rank Distance Aggregation
def RDAs(rankings, latin_word):
    l = CNT_BEST_PRODUCTIONS
    # u = universul de cuvinte
    u = list(set().union(*[x for x in rankings]))
    print('Univers: ' + str(u))
    _ord = make_ord(u, rankings)
    w = np.zeros((len(u), len(u)), dtype=int)
    for i in range(len(u)):
        for pos in range(len(u)):
            for j in range(len(rankings)):
                if pos <= CNT_BEST_PRODUCTIONS:
                    w[i][pos] += abs(_ord[i][j] - CNT_BEST_PRODUCTIONS + pos)
                else:
                    w[i][pos] += abs(_ord[i][j])
    solutions = AAP(w, len(u))

    best = []
    for i in range(len(solutions)):
        sir = 'SOURCE_' + latin_word
        aggregation = [''] * len(u)
        for (x, y) in solutions[i]:
            aggregation[y] = u[x]
        for word in range(CNT_BEST_PRODUCTIONS):
            if word == 0:
                sir = sir + '_' + aggregation[word]
            else:
                sir = sir + ' | ' + aggregation[word]
        best.append(sir)
    return best


def parse(f, latin_dict):
    sep0 = '_'
    sep1 = '|'
    for line in f:
        line = line.strip('\n')
        line = line.replace(' ', '')
        if line[len(line) - 1] != sep1:
            line = line + sep1    # sep1 = '|'

        i = line.find(sep0)    # sep0 = '_'
        modern_word = line[:i]
        i += 1
        j = line.find(sep0, i)
        latin_word = line[i:j]
      
        i = j + 1
        j = line.find(sep1, i)
        ranking = []
        while j != -1:
            ranking.append(line[i:j])
            i = j + 1
            j = line.find(sep1, i)    # sep1 = '|'
        if latin_word in latin_dict:
            latin_dict[latin_word].append(ranking[0:CNT_BEST_PRODUCTIONS])
        else:
            latin_dict[latin_word] = [ranking[0:CNT_BEST_PRODUCTIONS]]


def main():
    parser = argparse.ArgumentParser(description='Outputs all best rank distance aggregations')
    parser.add_argument('input', type=str, help='Input directory')

    args = parser.parse_args()
    if args.input is None:
        print('Must specify input file or directory!')
        return
    #print('Threading: ' + str(threading.active_count()))
    filepath = args.input + '/'
    for dir_name in os.listdir(filepath):
        latin_dict = {}
        print('Processing ' + dir_name)
        for file_name in os.listdir(filepath + dir_name):
            f = open(filepath + dir_name + '/' + file_name, 'r')
            parse(f, latin_dict)
            f.close
        out = open(str(dir_name) + '-all-best-' + str(CNT_BEST_PRODUCTIONS) + '.txt', 'w')
        for latin_word in latin_dict:
            print(latin_word)
            best = RDAs(latin_dict[latin_word], latin_word)
            for sir in best:
                out.write(sir+'\n')
        out.close


if __name__ == '__main__':
    sys.exit(main())
