from irving1985 import Irving1985
import numpy as np
import random
from collections import defaultdict
import matplotlib.pyplot as plt

# increment number of people
start_n = 4
end_n = 50
inter_n = 2

iters_per_n = 15
samples_per_n = 15

stable_rate = defaultdict(list)
for n in range(start_n, end_n, inter_n):
    result = []
    everybody = list(range(n))
    for i in range(iters_per_n):
        for j in range(samples_per_n):
            preferences = []
            for p in everybody:
                preference_p = list(everybody)
                preference_p.remove(p)
                random.shuffle(preference_p)
                preferences.append(preference_p)
            preferenceLists = np.array(preferences)
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
plt.title("Stability of Irving Algorithm")
plt.xlabel("Number of People in Match")
plt.ylabel("Percentage with Stable Match Found")
plt.show()
#ffc34d -- orange
#4da6ff -- blue
