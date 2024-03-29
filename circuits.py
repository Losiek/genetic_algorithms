# circuits.py
class Not:
    def __init__(self, input):
        self._input = input

    def get_output(self):
        if self._input is None:
            return None
        value = self._input.get_output()
        if value is None:
            return None
        return not value

    def __str__(self):
        if self._input is None:
            return "Not(?)"
        return "Not({})".format(self._input)

    @staticmethod
    def input_count():
        return 1


class GateWith2Inputs:
    def __init__(self, inputA, inputB, label, fnTest):
        self._inputA = inputA
        self._inputB = inputB
        self._label = label
        self._fnTest = fnTest

    def get_output(self):
        if self._inputA is None or self._inputB is None:
            return None
        aValue = self._inputA.get_output()
        if aValue is None:
            return None
        bValue = self._inputB.get_output()
        if bValue is None:
            return None
        return self._fnTest(aValue, bValue)

    def __str__(self):
        if self._inputA is None or self._inputB is None:
            return "{}(?)".format(self._label)
        return "{}({} {})".format(self._label, self._inputA, self._inputB)

    @staticmethod
    def input_count():
        return 2


class And(GateWith2Inputs):
    def __init__(self, inputA, inputB):
        super().__init__(inputA, inputB, type(self).__name__,
                         lambda a, b: a and b)


class Or(GateWith2Inputs):
    def __init__(self, inputA, inputB):
        super().__init__(inputA, inputB, type(self).__name__,
                         lambda a, b: a or b)


class Xor(GateWith2Inputs):
    def __init__(self, inputA, inputB):
        super().__init__(inputA, inputB, type(self).__name__,
                         lambda a, b: a != b)


class Source:
    def __init__(self, sourceId, sourceContainer):
        self._sourceId = sourceId
        self._sourceContainer = sourceContainer

    def get_output(self):
        return self._sourceContainer[self._sourceId]

    def __str__(self):
        return self._sourceId

    @staticmethod
    def input_count():
        return 0
