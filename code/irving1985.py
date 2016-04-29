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
            raise RuntimeError
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
            for i, match in enumerate(self.reducedPreferences[1:]):
                logging.info("Person "+str(i+1)+" matches with Person "+str(match[0]))
        else:
            logging.info("No Stable Match Possible")

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
        self.indexHoldBest = [n+1 for i in range(len(self.people)+1)]
        self.rejectedList = [[] for i in range(len(self.people)+1)]

        # follow irving algorithm almost directly
        for person in self.people:
            proposer = person
            proposee = None
            while True:
                proposee = [pref for pref in self.preferenceList[proposer] if pref not in self.rejectedList[proposer]][0]
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
        self.reducedPreferences = [[] for i in range(len(self.people)+1)]
        for y in self.people:
            possibleList = list(self.preferenceList[y])
            bestIndex = self.indexHoldBest[y]
            x = self.preferenceList[y][bestIndex]
            # remove all people worse than x for y
            if not (bestIndex == n-1):
                for i in range(bestIndex+1,n-1):
                    possibleList.remove(self.preferenceList[y][i])
            # remove all people who hold proposers they prefer to y
            remaining = list(possibleList) # copy the list for iteration
            for x in remaining:
                y_index = np.argwhere(self.preferenceList[x] == y)[0][0]
                hold_index = self.indexHoldBest[x]
                if hold_index < y_index:
                    possibleList.remove(x)
            self.reducedPreferences[y].extend(possibleList)
        return# answer stored in self.reducedPreferences

    def _findAllOrNothingCycle(self):
        remaining = set()
        for person in self.people:
            l = self.reducedPreferences[person]
            assert len(l) != 0
            if len(l) > 1:
                remaining.add(person)
        ps = []# list of people in cycle
        p_i = random.sample(remaining, 1)[0]
        p_i = 2 # for debugging purposes
        # import pdb; pdb.set_trace()
        while True:
            ps.append(p_i)
            q_i = self.reducedPreferences[p_i][1]# get the second person in preferences list
            p_ip1 = self.reducedPreferences[q_i][-1]# get last person in q_i's reduced list
            if p_ip1 in ps:
                p_s_Index = ps.index(p_ip1) # do not add the cycled person
                break
            p_i = p_ip1# cycle by reassigning p_i
        allOrNothingCycle = ps[p_s_Index:]
        tail = ps[:p_s_Index]
        return allOrNothingCycle, tail

    def _updateWithCycle(self, allOrNothingCycle):# update rejected lists and call self.reducePreferenceLists()
        for i, a_i in enumerate(allOrNothingCycle):
            # get bs
            # import pdb; pdb.set_trace()
            b_i = self.reducedPreferences[a_i].pop(0)
            if i == 0:
                b_1 = b_i# store the first person that rejects
            if i == len(allOrNothingCycle):
                b_ip1 = b_1# if at the end, cycle
            else:
                b_ip1 = self.reducedPreferences[a_i][0]
            # assert that there are more than 0 elements in the list
            assert len(self.reducedPreferences[a_i]) > 0

            # b_i rejects a_i
            self.rejectedList[a_i].append(b_i)
            logging.debug("Person "+str(b_i)+" rejects Person "+str(a_i))
            logging.debug("Person "+str(a_i)+" proposes to Person "+str(b_ip1))

            index = np.where(self.preferenceList[b_ip1]==a_i)[0][0]
            logging.debug("Person "+str(b_ip1)+" holds Person "+str(a_i))
            self.indexHoldBest[b_ip1] = index

    def _checkCompletion(self):
        for i, reducedList in enumerate(self.reducedPreferences[1:]):# start from 1 to ignore the empty entry that offsets to make indexing work
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
        while True:
            allOrNothingCycle, tail = self._findAllOrNothingCycle()
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
            self.reducePreferenceLists()
            completed, stableFound = self._checkCompletion()
            if completed:
                # print self.reducedPreferences
                return stableFound

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

    people = np.array([1,2,3,4,5,6])
    # the problem demands a strict preference order
    # example1 = np.array([[0,0,0,0,0],
    #                     [2,6,4,3,5],
    #                     [3,5,1,6,4],
    #                     [1,6,2,5,4],
    #                     [5,2,3,6,1],
    #                     [6,1,3,4,2],
    #                     [4,2,5,1,3]])
    example2 = np.array([[0,0,0,0,0],#added row to make indexing work
                         [4,6,2,5,3],
                         [6,3,5,1,4],
                         [4,5,1,6,2],
                         [2,6,5,1,3],
                         [4,2,3,6,1],
                         [5,1,4,2,3]])

    matcher = Irving1985(people, example2)
    matcher.match()

if __name__ == "__main__":
    main(sys.argv)
