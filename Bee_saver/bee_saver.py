'''bee_saver.py by Christoffer Hansson (chrhanss) and Vicky Norman (vnorman)
A QUIET2 Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this
problem formulation.  It is important that COMMON_CODE come
before all the other sections (except METADATA), including COMMON_DATA.
CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''
# <METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Bee Problem"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "11-OCT-2017"
PROBLEM_DESC = \
    '''This formulation of the mass dying of bees in the US problem uses generic
    Python 3 constructs and has been tested with Python 3.6.
    It is designed to work according to the QUIET2 tools interface.
    '''


# </METADATA>

# <COMMON_CODE>
class State:
    def __init__(self, d):
        self.d = d

    def __eq__(self, s2):
        for p in ['bee_pop', 'pest', 'hum_pop', 'food', 'flowers']:
            if self.d[p] != s2.d[p]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        txt = "The current state of the world is: "
        for i, var in enumerate(['bee_pop', 'pest', 'hum_pop', 'food', 'flowers']):
            txt += str(VARIABLES[i])+ ": " + str(self.d[var][0]) + " \n"
        return txt[:-2]

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        for p in ['bee_pop', 'pest', 'hum_pop', 'food', 'flowers']:
            news.d[p] = self.d[p][:]
        return news

    def can_move(self, From, To):
        '''Tests whether it's legal to move a disk in state s
           from the From peg to the To peg.'''
        try:
            pf = self.d[From]  # peg disk goes from
            pt = self.d[To]  # peg disk goes to
            if pf == []: return False  # no disk to move.
            df = pf[-1]  # get topmost disk at From peg..
            if pt == []: return True  # no disk to worry about at To peg.
            dt = pt[-1]  # get topmost disk at To peg.
            if df < dt: return True  # Disk is smaller than one it goes on.
            return False  # Disk too big for one it goes on.
        except (Exception) as e:
            print(e)

    def move(self, From, To):
        '''Assuming it's legal to make the move, this computes
           the new state resulting from moving the topmost disk
           from the From peg to the To peg.'''
        global MOVE_COUNTER
        news = self.copy()  # start with a deep copy.
        #pf = self.d[From]  # Variable it goes from.
        #pt = self.d[To]
        #df = pf  # the amount to move.
        news.d[From][0] -= 1000   # remove it from its old peg.
        news.d[To][0] += 1000   # Put disk onto destination peg.
        MOVE_COUNTER += 1
        return news  # return new state


def goal_test(s):
    '''If the world is still alive after 50 turns (years?) OR if any vital resource is eradicated'''
    global MOVE_COUNTER
    return MOVE_COUNTER == 50 # or any variable is below some critical value


def goal_message(s):
    return "The bee population is saved!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <COMMON_DATA>
# </COMMON_DATA>

# <INITIAL_STATE>
#       ['bee_pop', 'pest', 'hum_pop', 'food']:
INITIAL_DICT = {'bee_pop': [2700000], 'pest': [1000000000], 'hum_pop': [323000000], 'food': [304000000], 'flowers': [0]}
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)

VARIABLES = ['Number of bee colonies in the US',
             'Pounds of pesticides annually used in the US',
             'US population (humans)',
             'US crop production (acres)',
             'US flowers areal (acres)']

MOVE_COUNTER = 0
# </INITIAL_STATE>


# <OPERATORS>
''''''
operator_combinations = [('pest', 'bee_pop'), ('bee_pop', 'pest'), ('flowers', 'bee_pop'), ('bee_pop', 'flowers')]
OPERATORS = [Operator("Perform operator on " + p + " and " + q,
                      lambda s, p1=p, q1=q: s.can_move(p1, q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, p1=p, q1=q: s.move(p1, q1))
             for (p, q) in operator_combinations]
# </OPERATORS>

# <HEURISTICS>
def h1(state):
  return 1/state['bee_pop']

HEURISTICS = [h1]
# </HEURISTICS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
"""ADD A LOSE FUNCTION"""

# </GOAL_MESSAGE_FUNCTION>

