import pandas, operator, sys
import numpy as np

class MakeRoomingPrefs:
    def __init__(self, fileName):
        self.fileName = fileName
        self.maxWeight = 4
        self.maxDist = 4
        self.crossWalk = {}

    ''' keeps only selected gender and club '''
    def filter(self, P):
        # add IDs
        P["id"] = range(len(P))
        if self.gender != "all":
            P = P[P["Gender"] == self.gender]
        if self.club != "all":
            P = P[P["Are you in any of the following groups? (Check all that apply.)"].str.contains(self.club)]
        return P

    ''' select N observations '''
    def randomSelection(self, P, randN):
        if randN >= len(P):
            return P
        else:
            return P.sample(randN)

    ''' pandas dataframe to numpy array '''
    def clean(self, P):

        # remove timestamp and email
        P = P.drop("Timestamp", 1)
        P = P.drop("Username", 1)
        P = P.drop("Gender", 1)
        P = P.drop("Are you in any of the following groups? (Check all that apply.)", 1)

        # strings to numbers
        oldNewMap = {'Clean & Organized: Everything has a place': 3,
                     'Somewhat Clean & Organized: At least things look neat': 2,
                     'Somewhat Messy: I keep things on my side of the room.': 1,
                     'Messy: As long as my things are in my room, I don\'t care': 0}
        P['How clean and neat do you keep your room?'] = P['How clean and neat do you keep your room?'].map(oldNewMap)

        oldNewMap = {'Very Outgoing. I usually engage people first in conversations.': 3,
                     'Fairly Outgoing. I like to be social.': 2,
                     'Fairly Shy. I\'m friendly but I usually keep to myself.': 1,
                     'Very Shy. I usually only talk to people if they talk to me first.': 0}
        P['How outgoing are you?'] = P['How outgoing are you?'].map(oldNewMap)

        oldNewMap = {'We do everything together': 3,
                     'We hang out frequently': 2,
                     'We hang out occasionally': 1,
                     'We respect one another & peacefully coexist': 0}
        P['How close do you want to be with your roommate?'] = P['How close do you want to be with your roommate?'].map(oldNewMap)

        oldNewMap = {'Anytime, without asking': 3,
                     'Anytime usually, as long as they ask first': 2,
                     'Not unless they need something specific': 1,
                     'Only I can use my belongings': 0}
        P['Can your roommate use your belongings?'] = P['Can your roommate use your belongings?'].map(oldNewMap)

        oldNewMap = {'I\'m here to learn! All studying for me!': 4,
                     'Mostly studying, but go out once in a while': 3,
                     '50/50 split': 2,
                     'Mostly partying, but I don\'t plan to fail out!': 1,
                     'Where\'s the party at?!?!': 0}
        P['What\'s your planned Study/Party balance?'] = P['What\'s your planned Study/Party balance?'].map(oldNewMap)

        oldNewMap = {'Completely quiet. No TV or music. Wear headphones, please!': 3,
                     'Mostly quiet. TV and music are ok keep the volume down!': 2,
                     'Background noise is fine, but please don\'t be obnoxious.': 1,
                     'WTH? Study? This is college! Let\'s party!': 0}
        P['What noise level do you prefer while studying'] = P['What noise level do you prefer while studying'].map(oldNewMap)

        oldNewMap = {'Have friends over all the time': 3,
                     'I like having friends in my room': 2,
                     'I\'d prefer not having friends in my room': 1,
                     'My roommate & I should be the only ones in our room': 0}
        P['Do you plan on having friends in your room?'] = P['Do you plan on having friends in your room?'].map(oldNewMap)

        oldNewMap = {'Almost always, except for classes & getting food': 3,
                     'Most of the time. I have to get out every once in awhile': 2,
                     'Not too often, I\'m usually out & about': 1,
                     'Only when I\'m sleeping': 0}
        P['How often do you plan to be in the room?'] = P['How often do you plan to be in the room?'].map(oldNewMap)

        oldNewMap = {'I go to bed before 10': 3,
                     'I go to bed between 10 and midnight': 2,
                     'I go to bed between midnight and 2AM': 1,
                     'I go to bed after 2 AM': 0}
        P['What time do you go to bed?'] = P['What time do you go to bed?'].map(oldNewMap)

        oldNewMap = {'Yes': 3,
                     'Socially': 2,
                     'No': 1}
        P['Do you smoke?'] = P['Do you smoke?'].map(oldNewMap)

        oldNewMap = {'North pole!': 3,
                     '60 to 70': 2,
                     '71 to 81': 1,
                     'Pass me the pitchfork!': 0}
        P['What temperature do you prefer in your room?'] = P['What temperature do you prefer in your room?'].map(oldNewMap)

        oldNewMap = {'Very likely': 3,
                     'Likely': 2,
                     'Probably not': 1,
                     'Never!': 0}
        P['How likely are you to have overnight guests?'] = P['How likely are you to have overnight guests?'].map(oldNewMap)

        oldNewMap = {'Very Conservative': 4,
                     'Conservative': 3,
                     'Moderate': 2,
                     'Liberal': 1,
                     'Very Liberal': 0}
        P['What do you want your roommate\'s political views to be?'] = P['What do you want your roommate\'s political views to be?'].map(oldNewMap)

        oldNewMap = {'5 - Very Important': 4,
                     '4': 3,
                     '3': 2,
                     '2': 1,
                     '1 - Not at All Important': 0}
        P['On the above, how important is it that your roommate is the same as you?'] = P['On the above, how important is it that your roommate is the same as you?'].map(oldNewMap)
        P['How important is this to you?'] = P['How important is this to you?'].map(oldNewMap)
        for j in range(1, 12):
            P['On the above, how important is it that your roommate is the same as you?.' + str(j)] = P['On the above, how important is it that your roommate is the same as you?.' + str(j)].map(oldNewMap)

        return P.values[:,1:]

    ''' score of i for j '''
    def score(self, i, j):
        s = self.maxScore
        # for each question, decrement by distance(i, j) * i's importance
        for q in range(self.Q/2):
            s -= abs(self.X[i][2*q] - self.X[j][2*q]) * self.X[i][(2*q) + 1]
        return s

    ''' dictionary links prefs with real names '''
    def crossWalkFn(self, prefs):
        for i in range(len(prefs)):
            self.crossWalk[i] = self.P.loc[self.X[i][-1]]["Name"]

    ''' preference ordering '''
    def prefs(self, gender="all", club="all", randN=0, returnScores="n"):
        self.gender = gender
        self.club = club
        self.P = self.filter(pandas.read_csv(self.fileName, sep=','))
        if randN:
            self.P = self.randomSelection(self.P, randN)
        self.X = self.clean(self.P)
        self.N = np.size(self.X, axis = 0) # number of rows
        self.Q = np.size(self.X, axis = 1) # number of questions
        self.maxScore = (self.Q/2) * self.maxWeight * self.maxDist # best score
        scores = [{} for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    scores[i][j] = self.score(i, j)
                else:
                    scores[i][j] = -1 # can't match with self

        # sort scores and return preference ordering
        sortedScores = [list(reversed(sorted(scores[i].items(),
            key=operator.itemgetter(1)))) for i in range(self.N)]
        prefs = [[i[0] for i in sortedScores[j]][:-1] for j in range(self.N)]
        self.crossWalkFn(prefs) # sets crossWalk
        if returnScores == "y":
            return sortedScores
        else:
            return prefs
