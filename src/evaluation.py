#!/usr/bin/python3
import argparse
import numpy as np
import sys
import re


def parse(f):
    sep0 = '_'
    sep1 = '|'
    result = []
    for line in f:
        productions = []

        line = line.strip('\n')
        line = line.replace(' ', '')
        if line[len(line)-1] != sep1:
            line += sep1    # sep1 = '|'

        i = line.find(sep0)+1    # sep0 = '_'
        j = line.find(sep0, i)
        latin_word = line[i:j]

        i = j + 1
        j = line.find(sep1, i)    # sep1 = '|'
        while j != -1:
            productions.append(line[i:j])
            i = j + 1
            j = line.find(sep1, i)    # sep1 = '|'

        result.append((latin_word, productions))
    return result


def compute_cov(results, ln):
    cov = np.zeros(len(ln), dtype=float) 
    for j in range(len(ln)):
        n = ln[j]
        if n <= len(results[0][1]):
            cnt = 0
            for result in results:
                latin_word = result[0]
                for i in range(n):
                    if result[1][i] == latin_word:
                        cnt += 1
                        break
            cov[j] = cnt / len(results)
        else:
            cov[j] = 0
    return cov


def compute_mrr(results, ln):
    mrr = np.zeros(len(ln), dtype=float) 
    for j in range(len(ln)):
        n = ln[j]
        if n <= len(results[0][1]):
            for result in results:
                latin_word = result[0]
                for i in range(n):
                    if result[1][i] == latin_word:
                        mrr[j] += 1 / (i+1)
                        break
            mrr[j] = mrr[j] / len(results)
        else:
            mrr[j] = 0
    return mrr


def levenshtein_distance(a, b):
    n = len(a) + 1
    m = len(b) + 1
    d = np.zeros((n, m), dtype=int)

    penalty = {'MATCH': 0, 'INSERT': 1, 'DELETE': 1, 'CHANGE': 1};
    d[0][0] = 0;
    for i in range(1, n):
        d[i][0] = d[i-1][0] + penalty['DELETE']

    for j in range(1, m):
        d[0][j] = d[0][j-1] + penalty['INSERT']

    for i in range(1, n):
        for j in range(1, m):
            if a[i-1] == b[j-1]:
                d[i][j] = min(min(d[i-1][j-1] + penalty['MATCH'], d[i-1][j] + penalty['DELETE']), d[i][j-1] + penalty['INSERT'])
            else:
                d[i][j] = min(min(d[i-1][j-1] + penalty['CHANGE'], d[i-1][j] + penalty['DELETE']), d[i][j-1] + penalty['INSERT'])
    return d[n-1][m-1]


def compute_edit(results):
    edit_dist = 0.0
    edit_dist_norm = 0.0
    for result in results:
        latin_word = result[0]
        produced_word = result[1][0]
        edit_dist += levenshtein_distance(latin_word, produced_word)
        edit_dist_norm += levenshtein_distance(latin_word, produced_word) / max(len(latin_word), len(produced_word))
    edit_dist = edit_dist / len(results)
    edit_dist_norm = edit_dist_norm / len(results)
    return edit_dist, edit_dist_norm


def main():
    parser = argparse.ArgumentParser(description='Evaluation measures')
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('--output', type=str, help='Output file')
    args = parser.parse_args()

    if args.output:
        outputFile = args.output
    else:
        print('Will save results here {0}.out'.format(args.input))
        outputFile = args.input + '.out'

    if args.input:
        inputFile = args.input
    else:
        print('ERROR: Missing input file!')
        return
    inp = open(inputFile, 'r')
    results = parse(inp)
    inp.close

    cov = compute_cov(results, [1,5])
    mrr = compute_mrr(results, [1,5])
    edit, edit_norm = compute_edit(results)
    
    out = open(outputFile, 'w')
    out.write('COV:')
    for c in cov:
        out.write(' ' + str(c) + ' |')
    out.write('\n')
    out.write('MRR:')
    for m in mrr:
        out.write(' ' + str(m) + ' |')
    out.write('\n')
    out.write('EDIT_NORM: ' + str(edit_norm) + '\n')
    out.write('EDIT: ' + str(edit) + '\n')
    out.close
    

if __name__ == '__main__':
    sys.exit(main())
