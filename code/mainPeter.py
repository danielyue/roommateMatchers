from makeRoomingPrefs import MakeRoomingPrefs
from irving1985 import Irving1985
import numpy as np

# just pass in the file
prefsMaker = MakeRoomingPrefs('../roomingQuestionnaireResponses.csv')

# choose gender and club if desired, can delete to run on all
prefsList = np.array(prefsMaker.prefs(gender="Male",club="Leverett", randN=6))
print prefsList

people = np.array(range(len(prefsList)))

irvingMatcher = Irving1985(people, prefsList)
print irvingMatcher.match()
