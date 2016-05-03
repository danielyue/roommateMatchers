from pulp import *
import pdb
import numpy as np

class LinearProgram:
    def __init__(self,people, preferenceList):
        self.people = people
        self.preferenceList = preferenceList

    def match(self):
		#initialise the model
		prob = pulp.LpProblem('Stable Roommate', pulp.LpMinimize)

		i_vars = pulp.LpVariable.dicts("i", self.people, lowBound = 0, upBound = 1, cat = LpInteger)
		j_vars = pulp.LpVariable.dicts("j", self.people, 0, 1, LpBinary)
		match_vars = pulp.LpVariable.dicts("match", [(i,j) for i in i_vars for j in j_vars], 0, 1, LpBinary)

		for i in i_vars:
			prob += lpSum(match_vars[(i,j)] for j in j_vars) == 1

		for i in i_vars:
			for j in j_vars:
				preferences = self.preferenceList.tolist()
				x_s = preferences[j][preferences[j].index(i):]
				y_s = preferences[i][preferences[i].index(j):]
				prob += match_vars[(i,j)] + lpSum(match_vars[(x,j)] for x in x_s) + lpSum(match_vars[(i,y)] for y in y_s) == 1

		#problem is then solved with the default solver
		prob.solve()

		print("Status:", LpStatus[prob.status])

		if LpStatus[prob.status] is not 'Infeasible':
			for match_var in match_vars:
				if match_var.value() == 1:
					print match_var

def main(args):
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
    example2 = np.array([[3,5,1,4,2, 0],
                         [5,2,4,0,3, 1],
                         [3,4,0,5,1, 2],
                         [1,5,4,0,2, 3],
                         [3,1,2,5,0, 4],
                         [4,0,3,1,2, 5]])

    people3 = np.array(range(7))
    example3 = np.array([[3,1,4,5,6,2, 0],
                         [6,5,2,0,4,3, 1],
                         [6,0,1,4,5,3, 2],
                         [0,1,2,6,5,4, 3],
                         [1,5,0,3,6,2, 4],
                         [4,1,0,6,2,3, 5],
                         [2,1,0,5,4,3, 6]])

    matcher = LinearProgram(people3, example3)
    matcher.match()

if __name__ == "__main__":
    main(sys.argv)
