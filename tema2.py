
from collections import defaultdict

class DFA(object):
    # This function initialises the DFA
    def __init__(self, states, start_state=None, transitions=None, final_states=None, inputs=None):
        self.states = states
        self.start_state = start_state
        self.transitions = transitions
        self.final_states = final_states
        self.inputs = inputs



    # This function removes states that are unreachable/dead states
    def remove_unreachable_states(self):
        g = defaultdict(list)

        for k, v in self.transitions.items():
            g[k[0]].append(v)

        stack = [self.start_state]

        reachable_states = set()

        while stack:
            state = stack.pop()

            if state not in reachable_states:
                stack += g[state]

            reachable_states.add(state)

        self.states = [state for state in self.states if state in reachable_states]

        self.final_states = [state for state in self.final_states if state in reachable_states]

        self.transitions = {k: v for k, v in self.transitions.items() if k[0] in reachable_states}

    # This function minimizes the DFA
    def minimize(self):
        self.remove_unreachable_states()

        def order_tuple(a, b):
            return (a, b) if a < b else (b, a)

        table = {}

        sorted_states = sorted(self.states)
        # Checking if one state is final and the other is non-final
        # and marking the corresponding cell in the Table
        for i, state_1 in enumerate(sorted_states):
            for state_2 in sorted_states[i + 1:]:
                table[(state_1, state_2)] = (state_1 in self.final_states) \
                                            != (state_2 in self.final_states)

        flag = True
        # Checking the transitions of unmarked states
        while flag:
            flag = False
            for i, state_1 in enumerate(sorted_states):
                for state_2 in sorted_states[i + 1:]:
                    if table[(state_1, state_2)]:
                        continue
                    for input in self.inputs:
                        s1 = self.transitions.get((state_1, input), None)
                        s2 = self.transitions.get((state_2, input), None)
                        print((state_1, input), '-->', s1)
                        print((state_2, input), '-->', s2, "\n")
                        if s1 is not None and s2 is not None and s1 != s2:
                            marked = table[order_tuple(s1, s2)]
                            flag = flag or marked
                            table[(state_1, state_2)] = marked
                            if marked:

                                break
        print("Cells\t\tMarked/UnMarked")
        for k, v in table.items():
            print((k[0], k[1]), "\t\t", v)
        print("\n\n")

        set_of_states = ListSet(self.states)

        # print("States Before Minimization: ", set_of_states.get())
        # form new states
        for k, v in table.items():
            if not v:
                set_of_states.union(k[0], k[1])
                print(k, " cell is unmarked ,so we group them together \
				and get ", set_of_states.get())

        print("\n", "After Minimization: ", set_of_states.get())

        self.states = [str(x) for x in range(1, 1 + len(set_of_states.get()))]
        new_final_states = []
        self.start_state = str(set_of_states.find_set(self.start_state))
        for s in set_of_states.get():
            for state_1 in s:
                if state_1 in self.final_states:
                    new_final_states.append(str(set_of_states.find_set(state_1)))
                    break
        self.transitions = {(str(set_of_states.find_set(k[0])), k[1]): str(set_of_states.find_set(v))
                            for k, v in self.transitions.items()}
        self.final_states = new_final_states
        for k, v in self.transitions.items():
            print("State ", set_of_states.get()[int(k[0]) - 1], " on input ", k[1],
                  " goes to state ", set_of_states.get()[int(v) - 1])
        print("Now renaming minimized states we get,")
        for state in set_of_states.get():
            print("State ", set_of_states.get().index(state) + 1, "represents the combined state ", state)
        print("\n", "Number of states after minimization = ", len(self.states))
        print("Set of final states after minimization = ", self.final_states)
        print("Start State = ", self.start_state)


class ListSet(object):

    def __init__(self, items):

        self.list_set = list()

        if items:
            for item in set(items):
                self.list_set.append([item])

    def _get_index(self, item):
        for s in self.list_set:
            for _item in s:
                if _item == item:
                    return self.list_set.index(s)
        return None

    def find(self, item):
        for s in self.list_set:
            if item in s:
                return s
        return None

    def find_set(self, item):

        s = self._get_index(item)

        return s + 1 if s is not None else None

    def union(self, item1, item2):
        i = self._get_index(item1)
        j = self._get_index(item2)

        if i != j:
            self.list_set[i] += self.list_set[j]
            del self.list_set[j]

    def get(self):
        return self.list_set



states = input("Enter the states in DFA: ").split()
start_state = str(input("Enter the start state in DFA: "))
final_states = input("Enter the final states in DFA: ").split()
inputs = input("Enter the input symbols in DFA: ").split()
transitions = {}

print("Please enter the transitions in the format \
(State1 input State2) \n Enter * to stop")
while True:
  transition = input().split()
  if (transition == ['*']):
    break
  transitions[(transition[0], transition[1])] = transition[2]


dfa = DFA(states, start_state, transitions,final_states, inputs)

# minimize dfa
dfa.minimize()



''' 
Input  ex:

A B C D E 
A
D E
0 1
A 0 B
A 1 C
B 0 D
B 1 E
C 0 B
D 0 D
D 1 E
E 0 B
E 1 C

'''