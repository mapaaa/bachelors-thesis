#!/usr/bin/python3
import argparse
import numpy as np
import sys
import re

from collections import deque

def needlemann_wunsch(a, b):
    n = len(a) + 1
    m = len(b) + 1
    d = np.zeros((n, m), dtype=int)

    global penalty
    d[0][0] = 0;
    for i in range(1, n):
        d[i][0] = d[i - 1][0] + penalty['GAP']

    for j in range(1, m):
        d[0][j] = d[0][j - 1] + penalty['GAP']

    for i in range(1, n):
        for j in range(1, m):
            d[i][j] = max(d[i - 1][j], d[i][j - 1]) + penalty['GAP']
            if a[i - 1] == b[j - 1]:
                d[i][j] = max(d[i][j], d[i - 1][j - 1] + penalty['MATCH'])
            else:
                d[i][j] = max(d[i][j], d[i - 1][j - 1] + penalty['MISMATCH'])

    q = deque()
    q.append((n - 1, m - 1, []))
    alignments = []
    while len(q) > 0:
        (i, j, p) = q.popleft()
        if i == 0 and j == 0:
            alignments.append(p)
            continue

        if i == 0:
            q.append((i, j - 1, p + ['GAP_A']))
            continue

        if j == 0:
            q.append((i - 1, j, p + ['GAP_B']))
            continue

        if d[i][j] == d[i - 1][j] + penalty['GAP']:
            q.append((i - 1, j, p + ['GAP_B']))

        if d[i][j] == d[i][j - 1] + penalty['GAP']:
            q.append((i, j - 1, p + ['GAP_A']))

        if a[i - 1] == b[j - 1]:
            if d[i][j] == d[i - 1][j - 1] + penalty['MATCH']:
                q.append((i - 1, j - 1, p + ['MATCH']))
        else:
            if d[i][j] == d[i - 1][j - 1] + penalty['MISMATCH']:
                q.append((i - 1, j - 1, p + ['MISMATCH']))
    ans = len(alignments)
    print(ans)
    for i in range(0, ans):
        new_a = "" 
        new_b = ""
        stars = ""
        x = 0
        y = 0
        for op in reversed(alignments[i]):
            if op == 'MATCH':
                new_a = new_a + a[x]
                new_b = new_b + b[y]
                x = x + 1
                y = y + 1
                stars = stars + '*'
            if op == 'GAP_A':
                new_a = new_a + '_'
                new_b = new_b + b[y]
                y = y + 1
                stars = stars + ' '
            if op == 'GAP_B':
                new_a = new_a + a[x]
                new_b = new_b + '_'
                x = x + 1
                stars = stars + ' '
            if op == 'MISMATCH':
                new_a = new_a + a[x]
                new_b = new_b + b[y]
                stars = stars + ' '
                x = x + 1
                y = y + 1
        print(new_a)
        print(new_b)
        print(stars)

def main():
    parser = argparse.ArgumentParser(description='Needlemann-Wunsch alignment')
    parser.add_argument('input', type=str, help='File for input')
    parser.add_argument('--output', type=str, help='File for output')
    parser.add_argument('--match', type=int, help='Penalty for match')
    parser.add_argument('--mismatch', type=int, help='Penalty for mismatc')
    parser.add_argument('--gap', type=int, help='Penalty for gap')
    args = parser.parse_args()

    global penalty
    penalty = {'MATCH': 1, 'MISMATCH': -1, 'GAP': -2};

    if args.output:
        output = args.output
    else:
        print('Will save results here {0}.out'.format(args.input))
        output = args.input + '.out'

    if args.match:
        penalty['MATCH'] = args.match

    if args.mismatch:
        penalty['MISMATCH'] = args.mismatch

    if args.gap:
        penalty['GAP'] = args.gap

    fo = open(output, 'w')
    sys.stdout = fo

    if args.input:
        with open(args.input, 'r') as f:
            for line in f:
                line = line.strip('\n')
                words = line.split('_')
                print(words[0] + '_' + words[1])
                needlemann_wunsch(words[0], words[1])
                print('\n')
    fo.close
    

if __name__ == '__main__':
    sys.exit(main())
