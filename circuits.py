# Circuit infrastructure

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


class And:
    def __init__(self, inputA, inputB):
        self._inputA = inputA
        self._inputB = inputB

    def get_output(self):
        if self._inputA is None or self._inputB is None:
            return None
        aValue = self._inputA.get_output()
        if aValue is None:
            return None
        bValue = self._inputB.get_output()
        if bValue is None:
            return None
        return aValue and bValue

    def __str__(self):
        if self._inputA is None or self._inputB is None:
            return "And(?)"
        return "And({} {})".format(self._inputA, self._inputB)

    @staticmethod
    def input_count():
        return 2


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
