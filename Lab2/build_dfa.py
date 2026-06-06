from abc import ABC, abstractmethod
from collections import deque
from typing import Optional


class RegEx(ABC):
    @abstractmethod
    def nullable(self):
        pass

    @abstractmethod
    def derivative(self, symbol):
        pass

    def __eq__(self, other):
        if not isinstance(other, RegEx):
            return False
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))


class Empty(RegEx):
    def nullable(self):
        return False

    def derivative(self, symbol):
        return Empty()

    def __str__(self):
        return "∅"


class Epsilon(RegEx):
    def nullable(self):
        return True

    def derivative(self, symbol):
        return Empty()

    def __str__(self):
        return "ε"


class Symbol(RegEx):
    def __init__(self, symbol):
        self.symbol = symbol

    def nullable(self):
        return False

    def derivative(self, symbol):
        if self.symbol == symbol:
            return Epsilon()
        return Empty()

    def __str__(self):
        return self.symbol


class Concatenation(RegEx):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def nullable(self):
        return self.left.nullable() and self.right.nullable()

    def derivative(self, symbol):
        left_derivative = self.left.derivative(symbol)

        if isinstance(left_derivative, Empty):
            if self.left.nullable():
                return self.right.derivative(symbol)
            return Empty()

        if self.left.nullable():
            right_derivative = self.right.derivative(symbol)
            if isinstance(right_derivative, Empty):
                return Concatenation(left_derivative, self.right)
            return Alternative(
                Concatenation(left_derivative, self.right), right_derivative
            )
        else:
            return Concatenation(left_derivative, self.right)

    def __str__(self):
        return f"({self.left}{self.right})"


class Alternative(RegEx):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def nullable(self):
        return self.left.nullable() or self.right.nullable()

    def derivative(self, symbol):
        left_derivative = self.left.derivative(symbol)
        right_derivative = self.right.derivative(symbol)

        if isinstance(left_derivative, Empty):
            return right_derivative
        if isinstance(right_derivative, Empty):
            return left_derivative

        return Alternative(left_derivative, right_derivative)

    def __str__(self):
        return f"({self.left}|{self.right})"


class KleeneStar(RegEx):
    def __init__(self, expression):
        self.expression = expression

    def nullable(self):
        return True

    def derivative(self, symbol):
        derivative = self.expression.derivative(symbol)

        if isinstance(derivative, Empty):
            return Empty()

        return Concatenation(derivative, self)

    def __str__(self):
        return f"({self.expression})*"


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, string):
        """Check if the DFA accepts the given string."""
        current_state = self.start_state

        for i, symbol in enumerate(string):
            if symbol not in self.alphabet:
                return False

            if (current_state, symbol) not in self.transitions:
                return False

            current_state = self.transitions[(current_state, symbol)]

        return current_state in self.accept_states

    def __str__(self):
        result = "DFA:\n"
        result += f"  States: {self.states}\n"
        result += f"  Alphabet: {self.alphabet}\n"
        result += f"  Start State: {self.start_state}\n"
        result += f"  Accept States: {self.accept_states}\n"
        result += "  Transitions:\n"
        for (state, symbol), next_state in sorted(self.transitions.items()):
            result += f"    {state} --{symbol}--> {next_state}\n"
        return result


def simplify(regex):
    """
    Simplify regex expressions to canonical form to improve state identification.
    """
    if (
        isinstance(regex, Empty)
        or isinstance(regex, Epsilon)
        or isinstance(regex, Symbol)
    ):
        return regex

    # For alternatives
    if isinstance(regex, Alternative):
        left = simplify(regex.left)
        right = simplify(regex.right)

        if isinstance(left, Empty):
            return right
        if isinstance(right, Empty):
            return left

        if str(left) == str(right):
            return left

        return Alternative(left, right)

    # For concatenations
    if isinstance(regex, Concatenation):
        left = simplify(regex.left)
        right = simplify(regex.right)

        if isinstance(left, Empty) or isinstance(right, Empty):
            return Empty()

        if isinstance(left, Epsilon):
            return right

        if isinstance(right, Epsilon):
            return left

        return Concatenation(left, right)

    # For Kleene star
    if isinstance(regex, KleeneStar):
        inner = simplify(regex.expression)

        if isinstance(inner, KleeneStar):
            return inner

        if isinstance(inner, Epsilon):
            return Epsilon()

        if isinstance(inner, Empty):
            return Epsilon()

        return KleeneStar(inner)

    return regex


def build_dfa(regex: RegEx, alphabet: set[str]) -> Optional[DFA]:
    # Initialize data structures
    states = set()  # Set of state names (q0, q1, etc.)
    state_to_regex = {}  # Maps state names to their regex
    accept_states = set()  # Set of accepting state names
    transitions = {}  # Maps (state, symbol) pairs to next state
    regex_to_state = {}  # Maps string representations of regex to state names

    # Initialize state counter for generating unique state names
    state_counter = 0

    # YOUR CODE HERE

    initial_regex =simplify(regex)

    if str(initial_regex) not in regex_to_state: # jesli regex jest nowy
        statename = f"q{state_counter}" # nazywamy stan
        state_counter += 1
        states.add(statename)
        state_to_regex[statename] = initial_regex # mapujemy stan na regex i odwortnie
        regex_to_state[str(initial_regex)] = statename
        if initial_regex.nullable(): accept_states.add(statename)
        # jesli akceptuje puste dodajemy do stanow akceptujacych puste

    queue = deque([regex_to_state[str(initial_regex)]])

    while queue:
        current_state = queue.popleft() # pobieramy z poczatku
        current_regex = state_to_regex[current_state]

        for symbol in alphabet:
            derivative = simplify(current_regex.derivative(symbol)) # obliczanie pochodnej brzozowskiego
            derivative_str = str(derivative)

            if derivative_str not in regex_to_state: # jesli jest nowa to robi to samo co 10 lini wyzej
                new_state = f"q{state_counter}"
                state_counter += 1
                states.add(new_state)
                state_to_regex[new_state] = derivative
                regex_to_state[derivative_str] = new_state
                if derivative.nullable(): accept_states.add(new_state)
                queue.append(new_state) # i dodaj do kolejki

            next_state = regex_to_state[derivative_str]
            # budujemy przejscie do terazniejszego stanu przez pchodna
            transitions[(current_state, symbol)] = next_state
    start_state = regex_to_state[str(initial_regex)] # poczatkowy regex
    return DFA(states, alphabet, transitions, start_state, accept_states)