from makeRoomingPrefs import MakeRoomingPrefs
from irving1985 import Irving1985
import numpy as np

# just pass in the file
prefsMaker = MakeRoomingPrefs('../roomingQuestionnaireResponses.csv')

# choose gender and club if desired, can delete to run on all
prefsList = prefsMaker.prefs()

# I thought we might need this to get Irving to work, but Irving doesn't work
# prefsList.insert(0, [0] * (len(prefsList) - 1))

prefsList = np.array(prefsList)
people = np.array(range(len(prefsList)))

# it prints!
# print prefsList
# print people
# import pdb; pdb.set_trace()

# these don't work
irvingMatcher = Irving1985(people, prefsList)
print(irvingMatcher.match())
