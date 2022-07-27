import numpy as np
from core.aliases import NumericValue
from typing import List


class PrometheeOutrankingFlows:
    """
    This class computes positive and negative outranking flows
    based on preferences.
    """

    def __init__(self, alternatives: List[str], preferences: List[List[NumericValue]]):
        """
        :param alternatives: List of alternatives names (strings only)
        :param preferences: 2D array of aggregated preferences
        """
        self.alternatives = alternatives
        self.preferences = preferences

    def __calculate_flow(self, positive: bool = True) -> List[NumericValue]:
        """
        Calculate positive or negative outranking flow.

        :param positive: if True function returns positive outranking flow
        else returns negative outranking flow
        :return: List of outranking flow's values
        """
        n = len(self.alternatives)

        axis = 1 if positive else 0
        aggregatedPIes = np.sum(self.preferences, axis=axis)
        flows = aggregatedPIes / (n - 1)

        return flows
        # return np.sum(self.preferences, axis=1 if positive else 0)/(len(self.alternatives)-1)

    def calculate_flows(self):
        """
        Calculate both positive and negative outranking flows.
        :return: OUT1: positive outranking flow
                 OUT2: negative outranking flow
        """
        return self.__calculate_flow(), self.__calculate_flow(positive=False)
