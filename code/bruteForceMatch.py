from irving1985Mod import Irving1985Mod
import random, pandas
import numpy as np

''' finds possible swaps in preference ordering '''
def findSwitches(scores):
    indicesToSwitch = [] # list of (person, switchIndex1, switchIndex2)
    for r in range(len(scores)):
        for i in range(len(scores) - 1):
            for j in range(i, len(scores) - 1):
                if i != j and scores[r][i][1] == scores[r][j][1]:
                    indicesToSwitch.append((r, i, j))
    return indicesToSwitch

''' swaps n pairs with same score '''
def perturb(scores, indices, N):
    swaps = random.sample(indices, min(N, len(indices))) # swap N random pairs
    for swap in swaps:
        firstScore = scores[swap[0]][swap[1]]
        secondScore = scores[swap[0]][swap[2]]
        scores[swap[0]][swap[1]] = secondScore
        scores[swap[0]][swap[2]] = firstScore
    return scores

''' if at first match doesn't come: perturb, try again '''
def bruteForceMatch(scores, attempts):
    switches = findSwitches(scores)
    # make preference ordering from scores
    prefs = [[i[0] for i in scores[j]][:-1] for j in range(len(scores))]
    for n in range(attempts):
        matcher = Irving1985Mod(np.array(range(len(prefs))), np.array(prefs))
        stableMatching, match = matcher.match()
        if not stableMatching:
            # perturb scores, make prefs from new scores
            scores = perturb(scores, switches, 5)
            prefs = [[i[0] for i in scores[j]][:-1] for j in range(len(scores))]
        else:
            return match
    # if no stable matchings ever found
    return []
