from makeRoomingPrefs import MakeRoomingPrefs
from bruteForceMatch import bruteForceMatch
import random, csv, pandas
import numpy as np

''' prepare links to satisfaction surveys '''
def setSurveyLinks():
    surveyLinks = {}
    for club in clubs:
        surveyLinks[club] = {}
    surveyLinks["CS136"]["Male"] = "http://goo.gl/forms/51uL44NXI0"
    surveyLinks["Leverett"]["Male"] = "http://goo.gl/forms/7oyNBIYatu"
    surveyLinks["Lowell"]["Male"] = "http://goo.gl/forms/d6HOozge2h"
    surveyLinks["Winthrop"]["Male"] = "http://goo.gl/forms/O7KXtlQHaN"
    surveyLinks["HCFA"]["Male"] = "http://goo.gl/forms/7Vjl8GKJaF"
    surveyLinks["Ichthus"]["Male"] = "http://goo.gl/forms/bKN4uCuL5r"
    surveyLinks["CS136"]["Female"] = "http://goo.gl/forms/eu95z9YQw1"
    surveyLinks["Leverett"]["Female"] = "http://goo.gl/forms/Z3f9Xk5F4A"
    surveyLinks["Lowell"]["Female"] = "http://goo.gl/forms/uYWD7FlHRr"
    surveyLinks["Winthrop"]["Female"] = "http://goo.gl/forms/8FcVxuocQs"
    surveyLinks["HCFA"]["Female"] = "http://goo.gl/forms/l1NGA8qMdI"
    surveyLinks["Ichthus"]["Female"] = "http://goo.gl/forms/mqI41jIkyM"
    return surveyLinks

''' returns all harvard matches after brute forcing '''
def findMatches(prefsMaker, clubs, genders):
    matches = {}
    for club in clubs:
        matches[club] = {}
        for gender in genders:
            matches[club][gender] = {}
            scores = prefsMaker.prefs(gender=gender, club=club, returnScores="y")
            matchNums = bruteForceMatch(scores, 50) # matches without names
            # get names from crossWalk
            for i in range(len(matchNums)):
                matches[club][gender][prefsMaker.crossWalk[i]] = prefsMaker.crossWalk[matchNums[i]]
    return matches

''' prints to CSV '''
def printMatches(matches, clubs, genders, surveyLinks, P, fileName):
    f = open(fileName, "wb")
    writer = csv.writer(f)
    data = [["Email Address", "fullName", "firstName", "matchName", "club", "surveyLink"]]
    for club in clubs:
        for gender in genders:
            for fullName in matches[club][gender]:
                matchName = matches[club][gender][fullName]
                firstName = fullName.split(" ", 1)[0]
                email = P[P["Name"] == fullName]["Username"].values[0]
                surveyLink = surveyLinks[club][gender]
                data.append([email, fullName, firstName, matchName, club, surveyLink])
    writer.writerows(data)
    f.close()

# parameters for matching
prefsMaker = MakeRoomingPrefs('../roomingQuestionnaireResponsesMod.csv')
genders = ["Male", "Female"]
clubs = ["CS136", "Leverett", "Lowell", "Winthrop", "HCFA", "Ichthus"]
surveyLinks = setSurveyLinks()
P = pandas.read_csv('../roomingQuestionnaireResponsesMod.csv', sep=',')
outFile = "../harvardMatchesNew.csv"

# find the matches
matches = findMatches(prefsMaker, clubs, genders)
printMatches(matches, clubs, genders, surveyLinks, P, outFile)
