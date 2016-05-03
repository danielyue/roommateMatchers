from irving1985 import Irving1985
from makeRoomingPrefs import MakeRoomingPrefs
import numpy as np
import random
from collections import defaultdict
import matplotlib.pyplot as plt

# runs using real dataframe
prefsMaker = MakeRoomingPrefs('../roomingQuestionnaireResponses.csv')

# increment number of people
start_n = 4
end_n = 50
inter_n = 2

iters_per_n = 15
samples_per_n = 15

stable_rate = defaultdict(list)
for n in range(start_n, end_n, inter_n):
    print n
    result = []
    everybody = list(range(n))
    for i in range(iters_per_n):
        for j in range(samples_per_n):
            preferenceLists = np.array(prefsMaker.prefs(randN=n))
            # import pdb; pdb.set_trace()
            matcher = Irving1985(everybody, preferenceLists)
            result.append(matcher.match())
        stable_rate[n].append(float(sum(result)) / len(result))
# print(stable_rate)
stds = []
means = []
ns = []
for n, results in stable_rate.items():
    stds.append(np.std(results))
    means.append(np.mean(results))
    ns.append(n)

# plt.plot(ns, means)
# plt.errorbar(ns,means,yerr=stds)
# plt.show()

radius = 8
plt.scatter(ns,means,s=radius**2,c='#ffc34d',edgecolors='none')
plt.errorbar(ns,means,fmt='none',yerr=stds, ecolor='k', elinewidth=1.5)
plt.ylim([0,1])
plt.title("Stability of Irving Algorithm, Harvard Data")
plt.xlabel("Number of People in Match")
plt.ylabel("Percentage with Stable Match Found")
plt.savefig("../stabilityHarvard.png")
#ffc34d -- orange
#4da6ff -- blue
