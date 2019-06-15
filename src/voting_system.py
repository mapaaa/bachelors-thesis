import itertools
import numpy as np
import os
import sys

from munkres import Munkres, DISALLOWED, print_matrix
from copy import deepcopy


CNT_BEST_PRODUCTIONS = 5 
COV5 = 1


def start_vote(rankings, latin_word):
    l = CNT_BEST_PRODUCTIONS
    u = list(set().union(*[x[1] for x in rankings]))
    cnt_votes = np.zeros((len(u), 1), dtype=int)

    for ranking in rankings:
        actual_ranking = ranking[1]
        for idx, word in enumerate(actual_ranking):
            ind = u.index(word)
            cnt_votes[ind] += idx

    result = list(zip(cnt_votes, u))
    result.sort()
    best = 'SOURCE_' + latin_word
    for i in range(len(result)):
        if i == 0:
            best += '_' + result[i][1]
        else:
            if result[i][0] == result[i - 1][0]:
                best += '-' +result[i][1]
            else:
                best += ' | ' + result[i][1]
    return best


def main():
    filepath = 'voting_input_neatestate/'
    weights = { 
        'neatestate': {
              'ne': [0.2658959537572254, 0.44508670520231214, 0.5028901734104047, 0.5375722543352601, 0.5838150289017341, 0.6127167630057804],
              'fr': [0.0935672514619883, 0.23976608187134502, 0.2982456140350877, 0.3742690058479532, 0.40350877192982454, 0.45614035087719296],
              'it': [0.2786885245901639, 0.5901639344262295, 0.639344262295082, 0.6885245901639344, 0.7103825136612022, 0.7213114754098361],
              'pt': [0.21910112359550563, 0.4438202247191011, 0.4887640449438202, 0.5337078651685393, 0.5561797752808989, 0.5786516853932584],
              'ro': [0.1557377049180328, 0.39344262295081966, 0.4098360655737705, 0.47540983606557374, 0.5491803278688525, 0.5819672131147541]
         },

        'ripeanu': {
                      'es': [0.2658959537572254, 0.44508670520231214, 0.5028901734104047, 0.5375722543352601, 0.5838150289017341, 0.6127167630057804],
                      'fr': [0.0935672514619883, 0.23976608187134502, 0.2982456140350877, 0.3742690058479532, 0.40350877192982454, 0.45614035087719296],
                      'it': [0.2786885245901639, 0.5901639344262295, 0.639344262295082, 0.6885245901639344, 0.7103825136612022, 0.7213114754098361],
                      'pt': [0.21910112359550563, 0.4438202247191011, 0.4887640449438202, 0.5337078651685393, 0.5561797752808989, 0.5786516853932584],
                      'ro': [0.1557377049180328, 0.39344262295081966, 0.4098360655737705, 0.47540983606557374, 0.5491803278688525, 0.5819672131147541]
                    },
        'bouchard-o': {
            'es': [0.1282051282051282, 0.24786324786324787, 0.28205128205128205, 0.2905982905982906, 0.3076923076923077, 0.3076923076923077],
            'it': [0.1794871794871795, 0.3333333333333333, 0.38461538461538464, 0.4017094017094017, 0.42735042735042733, 0.4358974358974359],
            'pt': [0.1282051282051282, 0.29914529914529914, 0.3247863247863248, 0.3418803418803419, 0.3418803418803419, 0.37606837606837606]

        },
        'lrec': {
            'es': [0.44254658385093165, 0.6009316770186336, 0.6428571428571429, 0.6754658385093167, 0.6940993788819876, 0.7158385093167702],
            'fr': [0.42391304347826086, 0.577639751552795, 0.6071428571428571, 0.6444099378881988, 0.6599378881987578, 0.6816770186335404],
            'it': [0.422360248447205, 0.6288819875776398, 0.6583850931677019, 0.6894409937888198, 0.7096273291925466, 0.7236024844720497],
            'pt': [0.38354037267080743, 0.5729813664596274, 0.6133540372670807, 0.6444099378881988, 0.6739130434782609, 0.6909937888198758],
            'ro': [0.422360248447205, 0.59472049689441, 0.6335403726708074, 0.6754658385093167, 0.6940993788819876, 0.7251552795031055],
        }
    }
    for dir_name in os.listdir(filepath):
        out = open(str(dir_name) + '-voting-result-5.txt', 'w')
        latin_dict = {}
        print(dir_name)
        for file_name in os.listdir(filepath + dir_name):
            f = open(filepath + dir_name + '/' + file_name, 'r')
            for line in f:
                line = line.strip('\n')
                line = line.replace(' ', '')
                line = line + '|'
                first_sep = line.find('_')
                modern_word = line[:first_sep]
                second_sep = line.find('_', first_sep+1)
                latin_word = line[first_sep+1:second_sep]
              
                x = second_sep + 1
                y = line.find('|', x)
                ranking = []
                while y != -1:
                    ranking.append(line[x:y])
                    x = y + 1
                    y = line.find('|', x)
                if latin_word in latin_dict:
                    latin_dict[latin_word].append((weights[dir_name][file_name[0:2]][COV5], ranking[0:CNT_BEST_PRODUCTIONS]))
                else:
                    latin_dict[latin_word] = [(weights[dir_name][file_name[0:2]][COV5], ranking[0:CNT_BEST_PRODUCTIONS])]
        for latin_word in latin_dict:
            print(latin_word)
            best = start_vote(latin_dict[latin_word], latin_word)
            out.write(best+'\n')


if __name__ == '__main__':
    sys.exit(main())
