from makeRoomingPrefs import MakeRoomingPrefs
from irving1985 import Irving1985

# just pass in the file
prefsMaker = MakeRoomingPrefs('../roomingQuestionnaireResponses.csv')

# choose gender and club if desired, can delete to run on all
prefsList = prefsMaker.prefs(gender="Male", club="Leverett")

# I thought we might need this to get Irving to work, but Irving doesn't work
prefsList.insert(0, [0] * (len(prefsList) - 1))

# it prints!
print prefsList

# these don't work
#irvingMatcher = Irving1985(range(len(prefsList)), prefsList)
#irvingMatcher.match()
