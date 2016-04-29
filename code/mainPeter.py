from makeRoomingPrefs import MakeRoomingPrefs
from irving1985 import Irving1985
import numpy as np

# just pass in the file
prefsMaker = MakeRoomingPrefs('../roomingQuestionnaireResponses.csv')

# choose gender and club if desired, can delete to run on all
prefsList = prefsMaker.prefs(gender="Male", club="Leverett")

# it prints!
print prefsList
