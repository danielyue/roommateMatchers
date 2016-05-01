from makeRoomingPrefs import MakeRoomingPrefs
from irving1985 import Irving1985
import numpy as np

# just pass in the file
prefsMaker = MakeRoomingPrefs('../roomingQuestionnaireResponses.csv')

# choose gender and club if desired, can delete to run on all
prefsList = prefsMaker.prefsNames(gender="Male", club="Leverett", randN=4)

# it prints!
print prefsList
