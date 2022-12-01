"""
    This class computes positive and negative outranking flows based on preferences.
"""
import pandas as pd
from core.aliases import PreferencesTable, FlowsTable
from typing import Tuple, Union

__all__ = ["calculate_prometheeI_outranking_flows", "calculate_prometheeII_outranking_flows"]

from core.input_validation import prometheeI_outranking_flows_validation, prometheeII_outranking_flows_validation


def _calculate_flow(preferences: Union[Tuple[PreferencesTable, PreferencesTable], PreferencesTable],
                    positive: bool = True) -> pd.Series:
    """
    Calculate positive or negative outranking flow.

    :param positive: If True function returns positive outranking flow else returns negative outranking flow.
    :return: List of outranking flow's values.
    """
    if isinstance(preferences, tuple):
        if positive:
            flows = preferences[0].mean(axis=1)
        else:
            flows = preferences[1].mean(axis=0)
    else:
        axis = 1 if positive else 0
        aggregated_preferences = preferences.sum(axis=axis) / (preferences.shape[0] - 1)

        return aggregated_preferences

    return flows


def _calculate_prometheeII_style_flow(preferences: Tuple[PreferencesTable, PreferencesTable],
                                      profiles_preferences: PreferencesTable, positive: bool = True) -> pd.Series:
    """
    Calculate positive or negative outranking flow in PrometheeII style.

    :param preferences: Tuple of alternatives vs profiles preferences and profiles vs alternatives preferences.
    :param profiles_preferences: PreferencesTable of profiles vs alter.
    :param positive: If True function returns positive outranking flow else returns negative outranking flow.
    :return: List of outranking flow's values.
    """
    n_profiles = len(profiles_preferences)
    alternatives_groups_flows = []
    alternatives_groups_names = []
    axis = 1 if positive else 0

    for alternative, alternative_preferences in preferences[0].iterrows():
        alternative_group_preferences = profiles_preferences.copy()
        alternative_group_preferences.loc[alternative] = alternative_preferences
        alternative_group_preferences[alternative] = preferences[1][alternative]

        alternatives_groups_flows.append(alternative_group_preferences.sum(axis=axis)/n_profiles)
        alternatives_groups_names.append(f"R{alternative}")

    return pd.concat(alternatives_groups_flows, keys=alternatives_groups_names)


def calculate_prometheeI_outranking_flows(
        preferences: Union[Tuple[PreferencesTable, PreferencesTable], PreferencesTable]) -> FlowsTable:
    """
    Calculate both positive and negative outranking flows for Promethee I method.

    :return: FlowTable of both positive and negative outranking flows.
    """
    prometheeI_outranking_flows_validation(preferences)

    index = preferences[0].index if isinstance(preferences, tuple) else preferences.index
    return pd.DataFrame({'positive': _calculate_flow(preferences),
                         'negative': _calculate_flow(preferences, positive=False)
                         }, index=index)


def calculate_prometheeII_outranking_flows(
        preferences: Tuple[PreferencesTable, PreferencesTable],
        profiles_preferences: PreferencesTable) -> FlowsTable:
    """
    Calculate both positive and negative outranking flows for Promethee II method.

    :return: FlowTable of both positive and negative outranking flows.
    """
    prometheeII_outranking_flows_validation(preferences, profiles_preferences)

    return pd.DataFrame({'positive': _calculate_prometheeII_style_flow(preferences, profiles_preferences),
                         'negative': _calculate_prometheeII_style_flow(preferences, profiles_preferences,
                                                                       positive=False)})
