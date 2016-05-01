import logging
import numpy as np
from optparse import OptionParser
import random
import sys

class Irving1985:
    def __init__(self,people, preferenceList):
        self.people = people
        self.preferenceList = preferenceList

    def match(self):
        logging.debug("phase 1 begin:")
        logging.debug("--------------")
        noMatch = self.phase1()
        if noMatch:
            logging.info("No Stable Match Possible")
            # raise RuntimeError
            stableFound = False
        else:
            logging.debug("phase 1 complete. Reducing preferences:")
            self.reducePreferenceLists()
            logging.debug("reduction complete. Results:")
            logging.debug("----------------------------")
            for i in self.people:
                logging.debug("Person "+str(i)+" preferences")
                logging.debug(self.reducedPreferences[i])
                logging.debug('')
            logging.debug("Reduction leaves potential stable matches. Phase 2:")
            logging.debug("---------------------------------------------------")
            stableFound = self.phase2()
        logging.debug('')
        if stableFound:
            logging.info("Phase 2 completed. Final Results:")
            logging.info("---------------------------------")
            for i, match in enumerate(self.reducedPreferences):
                logging.info("Person "+str(i)+" matches with Person "+str(match[0]))
        else:
            logging.info("No Stable Match Possible")
        return stableFound

    def _assessProposal(self, proposer, proposee):
        logging.debug("Person "+str(proposer)+" proposes to Person "+str(proposee))

        # if proposer == 5 and proposee == 4:
        #     import pdb; pdb.set_trace();

        index = np.argwhere(self.preferenceList[proposee] == proposer)[0][0]
        noBestBool = (self.indexHoldBest[proposee] == len(self.indexHoldBest))
        if noBestBool or index < self.indexHoldBest[proposee]:
            # if someone was dropped by the proposee, add the proposee to their rejected list
            if not noBestBool:
                nextPerson = self.preferenceList[proposee][self.indexHoldBest[proposee]]
                self.rejectedList[nextPerson].append(proposee)
            else:
                nextPerson = None
            # make the proposer be held by the proposee
            self.indexHoldBest[proposee] = index
            logging.debug("Person "+str(proposee)+" holds Person "+str(proposer))
            if nextPerson is not None:
                logging.debug("Person "+str(proposee)+" rejects Person "+str(nextPerson))
            return True, nextPerson
        else:
            # cross the proposee off of the potential list for the proposer
            self.rejectedList[proposer].append(proposee)
            logging.debug("Person "+str(proposee)+" rejects Person "+str(proposer))
            return False, None

    def phase1(self):
        "runs phase 1 of the irving algorithm"
        self.setProposedTo = set()
        n = len(self.people)
        # create the IndexHoldList to store agents being held
        self.indexHoldBest = [n for i in range(n)]
        self.rejectedList = [[] for i in range(n)]

        # follow irving algorithm almost directly
        for person in self.people:
            proposer = person
            proposee = None
            while True:
                try:
                    proposee = [pref for pref in self.preferenceList[proposer] if pref not in self.rejectedList[proposer]][0]
                except:
                    # nobody left to propose to, no stable match found
                    return True
                accepted, nextPerson = self._assessProposal(proposer, proposee)
                if accepted:
                    if proposee in self.setProposedTo:
                        assert(nextPerson is not None)
                        # if proposee drops a priorProposer, then set that person to be proposer
                        proposer = nextPerson
                    else:
                        break
            assert(proposee is not None)
            logging.debug('')
            self.setProposedTo.add(proposee)

        # if someone rejected by everyone, then signal (noMatch = True)
        for l in self.rejectedList:
            if len(l) == n:
                return True
        # otherwise, signal successful completion of phase 1 (noMatch = False)
        return False

    def reducePreferenceLists(self):
        n = len(self.people)
        self.reducedPreferences = [[] for i in range(len(self.people))]
        for y in self.people:
            possibleList = list(self.preferenceList[y])
            bestIndex = self.indexHoldBest[y]
            x = self.preferenceList[y][bestIndex]
            # remove all people worse than x for y
            # there are n-1 other people
            if not (bestIndex == n-1):
                for i in range(bestIndex+1,n-1):
                    possibleList.remove(self.preferenceList[y][i])
                    self.rejectedList[y].append(self.preferenceList[y][i])
            # remove all people who hold proposers they prefer to y
            remaining = list(possibleList) # copy the list for iteration
            for x in remaining:
                y_index = np.argwhere(self.preferenceList[x] == y)[0][0]
                hold_index = self.indexHoldBest[x]
                if hold_index < y_index:
                    possibleList.remove(x)
                    self.rejectedList[x].append(y)
            self.reducedPreferences[y].extend(possibleList)
        return# answer stored in self.reducedPreferences

    def _findAllOrNothingCycle(self):
        remaining = set()
        for person in self.people:
            tohave = []
            l = self.reducedPreferences[person]
            assert len(l) != 0
            if len(l) >= 2:
                tohave.append(person)
        remaining = set(tohave)

        ps = []# list of people in cycle
        try:
            p_i = random.sample(remaining, 1)[0]
        except:
            return None,None,True
        # p_i = 2 # for debugging purposes
        # import pdb; pdb.set_trace()
        # for debugging
        # I NEED TO FIGURE OUT WHY REMAINING HAS EVERYBODY, NOT A REDUCED LIST
        self.remaining = remaining
        for person in remaining:
            assert len(self.reducedPreferences[person])>=2
        self.check = list(self.reducedPreferences)
        while True:
            ps.append(p_i)
            # try:
            q_i = self.reducedPreferences[p_i][1]# get the second person in preferences list
            # except:
                # import pdb; pdb.set_trace()
            p_ip1 = self.reducedPreferences[q_i][-1]# get last person in q_i's reduced list
            if p_ip1 in ps:
                p_s_Index = ps.index(p_ip1) # do not add the cycled person
                break
            p_i = p_ip1# cycle by reassigning p_i
            if p_i not in remaining:
                return None, None, True
        nocycle = False
        allOrNothingCycle = ps[p_s_Index:]
        self.ps = ps # for debugging
        tail = ps[:p_s_Index]
        return allOrNothingCycle, tail, nocycle

    def _updateWithCycle(self, allOrNothingCycle):# update rejected lists and call self.reducePreferenceLists()
        #for debugging
        redpref = list(self.reducedPreferences)
        assert (redpref == self.check)
        for i, a_i in enumerate(allOrNothingCycle):
            # get bs
            # import pdb; pdb.set_trace()
            b_i = self.reducedPreferences[a_i].pop(0)
            # b_i = self.reducedPreferences[a_i][0]
            if i == 0:
                b_1 = b_i# store the first person that rejects
            if i+1 == len(allOrNothingCycle):
                # import pdb; pdb.set_trace()
                b_ip1 = b_1# if at the end, cycle
            else:
                b_ip1 = self.reducedPreferences[a_i][0]
            # assert that there are more than 0 elements in the list
            assert len(self.reducedPreferences[a_i]) > 0

            # b_i rejects a_i
            self.rejectedList[a_i].append(b_i)
            logging.debug("Person "+str(b_i)+" rejects Person "+str(a_i))
            logging.debug("Person "+str(a_i)+" proposes to Person "+str(b_ip1))
            try:
                index = np.where(self.preferenceList[b_ip1]==a_i)[0][0]
            except:
                import pdb; pdb.set_trace()
            logging.debug("Person "+str(b_ip1)+" holds Person "+str(a_i))
            self.indexHoldBest[b_ip1] = index

    def _checkCompletion(self):
        for i, reducedList in enumerate(self.reducedPreferences):# start from 1 to ignore the empty entry that offsets to make indexing work
            if len(reducedList) != 1:
                try:
                    assert len(reducedList) != 0# if len(list) < 0, no match possible
                except:
                    completed = True
                    stableFound = False
                    return completed, stableFound
                completed = False
                stableFound = False
                return completed, stableFound
        completed = True
        stableFound = True
        return completed, stableFound

    def phase2(self):
        completedfail = False
        while True:
            completed, stableFound = self._checkCompletion()
            if completed or completedfail:
                # print self.reducedPreferences
                return stableFound

            allOrNothingCycle, tail, nocycle = self._findAllOrNothingCycle()
            if not nocycle:
                logging.debug("allOrNothingCycle found")
                for i in range(len(allOrNothingCycle)):
                    logging.debug("a_" + str(i+1) + ": " + str(allOrNothingCycle[i]))
                # print "tail found"
                # for i in range(len(tail)):
                #     print "p_"+str(i+1)+": "+str(tail[i])
                # break
                logging.debug('')
                logging.debug("updating reduced preference lists")
                self._updateWithCycle(allOrNothingCycle)
            else:
                completedfail = True
            # import pdb; pdb.set_trace()
            # self.reducePreferenceLists(returned=True)
            # import pdb; pdb.set_trace()


def configure_logging(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    root_logger = logging.getLogger('')
    strm_out = logging.StreamHandler(sys.__stdout__)
    strm_out.setFormatter(logging.Formatter('%(message)s'))
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(strm_out)

def main(args):
    usage_msg = "Usage: irving1985.py --loglevel OPTION(debug, info, etc.)"
    parser = OptionParser(usage=usage_msg)
    parser.add_option("--loglevel",
                      dest="loglevel", default="info",
                      help="Set the logging level: 'debug' or 'info'")
    (options, args) = parser.parse_args()
    configure_logging(options.loglevel)

    # people = np.array([1,2,3,4,5,6])
    people = np.array([0,1,2,3,4,5])

    # no stable matching exists
    # example1 = np.array([[1,5,3,2,4],
    #                      [2,4,0,5,3],
    #                      [0,5,1,4,3],
    #                      [4,1,2,5,0],
    #                      [5,0,2,3,1],
    #                      [3,1,4,0,2]])

    # stable matching exists
    example2 = np.array([[3,5,1,4,2],
                         [5,2,4,0,3],
                         [3,4,0,5,1],
                         [1,5,4,0,2],
                         [3,1,2,5,0],
                         [4,0,3,1,2]])

    people3 = np.array(range(7))
    example3 = np.array([[3,1,4,5,6,2],
                         [6,5,2,0,4,3],
                         [6,0,1,4,5,3],
                         [0,1,2,6,5,4],
                         [1,5,0,3,6,2],
                         [4,1,0,6,2,3],
                         [2,1,0,5,4,3]])

    matcher = Irving1985(people3, example3)
    matcher.match()

if __name__ == "__main__":
    main(sys.argv)
