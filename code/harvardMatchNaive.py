from makeRoomingPrefs import MakeRoomingPrefs
from irving1985Mod import Irving1985Mod
import numpy as np

prefsMaker = MakeRoomingPrefs('../roomingQuestionnaireResponsesMod.csv')
genders = ["Male", "Female"]
clubs = ["CS136", "Leverett", "Lowell", "Winthrop", "CS136", "HCFA", "Ichthus"]

matches = {}
for club in clubs:
    matches[club] = {}
    for gender in genders:
        prefs = np.array(prefsMaker.prefs(gender=gender, club=club))
        matcher = Irving1985Mod(np.array(range(len(prefs))), prefs)
        matches[club][gender] = matcher.match()[1]
print matches
